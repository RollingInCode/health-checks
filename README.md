
# Health Check Script

This Python script monitors a list of HTTP endpoints by periodically sending requests and recording their availability. After each monitoring cycle, it outputs a report to your console with the current success/failure counts and a cumulative availability percentage for each endpoint.

## Key Features

* Customizable Endpoints: Provide a YAML file containing endpoint definitions (URLs, methods, headers).
* Periodic Checks: Repeats the checks every 15 seconds by default (configurable).
* Cumulative Availability: Tracks how many times each endpoint has been up or down, along with the percentage over time.
* Configurable Requests: Supports GET, POST (with optional body), and custom headers.
### Prerequisites

    1. Python 3.6+ installed.

    2. Dependencies: bash

```
pip install requests pyyaml
```

### YAML Configuration
Create or update your YAML file to have a top-level `endpoints` key. Below is an example:
```yaml

endpoints:
  - url: https://fetch.com/
    name: fetch index page
    method: GET
    headers:
      user-agent: fetch-synthetic-monitor

  - url: https://fetch.com/careers
    name: fetch careers page
    method: GET
    headers:
      user-agent: fetch-synthetic-monitor

  - url: https://fetch.com/some/post/endpoint
    name: fetch some fake post endpoint
    method: POST
    headers:
      content-type: application/json
      user-agent: fetch-synthetic-monitor
    body: '{"foo":"bar"}'

  - url: https://www.fetchrewards.com/
    name: fetch rewards index page
    method: GET
```

### How to Run
    1. Save the Script
Copy the health-check Python script into a file, for example `health-check.py.`

    2. Ensure the Script is Executable (optional, on Linux/macOS):

`chmod +x health-check.py`

    3. Run the Script with Your YAML File

`
python health-check.py /path/to/endpoints.yaml
`

Or if you made it executable:


```bash
./health-check.py /path/to/endpoints.yaml
```
The script will:
* Load endpoint definitions from the specified file.
* Perform the checks.
* Output console logs showing whether each endpoint is UP (HTTP 200) or DOWN (non-200 status or exception).
* Print cumulative availability stats at the end of each check cycle.
#### Example Output
```javascript
[UP]   https://fetch.com/ - Status: 200
[DOWN] https://fetch.com/careers - Status: 404
[UP]   https://www.fetchrewards.com/ - Status: 200

Current Cumulative Availability Stats (end of cycle):
  https://fetch.com/: 100.00% availability (Success=1, Fail=0, Total=1)
  https://fetch.com/careers: 0.00% availability (Success=0, Fail=1, Total=1)
  https://www.fetchrewards.com/: 100.00% availability (Success=1, Fail=0, Total=1)
------------------------------------------------------------
```

### Configuration Options

* Endpoints File: Adjust the file path you pass in to point to your YAML file.
* Headers: Add or remove custom headers for each request within the YAML.
* Method: The script defaults to GET if not specified. You can override it to use POST or other HTTP methods as needed.
* Body: Include a JSON or text payload for POST requests.

### Tips and Best Practices
    1. Monitoring Frequency: The script defaults to 15-second intervals but can be changed by altering the time.sleep(15) value in the code.

    2. Timeout: The script uses a 5-second timeout for each request (timeout=5). Adjust this based on expected response times.

    3. Error Handling: If the request fails due to a networking error, the script logs a [DOWN] message along with the exception.

### Contributing
Feel free to modify the script for any additional features such as:

    1. Sending alerts or notifications when an endpoint goes down.

    2. Writing logs to a file or external monitoring service.

    3. Scheduling in a Docker container, Kubernetes CronJob, or a system-level scheduler (e.g., cron).