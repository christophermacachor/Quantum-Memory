fetch('/data/okinawa_trough_geochemistry_dataset.json')
  .then(r => r.json())
  .then(data => {
    const jade = data.table_2_analytical_results.find(r => r.sample === 'RV3' && r.dive === 'D423');
    // Inject into your existing gold nav container
    document.getElementById('scalar-feed').innerHTML = `
      <div class="scalar-node" style="border-color:var(--gold)">
        <span class="tag">JADE COHERENCE</span>
        <p>³He/⁴He: ${jade.R_Ra} — CO₂: ${jade.CO2_mmol_kg} mmol/kg</p>
      </div>`;
  });
