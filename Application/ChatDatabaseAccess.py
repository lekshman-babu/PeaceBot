import sqlite3 as sq

def drop(cursor,connect):
    cursor.execute("""DROP TABLE Chats""")
    connect.commit()

def create(cursor,connect):
    try:
        cursor.execute("""CREATE TABLE ChatsDetails(
            "ID" INTEGER PRIMARY KEY,
            "Chats" TEXT
        ) """)
        connect.commit()
        return '<created>'
    except Exception as exC:
        return exC
def insert(loginDetails,cursor,connect,token=''):
    try:
        cursor.execute("""INSERT INTO ChatsDetails VALUES(?,?)""",loginDetails)
        connect.commit()
        token+="<yes>"
        return token
    except Exception as exI:
        if isinstance(exI, sq.OperationalError) and 'no such table: ChatsDetails' in str(exI):
            token=create(cursor,connect)
            if token !='<created>':
                return token
            else:
                return insert(loginDetails,cursor,connect,token)
        else:
            return exI

def update(id,chats,cursor,connect):
    try:
        cursor.execute("""UPDATE ChatsDetails SET Chats=? WHERE ID=?""",(chats,id,))
        token="<yes>"
        connect.commit()
    except Exception as ex:
        token="<no>"
        print(ex)
    return token


def getChats(id,cursor,connect):
    try:
        cursor.execute("""SELECT Chats fROM ChatsDetails WHERE ID=?""",(id,))
        chatHistory=cursor.fetchone()[0]
        connect.commit()
        return chatHistory
    except Exception as ex:
        return ex
    
if __name__=="__main__":
    connect=sq.connect("Application/Database/ChatsDatabase.db")
    cursor=connect.cursor()
    print(getChats(1,cursor,connect))