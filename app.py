from flask import Flask, flash, redirect,request,render_template, url_for
from extensions import db
from models import Student

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    app.secret_key = "some_secret_key"
    db.init_app(app)
    with app.app_context():
        db.create_all()
    
    @app.route("/")
    def home():
        return "hello"
    
    @app.route("/insert", methods=["GET", "POST"])
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
 
    @app.route("/update/<int:id>", methods=["GET", "POST"])
    def update(id): 
        student = Student.query.get_or_404(id)

        if request.method == 'POST':
            student.name = request.form.get("name")
            student.email = request.form.get("email")
            student.standard = request.form.get("standard")
            student.devision = request.form.get("devision") 
            
            db.session.commit()
            return  "updated successfully"
                
        return render_template("update.html", student=student) 
          
    @app.route("/delete", methods=["GET", "POST"])
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
    def getwithid():
        student = None
        if request.method == "POST":
            student_id = request.form.get("student_id")
            student = Student.query.get(student_id)
        return render_template("getwithid.html", student=student)   
            
    @app.route("/getall") 
    def getall():    
            students = Student.query.all()
            return render_template("getall.html", students=students)
        
    return app

if __name__ == "__main__":
        app = create_app()
        app.run(debug=True)       
        