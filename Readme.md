# Employee Management System

## 📌 Project Overview

The Employee Management System is a web-based application developed to manage employee information, attendance, leave requests, salary management, and other employee-related activities.

The project is built using Flask and MySQL and is designed with DevOps practices in mind. Git, GitHub, Docker, Jenkins, and CI/CD are used to manage and automate the development and deployment process.

---

## 🎯 Objectives

* Manage employee information in one place.
* Allow HR/Admin to add, view, search, update, and manage employees.
* Allow employees to log in and view their own dashboard.
* Track employee attendance.
* Manage employee attendance records.
* Allow employees to submit leave requests.
* Allow HR/Admin to view and manage leave requests.
* Allow HR/Admin to approve or reject leave requests.
* Allow HR/Admin to reply to employee leave requests.
* Allow employees to submit early-going requests.
* Allow HR/Admin to approve or reject early-going requests.
* Manage employee salary information.
* View pending and processed salaries.
* Manage employee departments.
* Provide separate HR/Admin and Employee dashboards.
* Implement role-based login.
* Implement CI/CD using Jenkins.
* Use Docker for application containerization.
* Maintain project code using Git and GitHub.

---

## ✨ Features

### 👩‍💼 HR/Admin Features

* HR/Admin Login
* HR/Admin Dashboard
* Add Employee
* Automatically Generate Employee ID
* View Employees
* Search Employees
* View Employee Details
* Update Employee Details
* Delete Employee
* View Department-wise Employees
* Manage Employee Attendance
* View Employee Attendance
* Mark Attendance
* Mark Present
* Mark Absent
* Mark Leave
* Mark Late
* Add Check-in Time
* Add Check-out Time
* Add Attendance Notes
* View Attendance Summary
* View Leave Requests
* Approve Leave Requests
* Reject Leave Requests
* Reply to Employee Leave Requests
* View Early-Going Requests
* Approve Early-Going Requests
* Reject Early-Going Requests
* Reply to Employee Requests
* Salary Management
* Add Basic Salary
* View Pending Salaries
* View Processed Salaries
* Manage Salary Status
* Filter Salary Information
* View Salary Overview
* Export Salary Information
* View Dashboard Statistics

### 👨‍💻 Employee Features

* Employee Login
* Employee Dashboard
* View Personal Information
* View Attendance Summary
* View Attendance Records
* View Attendance Status
* Request Leave
* View Leave Request Status
* View HR/Admin Reply
* Request Early Going
* View Early-Going Request Status
* View Salary Information
* View Personal Employee Data

---

## 📊 Dashboard Features

### HR/Admin Dashboard

* Total Employees
* Department Count
* Today's Attendance
* Attendance Overview
* Salary Management Status
* Salary Overview
* Department-wise Employee Count
* Recent Employees
* Quick Actions
* Employee Search
* Dashboard Summary

### Employee Dashboard

* Personal Information
* Attendance Summary
* Attendance Records
* Leave Request Status
* Early-Going Request Status
* Salary Information
* Employee Dashboard Overview

---

## 🕒 Attendance Management

The attendance module is used to manage and track employee attendance.

### Attendance Status

* Present
* Absent
* Leave
* Late

### Attendance Information

* Employee
* Date
* Status
* Check-in Time
* Check-out Time
* Note

The system also provides attendance summary and monthly attendance information.

---

## 📝 Leave Management

Employees can submit leave requests from their employee dashboard.

### Employee

* Submit Leave Request
* Select Leave Date
* Enter Leave Reason
* View Leave Request Status
* View HR/Admin Reply

### HR/Admin

* View Leave Requests
* View Employee Leave Details
* Approve Leave Request
* Reject Leave Request
* Reply to Employee

---

## 🚪 Early-Going Management

Employees can submit a request when they want to leave the office early.

### Employee

* Submit Early-Going Request
* Select Date
* Select Leaving Time
* Enter Reason
* View Request Status

### HR/Admin

* View Early-Going Requests
* View Employee Request
* Approve Request
* Reject Request
* Reply to Employee

---

## 💰 Salary Management

The salary module is used to manage employee salary and payment information.

### HR/Admin

