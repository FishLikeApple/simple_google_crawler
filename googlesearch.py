'''
Created on May 5, 2017
@original author: anthony
https://github.com/anthonyhseb/googlesearch
'''
import urllib.request as urllib2
import math
import re
from bs4 import BeautifulSoup
from pprint import pprint
from threading import Thread
from collections import deque
from time import sleep
        
class GoogleSearch:
    USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/ 78.0.3904.108 Safari/537.36"
    SEARCH_URL = "https://google.com/search"
    RESULT_SELECTOR = "div > .r"
    TOTAL_SELECTOR = "#resultStats"
    RESULTS_PER_PAGE = 10
    DEFAULT_HEADERS = [
            ('User-Agent', USER_AGENT),
            ("Accept-Language", "en-US,en;q=0.5"),
        ]
    
    def search(self, query, num_results = 10, prefetch_pages = False, prefetch_threads = 10, language = "en"):
        searchResults = []
        fetcher_threads = deque([])
        i = 0
        while len(searchResults) < num_results:
            start = i * GoogleSearch.RESULTS_PER_PAGE
            opener = urllib2.build_opener()
            opener.addheaders = GoogleSearch.DEFAULT_HEADERS
            response = opener.open(GoogleSearch.SEARCH_URL + "?q="+ urllib2.quote(query) + "&hl=" + language + ("" if start == 0 else ("&start=" + str(start))))
            soup = BeautifulSoup(response.read(), "lxml")
            response.close()
            results = self.parseResults(soup.select(GoogleSearch.RESULT_SELECTOR))
            searchResults += results
            i += 1
            
            if prefetch_pages:
                for result in results:
                    while True:
                        running = 0
                        for thread in fetcher_threads:
                            if thread.is_alive():
                                running += 1
                        if running < prefetch_threads:
                            break
                        sleep(1)
                    fetcher_thread = Thread(target=result.getText)
                    fetcher_thread.start()
                    fetcher_threads.append(fetcher_thread)

        if len(searchResults) > num_results:
            searchResults = searchResults[:num_results]

        for thread in fetcher_threads:
            thread.join()

        return SearchResponse(searchResults, 'not used');
        
    def parseResults(self, results):
        searchResults = [];
        for result in results:
            url = result.a["href"];
            try:
                title = result.a.h3.span.text
            except:
                # some links are unique
                title = result.a.text
            searchResults.append(SearchResult(title, url))
        return searchResults

class SearchResponse:
    def __init__(self, results, total):
        self.results = results;
        self.total = total;

class SearchResult:
    def __init__(self, title, url):
        self.title = title
        self.url = url
        self.__text = None
        self.__markup = None
    '''
    def getText(self):
        if self.__text is None:
            soup = BeautifulSoup(self.getMarkup(), "lxml")
            for junk in soup(["script", "style"]):
                junk.extract()
                self.__text = soup.get_text()
        return self.__text
    
    # there is some problem
    def getMarkup(self):
        if self.__markup is None:
            opener = urllib2.build_opener()
            opener.addheaders = GoogleSearch.DEFAULT_HEADERS
            response = opener.open(self.url);
            self.__markup = response.read()
        return self.__markup
    '''
    
    def __str__(self):
        return  str(self.__dict__)
    def __unicode__(self):
        return unicode(self.__str__())
    def __repr__(self):
        return self.__str__()

if __name__ == "__main__":
    import sys
    search = GoogleSearch()
    i=1
    query = " ".join(sys.argv[1:])
    if len(query) == 0:
        query = "test case"
    count = 10
    print ("Fetching first " + str(count) + " results for \"" + query + "\"...")
    response = search.search(query, count)
    print ("TOTAL: " + str(response.total) + " RESULTS")
    for result in response.results:
        print("RESULT #"+str (i)+": "+result.title+'   '+result.url)
        i+=1
