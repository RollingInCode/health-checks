#!/usr/bin/env python3
import sys
import time
import yaml
import requests

def load_endpoints(yaml_file_path):
    """
    Loads a list of endpoints from the given YAML file.
    The YAML file is expected to have a top-level 'endpoints' key, for example:

    endpoints:
      - url: https://fetch.com/
        name: fetch index page
        method: GET
        headers:
          user-agent: fetch-synthetic-monitor
      - ...
    """
    with open(yaml_file_path, 'r') as f:
        data = yaml.safe_load(f)
        # 'data' should be a dict that contains a key 'endpoints'
        endpoints = data.get('endpoints', [])
        return endpoints

def check_endpoint_health(endpoints, stats):
    """
    Checks the health of each endpoint by sending a request and updates
    the cumulative stats dictionary with success/fail counters.
    """
    for endpoint in endpoints:
        # Initialize counters if not present
        url = endpoint.get("url")
        if url not in stats:
            stats[url] = {"success": 0, "fail": 0}

        method = endpoint.get("method", "GET")
        headers = endpoint.get("headers", {})
        body = endpoint.get("body", None)

        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, timeout=5)
            elif method.upper() == "POST":
                response = requests.post(url, headers=headers, data=body, timeout=5)
            else:
                # Fallback for other HTTP methods if needed
                response = requests.request(method, url, headers=headers, data=body, timeout=5)

            if response.status_code == 200:
                stats[url]["success"] += 1
                print(f"[UP]   {url} - Status: {response.status_code}")
            else:
                stats[url]["fail"] += 1
                print(f"[DOWN] {url} - Status: {response.status_code}")

        except requests.RequestException as e:
            stats[url]["fail"] += 1
            print(f"[DOWN] {url} - Error: {e}")

def print_availability_stats(stats):
    """
    Prints the current availability (cumulative) for each endpoint after the entire test cycle.
    Availability = (successful checks / total checks) * 100
    """
    print("\nCurrent Cumulative Availability Stats (end of cycle):")
    for url, counts in stats.items():
        total = counts["success"] + counts["fail"]
        if total == 0:
            availability_percentage = 0
        else:
            availability_percentage = counts["success"] / total * 100

        print(
            f"  {url}: "
            f"{availability_percentage:.2f}% availability "
            f"(Success={counts['success']}, Fail={counts['fail']}, Total={total})"
        )
    print("-" * 60)

def main():
    if len(sys.argv) != 2:
        print("Usage: python check_health.py <path_to_endpoints_yaml>")
        sys.exit(1)

    yaml_file_path = sys.argv[1]
    endpoints = load_endpoints(yaml_file_path)

    if not endpoints:
        print("No endpoints found in the YAML file or the file is empty.")
        sys.exit(1)

    # Dictionary to store cumulative stats for each endpoint
    stats = {}

    print(f"Loaded {len(endpoints)} endpoints. Starting health checks every 15 seconds...")

    while True:
        check_endpoint_health(endpoints, stats)
        # Print availability after the entire test cycle finishes
        print_availability_stats(stats)
        time.sleep(15)

if __name__ == "__main__":
    main()