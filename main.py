from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.login}>'


with app.app_context():
    db.create_all()

    # список пользователей,которые будут заноситься в базу данных
    users_to_create = [
        {'login': 'Slon333', 'password': '12345'},
        {'login': 'Qwerty1', 'password': 'RtR'},
        {'login': 'Virab', 'password': 'virr'}
    ]

    for user_data in users_to_create:
        user = User.query.filter_by(login=user_data['login']).first()
        if not user:
            new_user = User(login=user_data['login'], password=user_data['password'])
            db.session.add(new_user)
            db.session.commit()


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        user = User.query.filter_by(login=login).first()
        if user:
            return render_template('index2.html', username=user.login)
        else:
            return redirect(url_for('not_found'))
    return render_template('index.html')


@app.route('/not_found')
def not_found():
    return render_template('index3.html')


if __name__ == '__main__':
    app.run()
