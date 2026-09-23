from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__) 

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///users.db"
app.config["SECRET_KEY"]="add"
db = SQLAlchemy(app)

app.app_context().push()

class Users(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(100),nullable=False, unique=True)
    password=db.Column(db.String(15),nullable=False)
    tasks = db.relationship('Tasks', backref='users', lazy=True)
    categories= db.relationship('Category', backref='users', lazy=True)


class Tasks(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    task=db.Column(db.String(200),nullable=False)
    status=db.Column(db.String(100),nullable=False, default="Pending")
    date_added=db.Column(db.String(20), default=datetime.now().strftime("%d-%m-%Y %H:%M"))
    user_id= db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False )
    category_id= db.Column(db.Integer,db.ForeignKey("category.id"),nullable=False )

class Category(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(200),nullable=False)
    user_id= db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False )
    tasks = db.relationship('Tasks', backref='category', lazy=True)
   


@app.route("/")
def index():
    return render_template("index.html")



@app.route("/signup", methods=["POST","GET"])
def signup():
    if request.method=="POST":
        data = request.form
        name = data.get("name").strip()
        email = request.form.get("email").strip()
        password=request.form.get("password").strip()
        person=Users.query.filter_by(email=email).first()
        if not person:
            if len(name)>1 and len(name)<=100:
                if len(email)>=3 and len(email)<=100:
                    if len(password)>=8 and len(password)<=15:
                        newuser=Users(name=name, email=email, password=password)
                        db.session.add(newuser)
                        db.session.commit()
                        nuser=Users.query.filter_by(email=email).first()
                        session["user_id"]=nuser.id
                        session["user_name"]=nuser.name
                        flash("Your account has been created!!","success")
                        return redirect(url_for("page"))
                    else:
                        flash("Password must has 8 to 15 characters!","info")
                else:
                    flash("Enter a vaild email.","info")
            else:    
                flash("There must be a meaningful name.","info")
        else:
            flash("This email already exists, Please login.","info")
            return redirect(url_for("loginuser"))
    return render_template("signup.html")



# CRUD: create, read, update, delete
@app.route("/login", methods=["POST","GET"])
def loginuser():
    if request.method=="POST":
        data = request.form
        password = data.get("password")
        email = request.form.get("email")
        checkuser=Users.query.filter_by(email=email).first()
        if checkuser and checkuser.password==password:
            # return f"Hi {name}, this is your email {email}."
            session["user_id"]=checkuser.id
            session["user_name"]=checkuser.name
            flash("Login successfull!!","success")
            return redirect(url_for("page"))
        else:
            flash("Incorrect password or email!!","warning")
            return redirect(url_for("index"))
    return render_template("login.html")



@app.route("/homepage")
def page():
    if "user_name" in session:
        tasks = Tasks.query.filter_by(user_id=session.get("user_id")).all()
        user_details=Users.query.filter_by(id=session.get("user_id")).first()
        return render_template("home.html", name=user_details.name,tasks=tasks)
    flash("Please login to continue.","info")
    return redirect(url_for("index"))



@app.route("/task", methods=["GET","POST"])
def task():
    if "user_name" in session and "user_id" in session:
        if request.method=="POST":
            data = request.form
            task= data.get("task").strip()
            cat= data.get("cat")
            categ=Category.query.filter_by(name=cat,user_id=session.get("user_id")).first()
            if len(task)>1 and len(task)<=200:
                if not categ:
                    category=Category(name=cat, user_id=session.get("user_id"))
                    db.session.add(category)
                    db.session.flush()
                    tasknew=Tasks(task=task, user_id=session.get("user_id"),category_id=category.id)
                    db.session.add(tasknew)
                    db.session.commit()
                    flash("The task is added!","success")
                    return redirect(url_for("page"))
                else:
                    tasknew=Tasks(task=task, user_id=session.get("user_id"),category_id=categ.id)
                    db.session.add(tasknew)
                    db.session.commit()
                    flash("The task is added!","success")
                    return redirect(url_for("page"))
            else:
                flash("Task must has 2 to 200 characters.","info")
        user_details=Users.query.filter_by(id=session.get("user_id")).first()
        return render_template("task.html",name=user_details.name)
    flash("Please login to continue.","info")
    return redirect(url_for("index"))



