from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import numpy as np

app = FastAPI()

# 1. Enable CORS for POST requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods, including POST
    allow_headers=["*"],  # Allows all headers
)

# The sample telemetry data provided
telemetry_data = [
  {"region": "apac", "service": "payments", "latency_ms": 118.83, "uptime_pct": 97.493, "timestamp": 20250301},
  {"region": "apac", "service": "support", "latency_ms": 217.2, "uptime_pct": 98.751, "timestamp": 20250302},
  {"region": "apac", "service": "checkout", "latency_ms": 120.65, "uptime_pct": 98.982, "timestamp": 20250303},
  {"region": "apac", "service": "payments", "latency_ms": 135.75, "uptime_pct": 99.347, "timestamp": 20250304},
  {"region": "apac", "service": "analytics", "latency_ms": 189.06, "uptime_pct": 97.935, "timestamp": 20250305},
  {"region": "apac", "service": "support", "latency_ms": 160.37, "uptime_pct": 97.497, "timestamp": 20250306},
  {"region": "apac", "service": "checkout", "latency_ms": 197, "uptime_pct": 97.9, "timestamp": 20250307},
  {"region": "apac", "service": "payments", "latency_ms": 157.82, "uptime_pct": 98.601, "timestamp": 20250308},
  {"region": "apac", "service": "recommendations", "latency_ms": 190.88, "uptime_pct": 98.826, "timestamp": 20250309},
  {"region": "apac", "service": "catalog", "latency_ms": 203.42, "uptime_pct": 98.248, "timestamp": 20250310},
  {"region": "apac", "service": "payments", "latency_ms": 213.55, "uptime_pct": 98.486, "timestamp": 20250311},
  {"region": "apac", "service": "support", "latency_ms": 188.33, "uptime_pct": 98.787, "timestamp": 20250312},
  {"region": "emea", "service": "payments", "latency_ms": 194.59, "uptime_pct": 99.211, "timestamp": 20250301},
  {"region": "emea", "service": "analytics", "latency_ms": 149.81, "uptime_pct": 98.844, "timestamp": 20250302},
  {"region": "emea", "service": "recommendations", "latency_ms": 219.42, "uptime_pct": 98.932, "timestamp": 20250303},
  {"region": "emea", "service": "support", "latency_ms": 192.47, "uptime_pct": 99.061, "timestamp": 20250304},
  {"region": "emea", "service": "payments", "latency_ms": 159.13, "uptime_pct": 99.212, "timestamp": 20250305},
  {"region": "emea", "service": "analytics", "latency_ms": 229.88, "uptime_pct": 97.918, "timestamp": 20250306},
  {"region": "emea", "service": "support", "latency_ms": 138.33, "uptime_pct": 98.835, "timestamp": 20250307},
  {"region": "emea", "service": "checkout", "latency_ms": 199.58, "uptime_pct": 98.969, "timestamp": 20250308},
  {"region": "emea", "service": "catalog", "latency_ms": 139.4, "uptime_pct": 99.444, "timestamp": 20250309},
  {"region": "emea", "service": "support", "latency_ms": 151.95, "uptime_pct": 98.836, "timestamp": 20250310},
  {"region": "emea", "service": "catalog", "latency_ms": 138.25, "uptime_pct": 99.297, "timestamp": 20250311},
  {"region": "emea", "service": "analytics", "latency_ms": 226.79, "uptime_pct": 98.66, "timestamp": 20250312},
  {"region": "amer", "service": "support", "latency_ms": 179.11, "uptime_pct": 97.586, "timestamp": 20250301},
  {"region": "amer", "service": "checkout", "latency_ms": 217.13, "uptime_pct": 98.863, "timestamp": 20250302},
  {"region": "amer", "service": "payments", "latency_ms": 167.45, "uptime_pct": 97.965, "timestamp": 20250303},
  {"region": "amer", "service": "catalog", "latency_ms": 173.84, "uptime_pct": 97.369, "timestamp": 20250304},
  {"region": "amer", "service": "analytics", "latency_ms": 131.92, "uptime_pct": 98.234, "timestamp": 20250305},
  {"region": "amer", "service": "support", "latency_ms": 176.55, "uptime_pct": 97.179, "timestamp": 20250306},
  {"region": "amer", "service": "payments", "latency_ms": 212.66, "uptime_pct": 97.622, "timestamp": 20250307},
  {"region": "amer", "service": "analytics", "latency_ms": 212.37, "uptime_pct": 99.215, "timestamp": 20250308},
  {"region": "amer", "service": "checkout", "latency_ms": 210.93, "uptime_pct": 98.062, "timestamp": 20250309},
  {"region": "amer", "service": "catalog", "latency_ms": 213.86, "uptime_pct": 97.522, "timestamp": 20250310},
  {"region": "amer", "service": "analytics", "latency_ms": 145.49, "uptime_pct": 98.801, "timestamp": 20250311},
  {"region": "amer", "service": "payments", "latency_ms": 206.66, "uptime_pct": 97.819, "timestamp": 20250312}
]

# Pydantic model for the request body
class TelemetryRequest(BaseModel):
    regions: List[str]
    threshold_ms: int

@app.get("/")
def read_root():
    """A simple GET endpoint to confirm the server is running."""
    return {"message": "Telemetry analysis endpoint is running. Please POST to /analyze"}

@app.post("/analyze")
def analyze_telemetry(request: TelemetryRequest):
    """
    Accepts a POST request with regions and a threshold,
    and returns per-region metrics.
    """
    results = []
    for region_name in request.regions:
        # Filter data for the current region
        region_data = [d for d in telemetry_data if d["region"] == region_name]

        if not region_data:
            continue

        latencies = [d["latency_ms"] for d in region_data]
        uptimes = [d["uptime_pct"] for d in region_data]

        # Calculate metrics using numpy
        avg_latency = np.mean(latencies)
        p95_latency = np.percentile(latencies, 95)
        avg_uptime = np.mean(uptimes)
        
        # Count breaches
        breaches = sum(1 for latency in latencies if latency > request.threshold_ms)

        results.append({
            "region": region_name,
            "avg_latency": round(avg_latency, 2),
            "p95_latency": round(p95_latency, 2),
            "avg_uptime": round(avg_uptime, 3),
            "breaches": breaches,
        })

    return results

# This is the entry point for Vercel
handler = app


### Example of how to test with curl:
# curl -X POST "http://127.0.0.1:8000/analyze" \
# -H "Content-Type: application/json" \
# -d '{"regions":["emea","amer"],"threshold_ms":152}'
#
# Expected response for the example:
# [
#   {
#     "region": "emea",
#     "avg_latency": 178.3,
#     "p95_latency": 228.8,
#     "avg_uptime": 98.935,
#     "breaches": 9
#   },
#   {
#     "region": "amer",
#     "avg_latency": 187.33,
#     "p95_latency": 215.9,
#     "avg_uptime": 98.02,
#     "breaches": 11
#   }
# ]