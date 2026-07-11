#!/usr/bin/env python3
"""
Coherence Report Generator - Daily Assessment

Automated daily χ(C) coherence assessment for Quantum Memory.
Generates comprehensive reports on satellite network health and coherence metrics.
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import hashlib


class CoherenceReportGenerator:
    """
    Generates daily coherence assessment reports (χ(C)) for the Φ-669 satellite network.
    Tracks historical trends and alerts on anomalies.
    """
    
    VERSION = "1.0"
    REPORT_TYPE = "Daily Coherence Assessment"
    
    def __init__(self):
        """Initialize report generator."""
        self.report_date = datetime.utcnow().date()
        self.report_time = datetime.utcnow()
        self.metrics: Dict[str, Any] = {}
        self.alerts: List[Dict] = []
        self.historical_data: List[Dict] = []
    
    def calculate_chi_c_metric(self, satellite_data: Dict[str, Any]) -> float:
        """
        Calculate χ(C) - Main coherence metric for network assessment.
        
        Formula: χ(C) = (Σ coherence_i * weight_i) / Σ weight_i
        Where weight is based on satellite criticality and orbital band.
        """
        satellites = satellite_data.get("satellites", [])
        if not satellites:
            return 0.0
        
        # Assign weights based on satellite type
        weights = {
            "Master": 1.0,
            "Gate": 0.9,
            "Relay": 0.7,
            "Sync": 0.6,
            "Sensor": 0.4
        }
        
        total_weighted_coherence = 0
        total_weight = 0
        
        for sat in satellites:
            sat_type = sat.get("type", "Sensor")
            weight = weights.get(sat_type, 0.4)
            coherence = sat.get("coherence", 0.5)
            
            total_weighted_coherence += coherence * weight
            total_weight += weight
        
        if total_weight == 0:
            return 0.0
        
        return total_weighted_coherence / total_weight
    
    def assess_coherence_state(self, chi_c: float) -> Dict[str, Any]:
        """
        Classify network state based on χ(C) metric.
        """
        if chi_c >= 0.85:
            return {
                "state": "OPTIMAL",
                "description": "Network operating at peak coherence",
                "color": "green",
                "action": "MAINTAIN"
            }
        elif chi_c >= 0.70:
            return {
                "state": "NOMINAL",
                "description": "Network within acceptable parameters",
                "color": "yellow",
                "action": "MONITOR"
            }
        elif chi_c >= 0.50:
            return {
                "state": "DEGRADED",
                "description": "Network performance reduced",
                "color": "orange",
                "action": "INVESTIGATE"
            }
        else:
            return {
                "state": "CRITICAL",
                "description": "Network coherence critically low",
                "color": "red",
                "action": "IMMEDIATE_INTERVENTION"
            }
    
    def identify_anomalies(self, satellite_data: Dict[str, Any]) -> List[Dict]:
        """
        Identify satellites or patterns that deviate from expected performance.
        """
        anomalies = []
        satellites = satellite_data.get("satellites", [])
        
        # Calculate network average
        avg_coherence = sum(s.get("coherence", 0.5) for s in satellites) / len(satellites) if satellites else 0.5
        std_dev = self._calculate_std_dev([s.get("coherence", 0.5) for s in satellites])
        
        # Identify outliers (more than 2 std devs from mean)
        threshold = avg_coherence - (2 * std_dev)
        
        for sat in satellites:
            coherence = sat.get("coherence", 0.5)
            if coherence < threshold:
                anomalies.append({
                    "satellite_id": sat.get("id", "UNKNOWN"),
                    "name": sat.get("name", "Unknown"),
                    "coherence": coherence,
                    "deviation": avg_coherence - coherence,
                    "severity": "HIGH" if coherence < 0.3 else "MEDIUM",
                    "recommendation": "Investigate cause" if coherence < 0.3 else "Monitor"
                })
        
        return anomalies
    
    def generate_daily_report(self, satellite_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive daily coherence report.
        """
        # Calculate main metric
        chi_c = self.calculate_chi_c_metric(satellite_data)
        
        # Assess state
        state_assessment = self.assess_coherence_state(chi_c)
        
        # Identify anomalies
        anomalies = self.identify_anomalies(satellite_data)
        
        # Build report
        report = {
            "report_metadata": {
                "type": self.REPORT_TYPE,
                "version": self.VERSION,
                "date": self.report_date.isoformat(),
                "generated_at": self.report_time.isoformat() + "Z",
                "report_id": self._generate_report_id()
            },
            "network_metrics": {
                "chi_c_score": chi_c,
                "satellites_total": len(satellite_data.get("satellites", [])),
                "satellites_coherent": sum(1 for s in satellite_data.get("satellites", []) if s.get("coherence", 0) >= 0.7),
                "satellites_degraded": sum(1 for s in satellite_data.get("satellites", []) if 0.3 <= s.get("coherence", 0) < 0.7),
                "satellites_critical": sum(1 for s in satellite_data.get("satellites", []) if s.get("coherence", 0) < 0.3)
            },
            "state_assessment": state_assessment,
            "anomalies": {
                "count": len(anomalies),
                "high_severity": sum(1 for a in anomalies if a["severity"] == "HIGH"),
                "details": anomalies[:10]  # Top 10 anomalies
            },
            "recommendations": self._generate_recommendations(chi_c, len(anomalies), state_assessment),
            "historical_trend": self._calculate_trend()
        }
        
        return report
    
    def _generate_recommendations(self, chi_c: float, anomaly_count: int, state: Dict) -> List[str]:
        """
        Generate actionable recommendations based on assessment.
        """
        recommendations = []
        
        if chi_c < 0.7:
            recommendations.append("Perform network-wide coherence recalibration")
        
        if chi_c < 0.5:
            recommendations.append("URGENT: Initiate emergency gate synchronization")
        
        if anomaly_count > 10:
            recommendations.append("Investigate root cause of widespread anomalies")
        
        if state["state"] == "CRITICAL":
            recommendations.append("Activate backup coherence protocols")
            recommendations.append("Prepare scalar override adjustments for critical satellites")
        
        if not recommendations:
            recommendations.append("Continue routine monitoring and maintenance")
        
        return recommendations
    
    def _calculate_trend(self) -> Dict[str, Any]:
        """
        Calculate historical trend (placeholder for historical data).
        """
        return {
            "period_days": 7,
            "trend": "STABLE",
            "average_chi_c_7d": 0.742,
            "min_chi_c_7d": 0.718,
            "max_chi_c_7d": 0.765
        }
    
    def _calculate_std_dev(self, values: List[float]) -> float:
        """
        Calculate standard deviation of values.
        """
        if not values:
            return 0.0
        
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance ** 0.5
    
    def _generate_report_id(self) -> str:
        """
        Generate unique report ID based on date and hash.
        """
        date_str = self.report_date.isoformat()
        hash_input = f"CHI_C_REPORT_{date_str}"
        report_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:12]
        return f"CHI_C_{date_str}_{report_hash}"
    
    def export_report_json(self, report: Dict) -> str:
        """
        Export report as JSON string.
        """
        return json.dumps(report, indent=2, default=str)
    
    def export_report_markdown(self, report: Dict) -> str:
        """
        Export report as Markdown for easy sharing.
        """
        md = f"""
# Daily Coherence Assessment Report (χ(C))

**Date:** {report['report_metadata']['date']}  
**Report ID:** {report['report_metadata']['report_id']}  
**Generated:** {report['report_metadata']['generated_at']}

## Executive Summary

**χ(C) Score:** {report['network_metrics']['chi_c_score']:.3f}  
**Network State:** {report['state_assessment']['state']}  
**Status:** {report['state_assessment']['description']}

## Network Metrics

| Metric | Value |
|--------|-------|
| Total Satellites | {report['network_metrics']['satellites_total']} |
| Coherent | {report['network_metrics']['satellites_coherent']} |
| Degraded | {report['network_metrics']['satellites_degraded']} |
| Critical | {report['network_metrics']['satellites_critical']} |

## Anomalies Detected

Total: {report['anomalies']['count']} anomalies  
High Severity: {report['anomalies']['high_severity']}

## Recommendations

"""
        for i, rec in enumerate(report['recommendations'], 1):
            md += f"- {rec}\n"
        
        md += f"""
## Historical Trend

**7-Day Average χ(C):** {report['historical_trend']['average_chi_c_7d']:.3f}  
**Range:** {report['historical_trend']['min_chi_c_7d']:.3f} - {report['historical_trend']['max_chi_c_7d']:.3f}

---

*Generated by Coherence Report Generator v{report['report_metadata']['version']}*
"""
        return md


if __name__ == "__main__":
    # Example usage
    generator = CoherenceReportGenerator()
    
    # Sample satellite data
    sample_data = {
        "satellites": [
            {"id": "SCP-001", "name": "Prime Anchor", "type": "Master", "coherence": 0.995},
            {"id": "SCP-002", "name": "Relay A", "type": "Relay", "coherence": 0.887},
            {"id": "SCP-003", "name": "Relay B", "type": "Relay", "coherence": 0.865},
            {"id": "SCP-004", "name": "Sensor A", "type": "Sensor", "coherence": 0.754},
            {"id": "SCP-005", "name": "Sensor B", "type": "Sensor", "coherence": 0.721},
            {"id": "SCP-006", "name": "Gate Node", "type": "Gate", "coherence": 0.812},
        ]
    }
    
    # Generate report
    report = generator.generate_daily_report(sample_data)
    
    print("=== Daily Coherence Assessment Report ===")
    print(generator.export_report_markdown(report))
    print()
    print("=== JSON Export ===")
    print(generator.export_report_json(report))
