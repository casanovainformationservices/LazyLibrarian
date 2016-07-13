class SQLStatementGen():

    def read(self, bookID = None):
        if bookID is None:
            return 'SELECT BookID, AuthorName, Bookname from books WHERE Status="Wanted"'
        else:
            return ('SELECT BookID, AuthorName, BookName from books WHERE BookID=? AND Status="Wanted"', str(bookID))

    def update(self, tableName, paramDict):
        statementList = []
        statementList.append("UPDATE " + tableName)
        statementList.append(" SET " + ", ".join(paramDict.values()))
        statementList.append(" WHERE " + " AND " + " ".join(paramDict.keys()))
        return " ".join(statementList)

    def insert(self, tableName, paramDict):
        statementList = []
        statementList.append("INSERT INTO " + tableName)
        statementList.append(" (" + ", ".join(paramDict.keys()))
        statementList.append(")" + " VALUES (" + ", ".join(paramDict.values()))
        statementList.append(")")
        return " ".join(statementList)

    def genParams(self, myDict):
        return [x + " = ?" for x in list(myDict.keys())]

