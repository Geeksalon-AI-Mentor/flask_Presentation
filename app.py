from flask import Flask, url_for, render_template,request,redirect,session,flash
from datetime import timedelta 

app = Flask(__name__)
# sessionKeyの指定
# セッション情報を暗号化するための秘密鍵
# これは乱数になるように設定するのが好ましい
'''
以下のコードでランダムな秘密鍵を生成できる
import secret
print(secrets.token_hex())
'''
app.secret_key = '07705d19ff8c59ad8e3f4ab58fee6b00c84a23f313e506c185f70f41713122a6'

# sessionの保持時間の指定(デフォルトは31日)
# 30秒に指定
app.permanent_session_lifetime = timedelta(minutes=0.5) 

@app.route('/')
def index():
    # sessionを設定
    session['state'] = True
    print(session)
    return render_template('index.html')


@app.route('/hello')
def hello():
    return render_template('hello.html')

@app.route('/old_page')
def old_page():
    # 普通にrender_templateした場合
    # return render_template('old_page.html')
    # あたらしいページにリダイレクトする場合
    return redirect(url_for('new_page'))   

@app.route('/new_page',methods=['GET','POST'])
def new_page():
    # 格納した情報を確認する
    # sessionが切れていたらNoneが返ってくる
    state = session.get('state')
    return render_template('new_page.html',state=state)

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        # inputのname属性の値を受け取りnameに格納
        name = request.form['name']
        if name != 'anonymous':
            flash('名前が異なります')
            return redirect(url_for('new_page'))
        else:
            return render_template('login.html')

# URLに変数を組み込んで情報を共有
@app.route('/result/<user_name>')
def accept_login(user_name):
    return render_template('result.html',user_name = user_name)


if __name__ == '__main__':
    app.run(debug=True)