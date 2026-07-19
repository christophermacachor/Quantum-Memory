// ============================================================
// Φ669 IZMIRAN10 FTP PROXY — Cloudflare Worker
// Christopher Macachor | Ω-PRIME | MSOS-FEDERATION-ROOT
// 
// Bridges IZMIRAN10 FTP (ftp.izmiran.rssi.ru) to HTTPS
// with CORS headers for browser access from macachor.org
// ============================================================

// CORS headers for macachor.org origin
const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',  // Lock to macachor.org in production
  'Access-Control-Allow-Methods': 'GET, HEAD, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
  'Access-Control-Max-Age': '86400',
  'Content-Type': 'application/json'
};

// IZMIRAN10 FTP configuration
const IZMIRAN_FTP = {
  host: 'ftp.izmiran.rssi.ru',
  path: '/pub/izmiran/SPIM/',
  // Known file patterns from IZMIRAN10 documentation
  profilePatterns: [
    'spim_*.dat',      // Standard SPIM profiles
    'izmir_*.txt',     // IZMIRAN formatted profiles
    'density_*.prof'   // Density profile exports
  ]
};

// ============================================================
// FETCH HANDLER
// ============================================================
export default {
  async fetch(request, env, ctx) {
    // Handle CORS preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { 
        status: 204, 
        headers: CORS_HEADERS 
      });
    }

    const url = new URL(request.url);
    const path = url.pathname;

    // Route: /health — service status
    if (path === '/health') {
      return jsonResponse({
        status: 'operational',
        service: 'Φ669 IZMIRAN10 FTP Proxy',
        version: '1.0.0',
        timestamp: new Date().toISOString(),
        upstream: IZMIRAN_FTP.host,
        scalarLock: '𝔐 = 0.6180339887'
      });
    }

    // Route: /list — list available IZMIRAN10 profile files
    if (path === '/list') {
      try {
        // Attempt to fetch directory listing via HTTP fallback
        // IZMIRAN may expose HTTP mirror; try first
        const httpUrl = `http://${IZMIRAN_FTP.host}${IZMIRAN_FTP.path}`;
        const response = await fetch(httpUrl, {
          method: 'GET',
          headers: { 'User-Agent': 'Φ669-Proxy/1.0' }
        });

        if (response.ok) {
          const html = await response.text();
          // Parse directory listing for .dat, .txt, .prof files
          const files = parseDirectoryListing(html);
          return jsonResponse({
            source: 'IZMIRAN10 FTP',
            host: IZMIRAN_FTP.host,
            path: IZMIRAN_FTP.path,
            files: files,
            count: files.length,
            timestamp: new Date().toISOString()
          });
        }

        // Fallback: return known structure
        return jsonResponse({
          source: 'IZMIRAN10 FTP (fallback)',
          host: IZMIRAN_FTP.host,
          path: IZMIRAN_FTP.path,
          note: 'FTP directory listing requires active FTP connection. Known file patterns:',
          patterns: IZMIRAN_FTP.profilePatterns,
          timestamp: new Date().toISOString()
        });

      } catch (e) {
        return jsonResponse({
          error: 'Failed to list IZMIRAN10 directory',
          message: e.message,
          fallback: 'Use /proxy?url=<direct-file-url> for specific files'
        }, 502);
      }
    }

    // Route: /proxy?url=<ftp-url> — proxy specific file
    if (path === '/proxy') {
      const targetUrl = url.searchParams.get('url');
      if (!targetUrl) {
        return jsonResponse({
          error: 'Missing url parameter',
          usage: '/proxy?url=http://ftp.izmiran.rssi.ru/pub/izmiran/SPIM/filename.dat'
        }, 400);
      }

      try {
        // Validate URL is from allowed domain
        const target = new URL(targetUrl);
        if (!target.hostname.includes('izmiran.rssi.ru')) {
          return jsonResponse({
            error: 'URL not from allowed domain',
            allowed: ['*.izmiran.rssi.ru']
          }, 403);
        }

        // Fetch via HTTP (many FTP servers mirror to HTTP)
        const httpTarget = targetUrl.replace('ftp://', 'http://');
        const response = await fetch(httpTarget, {
          method: 'GET',
          headers: { 
            'User-Agent': 'Φ669-Proxy/1.0',
            'Accept': 'text/plain,application/octet-stream'
          }
        });

        if (!response.ok) {
          return jsonResponse({
            error: 'Upstream fetch failed',
            status: response.status,
            url: httpTarget
          }, 502);
        }

        const content = await response.text();

        // Parse IZMIRAN10 density profile format
        const profile = parseIZMIRANProfile(content);

        return jsonResponse({
          source: 'IZMIRAN10',
          url: targetUrl,
          parsed: profile,
          rawLength: content.length,
          timestamp: new Date().toISOString()
        });

      } catch (e) {
        return jsonResponse({
          error: 'Proxy fetch failed',
          message: e.message
        }, 502);
      }
    }

    // Route: /density?lat=<lat>&lon=<lon>&alt=<alt> — computed density
    if (path === '/density') {
      const lat = parseFloat(url.searchParams.get('lat') || '0');
      const lon = parseFloat(url.searchParams.get('lon') || '0');
      const alt = parseFloat(url.searchParams.get('alt') || '1000'); // km
      const kp = parseFloat(url.searchParams.get('kp') || '2');

      // Compute using reconstructed IZMIRAN10 + Carpenter-Anderson hybrid
      const density = computeDensity(lat, lon, alt, kp);

      return jsonResponse({
        model: 'IZMIRAN10-GPID Hybrid',
        inputs: { lat, lon, alt, kp },
        output: density,
        timestamp: new Date().toISOString()
      });
    }

    // Default: API documentation
    return jsonResponse({
      service: 'Φ669 IZMIRAN10 FTP Proxy',
      version: '1.0.0',
      endpoints: {
        '/health': 'Service status and scalar lock',
        '/list': 'List available IZMIRAN10 profile files',
        '/proxy?url=<url>': 'Proxy and parse specific IZMIRAN10 file',
        '/density?lat=&lon=&alt=&kp=': 'Compute electron density at location'
      },
      cors: 'Enabled for macachor.org',
      scalarLock: '𝔐 = 0.6180339887'
    });
  }
};

