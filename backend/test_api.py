"""Quick test for the /api/analyze endpoint."""
import urllib.request
import urllib.parse
import json

url = "http://localhost:8000/api/analyze"

text = (
    "Our AP process starts when invoices arrive by email. Sarah downloads them "
    "and keys data into SAP manually every morning, about 200 invoices per week. "
    "She runs 3-way matching and chases procurement for discrepancies. "
    "Approvals over 5000 dollars go to managers via email. "
    "Mike creates payment batches on Friday. "
    "Lisa does month-end reconciliation in Excel."
)

# Send as form data
data = urllib.parse.urlencode({"text": text}).encode()
req = urllib.request.Request(url, data=data)
req.add_header("Content-Type", "application/x-www-form-urlencoded")

print("Sending request to /api/analyze...")
print("This may take 30-60 seconds...\n")

response = urllib.request.urlopen(req, timeout=120)
result = json.loads(response.read())

print("Status:", result["status"])
print()
print("=== EXECUTIVE SUMMARY ===")
print(result["data"]["executive_summary"])
print()
print("Steps found:", len(result["data"]["scored_steps"]))
print("Priority targets:", len(result["data"]["priority_targets"]))
print("Opportunities:", len(result["data"]["opportunities"]))
print()
print("=== TOP OPPORTUNITIES ===")
for opp in result["data"]["opportunities"]:
    print(f"  - {opp['step_name']} -> {opp['ap_pattern']} ({opp['effort_reduction_pct']}% effort reduction)")
print()
print("API test PASSED!")