@app.route("/edit/<int:task_id>", methods=["POST","GET"])
def edit(task_id):
    if "user_name" in session:
        task=Tasks.query.filter_by(id=task_id).first()
        category=Category.query.filter_by(user_id=session.get("user_id")).all()
        if task and task.user_id==session.get("user_id"):
            if request.method=="POST":
                data = request.form
                tasks= data.get("task").strip()
                if len(tasks)>1 and len(tasks)<=200:
                    status= data.get("status")
                    category=data.get("category")
                    task.task=tasks
                    task.status=status
                    task.category_id=category
                    db.session.commit()
                    flash("Task is edited!!","success")
                    return redirect(url_for("page"))
                else:
                    flash("Task must has 2 to 200 characters.","info")
            user_details=Users.query.filter_by(id=session.get("user_id")).first()
            return render_template("edit.html", task=task, category=category,name=user_details.name )    
        flash("Task not found.","info")
        return redirect(url_for("page"))
    flash("Please login to continue.","info")
    return redirect(url_for("index"))



@app.route("/delete/<int:task_id>", methods=["POST","GET"])
def delete(task_id):
    if "user_name" in session:
        task=Tasks.query.filter_by(id=task_id).first()
        if task and task.user_id==session.get("user_id"):
            if request.method=="POST":
                db.session.delete(task)
                db.session.commit() 
                flash("Task is deleted!!","success")
                return redirect(url_for("page"))
            user_details=Users.query.filter_by(id=session.get("user_id")).first()
            object,link="task","/homepage"
            return render_template("conf.html",name=user_details.name, object=object,link=link)
        flash("Task not found.","info")
        return redirect(url_for("page"))
    flash("Please login to continue.","info")
    return redirect(url_for("index"))



@app.route("/category")
def category():
    if "user_name" in session:
        tasks= Tasks.query.filter_by(user_id=session.get("user_id")).all()
        category=Category.query.filter_by(user_id=session.get("user_id")).all()
        user_details=Users.query.filter_by(id=session.get("user_id")).first()
        return render_template("category.html",name=user_details.name,tasks=tasks,category=category)
    else:
        flash("Please login to continue.","info")
        return redirect(url_for("index"))




@app.route("/deletecategory/<int:category_id>", methods=["GET","POST"])
def deletecategory(category_id):
    if "user_name" in session:  
        category=Category.query.filter_by(id=category_id).first()
        if request.method=="POST":
            Tasks.query.filter_by(category_id=category_id).delete()
            db.session.delete(category)
            db.session.commit()
            flash("Category is deleted!","success")
            return(redirect(url_for("category")))
        user_details=Users.query.filter_by(id=session.get("user_id")).first()
        object,link="category","/category"
        return render_template("conf.html",name=user_details.name, object=object,link=link)
    else:
        flash("Please login to continue.","info")
        return redirect(url_for("index"))

    



@app.route("/user")
def user():
    if "user_name" in session:
        tasks=Tasks.query.filter_by(user_id=session.get("user_id")).all()
        user_details=Users.query.filter_by(id=session.get("user_id")).first()
        return render_template("user.html", tasks=tasks, user_details=user_details, name=user_details.name)
    flash("Please login to continue.","info")
    return redirect(url_for("index"))



@app.route("/edituser/<int:user_id>", methods=["POST","GET"])
def edituser(user_id):
    if "user_name" in session:
        user=Users.query.filter_by(id=user_id).first()
        if user and user_id==session.get("user_id"):
            if request.method=="POST":
                data = request.form
                name = data.get("name").strip()
                password = data.get("password").strip()
                if len(name)>1 and len(name)<=100:
                    user.name=name
                    user.password=password
                    db.session.commit()
                    flash("User details edited!!","success")
                    return redirect(url_for("user"))
                else:
                    flash("There must be a meaningful name.","info")
            name=Users.query.filter_by(id=user_id).first()
            return render_template("edituser.html",user=user,name=name.name)    
        flash("User not found.","info")
        return redirect(url_for("user"))
    flash("Please login to continue.","info")
    return redirect(url_for("index"))



@app.route("/deleteuser/<int:user_id>", methods=["POST","GET"])
def deleteuser(user_id):
    if "user_name" in session:
        name=Users.query.filter_by(id=user_id).first()
        if name and user_id==session.get("user_id"):
            if request.method=="POST":
                Tasks.query.filter_by(user_id=session.get("user_id")).delete()
                Category.query.filter_by(user_id=session.get("user_id")).delete()
                db.session.delete(name)
                db.session.commit() 
                flash("User data is deleted!!","success")
                return redirect(url_for("index"))
            object,link="user data","/user"
            user_details=Users.query.filter_by(id=session.get("user_id")).first()
            return render_template("conf.html",name=user_details.name,object=object, link=link )
        flash("User not found.","info")
        return redirect(url_for("index"))
    flash("Please login to continue.","info")
    return redirect(url_for("index"))



@app.route("/logout")
def logout():
    if "user_name" in session:
        session.pop("user_id")
        session.pop("user_name")
        flash("You have been logged out!!","info")
        return redirect(url_for("index"))
    flash("Please login to continue.","info")
    return redirect(url_for("index"))




if __name__=="__main__":
    db.create_all()
    app.run(debug=True, port=8000)