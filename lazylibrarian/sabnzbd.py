import os
import urllib.request
import urllib.parse
import urllib.error
import datetime

import lazylibrarian

from lazylibrarian import logger, database

def SABnzbd(title=None, nzburl=None):
#Changes https to http
    HOST = lazylibrarian.SAB_HOST + ":" + lazylibrarian.SAB_PORT
    if not str(HOST)[:4] == "http":
        HOST = 'http://' + HOST

    params = {}
	#Login for user
    params['mode'] = 'addurl'
    params['name'] = nzburl
	#Checks that all are defined and nothing is missing
    if lazylibrarian.SAB_USER:
        params['ma_username'] = lazylibrarian.SAB_USER
    if lazylibrarian.SAB_PASS:
        params['ma_password'] = lazylibrarian.SAB_PASS
    if lazylibrarian.SAB_API:
        params['apikey'] = lazylibrarian.SAB_API
    if lazylibrarian.SAB_CAT:
        params['cat'] = lazylibrarian.SAB_CAT

    if lazylibrarian.USENET_RETENTION:
        params["maxage"] = lazylibrarian.USENET_RETENTION

## FUTURE-CODE
#    if lazylibrarian.SAB_PRIO:
#        params["priority"] = lazylibrarian.SAB_PRIO
#    if lazylibrarian.SAB_PP:
#        params["script"] = lazylibrarian.SAB_SCRIPT
#    Encodes parameters
    URL = HOST + "/api?" + urllib.parse.urlencode(params) 

    # to debug because of api
    logger.debug('Request url for <a href="%s">SABnzbd</a>' % URL)

    try:
        request = urllib.request.urlopen(URL)

    except (EOFError, IOError) as e:
        logger.error("Unable to connect to SAB with URL: %s" % url)
        return False

    except httplib.InvalidURL as e:
        logger.error("Invalid SAB host, check your config. Current host: %s" % HOST)
        return False

    result = request.read().strip()
    if not result:
        log.error("SABnzbd didn't return anything.")
        return False

    logger.debug("Result text from SAB: " + result)
    if result == "ok":
        logger.info("NZB sent to SAB successfully.")
        return True
    elif result == "Missing authentication":
        logger.error("Incorrect username/password.")
        return False
    else:
        logger.error("Unknown error: " + result)
        return False
