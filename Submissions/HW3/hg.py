from BeautifulSoup import BeautifulSoup, SoupStrainer
import urllib
r = urllib.urlopen('http://www.aflcio.org/Legislation-and-Politics/Legislative-Alerts').read()
soup = BeautifulSoup(r)
print type(soup)







