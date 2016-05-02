from flask import Flask, render_template, redirect, url_for, request, session, flash, g, Blueprint, abort
from flask.json import jsonify
from functools import wraps
from flask.ext.sqlalchemy import SQLAlchemy
import sqlite3

from models import *

app = Flask(__name__)

app.secret_key = "my precious"
app.database = 'testjwz.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
#app.config.from_object(os.environ['APP_SETTINGS'])

db = SQLAlchemy(app)

# from models import *

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap
    
@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    username = session['current_username']
    persons = get_people()
    news = ['here will come something']
    posts = db.session.query(BlogPost).all()
    return render_template('index.html', user=username, posts=posts)

@app.route('/welcome')
def welcome():
    return render_template("welcome.html")   

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid credentilals. please try again.'
        else:
            session['logged_in'] = True
            session['current_username'] = request.form['username']
            flash('you were just logged in')
            return redirect(url_for('home'))    
    
    return render_template('login.html', error=error)

@app.route('/added_persons', methods=['POST'])
def add_person():
    g.db = connect_db()
    
    post = []
    
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    ip_address = request.form['ip_address']
    email = request.form['email']
    gender = request.form['gender']
    id = request.form['id']
    
    cur = g.db.execute(
        'INSERT INTO MOCK_DATA(id,first_name,last_name,ip_address,email,gender) VALUES (?,?,?,?,?,?)',
        (id,first_name,last_name,ip_address,email,gender))
   
    for row in cur.fetchall():
        post.append(dict(
            first_name=row[1],last_name=row[2],ip_address=row[5],email=row[3],gender=row[4],id=row[0]))
    
    g.db.commit()
    g.db.close()
    redirect(url_for('home'))
    results = search_specific_people(first_name)
    return render_template('index.html', results=results)

def search_specific_people(id):
    g.db = connect_db()
    id = id
    search_criteria = id
    results = []
    cur = g.db.execute("SELECT * FROM MOCK_DATA WHERE first_name LIKE '%s'" % search_criteria)
    
    for item in cur.fetchall():
        results.append(dict(id = item[0], first_name = item[1],
        last_name = item[2], email = item[3], gender = item[4], ip_address = item[5]))
    
    g.db.close()
    return results

@app.route('/delete/<id>', methods=['GET','POST'])
def delete_person(id):
    g.db = connect_db()
    print id
    cur = g.db.execute("DELETE FROM MOCK_DATA WHERE id='%s'" % id)
    g.db.commit()
    g.db.close()
    redirect(url_for('home'))
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search_people():
    g.db = connect_db()
    search_query = request.form['search_query']
    results = []
    
    cur = g.db.execute("SELECT * FROM MOCK_DATA WHERE first_name LIKE '%s'" % search_query)
    
    for item in cur.fetchall():
        results.append(dict(id = item[0], first_name = item[1],
        last_name = item[2], email = item[3], gender = item[4], ip_address = item[5]))
    
    g.db.close()
    redirect(url_for('home'))
    return render_template('index.html', results=results)

@app.route('/update/<id>', methods=['GET','POST', 'PUT'])
def update_values_people(id):
    g.db = connect_db()
    first_name = request.form['first_name']
    post_id = id
  
    cur = g.db.execute("UPDATE 'MOCK_DATA' set 'first_name' = '%s' WHERE id='%s'" % (first_name, post_id))
    
    g.db.commit()
    g.db.close()
    redirect(url_for('search_people')) 
    return render_template('index.html', search_query=first_name)

@app.route('/people', methods=['GET'])
def get_people():
    g.db = connect_db()
    cur = g.db.execute('SELECT * FROM MOCK_DATA LIMIT 5')
    posts = []
    
    for row in cur.fetchall():
        posts.append(dict(id = row[0], first_name = row[1],
        last_name = row[2], email = row[3], gender = row[4], ip_address = row[5]))
    
    g.db.close()
    return posts

# add blogpost
@app.route('/post', methods=['POST'])
def add_post():
    g.db = connect_db()
    blog_post_title = request.form['blog_title']
    blog_post = request.form['blog_post']
    first_name = session['current_username']
    blog = []
    #cur = g.db.execute('SELECT * FROM MOCK_DATA WHERE first_name = first_name INSERT INTO MOCK_DATA (blog_post_title, blog_post) VALUES(?,?)',  
    #(blog_post_title, blog_post))
    #cur = g.db.execute('INSERT INTO MOCK_DATA (blog_post_title, blog_post) VALUES (?,?)', (blog_post_title, blog_post), 'SELECT blogpost FROM MOCK_DATA WHERE first_name = first_name')
    # cur = g.db.execute("INSERT INTO MOCK_DATA(blog_post_title, blog_post) VALUES(?, ?), (blog_post_title, blog_post), SELECT * WHERE first_name = '%s'" % first_name)
    #cur =  g.db.execute("INSERT INTO MOCK_DATA(blog_post_title,blog_post) SELECT ")
    g.db.commit()
    g.db.close()
    redirect(url_for('home'))    
    return render_template('index.html', blogPost=blog)
# update blogpost

# remove blogpost

# state of the app somehow implement with sessions
    
@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('logged out')
    return redirect(url_for('welcome'))

def connect_db():
    return sqlite3.connect(app.database)
    
if __name__ == '__main__':
    app.run(debug=True)

#blue prints 
    #file directory structure that organizes files to a specific view

#sql alchemey
#update an existing value in the api
#dive deeper in to pip?

#create blog post