from datetime import timedelta
from flask import Flask, redirect,request,render_template, url_for
from flask_sqlalchemy import session
from flask_login import LoginManager, login_required,login_user
from extensions import db
from models import Student, User
from flask import session




def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    app.secret_key = "some_secret_key"
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login' 

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    with app.app_context():
        db.create_all()
    
    @app.route("/")
    def home():
        return redirect(url_for("login"))
    
    
    @app.route("/login", methods=["GET","POST"])
    def login():

        if request.method == "POST":

            username = request.form.get("username")
            password = request.form.get("password")

            user = User.query.filter_by(username=username).first()

            if user and user.password == password:

                session.permanent = True
                session["user"] = user.username
                app.config["SESSION_COOKIE_SECURE"] = True
                app.permanent_session_lifetime = timedelta(minutes=60)
                login_user(user)
                return redirect("/getall")

            else:
                return "Invalid credentials"

        return render_template("login.html")
        
    
    @app.route("/insert", methods=["GET", "POST"])
    @login_required
    def insert():
        if request.method == 'POST':
            new_student = Student(
                name = request.form.get("name"),
                email = request.form.get("email"),
                standard = request.form.get("standard"),
                devision = request.form.get("devision")
            )
            db.session.add(new_student)
            db.session.commit()
            
            return redirect(url_for('getall')) 
    
        return render_template("insert.html") 
 
    
    @app.route("/update/<int:id>", methods=["POST", "GET"])
    @login_required
    def update(id): 
        student = Student.query.get(id)

        if request.method == 'POST':
            student.name = request.form.get("name")
            student.email = request.form.get("email")
            student.standard = request.form.get("standard")
            student.devision = request.form.get("devision") 
            
            db.session.commit()
            return  "updated successfully"
                
        return render_template("update.html", student=student) 
     
          
    @app.route("/delete", methods=["GET", "POST"])
    @login_required
    def delete():
        if request.method == 'POST':
            student_id = request.form.get("id")
            student = Student.query.get(student_id)

            if student: 
                db.session.delete(student)
                db.session.commit()
                return "Student Deleted"
            else:
                return " not found."
            
        return render_template("delete.html")       
    
    
    @app.route("/getwithid", methods=["GET", "POST"])
    @login_required
    def getwithid():
        student = None
        if request.method == "POST":
            student_id = request.form.get("student_id")
            student = Student.query.get(student_id)
        return render_template("getwithid.html", student=student)   
     
           
    @app.route("/getall") 
    @login_required 
    def getall():    
            students = Student.query.all()
            return render_template("getall.html", students=students)
        
    return app

if __name__ == "__main__":
        app = create_app()
        app.run(debug=True)       
        