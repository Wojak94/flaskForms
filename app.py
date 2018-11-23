from flask import Flask, render_template, request, url_for, redirect, flash
from models import db, User
import os

app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

db.init_app(app)


@app.route("/")
def show_all():
    return render_template('show_all.html', users = User.query.all() )

@app.route('/new', methods = ['GET', 'POST'])
def new():
   if request.method == 'POST':
      if not request.form['login'] or not request.form['email'] or not request.form['paswd']:
         flash('Please enter all the fields', 'error')
      else:
         user = User(login=request.form['login'], mail=request.form['email'],
            paswd=request.form['paswd'])

         db.session.add(user)
         db.session.commit()
         flash('Record was successfully added')
         return redirect(url_for('show_all'))
   return render_template('new.html')

if __name__ == '__main__':
    app.run()
