import sqlite3 as sq

def drop(cursor,connect):
    cursor.execute("""DROP TABLE LoginDetails""")
    connect.commit()

def create(cursor,connect):
    try:
        cursor.execute("""CREATE TABLE LoginDetails(
            "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
            "FirstName" TEXT,
            "LastName" TEXT,
            "Email" TEXT,
            "Password" TEXT,
            "Occupation" TEXT
        ) """)
        connect.commit()
        return '<created>'
    except Exception as exC:
        return exC
def insert(loginDetails,cursor,connect,token=''):
    try:
        cursor.execute("""INSERT INTO LoginDetails (FirstName,LastName,Email,Password,Occupation) VALUES(?,?,?,?,?)""",loginDetails)
        connect.commit()
        token+="<yes>"
        return token
    except Exception as exI:
        if isinstance(exI, sq.OperationalError) and 'no such table: LoginDetails' in str(exI):
            token=create(cursor,connect)
            if token !='<created>':
                return token
            else:
                return insert(loginDetails,cursor,connect,token)
        else:
            return exI

def validate(email,password,cursor,connect):
    cursor.execute("""SELECT Password FROM LoginDetails WHERE Email=?""",(email,))
    storedPassword=cursor.fetchone()['Password']
    token="<no>"
    if password==storedPassword:
        token="<yes>"
    connect.commit()
    return token

def getID(email,cursor,connect):
    try:
        cursor.execute("""SELECT ID FROM LoginDetails WHERE Email=?""",(email,))
        chatID=cursor.fetchone()['ID']
        connect.commit()
        return chatID
    except Exception as ex:
        return ex

# if __name__=='__main__':
#     connect=sq.connect("MentalHeathBot")
#     cursor=connect.cursor()
#     # Get the list of tables in the database
#     cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
#     tables = cursor.fetchall()
#     print(tables)