import urllib


def getSentiments(tweet):
    data = urllib.urlencode({"text": tweet})
    u = urllib.urlopen("http://text-processing.com/api/sentiment/", data)
    the_page = u.read()
    return the_page
