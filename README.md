# ASKHUB

## About the Project

ASKHUB is a simple question and answer platform inspired by Quora. It allows users to create an account, log in, ask questions, browse questions posted by other users, and share answers.

The project was developed as part of the Earny.in Internship Program to learn full-stack web development using Flask and MySQL.

The main goal of this project is to understand how frontend, backend, and database systems work together in a real-world application.

---

## Technologies Used

### Frontend

* HTML
* CSS

### Backend

* Python
* Flask

### Database

* MySQL

### Development Tools

* Git
* GitHub
* Visual Studio Code

---

## Features

* User Registration
* User Login and Logout
* Ask Questions
* View Questions Feed
* Submit Answers
* Session Management
* Flash Messages
* Database Connectivity using MySQL
* Responsive Interface

---

## Software Requirements

Before running the project, install the following software:

* Python 3.x
* MySQL Server
* MySQL Workbench
* Visual Studio Code

---

## Required Packages

Install the required Python packages:

```bash
pip install flask
pip install flask-mysqldb
pip install flask-bcrypt
pip install mysqlclient
```

Or install all packages together:

```bash
pip install flask flask-mysqldb flask-bcrypt mysqlclient
```

---

## Database Setup

Create a database named:

```sql
CREATE DATABASE quora_clone;
```

Run the provided `schema.sql` file to create all required tables.

---

## Project Structure

```text
ASKHUB/
│
├── app.py
├── schema.sql
├── README.md
│
├── static/
│   └── style.css
│
└── templates/
    ├── base.html
    ├── login.html
    ├── signup.html
    ├── feed.html
    ├── ask.html
    └── question.html
```

---

## Running the Project

Run the application using:

```bash
python app.py
```

Open the browser and visit:

```text
http://127.0.0.1:5000
```

---

## Team Contributions

### Rajan Maurya

**Project Coordinator & Repository Manager**

Responsibilities:

* Coordinated project development
* Managed GitHub repository and branches
* Reviewed and integrated team changes
* Maintained project documentation
* Tested overall project functionality
* Organized project structure

---

### Om
**Authentication Module**

Responsibilities:

* User Registration System
* User Login System
* Session Management
* Input Validation
* Authentication Improvements

Files Worked On:

* login.html
* signup.html
* app.py

---

### Nyashaa 
**Question Management Module**

Responsibilities:

* Ask Question Feature
* Question Feed Display
* Question Validation
* Feed Management
* Question System Improvements

Files Worked On:

* ask.html
* feed.html
* app.py

---

### Retish
**Answer Management Module**

Responsibilities:

* Answer Submission Feature
* Answer Display System
* Answer Validation
* Question Detail Page Management

Files Worked On:

* question.html
* app.py

---

### Sanjana
**User Interface & Styling Module**

Responsibilities:

* Frontend Design Improvements
* CSS Styling
* Layout Management
* Navigation Enhancements
* User Experience Improvements

Files Worked On:

* style.css
* base.html
* templates files


---

## Internship Project

ASKHUB was developed as part of the Earny.in Internship Program to gain practical experience in web development, database management, GitHub collaboration, and software project workflow.
