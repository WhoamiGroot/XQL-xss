advanced XSS (Cross-Site Scripting) scanner that's designed to be used for web application security testing, often as part of bug bounty hunting. It utilizes a combination of different techniques to test for potential XSS vulnerabilities on a website. 

![Screenshot from 2025-02-09 18-00-41](https://github.com/user-attachments/assets/0a30d1d0-7cc5-434e-911a-6b9f88937925)

Here is a write up about what you can do with reflected xss for example:

```
https://pwnsauc3.medium.com/weaponizing-reflected-xss-to-account-takeover-ae8aeea7aca3
```

Installation:

```
git clone https://github.com/WhoamiGroot/XQL-xss
```
```
cd XQL-xss
```
```
pip install requests
```
```
pip3 install beautifulsoup4
```
```
pip install selenium
```
Run the script:
```
python3 xql.py https://example.com
```

Additional Considerations:

    Webdriver: Make sure that you have the Chrome WebDriver installed for Selenium to work.
    Legal Authorization: Only run this script on websites you have permission to test.


To install the Chrome WebDriver for Selenium, you need to follow these steps:
1. Install Google Chrome (if you haven't already)

Ensure that you have Google Chrome installed on your machine. You can download it from Google Chrome.
2. Install Selenium via pip

First, you need to install the Selenium Python package, which allows you to control the browser. You can install it using pip:

~ pip install selenium

Here's a breakdown of the key parts:
1. Payloads for XSS testing:

    WAF Bypass Payloads: These are simple XSS payloads that are crafted to bypass basic web application firewalls (WAFs).
    Polyglot Payloads: These are crafted payloads that can potentially work across different contexts or encodings.
    Blind XSS Payload: This payload is used for blind XSS attacks, where the XSS might not show up immediately but can be triggered when the payload is processed by the server.

2. Functions for Testing XSS:

    encode_payload(): Encodes the payload to bypass certain types of filters like URL encoding or HTML entity encoding.
    get_forms(): Extracts forms from the HTML of the target URL.
    form_details(): Gathers the form action, method, and input types.
    submit_form(): Submits a form with an XSS payload to check for stored XSS.
    test_xss(): Tests for reflected XSS by modifying URL query parameters with payloads and checking if they appear in the response.
    scan_dom_xss(): Tests for DOM-based XSS using Selenium, which simulates interactions with a browser.
    scan_xss(): A high-level function that tests for reflected XSS on URLs.
    scan_stored_xss(): Tests for stored XSS by submitting a payload to forms.

3. Crawling:

    crawl_and_scan(): This is the function that crawls a domain, visiting each page and scanning for XSS vulnerabilities.
    ThreadPoolExecutor is used to speed up the process by testing multiple parameters and payloads concurrently.

4. Blind XSS Logging:

    The Blind XSS payload sends the data to a remote logging server (defined by the BLIND_XSS_SERVER variable). You would replace this with your own XSS logging server, which allows you to track when the payload is executed.

5. Main Execution:

    The script accepts a URL as a command-line argument and then starts crawling and scanning the target website for XSS vulnerabilities.

Key Points to Keep in Mind:

    Legal Considerations: Running this code on any website without permission is illegal. Always ensure you have explicit authorization to test a site.
    Burp Suite or Logging Server: You need an XSS logger like Burp Collaborator or a custom logging server for the Blind XSS payloads to work.
    External Dependencies: This script relies on several libraries such as requests, BeautifulSoup, and selenium, and you'll need the Chrome WebDriver for Selenium.

First go to BurpCollaborator:
![Screenshot from 2025-02-09 17-25-08](https://github.com/user-attachments/assets/431814fb-d2fa-4112-bcfc-3a84add7ebb6)

Then Copy to clipboard:
![Screenshot from 2025-02-09 17-25-45](https://github.com/user-attachments/assets/40b7cff5-d660-4d74-ad98-83782b4a1c7b)

Then edit line 14 in the script: (The blue selected line and paste from your clipboard).
![Screenshot from 2025-02-09 17-26-33](https://github.com/user-attachments/assets/19d75b62-2018-4421-9d73-d156df0ff358)

And have fun happy hacking, Don't forget foxy proxy on port 8080, localhost 127.0.0.1
![XSS_NEW](https://github.com/user-attachments/assets/39e4f825-fe9f-4e8d-a1a6-ef0a4f5b6f6e)

When you are finished you can view the results in txt or JSON file.
example:
![Screenshot from 2025-02-09 17-43-15](https://github.com/user-attachments/assets/5a07eb92-21ad-4a07-8b13-1dcfc2b4c4c8)

Key Points to Keep in Mind:

    Legal Considerations: Running this code on any website without permission is illegal. Always ensure you have explicit authorization to test a site.
    Burp Suite or Logging Server: You need an XSS logger like Burp Collaborator or a custom logging server for the Blind XSS payloads to work.
    External Dependencies: This script relies on several libraries such as requests, BeautifulSoup, and selenium, and you'll need the Chrome WebDriver for Selenium.
