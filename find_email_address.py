from selenium import webdriver
from pprint import pprint
from urlparse import urlparse
import argparse
import time


def log(msg):
    if args.verbose:
        print(msg)

def find_links(driver, domain):
    links = set()
    elems = driver.find_elements_by_xpath('//a[@href]')
    # could use //a[startswith(href'mailto')] to get emails and do email links
    # separately but we'll just get all links and then divvy them up
    for el in elems:
        link = el.get_attribute('href')
        if (link is None):
            continue
        url = urlparse(link)
        if url.hostname == domain or url.scheme == 'mailto':
            links.add(link)
        else:
            log('Ignoring off domain address: ' + link)

    return links

def scrape_page(url):
    """ Loads url parameter in browser, returns set of links
    """
    links = set()
    domain = urlparse(url).hostname

    log("Scraping url: " + url)

    driver.get(url)
    time.sleep(2) # TODO: undo this hack by catching stale element exception and retry
    # this will let us know if we were 30x'd to a different host
    page_hostname = driver.execute_script('return window.location.hostname')
    # unfortunately, WebDriver does not expose HTTP headers, so we can't
    # be sure we'll be able to inject this JavaScript in the host page, but
    # it seems to fail silently with HTMLUNIT at least

    if (not page_hostname == domain):
        return links
    links = find_links(driver, domain)
    return links

def scrape_domain(domain, port, max_pages):
    """ Wraps scrape_page, making the initial URL out of the domain and port numbers """
    initial_page = "http://"+domain;
    emails = set()
    if port != 80:
        initial_page+=':'+str(port)

    links = scrape_page(initial_page)
    while len(links) > 0 and max_pages > 0:
        link = links.pop()
        if link not in visited_links:
            url = urlparse(link)
            if (url.scheme == 'mailto'):
                log('Found email:' + link)

                emails.add(url.path)
                continue
            elif url.path.endswith('.zip') or url.path.endswith('.pdf') or url.path.endswith('.txt'):
                log('Skipping suspected bad content type:' +link)
                continue
            visited_links.add(link)
            links = links | scrape_page(link)
            max_pages-=1
        else:
            log('Skipping previously visited link: ' + link)
    return emails


parser = argparse.ArgumentParser(description='Scrape a domain for email addresses.')
parser.add_argument('hostname', metavar='domain', nargs=1,
                    help='Host to scrape')
parser.add_argument('--port',
                    help='Port number, default: 80')
parser.add_argument('--browser', nargs=1, type=str,
                    help='Use Chrome instead of HTMLUNIT')
parser.add_argument('--verbose',
                    help='Output additional logging',  action="store_true")
parser.add_argument('--max-pages',
                    help='Max number of pages to fetch, default: 1000')


args = parser.parse_args()

domain = args.hostname[0]

if args.port is None:
    port = 80
else:
    port = args.port

if (args.max_pages is None):
    max_pages = 1000
else:
    max_pages = int(args.max_pages)

if args.browser is None or args.browser[0].lower() == 'htmlunit':
    driver = webdriver.Remote(
        desired_capabilities=webdriver.DesiredCapabilities.HTMLUNIT)
elif args.browser[0].lower() == 'chrome':
    driver = webdriver.Chrome()
elif args.browser[0].lower() == 'firefox':
    driver = webdriver.Firefox()

visited_links = set()

try:
    emails = scrape_domain(domain, port, max_pages)
    print 'Emails found:'
    for email in emails:
        print('\t'+email)

    if args.verbose:
        log('Links visited:')
        for link in visited_links:
            log('\t' + link)
finally:
    # make sure we always shut down webdriver
    driver.close()
