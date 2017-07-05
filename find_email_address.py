from selenium import webdriver
from pprint import pprint
from urlparse import urlparse
import argparse

parser = argparse.ArgumentParser(description='Scrape a domain for email addresses.')
parser.add_argument('hostname', metavar='domain', nargs=1,
                    help='Host to scrape')
parser.add_argument('--port',
                    help='Port number, default: 80')
parser.add_argument('--chrome',
                    help='Use Chrome instead of HTMLUNIT',  action="store_true")
parser.add_argument('--verbose',
                    help='Output additional logging',  action="store_true")
#parser.add_argument('--depth',
#                    help='Unimplemented: Max number of pages to fetch, default: 100')

args = parser.parse_args()

domain = args.hostname[0]

if args.port is None:
    port = 80
else:
    port = args.port

if args.chrome:
    driver = webdriver.Chrome()
else:
    driver = webdriver.Remote(desired_capabilities=webdriver.DesiredCapabilities.HTMLUNIT)

def log(msg):
    if args.verbose:
        print(msg)

def find_links(driver, domain):
    retval = {'emails': set(), 'links': set()} # emails for mailto: links, links for everything else
    elems = driver.find_elements_by_xpath('//a[@href]')
    # could use //a[startswith(href'mailto')] to get emails and do email links
    # separately but we'll just get all links and then divvy them up
    for el in elems:
        link = el.get_attribute('href')
        if (link is None):
            continue
        url = urlparse(link)

        if url.scheme.startswith('mailto'):
            log('Email found: ' + url.path)
            retval['emails'].add(url.path)
        else:
            #pprint(url)

            if url.netloc.startswith(domain):
                log('Address found: ' + link)
                retval['links'].add(link)
            else:
                log('Ignoring off domain address: ' + url.netloc)
    return retval

def scrape_page(url, visited_links=set()):
    """ Scrapes url parameter for links, then recurses through each link found.

        visited_links is the set of links already visited in order to keep from
        looping.
        Returns a dictionary with keys of emails and links, where emails is a
        set containing the email address portion of all anchors that contain an href
        attribute that starts with mailto:, while links contains all other links
        found on the page, which will then be traversed
    """
    domain = urlparse(url).hostname
    retval = {'emails': set(), 'links': set(), 'visited': set()}

    log("Scraping url: " + url)

    driver.get(url)
    # this will let us know if we were 30x'd to a different host
    page_hostname = driver.execute_script('return window.location.hostname')
    # unfortunately, WebDriver does not expose HTTP headers, so we can't
    # be sure we'll be able to inject this JavaScript in the host page, but
    # it seems to fail silently with HTMLUNIT at least


    if (not page_hostname == domain):
        return retval
    visited_links.add(url)

    links = find_links(driver, domain)
    # get union of emails and links and maintain them in retval
    retval['emails'] = retval['emails'] | links['emails']
    retval['links'] = retval['links'] | links['links']

    for ii in links['links']:
        if ii not in visited_links:
            # hack to skip over content-types that we can't work on
            if ii.endswith('.zip') or ii.endswith('.pdf') or ii.endswith('.txt'):
                continue
            links = scrape_page(ii, visited_links)
            retval['emails'] = retval['emails'] | links['emails']
            retval['links'] = retval['links'] | links['links']
        else:
            log('Skipping visited link:  ' + ii)
    retval['visited'] = retval['visited'] |visited_links
    return retval

def scrape_domain(domain, port=80):
    """ Wraps scrape_page, making the initial URL out of the domain and port numbers """
    initial_page = "http://"+domain;
    if port != 80:
        initial_page+=':'+str(port)
    return scrape_page(initial_page)

results = scrape_domain(domain, port)
print 'Emails found:'
for email in results['emails']:
    print('\t'+email)

if args.verbose:
    log('Links visited:')
    for ii in results['visited']:
        log('\t'+ii)


driver.close()