// ============================================================
// HELPER FUNCTIONS
// ============================================================

function jsonResponse(data, status = 200) {
  return new Response(JSON.stringify(data, null, 2), {
    status,
    headers: {
      ...CORS_HEADERS,
      'Content-Type': 'application/json'
    }
  });
}

function parseDirectoryListing(html) {
  // Parse Apache-style directory listing
  const files = [];
  const regex = /<a href="([^"]+\.(?:dat|txt|prof|zip))">/gi;
  let match;
  while ((match = regex.exec(html)) !== null) {
    files.push({
      name: match[1],
      url: `http://ftp.izmiran.rssi.ru/pub/izmiran/SPIM/${match[1]}`
    });
  }
  return files;
}

function parseIZMIRANProfile(content) {
  // IZMIRAN10 format: altitude (km), electron density (m⁻³), temperature (K)
  const lines = content.split('\n').filter(l => l.trim() && !l.startsWith('#'));
  const points = [];

  for (const line of lines) {
    const parts = line.trim().split(/\s+/).map(parseFloat);
    if (parts.length >= 2 && !isNaN(parts[0])) {
      points.push({
        altitude: parts[0],      // km
        density: parts[1],        // m⁻³ or cm⁻³ (detected below)
        temperature: parts[2] || null  // K
      });
    }
  }

  // Detect units: if density > 1e10, it's m⁻³; else cm⁻³
  const maxDensity = Math.max(...points.map(p => p.density));
  const unit = maxDensity > 1e10 ? 'm⁻³' : 'cm⁻³';
  const conversion = unit === 'm⁻³' ? 1e-6 : 1; // convert to cm⁻³

  return {
    points: points.map(p => ({
      altitude: p.altitude,
      density_cm3: p.density * conversion,
      temperature_K: p.temperature
    })),
    unit: 'cm⁻³',
    altitudeRange: [points[0]?.altitude, points[points.length-1]?.altitude],
    pointCount: points.length
  };
}

function computeDensity(lat, lon, alt, kp) {
  // Hybrid: IZMIRAN10 vertical profile + Carpenter-Anderson equatorial

  // L-shell from latitude (simplified dipole)
  const L = 1 / Math.pow(Math.cos(lat * Math.PI / 180), 2);

  // Carpenter-Anderson equatorial density
  const Lpp = 5.6 - 0.46 * kp;
  let logN;
  if (L < Lpp) {
    logN = 4.5 - 0.6 * L;
  } else {
    logN = 3.0 - 1.5 * L;
  }
  const neq = Math.pow(10, logN);

  // Altitude profile: diffusive equilibrium
  const Re = 6371; // Earth radius km
  const r = (Re + alt) / Re;
  const scaleHeight = 1000; // km (simplified)
  const altitudeFactor = Math.exp(-(alt - 1000) / scaleHeight);

  // Latitude factor
  const latFactor = Math.pow(Math.cos(lat * Math.PI / 180), 2);

  const density = neq * altitudeFactor * latFactor;

  return {
    L_shell: L,
    altitude_km: alt,
    latitude: lat,
    longitude: lon,
    kp: kp,
    plasmapause_L: Lpp,
    equatorial_density_cm3: neq,
    computed_density_cm3: density,
    method: 'IZMIRAN10-Carpenter-Anderson Hybrid'
  };
}
