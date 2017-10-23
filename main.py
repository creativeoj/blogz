from flask import Flask, render_template, redirect, session, request, flash
from app import app, db, check_pw_hash
from models import User, Blog


@app.before_request
def require_login():
    allowed_routes = ['login', 'signup', 'index', 'blog']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')


@app.route("/login", methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if not user:
            flash("Username does not exist",'error')
            return render_template('login.html')
        
        elif user and not check_pw_hash(password, user.pw_hash):
            flash("User password incorrect", 'error')

        elif user and check_pw_hash(password, user.pw_hash):
            session['username'] = username
            flash("Logged in  " + user.username)
            return render_template('newpost.html')

    return render_template("login.html")


@app.route("/signup", methods=['GET', 'POST'])
def signup():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        username_error =''
        password_error =''
        verify_error = ''

        if len(username) == 0 :
            username_error = "That's not a valid username"
        elif len(username) < 3 :
            username_error = "Username must be greater than 3 characters!"
        else:
            for chr in username:
                if not chr :
                    username_error = "That's not a valid username!"

        if len(password) == 0  :
            password_error = "That's not a valid password!"
        elif len(password) < 3 :
            password_error = "Password must be greater than 3 characters!"

        if password != verify:
            password_error = "passwords did not match"
        elif len(verify) == 0 :
            verify_error = "That's not a valid password!"
        elif len(verify) <3 :
                verify_error = "Password must be greater than 3 characters!"


        existing_user = User.query.filter_by(username=username).first()

        if (username_error !=''or password_error !=''or verify_error!=''):
            return render_template('signup.html', username_error = username_error, password_error = password_error, verify_error = verify_error)

        if not existing_user and password == verify:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                return redirect('/newpost')
        else:
             flash("Username already exists", "error")
    return render_template("signup.html")

@app.route("/logout")
def logout():
    del session['username']
    return redirect('/blog')
 
@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/blog', methods =['POST', 'GET'])
def blog():
 
    blog = request.args.get('id', default=None, type=int)
    user = request.args.get('user', default=None, type=int)
    
    if user:
        blogs = Blog.query.filter_by(owner_id=user).order_by(Blog.date.desc()).all()
        return render_template('singleUser.html', blogs=blogs)
    if blog is None :
        blogs = Blog.query.order_by(Blog.date.desc()).all()
        return render_template('blog.html' ,blogs=blogs)
    else:
        blog_id = Blog.query.filter_by(id=blog).first()
        return render_template('viewblog.html', blog_id=blog_id)
   
@app.route('/newpost', methods =['POST','GET'])
def newpost():
    
    title_error = ''
    newBlog_error = ''
    
    if  request.method == 'POST':
        blog_name_title = request.form['blog_title']
        blog_name_content = request.form['blog_content']
        username= session['username']
        owner = User.query.filter_by(username=username).first()

        if not blog_name_title:
            title_error = "Please fill in the title."
            
        if not blog_name_content:
            newBlog_error = "Please fill in the content."
            return render_template('newpost.html', title_error=title_error, newBlog_error=newBlog_error)
        
        else:
            new_blog = Blog(blog_name_title, blog_name_content, owner)
            db.session.add(new_blog)
            db.session.commit()
            return render_template('viewblog.html', blog_id=new_blog)

    return render_template("newpost.html", title_error=title_error, newBlog_error=newBlog_error)


if __name__ == '__main__':
    app.run()