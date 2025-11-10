import http.client
import json
import csv

# === Replace this with your actual API token ===
TOKEN = "<your_token_here>"

# === Folder options ===
folder_options = {
    "1": "Shared",
    "2": "Mobile Users",
    "3": "Remote Networks",
    "4": "Service Connection",
    "5": "Mobile Users Container",
    "6": "Mobile Users Explicit Proxy"
}

# === Display folder choices ===
print("Select Folder:")
for key, value in folder_options.items():
    print(f"{key}. {value}")

# === Get user input ===
choice = input("\nEnter your choice (1-6): ").strip()
if choice not in folder_options:
    print("Invalid choice. Please run again.")
    exit()

folder_name = folder_options[choice]
print(f"\n📁 Selected Folder: {folder_name}\n")

# === API connection ===
print("📡 Fetching data from Palo Alto SASE API...")

conn = http.client.HTTPSConnection("api.sase.paloaltonetworks.com")
headers = {
    'Accept': 'application/json',
    'Authorization': f'Bearer {TOKEN}'
}

endpoint = f"/sse/config/v1/url-access-profiles?folder={folder_name.replace(' ', '%20')}"
conn.request("GET", endpoint, '', headers)
res = conn.getresponse()
data = res.read().decode("utf-8")

try:
    response_json = json.loads(data)
except json.JSONDecodeError:
    print("Failed to parse API response. Check your token or API URL.")
    exit()

# === Check for data and save to CSV ===
if "data" not in response_json or not response_json["data"]:
    print("No profiles found in this folder or invalid response.\n")
    print("Here’s what the API returned:")
    print(json.dumps(response_json, indent=2))
else:
    profiles = response_json["data"]

    # Define CSV file name based on folder
    filename = f"url_profiles_{folder_name.replace(' ', '_')}.csv"

    # Extract all possible keys dynamically from all profiles
    fieldnames = set()
    for profile in profiles:
        fieldnames.update(profile.keys())
    fieldnames = sorted(fieldnames)

    # Write to CSV
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(profiles)

    print(f"Data saved successfully to: {filename}")

# === Close connection ===
conn.close()  


### Testing Note #### To test this script, replace <your_token_here> with a valid Palo Alto SASE API

## Testing Instructions:

## Testing 2
