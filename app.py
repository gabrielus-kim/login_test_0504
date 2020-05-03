from flask import Flask, render_template, redirect
from flask import request, session
import pymysql

app=Flask(__name__,
        static_folder='static',
        template_folder='template')

app.config['ENV']='development'
app.config['DEBUG']=True
app.secret_key='who are you?'

db = pymysql.connect(
    user='root',
    passwd='avante',
    host='localhost',
    db='web',
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def index():
    if 'owner' in session:
        content='Welcome Python : '+session['owner']['name']
    else:
        content='login 해주세요'

    return render_template('template.html',
                        content=content)

@app.route('/login', methods=['GET','POST'])
def login():
    content=''
    if request.method == 'POST':
        cur=db.cursor()
        cur.execute(f"""
            select name from author where name='{request.form['id']}'
        """)
        user=cur.fetchone()
        if user is None:
            content="등록된 회원이 아닙니다."
        else:
            cur=db.cursor()
            cur.execute(f"""
                select id, name from author 
                where name='{request.form['id']}'
                and password=SHA2('{request.form['pw']}',256)
            """)
            passwd=cur.fetchone()
            if passwd is None:
                content="패스워드을 확인해 주세요."
            else:
                session['owner']=passwd
                return redirect('/')

    return render_template('login.html',
                        content=content)

@app.route('/logout')
def logout():
    session.pop('owner',None)
    return redirect('/')

app.run(port=8000)