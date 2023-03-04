from flask import Flask, render_template, redirect
from forms.LoginForm import LoginForm
from forms.RegisterForm import RegisterForm
from flask_login import LoginManager
from data import db_session
from data.users import User

db_session.global_init('db/users.db')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Audio_editor_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def main():
    return render_template('start.html')


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/success')
def success():
    return render_template('base.html')


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080)
