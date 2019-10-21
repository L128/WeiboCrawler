import requests
from requests import get
from requests.exceptions import RequestException
from requests.exceptions import Timeout
from contextlib import closing
from bs4 import BeautifulSoup



def simple_get(url):
    # """
    # Attempts to get the content at `url` by making an HTTP GET request.
    # If the content-type of response is some kind of HTML/XML, return the
    # text content, otherwise return None.
    # """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                # print("False URL")
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    # """
    # Returns True if the response seems to be HTML, False otherwise.
    # """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    # """
    # It is always a good idea to log errors.
    # This function just prints them, but you can
    # make it do anything.
    # """
    print(e)



mainpage = "https://m.weibo.cn"
# Fill in your details here to be posted to the login form.
payload = {
    'inUserName': '18822181747',
    'inUserPass': 'Aptx4869'
}

# Use 'with' to ensure the session context is closed after use.
with requests.Session() as s:
    p = s.post("https://passport.weibo.cn/signin/login?entry=mweibo&res=wel&wm=3349&r=https%3A%2F%2Fm.weibo.cn%2F", data=payload)
    mainHTML = BeautifulSoup(p.content, "html.parser")  # type: BeautifulSoup
    print (mainHTML.head)


    # An authorised request.
    # r = s.get('A protected web page url')
    # print (r.text)
# raw_html = simple_get("https://m.weibo.cn")
# html = BeautifulSoup(raw_html, "html.parser")
