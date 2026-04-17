# ============================================================
#  WEEK 14 LAB — Q1: API EXPLORER
#  COMP2152 — Joshua Zaakir
# ============================================================

import urllib.request
import json


# TODO: Complete make_request(url)
#   Use urllib.request.urlopen(url)
#   Read response body: response.read().decode()
#   Return: {"status": response.status, "headers": dict(response.headers), "body": body}
#   If error occurs, return: {"status": 0, "headers": {}, "body": "", "error": str(e)}
def make_request(url):
    try:
        response = urllib.request.urlopen(url)
        body = response.body().decode()
        return {"status": response.status, "headers": dict(response.headers), "body": body}
    except Exception as e:
        return {"status": 0, "headers": {}, "body": "", "error": str(e)}


# TODO: Complete parse_json(body)
#   Use json.loads(body) to convert JSON string to a dictionary
#   If it fails (ValueError), return None
def parse_json(body):
    try:
        return json.loads(body)
    except (ValueError, json.JSONDecodeError):
        return None


# TODO: Complete check_api_info(response)
#   Create a findings list
#   Check headers for security issues:
#     If "Server" in headers → append f"Server version exposed: {value}"
#     If "X-Powered-By" in headers → append f"Technology exposed: {value}"
#     If headers.get("Access-Control-Allow-Origin") == "*" → append "CORS: open to all origins"
#   Return findings
def check_api_info(response):
    findings = []
    headers = response.get("headers", {})
    if "Server" in headers:
        findings.append(f"Server version exposed: {headers['Server']}")
    if "X-Powered-By" in headers:
        findings.append(f"Technology exposed: {headers['X-Powered-By']}")
    if headers.get("Access-Control-Allow-Origin") == "*":
        findings.append("CORS: open to all origins")
        return findings

# --- Main (provided) ---
if __name__ == "__main__":
    print("=" * 60)
    print("  Q1: API EXPLORER")
    print("=" * 60)

    url = "http://httpbin.org/headers"
    print(f"\n--- Requesting {url} ---")

    resp = make_request(url)

    if resp and resp.get("status"):
        print(f"  Status: {resp['status']}")

        print("\n--- Response Headers ---")
        for key, val in resp["headers"].items():
            print(f"  {key:<16}: {val}")

        print("\n--- Parsed JSON Body ---")
        data = parse_json(resp["body"])
        if data:
            for key, val in data.items():
                print(f"  {key}: {val}")
        else:
            print("  (not JSON or parse failed)")

        print("\n--- Security Findings ---")
        findings = check_api_info(resp)
        if findings:
            for f in findings:
                print(f"  {f}")
        else:
            print("  (no issues found)")
    else:
        error = resp.get("error", "unknown") if resp else "make_request returned None"
        print(f"  Error: {error}")

    print("\n" + "=" * 60)