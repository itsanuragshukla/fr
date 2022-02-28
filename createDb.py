import sqlite3
con = sqlite3.connect("userInfo.db")
print("Database opened successfully")

con.execute("create table userInfo (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT UNIQUE NOT NULL,phone INTEGER NOT NULL,user TEXT UNIQUE NOT NULL)")

print("Table created successfully")

con.close() 
