def webscraper(urlpath, item):

    if item == 'links':
        r = urllib.urlopen(urlpath).read()
        soup = BeautifulSoup(r)
        print type(soup)
        print('hi')
        print soup.prettify()[0:1000]
        links = soup.findAll("a", class_="href")
        #print(links[0])

def html2txt(urlpath):
    html = urlopen(urlpath).read()
    raw = nltk.clean_html(html)
    print(raw)

def import_packages():
    global re
    global BeautifulSoup
    global urllib
    global nltk
    global urlopen
    global html2text

    import re
    from BeautifulSoup import BeautifulSoup
    import urllib
    import nltk
    from urllib import urlopen
    from html2text import html2text







def html_to_text(urlpath):


    #url = "http://news.bbc.co.uk/2/hi/health/2284783.stm"
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html)

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()  # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    print(text)

if __name__ == "__main__":

    import_packages()
    urlpath = 'https://en.wikipedia.org/wiki/Iran'

    #webscraper(urlpath, 'links')

    html_to_text(urlpath)