* Add Basic Salary
* Manage Employee Salary
* View Pending Salaries
* View Processed Salaries
* View Salary Status
* Filter Salary by Month
* Filter Salary by Department
* Filter Salary by Payment Status
* View Salary Overview
* Export Salary Information

### Salary Status

* Pending
* Processed

---

## 🏢 Department Management

The system manages employees according to their departments.

* Add Department
* Assign Department to Employee
* View Department-wise Employees
* View Department Employee Count
* Filter Employees by Department
* Use Department Information in Dashboard
* Use Department Information in Salary Management

---

## 🔐 Login and Role Management

The system provides different access for HR/Admin and Employees.

### HR/Admin

* Login to HR/Admin Dashboard
* Manage Employees
* Manage Attendance
* Manage Leave Requests
* Manage Early-Going Requests
* Manage Salary Information

### Employee

* Login to Employee Dashboard
* View Personal Information
* View Attendance
* Submit Leave Requests
* Submit Early-Going Requests
* View Salary Information

---

## 🛠️ Technologies Used

### Frontend

* HTML5
* CSS3
* JavaScript
* Bootstrap 5
* AJAX

### Backend

* Python
* Flask

### Database

* MySQL
* MySQL Workbench

### DevOps Tools

* Git
* GitHub
* Docker
* Jenkins
* CI/CD

---

## 🏗️ Project Structure

```text
employee-project/
│
├── app.py
├── requirements.txt
├── README.md
├── Dockerfile
├── Jenkinsfile
│
├── templates/
│   ├── login.html
│   ├── signup.html
│   ├── dashboard.html
│   ├── employees.html
│   ├── register.html
│   ├── employee_dashboard.html
│   ├── employee_attendance.html
│   ├── request_leave.html
│   ├── hr_leave_requests.html
│   └── salary.html
│
├── static/
│   ├── login.css
│   ├── style.css
│   ├── attendance.css
│   └── salary.css
│
└── database/
    └── management_db.sql
```

---

## 🗄️ Database

The application uses MySQL to store and manage employee-related information.

The database contains information related to:

* Users
* Employees
* Departments
* Attendance
* Leave Requests
* Early-Going Requests
* Salaries

MySQL Workbench is used for database creation, management, and SQL operations.

---

## 🔄 CI/CD and DevOps

The project uses DevOps practices to automate the development and deployment process.

### Git

Git is used for:

* Version Control
* Tracking Code Changes
* Managing Project Versions

### GitHub

GitHub is used for:

* Storing Project Code
* Managing Source Code
* Version Control
* Connecting the Project with Jenkins

### Docker

Docker is used to:

* Containerize the Flask Application
* Package the Application and Dependencies
* Create a Consistent Environment
* Make the Application Easier to Deploy

### Jenkins

Jenkins is used to automate the CI/CD pipeline.

Jenkins can perform:

* Get Latest Code from GitHub
* Install Dependencies
* Run Tests
* Build Docker Image
* Run Required Checks
* Prepare Application for Deployment

### CI/CD Pipeline

```text
Developer
    ↓
Git
    ↓
GitHub
    ↓
Jenkins
    ↓
Build
    ↓
Test
    ↓
Docker
    ↓
Deployment
```

---

## 🚀 Deployment

The application is containerized using Docker and Jenkins is used to automate the CI/CD process.

The deployment process can be:

```text
GitHub
   ↓
Jenkins
   ↓
Build
   ↓
Test
   ↓
Docker Image
   ↓
Docker Container
   ↓
Deployment
```

---

## 📋 Project Modules

The project contains the following major modules:

1. Login and Authentication
2. Employee Registration
3. Employee Management
4. Department Management
5. HR/Admin Dashboard
6. Employee Dashboard
7. Attendance Management
8. Leave Management
9. Early-Going Management
10. Salary Management
11. Database Management
12. Git and GitHub
13. Docker
14. Jenkins
15. CI/CD
16. Deployment

---

## 🎯 Expected Outcome

The Employee Management System provides a single platform for HR/Admin and employees to manage employee-related activities.

The system reduces manual work by providing employee management, attendance tracking, leave management, early-going requests, salary management, department management, and separate dashboards for HR/Admin and employees.

The project also uses Git, GitHub, Docker, Jenkins, and CI/CD to follow DevOps practices and make the application easier to manage, test, and deploy.
