# example
# https://www.googleapis.com/books/v1/volumes?q=+inauthor:george+martin+intitle:song+ice+fire

import urllib.request
import urllib.parse
import urllib.error
import json
import time

import lazylibrarian
from lazylibrarian import logger, formatter, database

class GoogleBooks:

    def __init__(self, name=None, type=None):
        self.name = name
        self.type = type
        self.url = 'https://www.googleapis.com/books/v1/volumes?q='
        self.params = {
            'maxResults': 40,
            'printType': 'books',
            }


    def find_results(self):
        resultlist = []

        if self.type == 'book':
            set_url = self.url + urllib.parse.quote('intitle:' + '"' + self.name + '"')
        else:
            set_url = self.url + urllib.parse.quote('inauthor:' + '"' + self.name + '"')

        logger.info('Searching url: ' + set_url)

        try:
            startindex = 0
            resultcount = 0
            ignored = 0
		
		#Find loop
            while True:
		#URL encode request
                self.params['startIndex'] = startindex
                URL = set_url + '&' + urllib.parse.urlencode(self.params)
		#Decode response From Server
                response = urllib.request.urlopen(URL, timeout=30)
                encoding = response.headers.get_content_charset()
                jsonresults = json.loads(response.read().decode(encoding))
                startindex = startindex+40
		#Parse Book Attributes
                for item in jsonresults['items']:

                    # skip if no author, no author is no book.
                    try:
                        authorname = item['volumeInfo']['authors'][0]
                    except KeyError:
                        logger.debug('Skipped a result without authorfield.')
                        break

                    try:
                        #skip if language is in ignore list
                        booklang = item['volumeInfo']['language']
                        if not booklang in lazylibrarian.IMP_PREFLANG:
                            ignored = ignored+1
                            break
                    except KeyError:
                        ignored = ignored+1
                        logger.debug('Skipped a result where no language is found')
                        break

                    try:
                        bookpub = item['volumeInfo']['publisher']
                    except KeyError:
                        bookpub = None

                    try:
                        booksub = item['volumeInfo']['subtitle']
                    except KeyError:
                        booksub = None

                    try:
                        bookdate = item['volumeInfo']['publishedDate']
                    except KeyError:
                        bookdate = '0000/00/00'

                    try:
                        bookimg = item['volumeInfo']['imageLinks']['thumbnail']
                    except KeyError:
                        bookimg = 'images/nocover.png'

                    try:
                        bookrate = item['volumeInfo']['averageRating']
                    except KeyError:
                        bookrate = 0

                    try:
                        bookpages = item['volumeInfo']['pageCount']
                    except KeyError:
                        bookpages = '0'

                    try:
                        bookgenre = item['volumeInfo']['categories'][0]
                    except KeyError:
                        bookgenre = None

                    try:
                        bookdesc = item['volumeInfo']['description']
                    except KeyError:
                        bookdesc = 'Not available'

                    try:
                        if item['volumeInfo']['industryIdentifiers'][0]['type'] == 'ISBN_10':
                            bookisbn = item['volumeInfo']['industryIdentifiers'][0]['identifier']
                        else:
                            bookisbn = 0
                    except KeyError:
                        bookisbn = 0

                    resultlist.append({
                        'authorname': authorname,
                        'bookid': item['id'],
                        'bookname': item['volumeInfo']['title'],
                        'booksub': booksub,
                        'bookisbn': bookisbn,
                        'bookpub': bookpub,
                        'bookdate': bookdate,
                        'booklang': booklang,
                        'booklink': item['volumeInfo']['canonicalVolumeLink'],
                        'bookrate': float(bookrate),
                        'bookimg': bookimg,
                        'bookpages': bookpages,
                        'bookgenre': bookgenre,
                        'bookdesc': bookdesc
                        })

                    resultcount = resultcount+1

        except KeyError:
            logger.info('Found %s results for %s with name: %s' % (resultcount, self.type, self.name))
            if ignored > 0:
                logger.info('Skipped %s results because it is not a preferred language.' % ignored)

        return resultlist


    def find_book(self, bookid=None):
        resultlist = []
	#URL Encode Request
        URL = 'https://www.googleapis.com/books/v1/volumes/' + bookid
        #jsonresults = json.JSONDecoder().decode(urllib.request.urlopen(URL, timeout=30).read())
	#Decode Response From Server
        response = urllib.request.urlopen(URL, timeout=30)
        encoding = response.headers.get_content_charset()
        jsonresults = json.loads(response.read().decode(encoding))
	#Parse book information
        try:
            bookdate = item['volumeInfo']['publishedDate']
        except KeyError:
            bookdate = 'Unknown'

        try:
            bookimg = item['volumeInfo']['imageLinks']['thumbnail']
        except KeyError:
            bookimg = 'images/nocover.png'

        try:
            bookrate = item['volumeInfo']['averageRating']
        except KeyError:
            bookrate = 0

        try:
            bookpages = item['volumeInfo']['pageCount']
        except KeyError:
            bookpages = 0

        try:
            bookgenre = item['volumeInfo']['categories']
        except KeyError:
            bookgenre = 'Unknown'

        try:
            bookdesc = item['volumeInfo']['description']
        except KeyError:
            bookdesc = 'Not available'

        try:
            if item['volumeInfo']['industryIdentifiers'][0]['type'] == 'ISBN_10':
                bookisbn = item['volumeInfo']['industryIdentifiers'][0]['identifier']
            else:
                bookisbn = 0
        except KeyError:
            bookisbn = 0

        resultlist.append({
            'bookname': item['volumeInfo']['title'],
            'bookisbn': bookisbn,
            'bookdate': bookdate,
            'booklang': item['volumeInfo']['language'],
            'booklink': item['volumeInfo']['canonicalVolumeLink'],
            'bookrate': float(bookrate),
            'bookimg': bookimg,
            'bookpages': bookpages,
            'bookgenre': bookgenre,
            'bookdesc': bookdesc
            })

        return resultlist



