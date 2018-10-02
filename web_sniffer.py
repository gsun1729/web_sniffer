import os
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import urllib2


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    https://realpython.com/python-web-scraping-practical-introduction/
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    https://realpython.com/python-web-scraping-practical-introduction/
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    https://realpython.com/python-web-scraping-practical-introduction/
    """
    print(e)
os.system('cls' if os.name == 'nt' else 'clear')

raw_html = simple_get('https://www.yeastgenome.org/search?q=YBR011C&is_quick=true')


soup = BeautifulSoup(raw_html, 'html.parser')
# print soup


test = soup.find_all("section", {'id':'overview'})
# print test
print test[0].find_all('dd')
print "=================="
print test[0]
print type(test[0])



raise Exception('asdf')
for index, element in enumerate(soup.select('section')):
    if element['id'] == 'overview':
        print element.text
    # if li['class'] == 'key-value':
    #     print(li.text)
