from flask import Flask, render_template, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import OperationalError

app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///GitUsersDb.db'
app.config['SECRET_KEY'] = "dsfaewfr12324r5"
db = SQLAlchemy(app)
ROWS_PER_PAGE = 25

class Users (db.Model):
   id = db.Column(db.Integer, primary_key = True)
   user_name = db.Column(db.String)
   image_url = db.Column(db.String)
   type = db.Column(db.String) 
   github_url = db.Column(db.String)

@app.route('/users', methods=['GET', 'POST'])
@app.route('/users/page/<int:page>')
def users(page=1):
    if request.method == 'POST':
        session["a"] = int(request.form['text'])
    if session["a"] is None:
        session["a"] =  ROWS_PER_PAGE
    try:
        users_list = Users.query.paginate(page=page, per_page=session["a"])
    except OperationalError:
        flash("No users in the database.")
        users_list = None
    return render_template('users.html', users_list = users_list)


if __name__ == "__main__":
    app.run(debug = True, host = "0.0.0.0", port = 3000)
