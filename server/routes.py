from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from server import app, db
from server.models import Article, User


@app.route('/', methods=['GET'])
@login_required
def index():
    return render_template("index.html")


@app.route('/posts', methods=['GET'])
@login_required
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)


@app.route('/posts/<int:id>', methods=['POST', 'GET'])
@login_required
def post_detail(id):
    article = Article.query.get(id)
    return render_template("post_detail.html", article=article)


@app.route('/posts/<int:id>/delete', methods=['POST', 'GET'])
@login_required
def post_delete(id):
    article = Article.query.get(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return 'При удаление статьи произошла ошибка'


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
@login_required
def post_update(id):
    article = Article.query.get(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return 'При Обновление статьи произошла ошибка'
    else:
        return render_template("post_update.html", article=article)


@app.route('/post_add', methods=['POST', 'GET'])
@login_required
def post_add():
    if request.method == "POST":
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return 'При добавление статьи произошла ошибка'
    else:
        return render_template("post_add.html")


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    login = request.form.get('login')
    password = request.form.get('password')

    if login and password:
        user = User.query.filter_by(login=login).first()

        if user and check_password_hash(user.password, password):
            login_user(user)

            next_page = request.args.get('next')
            if next_page == None:
                return redirect(url_for('index'))
            return redirect(next_page)
        else:
            flash('Неверный логин или пароль')
    elif login:
        flash('Введите пароль')
    else:
        flash('Введите логин')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    login = request.form.get('login')
    password = request.form.get('password')
    password2 = request.form.get('password2')

    user = User.query.filter_by(login=login).first()

    if request.method == 'POST':
        if user:
            flash('Пользовател уже регистрирован')
        elif not (login and password and password2):
            flash('Пожалуйста, пополните все поля!')
        elif password != password2:
            flash('Пароли неравны!')
        else:
            hash_pwd = generate_password_hash(password)
            new_user = User(login=login, password=hash_pwd)
            db.session.add(new_user)
            db.session.commit()

            return redirect(url_for('login_page'))

    return render_template('register.html')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login_page'))


@app.after_request
def redirect_to_sign_in(response):
    if response.status_code == 401:
        return redirect(url_for('login_page') + '?next=' + request.url)

    return response
