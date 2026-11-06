# 🎓 CampusQueue
### Smart College Queue & Appointment Management System

A web-based platform that simplifies college administrative services by allowing students to generate digital queue tokens, book appointments, and track their requests without waiting in long physical queues.

---

## 📌 About the Project

**CampusQueue** is a digital queue and appointment management platform designed to make college administrative services faster, more organized, and convenient.

The system connects students, administrative staff, and administrators through a centralized platform. Students can access services online, while staff can manage queues and appointments efficiently.

The goal is to reduce waiting time, improve service management, and create a smoother administrative experience on campus.

## ✨ Key Features

### 👨‍🎓 Student Module
- Student registration and secure login.
- View available college services.
- Generate digital queue tokens.
- Check queue position and token status.
- Cancel waiting tokens.
- Book appointments for administrative services.
- View appointment history.

### 👩‍💼 Staff Module
- Dedicated staff dashboard.
- View student queue tokens.
- Call the next waiting student.
- Update token status.
- View appointment requests.
- Confirm and complete appointments.

### 🛡️ Admin Module
- Dedicated administrator dashboard.
- View registered students and staff.
- Add new administrative services.
- Create staff accounts.
- Monitor tokens and appointments.
- View queue statistics and system overview.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| MySQL | Database management |
| Flask-SQLAlchemy | Database integration |
| HTML5 | Webpage structure |
| CSS3 | Styling and responsive design |
| JavaScript | Frontend interactions |
| Flask-WTF | CSRF protection |
| Flask-Limiter | Login rate limiting |
| Werkzeug | Password hashing |

## 🔐 Security Features

- Password hashing instead of storing plain-text passwords.
- Role-based access control for Students, Staff, and Admin.
- CSRF protection for form submissions.
- Login rate limiting.
- Server-side input validation.
- Session-based authentication.
- Environment variables for sensitive configuration.
- `.env` and virtual environment excluded through `.gitignore`.

## 📂 Project Structure

```text
CampusQueue/
│
├── app.py
├── config.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── static/
│   └── css/
│       └── style.css
│
└── templates/
    ├── index.html
    ├── login.html
    ├── register.html
    ├── registration_success.html
    ├── dashboard.html
    ├── staff.html
    ├── admin.html
    └── book_appointment.html
```

## ⚙️ Installation and Setup

Follow these steps to run CampusQueue locally.

### 1. Clone the Repository

```bash
git clone https://github.com/amaan3131-rgb/CampusQueue.git
```

### 2. Open the Project Directory

```bash
cd CampusQueue
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on macOS/Linux:

```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a local `.env` file in the project root:

```env
SECRET_KEY=your_private_secret_key
DB_PASSWORD=your_mysql_password
```

Replace the example values with your own private credentials. Never upload `.env` to GitHub.

### 6. Create the MySQL Database

Open MySQL and execute:

```sql
CREATE DATABASE campusqueue;
```

### 7. Run the Application

```bash
python app.py
```

Open your browser and visit:

```text
http://127.0.0.1:5000/
```

## 🔮 Future Enhancements

- Cloud deployment using Microsoft Azure.
- Real-time queue position updates.
- Email and notification integration.
- Improved analytics and reporting.
- Enhanced appointment scheduling.
- Responsive mobile-friendly interface.

## 🎯 Project Objective

CampusQueue aims to modernize traditional college administrative services through digital queue management and appointment scheduling.

It helps students save time, enables staff to manage requests efficiently, and gives administrators better visibility into service operations.

## 👨‍💻 Project Information

**Project Name:** CampusQueue  
**Category:** Web-Based Application  
**Domain:** College Administration / Queue Management  
**Backend:** Python Flask  
**Database:** MySQL  
**Repository:** [GitHub – CampusQueue](https://github.com/amaan3131-rgb/CampusQueue)

---

⭐ If you find this project interesting, consider giving the repository a star!