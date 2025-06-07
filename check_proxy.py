import requests
import os

if not os.path.exists("valid_proxies"):
    print("Error: 'valid_proxies' file not found!")
    print("Please run the proxy checker script first to generate valid proxies.")
    exit(1)

# Load valid proxies
with open("valid_proxies", "r") as f:
    proxies = f.read().split("\n")
    proxies = [p.strip() for p in proxies if p.strip()]

if not proxies:
    print("No valid proxies found in file")
    exit(1)

print(f"Loaded {len(proxies)} valid proxies")

sites_to_check = [""]

counter = 0

for site in sites_to_check:

    if counter >= len(proxies):
        print(f"No more proxies available for site: {site}")
        break
        
    try:
        print(f"Using proxy: {proxies[counter]}")
        res = requests.get(site, 
                          proxies={"http": proxies[counter], "https": proxies[counter]},
                          timeout=15)
        print(f" {site}: Status {res.status_code}")
        
    except requests.exceptions.RequestException as e:
        print(f" Failed to access {site} with proxy {proxies[counter]}: {str(e)}")
    except Exception as e:
        print(f" Unexpected error: {str(e)}")
    finally:
        counter += 1

print(f"\nSummary: Checked {min(counter, len(sites_to_check))} sites with {len(proxies)} available proxies")