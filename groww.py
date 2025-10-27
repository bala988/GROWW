import http.client
import json
import csv
import urllib.parse

# 🔐 Paste your API access token here (replace <token> with actual one)
ACCESS_TOKEN = "Bearer "

# Position options
position_options = {
    "1": "pre",
    "2": "post"
}

# Folder options
folder_options = {
    "1": "Shared",
    "2": "Mobile Users",
    "3": "Remote Networks",
    "4": "Service Connections",
    "5": "Mobile Users Container",
    "6": "Mobile Users Explicit Proxy"
}

# --- Ask user to choose position ---
print("\nSelect Position:")
for k, v in position_options.items():
    print(f"{k}. {v}")
position_choice = input("Enter the number for Position: ").strip()
position = position_options.get(position_choice, "pre")

# --- Ask user to choose folder ---
print("\nSelect Folder:")
for k, v in folder_options.items():
    print(f"{k}. {v}")
folder_choice = input("Enter the number for Folder: ").strip()
folder = folder_options.get(folder_choice, "Shared")

print(f"\n📡 Using Position: {position}, Folder: {folder}\n")

# Encode folder for URL
encoded_folder = urllib.parse.quote(folder)

# API request setup
conn = http.client.HTTPSConnection("api.sase.paloaltonetworks.com")
headers = {
    'Accept': 'application/json',
    'Authorization': ACCESS_TOKEN.strip()
}

endpoint = f"/sse/config/v1/security-rules?position={position}&folder={encoded_folder}&limit=500"
print(f"Requesting: {endpoint}\n")

# Send request
conn.request("GET", endpoint, '', headers)
res = conn.getresponse()
data = res.read()
decoded_data = data.decode("utf-8")

print(f"HTTP Status: {res.status}")

# Parse response
try:
    json_data = json.loads(decoded_data)
except json.JSONDecodeError:
    print("❌ Failed to parse JSON response.")
    print(decoded_data)
    exit()

# Check API response
if res.status != 200:
    print("❌ API Error:")
    print(json.dumps(json_data, indent=4))
    exit()

rules = json_data.get("data", [])
if not rules:
    print("⚠️ No rules found in the response.")
    exit()

# --- Write to CSV ---
fieldnames = sorted(set().union(*(r.keys() for r in rules)))
safe_folder = folder.replace(" ", "_")
csv_filename = f"{position}_{safe_folder}_rules.csv"

with open(csv_filename, "w", newline='', encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rules)

print(f"✅ Successfully saved {len(rules)} rules to '{csv_filename}'.")
