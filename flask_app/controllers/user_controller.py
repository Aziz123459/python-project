from flask import session,request,render_template,redirect,url_for
from flask_app import app
from flask_app.models.user_model import User
from flask import flash
from flask_bcrypt import Bcrypt

bcrypt=Bcrypt(app)


@app.route('/signUp')
def index():
    return render_template("index.html")

@app.route("/new/user",methods=["POST"])
def add_user():
    
    if not User.validate(request.form):
        return redirect('/signUp')
    else:
        pw=bcrypt.generate_password_hash(request.form["password"])
        data={**request.form,
              "password": pw}
        user_id=User.add_one(data)
        
        session["user_id"]=user_id
        return redirect('/home')

@app.route('/login')
def login():
    
    return render_template("login.html")



@app.route('/user/login', methods=["POST"])
def submit_login():
    user=User.get_by_email(request.form)
    if user==None:
        return redirect("/login")
    elif not bcrypt.check_password_hash(request.form["password"],user.password):
            flash("Invalid Email/Password","login_password_validation")
            return redirect("/login")
    else:
        session["user_id"]=user.id
        session["name"]=user.user_name
        return redirect("/home")
