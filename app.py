
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect

from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from config import Config

app = Flask(__name__)
csrf = CSRFProtect(app)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[]
)
app.config.from_object(Config)

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="student")
class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))

class Token(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token_number = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(20), default="waiting")

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey("service.id"), nullable=False) 
    service = db.relationship("Service")   

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appointment_date = db.Column(db.String(20), nullable=False)
    appointment_time = db.Column(db.String(20), nullable=False)
    status = db.Column(db.String(20), default="booked")

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey("service.id"), nullable=False)

    service = db.relationship("Service")

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        # Check empty fields
        if not name or not email or not password:
            return "All fields are required!"

        # Validate name
        if len(name) < 2 or len(name) > 100:
            return "Name must be between 2 and 100 characters!"

        # Validate email
        if "@" not in email or "." not in email.split("@")[-1]:
            return "Please enter a valid email address!"

        # Validate password
                
        if len(password) < 8:
            return "Password must contain at least 8 characters!"

        if not any(char.isupper() for char in password):
            return "Password must contain at least one uppercase letter!"

        if not any(char.islower() for char in password):
            return "Password must contain at least one lowercase letter!"

        if not any(char.isdigit() for char in password):
            return "Password must contain at least one number!"
        # Check existing user
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return "Email already registered!"

        # Hash password
        hashed_password = generate_password_hash(password)

        new_user = User(
            name=name,
            email=email,
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        return render_template("registration_success.html")

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def login():
    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        # Validate empty fields
        if not email or not password:
            return "Email and password are required!"

        # Find user
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):

            # Clear old session
            session.clear()

            # Create new session
            session["user_id"] = user.id

            if user.role == "admin":
                return redirect(url_for("admin_dashboard"))

            elif user.role == "staff":
                return redirect(url_for("staff_dashboard"))

            else:
                return redirect(url_for("dashboard"))

        return "Invalid email or password!"

    return render_template("login.html")
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user = db.session.get(User, session["user_id"])
    if not user or user.role != "student":
     return "Access denied! Students only."
    services = Service.query.all()
    tokens = Token.query.filter_by(user_id=user.id).all()
    appointments = Appointment.query.filter_by(user_id=user.id).all()

    return render_template(
        "dashboard.html",
        user=user,
        services=services,
        tokens=tokens,
        appointments=appointments
    )
