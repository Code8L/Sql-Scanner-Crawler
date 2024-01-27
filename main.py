import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import colorama


# NB: Colorama is to be used to distinguish different colors when printing output of internal and external links

colorama.init()
GREEN = colorama.Fore.GREEN
GRAY = colorama.Fore.LIGHTBLACK_EX
RESET = colorama.Fore.RESET
YELLOW = colorama.Fore.YELLOW

# Create two global variables one for internal links another for external links
internal_urls = set()
external_urls = set()

#A function to validate URLs

def is_valid(url):
    """

    Checks Whether 'url' is a valid URL

    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)
    # The above code ensures that a proper scheme (protocol, e.g http or https) and domain name exist in the URL

#A function to return all the valid URLs of a web page
def get_all_website_links(url):
    """

    Returns all URLs that is found on 'url' in which it belongs to the same website

    """

    #all the URLs of 'url'

    urls = set()

    # domain name of the URL without the protocol

    domain_name = urlparse(url).netloc
    soup = BeautifulSoup(requests.get(url).content, "html.parser")

    #get all HTML a tags, which is anchor tags that contain the links of the web page
    for a_tag in soup.findAll("a"):
        href = a_tag.attrs.get("href")
        if href == "" or href is None:
            #if href empty tag
            continue

        #join the url if it's relative (not absolute link)
        href = urljoin(url, href)

        #To prevent redundancy, we need to remove HTTP GET parameters from the URLs
        parsed_href = urlparse(href)
        href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path
        if not is_valid(href):
            continue
        if href in internal_urls:
            continue
        if domain_name not in href:
            if href not in external_urls:
                print(f"{GRAY}[!] External link: {href}{RESET}")
                external_urls.add(href)
            continue
        print(f"{GREEN}[*] Internal link: {href}{RESET}")
        urls.add(href)
        internal_urls.add(href)
    return urls

total_urls_visited = 0


def crawl(url, max_urls=30):
    """
    Crawls a web page and extracts all links.
    You'll find all links in external_urls and internal_urls global set variables.
    params:
        max_urls (int): number of max urls to crawl, default is 30.
    """

    global total_urls_visited
    total_urls_visited += 1
    print(f"{YELLOW}[*] Crawling: {url}{RESET}")
    links = get_all_website_links(url)
    for link in links:
        if total_urls_visited > max_urls:
            break
        crawl(link, max_urls= max_urls)


if __name__ == "__main__":
    crawl("http://books.toscrape.com")
    print("[+] Total Internal links:", len(internal_urls))
    print("[+] Total External links:", len(external_urls))
    print("[+] Total URLs:", len(external_urls) + len(internal_urls))
    print("[+] Total crawled URLs:", 200)
