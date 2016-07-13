import SQLStatementGen as SQL

s = SQL.SQLStatementGen()

print(s.read(3))

print(s.insert("myTable", {"testValue": "1"}))
print(s.genParams({"testValue": "1"}))