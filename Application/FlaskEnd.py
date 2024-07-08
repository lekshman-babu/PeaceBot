from flask import Flask, render_template, request, redirect,url_for, jsonify
from flask_socketio import SocketIO
import LoginDatabaseAccess as ls
import ChatDatabaseAccess as cd
import sqlite3 as s
import Inference as i
app=Flask(__name__,static_url_path="/static")
socketio=SocketIO(app)

def getDatabaseConnection(databaseType):
    connect=s.connect(f"Application/Database/{databaseType}.db")
    connect.row_factory=s.Row
    return connect


@app.route('/',methods=['POST','GET'])
def login():
    if request.method=="POST":
        email=request.form['email']
        password=request.form['password']
        connect=getDatabaseConnection('LoginDatabase')
        cursor=connect.cursor()
        validateToken=ls.validate(email,password,cursor,connect)
        if validateToken=="<yes>":
            id=ls.getID(email,cursor,connect)
            return redirect(url_for('chatBot',id=id))
        else:
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method=="POST":
        firstName=request.form['firstName']
        lastName=request.form['lastName']
        email=request.form['email']
        password=request.form['password']
        occupation=request.form['occupation']
        connectL=getDatabaseConnection('LoginDatabase')
        cursorL=connectL.cursor()
        token=ls.insert((firstName,lastName,email,password,occupation),cursorL,connectL)
        if "<yes>" in token:
            id=ls.getID(email,cursorL,connectL)
            connectC=getDatabaseConnection('ChatsDatabase')
            cursorC=connectC.cursor()
            token=cd.insert((id,"[]"),cursorC,connectC)
            if "<yes>" in token:
                return redirect(url_for('login'))
            else:
                return redirect(url_for('signup'))
        else:
            return redirect(url_for('signup'))
    return render_template('signup.html')


@app.route('/chat',methods=["GET","POST"])
def chatBot():
    if request.method=="GET":
        id = request.args.get('id')
    if request.method=="POST":
        convo={}
        data=request.get_json()
        id=int(data['userID'])
        user=data['userText']
        bot=i.output(user)
        convo["human"]=user
        convo["bot"]=bot
        chatStoreManager(convo,id)
        return jsonify({'message':bot})
    return render_template('chat.html',id=id)


def chatStoreManager(convo,chatId):
    connectC=getDatabaseConnection('ChatsDatabase')
    cursorC=connectC.cursor()
    chatHistory=cd.getChats(chatId,cursorC,connectC)
    chatHistory=eval(chatHistory)
    chatHistory.append(convo)
    cd.update(chatId,str(chatHistory),cursorC,connectC)

if __name__=='__main__':
    socketio.run(app,debug=True)