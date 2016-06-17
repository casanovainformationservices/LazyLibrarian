import time, threading, urllib.request, urllib.parse, urllib.error, urllib.request, urllib.error, urllib.parse, re

from xml.etree import ElementTree

import lazylibrarian

from lazylibrarian import logger


def NewzNab(book=None):

    HOST = lazylibrarian.NEWZNAB_HOST
    results = []

    logger.info('Searching for %s.' % book['searchterm'])
    params = {
        "t": "search",
        "apikey": lazylibrarian.NEWZNAB_API,
        "cat": 7020,
        "q": book['searchterm']
        }

    if not str(HOST)[:4] == "http":
        HOST = 'http://' + HOST

    URL = HOST + '/api?' + urllib.parse.urlencode(params)

    try:
        data = ElementTree.parse(urllib.request.urlopen(URL, timeout=30))
    except (urllib.error.URLError, IOError, EOFError) as e:
        logger.warn('Error fetching data from %s: %s' % (lazylibrarian.NEWZNAB_HOST, e))
        data = None

    if data:
        # to debug because of api
        logger.debug('Parsing results from <a href="%s">%s</a>' % (URL, lazylibrarian.NEWZNAB_HOST))
        rootxml = data.getroot()
        resultxml = rootxml.getiterator('item')
        nzbcount = 0
        for nzb in resultxml:
            try:
                nzbcount = nzbcount+1
                results.append({
                    'bookid': book['bookid'],
                    'nzbprov': "NewzNab",
                    'nzbtitle': nzb[0].text,
                    'nzburl': nzb[2].text,
                    'nzbdate': nzb[4].text,
                    'nzbsize': nzb[7].attrib.get('length')
                    })
            except IndexError:
                logger.info('No results')
        if nzbcount:
            logger.info('Found %s nzb for: %s' % (nzbcount, book['searchterm']))
        else:
            logger.info('Newznab returned 0 results for: ' + book['searchterm'])
    return results

def NZBMatrix(book=None):

    results = []

    params = {
        "page": "download",
        "username": lazylibrarian.NZBMATRIX_USER,
        "apikey": lazylibrarian.NZBMATRIX_API,
        "subcat": 36,
        "age": lazylibrarian.USENET_RETENTION,
        "term": book['searchterm']
        }

    URL = "http://rss.nzbmatrix.com/rss.php?" + urllib.parse.urlencode(params)
    # to debug because of api
    logger.debug('Parsing results from <a href="%s">NZBMatrix</a>' % (URL))

    try:
        data = ElementTree.parse(urllib.request.urlopen(URL, timeout=30))
    except (urllib.error.URLError, IOError, EOFError) as e:
        logger.warn('Error fetching data from NZBMatrix: %s' % e)
        data = None

    if data:
        rootxml = data.getroot()
        resultxml = rootxml.getiterator('item')
        nzbcount = 0
        for nzb in resultxml:
            try:
                results.append({
                    'bookid': book['bookid'],
                    'nzbprov': "NZBMatrix",
                    'nzbtitle': nzb[0].text,
                    'nzburl': nzb[2].text,
                    'nzbsize': nzb[7].attrib.get('length')
                    })
                nzbcount = nzbcount+1
            except IndexError:
                logger.info('No results')

        if nzbcount:
            logger.info('Found %s nzb for: %s' % (nzbcount, book['searchterm']))
        else:
            logger.info('NZBMatrix returned 0 results for: ' + book['searchterm'])
    return results
