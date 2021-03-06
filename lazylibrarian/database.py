import os
import sqlite3
import threading
import time

import lazylibrarian

from lazylibrarian import logger

db_lock = threading.Lock()
#Default to data directory for path
def dbFilename(filename="lazylibrarian.db"):

    return os.path.join(lazylibrarian.DATADIR, filename)

class DBConnection:

    def __init__(self, filename="lazylibrarian.db"):
        self.filename = filename
        self.connection = sqlite3.connect(dbFilename(filename), 20)
        self.connection.row_factory = sqlite3.Row

    def action(self, query, args=None):
	#Lock database before change
        with db_lock:

            if query == None:
                return

            sqlResult = None
            attempt = 0
		#Limit actions to 5 attempts
            while attempt < 5:

                try:
                    if args == None:
                        #logger.debug(self.filename+": "+query)
                        sqlResult = self.connection.execute(query)
                    else:
                        #logger.debug(self.filename+": "+query+" with args "+str(args))
                        sqlResult = self.connection.execute(query, args)
                    self.connection.commit()
                    break

                except sqlite3.OperationalError as e:
                    if "unable to open database file" in e.message or "database is locked" in e.message:
                        logger.warn('Database Error: %s' % e)
                        attempt += 1
                        time.sleep(1)
                    else:
                        logger.error('Database error: %s' % e)
                        raise

                except sqlite3.DatabaseError as e:
                    logger.error('Fatal error executing %s :: %s' % (query, e))
                    raise

            return sqlResult

    def select(self, query, args=None):
        sqlResults = self.action(query, args).fetchall()

        if sqlResults == None:
            return []

        return sqlResults
	#To DO: Limit lines to 80 char. 
    def upsert(self, tableName, valueDict, keyDict):
        changesBefore = self.connection.total_changes

        genParams = lambda myDict : [x + " = ?" for x in list(myDict.keys())]

        query = "UPDATE "+tableName+" SET " + ", ".join(genParams(valueDict)) + " WHERE " + " AND ".join(genParams(keyDict))

        self.action(query, list(valueDict.values()) + list(keyDict.values()))

        if self.connection.total_changes == changesBefore:
            query = "INSERT INTO "+tableName+" (" + ", ".join(list(valueDict.keys()) + list(keyDict.keys())) + ")" + \
                        " VALUES (" + ", ".join(["?"] * len(list(valueDict.keys()) + list(keyDict.keys()))) + ")"
            self.action(query, list(valueDict.values()) + list(keyDict.values()))