@app.route("/generate-token/<int:service_id>", methods=["POST"])
def generate_token(service_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    user = db.session.get(User, session["user_id"])

    if not user or user.role != "student":
        return "Access denied! Students only."
    service = db.session.get(Service, service_id)

    if not service:
        return "Service not found!"

    last_token = Token.query.filter_by(service_id=service_id).order_by(Token.token_number.desc()).first()

    next_number = 1 if last_token is None else last_token.token_number + 1

    new_token = Token(
        token_number=next_number,
        user_id=session["user_id"],
        service_id=service_id
    )

    db.session.add(new_token)
    db.session.commit()

    position = Token.query.filter_by(
    service_id=service_id,
    status="waiting"
).filter(Token.token_number <= next_number).count()

    return f"Your token number is {next_number} for {service.name}. Your queue position is {position}."

@app.route("/book-appointment/<int:service_id>", methods=["GET", "POST"])
def book_appointment(service_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    service = db.session.get(Service, service_id)

    if not service:
        return "Service not found!"

    if request.method == "POST":
        appointment = Appointment(
            appointment_date=request.form["date"],
            appointment_time=request.form["time"],
            user_id=session["user_id"],
            service_id=service_id
        )

        db.session.add(appointment)
        db.session.commit()

        return redirect(url_for("dashboard"))

    return render_template("book_appointment.html", service=service)

@app.route("/cancel-token/<int:token_id>", methods=["POST"])
def cancel_token(token_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    user = db.session.get(User, session["user_id"])

    if not user or user.role != "student":
        return "Access denied! Students only."

    token = db.session.get(Token, token_id)

    if not token or token.user_id != user.id:
        return "Token not found!"

    if token.status != "waiting":
        return "This token cannot be cancelled!"

    token.status = "cancelled"
    db.session.commit()

    return redirect(url_for("dashboard"))

@app.route("/staff")
def staff_dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user = db.session.get(User, session["user_id"])

    if not user or user.role != "staff":
        return "Access denied! Staff only."

    tokens = Token.query.order_by(Token.id.asc()).all()
    appointments = Appointment.query.order_by(Appointment.id.asc()).all()

    return render_template(
        "staff.html",
        user=user,
        tokens=tokens,
        appointments=appointments
    )

@app.route("/admin")
def admin_dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user = db.session.get(User, session["user_id"])

    if not user or user.role != "admin":
        return "Access denied! Admin only."

    users = User.query.all()
    services = Service.query.all()
    tokens = Token.query.all()
    appointments = Appointment.query.all()

    waiting_tokens = Token.query.filter_by(status="waiting").count()
    serving_tokens = Token.query.filter_by(status="serving").count()
    completed_tokens = Token.query.filter_by(status="completed").count()

    return render_template(
        "admin.html",
        user=user,
        users=users,
        services=services,
        tokens=tokens,
        appointments=appointments,
        waiting_tokens=waiting_tokens,
        serving_tokens=serving_tokens,
        completed_tokens=completed_tokens
    )

@app.route("/add-service", methods=["POST"])
def add_service():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user = db.session.get(User, session["user_id"])

    if not user or user.role != "admin":
        return "Access denied!"

    name = request.form.get("name", "").strip()
    description = request.form.get("description", "").strip()

    if not name or not description:
        return "Service name and description are required!"

    if len(name) > 100 or len(description) > 255:
        return "Service name or description is too long!"

    new_service = Service(
        name=name,
        description=description
    )

    db.session.add(new_service)
    db.session.commit()

    return redirect(url_for("admin_dashboard"))


@app.route("/add-staff", methods=["POST"])
def add_staff():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user = db.session.get(User, session["user_id"])

    if not user or user.role != "admin":
        return "Access denied!"

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    # Validate required fields
    if not name or not email or not password:
        return "All fields are required!"

    # Validate name
    if len(name) < 2 or len(name) > 100:
        return "Staff name must be between 2 and 100 characters!"

    # Validate email
    if "@" not in email or "." not in email.split("@")[-1]:
        return "Please enter a valid email address!"

    # Validate password
    if len(password) < 8:
        return "Password must contain at least 8 characters!"

    if not any(char.isupper() for char in password):
        return "Password must contain an uppercase letter!"

    if not any(char.islower() for char in password):
        return "Password must contain a lowercase letter!"

    if not any(char.isdigit() for char in password):
        return "Password must contain a number!"

    # Check existing user
    if User.query.filter_by(email=email).first():
        return "Email already registered!"

    # Create staff account
    new_staff = User(
        name=name,
        email=email,
        password=generate_password_hash(password),
        role="staff"
    )

    db.session.add(new_staff)
    db.session.commit()

    return redirect(url_for("admin_dashboard"))


@app.route("/update-token/<int:token_id>/<status>", methods=["POST"])
def update_token(token_id, status):
    if "user_id" not in session:
        return redirect(url_for("login"))

    user = db.session.get(User, session["user_id"])

    if not user or user.role != "staff":
        return "Access denied!"

    if status not in ["serving", "completed"]:
        return "Invalid status!"

    token = db.session.get(Token, token_id)

    if not token:
        return "Token not found!"

    if status == "serving" and token.status != "waiting":
        return "Only waiting tokens can be called!"

    if status == "completed" and token.status != "serving":
        return "Only serving tokens can be completed!"

    token.status = status
    db.session.commit()

    return redirect(url_for("staff_dashboard"))

    return redirect(url_for("staff_dashboard"))

@app.route("/update-appointment/<int:appointment_id>/<status>", methods=["POST"])
def update_appointment(appointment_id, status):
    if "user_id" not in session:
        return redirect(url_for("login"))

    user = db.session.get(User, session["user_id"])

    if not user or user.role != "staff":
        return "Access denied!"

    if status not in ["confirmed", "completed"]:
        return "Invalid status!"

    appointment = db.session.get(Appointment, appointment_id)

    if not appointment:
        return "Appointment not found!"

    if status == "confirmed" and appointment.status != "booked":
        return "Only booked appointments can be confirmed!"

    if status == "completed" and appointment.status != "confirmed":
        return "Only confirmed appointments can be completed!"

    appointment.status = status
    db.session.commit()

    return redirect(url_for("staff_dashboard"))

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
