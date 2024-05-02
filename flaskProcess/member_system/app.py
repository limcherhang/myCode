import os
import sys
rootPath = os.getcwd() + '/../../'
sys.path.append(rootPath)
from flask import * 
import configparser
from connection.mysql_connection import MySQLConn

config = configparser.ConfigParser()
config.read(rootPath+'/config.ini')

conn = MySQLConn(config['mysql_own'])

app = Flask(
    __name__,
    static_folder='static',
    static_url_path='/'
)

app.secret_key = 'any string but secret'

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/member")
def member():
    if "nickname" in session:
        return render_template("member.html", nickname=session['nickname'])
    else:
        return redirect("/")

# error?msg=錯誤訊息
@app.route("/error")
def error():
    msg = request.args.get("msg", "發生錯誤，請聯繫客服")
    return render_template("error.html", message=msg)

@app.route("/signup", methods=["POST"])
def signup():
    # 從前端取得資料
    nickname = request.form['nickname']
    email = request.form['email']
    password = request.form['password']
    with conn.cursor() as cursor:
        sqlCommad = f"SELECT email FROM member_system.user WHERE email='{email}'"
        cursor.execute(sqlCommad)
        if cursor.rowcount > 0:
            return redirect("/error?msg=信箱已被註冊！")
        else:
            sqlCommad = f"SELECT IFNULL(MAX(id),0) FROM member_system.user;"
            cursor.execute(sqlCommad)
            (maxId, ) = cursor.fetchone()

            nextId = maxId+1

            insert_sql = f"INSERT INTO member_system.user VALUES({nextId}, '{nickname}', '{email}', '{password}')"
            print(insert_sql)
            cursor.execute(insert_sql)
            return redirect("/signupsuccees")
        
@app.route("/signupsuccees")
def signupsucceess():
    return render_template("signupsucceess.html")

@app.route("/signin", methods=["POST"])
def signin():
    # 從前端取得使用者輸入
    email = request.form["email"]
    password = request.form["password"]
    
    # 和資料庫做互動
    with conn.cursor() as cursor:
        sqlCommand = f"SELECT nickname FROM member_system.user WHERE email='{email}' AND password='{password}';"

        cursor.execute(sqlCommand)
        if cursor.rowcount == 0:
            # 登錄失敗
            return redirect('/error?msg=該信箱為註冊或密碼錯誤')
        else:
            # 登陸成功，在session記錄會員資訊，導向到會員頁面
            (result, ) = cursor.fetchone()
            session['nickname'] = result
            return redirect('/member')

@app.route("/signout")
def sighout():
    del session['nickname']
    return redirect("/")

app.run(port=3000)