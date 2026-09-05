from flask import Flask, render_template, request, redirect, Response, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import re
from datetime import datetime
import mysql.connector
import pymysql

pymysql.install_as_MySQLdb()
import csv
import io
import os


app = Flask(__name__)
app.secret_key = 'employee-management-system-secret'

# ---------------- MYSQL CONNECTION ----------------
try:
    db = mysql.connector.connect(
        host=os.getenv('MYSQL_HOST', 'localhost'),
        user=os.getenv('MYSQL_USER', 'root'),
        password=os.getenv('MYSQL_PASSWORD', 'root'),
        database=os.getenv('MYSQL_DATABASE', 'employee_db'),
        autocommit=True
    )
    cursor = db.cursor(dictionary=True)
except Exception as e:
    print(f"Database connection warning: {e}")
    db = None
    cursor = None


# ---------------- LOGIN PAGE ----------------
@app.route('/')
def login():
    return render_template('login.html')


# ---------------- SIGNUP PAGE ----------------
@app.route('/signup')
def signup():
    role = request.args.get('role', 'admin').strip().lower()

    print("SIGNUP PAGE ROLE =", role)

    return render_template(
        'signup.html',
        role=role
    )

# ---------------- REGISTER USER ----------------
@app.route('/register-user', methods=['POST'])
def register_user():

    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    confirm_password = request.form.get('confirm_password', '')
    role = request.form.get('role', 'admin')
    employee_code = request.form.get('employee_code', '').strip()

    print("ROLE =", role)
    print("EMPLOYEE CODE =", employee_code)

    print("SIGNUP ROLE RECEIVED =", role)

    # =====================================================
    # BASIC VALIDATION
    # =====================================================

    if not username:
        return render_template(
            'signup.html',
            error="Username is required.",
            role=role
        )

    if not password:
        return render_template(
            'signup.html',
            error="Password is required.",
            role=role
        )

    if not confirm_password:
        return render_template(
            'signup.html',
            error="Please confirm your password.",
            role=role
        )

    # =====================================================
    # PASSWORD VALIDATION
    # =====================================================

    password_pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z\d]).{8,}$'

    if not re.match(password_pattern, password):
        return render_template(
            'signup.html',
            error="Password must contain 8+ characters, uppercase, lowercase, number and special character.",
            role=role
        )

    if password != confirm_password:
        return render_template(
            'signup.html',
            error="Passwords do not match.",
            role=role
        )

    # =====================================================
    # CHECK USERNAME
    # =====================================================

    cursor.execute(
        "SELECT * FROM users WHERE username=%s",
        (username,)
    )

    existing_user = cursor.fetchone()

    if existing_user:
        return render_template(
            'signup.html',
            error="Username already exists.",
            role=role
        )

    # =====================================================
    # EMPLOYEE SIGNUP
    # =====================================================

    employee_id = None

    if role == 'employee':

        employee_code = request.form.get('employee_code', '').strip()

        if not employee_code:
            return render_template(
                'signup.html',
                error="Employee Code is required.",
                role=role
            )

        # Find employee using employee code
        cursor.execute("""
            SELECT id
            FROM employees
            WHERE employee_code = %s
        """, (employee_code,))

        employee = cursor.fetchone()

        if not employee:
            return render_template(
                'signup.html',
                error="Employee Code not found. Please enter a valid Employee Code.",
                role=role
            )

        employee_id = employee['id']

        # Check whether this employee already has an account
        cursor.execute("""
            SELECT id
            FROM users
            WHERE employee_id = %s
        """, (employee_id,))

        existing_employee_account = cursor.fetchone()

        if existing_employee_account:
            return render_template(
                'signup.html',
                error="This employee already has an account.",
                role=role
            )
        

        # ---------------- EMPLOYEE LINK ----------------
        employee_id=None
        if role == 'employee':
            employee_code = request.form.get('employee_code', '').strip()

           

            # Find employee using employee code
            cursor.execute("""
                SELECT id
                FROM employees
                WHERE employee_code = %s
            """, (employee_code,))

            employee = cursor.fetchone()

            if not employee:
                return render_template(
                    'signup.html',
                    error="Employee Code not found.",
                    role=role
                )

            employee_id = employee['id']

            # Check whether this employee already has an account
            cursor.execute("""
                SELECT id
                FROM users
                WHERE employee_id = %s
            """, (employee_id,))

            existing_employee_account = cursor.fetchone()

            if existing_employee_account:
                return render_template(
                    'signup.html',
                    error="This employee already has an account.",
                    role=role
                )
       
       

    # =====================================================
    # CREATE USER
    # =====================================================

    hashed_password = generate_password_hash(password)

    cursor.execute("""
        INSERT INTO users
        (
            username,
            password,
            role,
            employee_id
         
        )
        VALUES (%s, %s, %s, %s)
    """, (
        username,
        hashed_password,
        role,
        employee_id
    ))

    db.commit()

    print("REGISTRATION SUCCESSFUL:", username)
    print("ROLE:", role)
    print("EMPLOYEE ID:", employee_id)

    # Keep role when returning to login
    return redirect(f'/?role={role}')

# ---------------- LOGIN CHECK ----------------
@app.route('/login', methods=['POST'])
def do_login():

    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    selected_role = request.form.get('role', 'admin').strip().lower()

    cursor.execute("""
        SELECT
            id,
            username,
            password,
            role,
            employee_id
        FROM users
        WHERE username = %s
    """, (username,))

    user = cursor.fetchone()

    print("LOGIN USER =", user)

    # Wrong username or password
    if not user or not check_password_hash(user['password'], password):
        return render_template(
            'login.html',
            error="Wrong username or password."
        )
        # User selected wrong portal

    if user['role'] != selected_role:

        if selected_role == 'employee':
            return render_template(
                'login.html',
                error="Employee username does not exist."
            )

        else:
            return render_template(
                'login.html',
                error="Admin username does not exist."
            )

    print("LOGIN USERNAME:", user['username'])
    print("EMPLOYEE ID:", user['employee_id'])

    # =========================
    # ADMIN LOGIN
    # =========================

    if user['role'] == 'admin':

        session.clear()

        session['user_id'] = user['id']
        session['username'] = user['username']
        session['role'] = 'admin'

        return redirect('/dashboard')

    # =========================
    # EMPLOYEE LOGIN
    # =========================

    elif user['role'] == 'employee':

        if not user['employee_id']:
            return "Employee account is not linked to an employee record.", 404

        session.clear()

        session['user_id'] = user['id']
        session['username'] = user['username']
        session['role'] = 'employee'
        session['employee_id'] = user['employee_id']

        return redirect('/employee-dashboard')

    return render_template(
        'login.html',
        error="Invalid user role."
    )




@app.route('/dashboard')
def dashboard():

    current_date = datetime.now().strftime('%Y-%m-%d')

    # =========================================================
    # TOTAL EMPLOYEES
    # =========================================================

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM employees
    """)

    total_employees = cursor.fetchone()['total']


    # =========================================================
    # TODAY'S PRESENT
    # =========================================================

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM attendance a
        JOIN employees e
            ON a.employee_id = e.id
        WHERE a.attendance_date = %s
        AND a.status = 'Present'
    """, (current_date,))

    today_present = cursor.fetchone()['total']


    # =========================================================
    # TODAY'S ATTENDANCE
    # =========================================================

    cursor.execute("""
        SELECT
            a.status,
            a.check_in,
            e.employee_code,
            e.first_name,
            e.last_name,
            d.dept_name AS department
        FROM attendance a
        JOIN employees e
            ON a.employee_id = e.id
        LEFT JOIN departments d
            ON e.dept_id = d.dept_id
        WHERE a.attendance_date = %s
        ORDER BY a.id DESC
    """, (current_date,))

    today_attendance = cursor.fetchall()


    # =========================================================
    # DEPARTMENT OVERVIEW
    # =========================================================

    cursor.execute("""
        SELECT
            d.dept_name AS department,
            COUNT(e.id) AS total
        FROM departments d
        LEFT JOIN employees e
            ON d.dept_id = e.dept_id
        GROUP BY d.dept_id, d.dept_name
        ORDER BY total DESC, d.dept_name ASC
    """)

    department_data = cursor.fetchall()


    # =========================================================
    # DEPARTMENT PERCENTAGES
    # =========================================================

    max_department_employees = 0

    if department_data:

        max_department_employees = max(
            int(dept['total'])
            for dept in department_data
        )

    for dept in department_data:

        if max_department_employees > 0:

            dept['percentage'] = round(
                (int(dept['total']) /
                 max_department_employees) * 100
            )

        else:

            dept['percentage'] = 0


    # =========================================================
    # SELECTED MONTH
    # =========================================================

    current_month = request.args.get(
        'month',
        datetime.now().strftime('%Y-%m')
    )


    # =========================================================
    # MONTHLY ATTENDANCE
    # =========================================================

    cursor.execute("""
        SELECT
            a.status,
            COUNT(*) AS total
        FROM attendance a
        JOIN employees e
            ON a.employee_id = e.id
        WHERE a.attendance_date >= %s
        AND a.attendance_date < DATE_ADD(%s, INTERVAL 1 MONTH)
        GROUP BY a.status
    """, (
        current_month + '-01',
        current_month + '-01'
    ))

    monthly_data = cursor.fetchall()


    # Default values

    monthly_present = 0
    monthly_absent = 0
    monthly_leave = 0


    # Read monthly results

    for row in monthly_data:

        if row['status'] == 'Present':

            monthly_present = row['total']

        elif row['status'] == 'Absent':

            monthly_absent = row['total']

        elif row['status'] == 'Leave':

            monthly_leave = row['total']


    # Monthly total

    monthly_total = (
        monthly_present +
        monthly_absent +
        monthly_leave
    )


    # Monthly attendance rate

    if monthly_total > 0:

        monthly_rate = round(
            (monthly_present / monthly_total) * 100,
            2
        )

    else:

        monthly_rate = 0


    # =========================================================
    # MONTHLY PAYROLL
    # =========================================================

    # Total payroll

    cursor.execute("""
        SELECT COALESCE(SUM(net_salary), 0) AS total_payroll
        FROM salary
        WHERE DATE_FORMAT(salary_month, '%Y-%m') = %s
    """, (current_month,))

    total_payroll = cursor.fetchone()['total_payroll']


    # =========================================================
    # PAID PAYROLL
    # =========================================================

    cursor.execute("""
        SELECT COALESCE(SUM(net_salary), 0) AS paid_payroll
        FROM salary
        WHERE DATE_FORMAT(salary_month, '%Y-%m') = %s
        AND payment_status = 'Paid'
    """, (current_month,))

    paid_payroll = cursor.fetchone()['paid_payroll']


    # =========================================================
    # PENDING PAYROLL
    # =========================================================

    cursor.execute("""
        SELECT COALESCE(SUM(net_salary), 0) AS pending_payroll
        FROM salary
        WHERE DATE_FORMAT(salary_month, '%Y-%m') = %s
        AND payment_status = 'Pending'
    """, (current_month,))

    pending_payroll = cursor.fetchone()['pending_payroll']


    # =========================================================
    # PAID EMPLOYEE COUNT
    # =========================================================

    cursor.execute("""
        SELECT COUNT(*) AS paid_count
        FROM salary
        WHERE DATE_FORMAT(salary_month, '%Y-%m') = %s
        AND payment_status = 'Paid'
    """, (current_month,))

    processed_salaries = cursor.fetchone()['paid_count']


    # =========================================================
    # PENDING EMPLOYEE COUNT
    # =========================================================

    cursor.execute("""
        SELECT COUNT(*) AS pending_count
        FROM salary
        WHERE DATE_FORMAT(salary_month, '%Y-%m') = %s
        AND payment_status = 'Pending'
    """, (current_month,))

    pending_salary_count = cursor.fetchone()['pending_count']


    # =========================================================
    # INITIATED EMPLOYEE COUNT
    # =========================================================

    cursor.execute("""
        SELECT COUNT(*) AS initiated_count
        FROM salary
        WHERE DATE_FORMAT(salary_month, '%Y-%m') = %s
        AND payment_status = 'Initiated'
    """, (current_month,))

    initiated_salary_count = cursor.fetchone()['initiated_count']


    # =========================================================
    # PAYROLL COMPLETION
    # =========================================================

    if total_payroll and float(total_payroll) > 0:

        completion_rate = round(
            (float(paid_payroll) /
             float(total_payroll)) * 100,
            2
        )

    else:

        completion_rate = 0


    # =========================================================
    # SEND DATA TO DASHBOARD
    # =========================================================

    return render_template(
        'dashboard.html',

        # Employees
        total_employees=total_employees,

        # Today's attendance
        today_present=today_present,
        today_attendance=today_attendance,

        # Departments
        department_data=department_data,
        max_department_employees=max_department_employees,

        # Monthly attendance
        monthly_present=monthly_present,
        monthly_absent=monthly_absent,
        monthly_leave=monthly_leave,
        monthly_rate=monthly_rate,

        # Monthly payroll
        processed_salaries=processed_salaries,
        pending_salary_count=pending_salary_count,
        initiated_salary_count=initiated_salary_count,

        total_payroll=total_payroll,
        paid_payroll=paid_payroll,
        pending_payroll=pending_payroll,

        completion_rate=completion_rate,

        # Selected month
        current_month=current_month
    )
# ---------------- REGISTER PAGE ----------------
@app.route('/register')
def register():

    cursor.execute("""
        SELECT dept_id, dept_name
        FROM departments
        ORDER BY dept_name
    """)

    departments = cursor.fetchall()

    return render_template(
        'register.html',
        departments=departments
    )



# ---------------- SAVE EMPLOYEE ----------------
@app.route('/save-employee', methods=['POST'])
def save_employee():

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    dept_id = request.form['dept_id']
    role = request.form['role']
    email = request.form['email']
    phone = request.form['phone']
    join_date = request.form['join_date']
    birth_date = request.form['birth_date']

    employee_code = 'EMP' + phone[-4:]

    sql = """
        INSERT INTO employees
        (
            employee_code,
            first_name,
            last_name,
            role,
            email,
            join_date,
            birth_date,
            phone,
            dept_id
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        employee_code,
        first_name,
        last_name,
        role,
        email,
        join_date,
        birth_date,
        phone,
        dept_id
    )

    cursor.execute(sql, values)
    db.commit()

    return redirect('/employees')
# ---------------- EMPLOYEE LIST ----------------
@app.route('/employees')
def employees():
    cursor.execute("""
        SELECT
            e.*,
            d.dept_name AS department
        FROM employees e
        LEFT JOIN departments d
            ON e.dept_id = d.dept_id
        ORDER BY e.id DESC
    """)

    employees_data = cursor.fetchall()

    return render_template(
        'employees.html',
        employees=employees_data
    )


# ---------------- EDIT EMPLOYEE ----------------
@app.route('/edit-employee/<int:id>')
def edit_employee(id):

    cursor.execute("""
        SELECT
            e.id,
            e.employee_code,
            e.first_name,
            e.last_name,
            e.role,
            e.email,
            e.join_date,
            e.birth_date,
            e.phone,
            e.dept_id,
            d.dept_name
        FROM employees e
        LEFT JOIN departments d
            ON e.dept_id = d.dept_id
        WHERE e.id = %s
    """, (id,))

    emp = cursor.fetchone()

    if not emp:
        return "Employee not found", 404

    cursor.execute("""
        SELECT dept_id, dept_name
        FROM departments
        ORDER BY dept_name
    """)

    departments = cursor.fetchall()

    return render_template(
        'edit.html',
        emp=emp,
        departments=departments
    )
@app.route('/update-employee/<int:id>', methods=['POST'])
def update_employee(id):

    try:

        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        dept_id = request.form.get('dept_id')
        role = request.form.get('role')
        join_date = request.form.get('join_date')
        birth_date = request.form.get('birth_date')

        cursor.execute("""
            UPDATE employees
            SET
                first_name = %s,
                last_name = %s,
                email = %s,
                phone = %s,
                dept_id = %s,
                role = %s,
                join_date = %s,
                birth_date = %s
            WHERE id = %s
        """, (
            first_name,
            last_name,
            email,
            phone,
            dept_id,
            role,
            join_date,
            birth_date,
            id
        ))

        db.commit()

        return redirect('/employees')

    except Exception as e:

        db.rollback()

        print("Update employee error:", e)

        return f"""
        <h2>Error updating employee</h2>
        <pre>{e}</pre>
        """, 500
# ---------------- DELETE EMPLOYEE ----------------
@app.route('/delete-employee/<int:id>')
def delete_employee(id):

    try:
        # Delete salary records first
        cursor.execute(
            "DELETE FROM salary WHERE employee_id = %s",
            (id,)
        )

        # Delete attendance records
        cursor.execute(
            "DELETE FROM attendance WHERE employee_id = %s",
            (id,)
        )

        # Delete employee
        cursor.execute(
            "DELETE FROM employees WHERE id = %s",
            (id,)
        )

        db.commit()

        return redirect('/employees')

    except Exception as e:
        db.rollback()
        print("Delete employee error:", e)

        return "Error deleting employee", 500

@app.route('/attendance')
def attendance():

    current_date = datetime.now().strftime('%Y-%m-%d')

    selected_date = request.args.get('filter_date') or current_date
    selected_department = request.args.get('department')
    selected_status = request.args.get('status_filter')

    # ---------------- ATTENDANCE RECORDS ----------------

    query = """
        SELECT
            a.id,
            a.employee_id,
            a.attendance_date,
            a.status,
            a.check_in,
            a.check_out,
            e.employee_code,
            e.first_name,
            e.last_name,
            d.dept_name AS department
        FROM attendance a
        JOIN employees e
            ON a.employee_id = e.id
        LEFT JOIN departments d
            ON e.dept_id = d.dept_id
        WHERE a.attendance_date = %s
    """

    params = [selected_date]

    # Department filter
    if selected_department:
        query += " AND d.dept_name = %s"
        params.append(selected_department)

    # Status filter
    if selected_status:
        query += " AND a.status = %s"
        params.append(selected_status)

    query += " ORDER BY a.id DESC"

    cursor.execute(query, tuple(params))
    attendance = cursor.fetchall()

    # ---------------- DEPARTMENTS ----------------

    cursor.execute("""
        SELECT dept_name
        FROM departments
        ORDER BY dept_name
    """)

    departments = [
        row['dept_name']
        for row in cursor.fetchall()
    ]

    # ---------------- EMPLOYEES FOR QUICK MARK ----------------

    cursor.execute("""
        SELECT
            id,
            employee_code,
            first_name,
            last_name
        FROM employees
        ORDER BY first_name, last_name
    """)

    employees = cursor.fetchall()

    # ---------------- TOTAL ATTENDANCE ----------------

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM attendance a
        JOIN employees e
            ON a.employee_id = e.id
        WHERE a.attendance_date = %s
    """, (selected_date,))

    total = cursor.fetchone()['total']

    # ---------------- PRESENT ----------------

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM attendance a
        JOIN employees e
            ON a.employee_id = e.id
        WHERE a.attendance_date = %s
        AND a.status = 'Present'
    """, (selected_date,))

    present_count = cursor.fetchone()['total']

    # ---------------- ABSENT ----------------

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM attendance a
        JOIN employees e
            ON a.employee_id = e.id
        WHERE a.attendance_date = %s
        AND a.status = 'Absent'
    """, (selected_date,))

    absent_count = cursor.fetchone()['total']

    # ---------------- LEAVE ----------------

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM attendance a
        JOIN employees e
            ON a.employee_id = e.id
        WHERE a.attendance_date = %s
        AND a.status = 'Leave'
    """, (selected_date,))

    leave_count = cursor.fetchone()['total']

    # ---------------- ATTENDANCE RATE ----------------

    attendance_rate = (
        round((present_count / total) * 100, 2)
        if total > 0
        else 0
    )

    return render_template(
        'attendance.html',
        attendance=attendance,
        employees=employees,
        departments=departments,
        selected_date=selected_date,
        current_date=current_date,
        selected_department=selected_department,
        selected_status=selected_status,
        present_count=present_count,
        absent_count=absent_count,
        leave_count=leave_count,
        attendance_rate=attendance_rate
    )
# ---------------- SAVE ATTENDANCE ----------------
@app.route('/save-attendance', methods=['POST'])
def save_attendance():

    employee_id = request.form.get('employee_id')

    print("EMPLOYEE ID =", employee_id)

    if not employee_id:
        return "Please select an employee.", 400

    attendance_date = request.form['attendance_date']
    status = request.form['status']

    cursor.execute("""
        INSERT INTO attendance
        (employee_id, attendance_date, status)
        VALUES (%s, %s, %s)
    """, (
        employee_id,
        attendance_date,
        status
    ))

    db.commit()

    return redirect('/attendance')


# ---------------- UPDATE ATTENDANCE STATUS ----------------
@app.route('/update-attendance-status', methods=['POST'])
def update_attendance_status():

    attendance_id = request.form['attendance_id']
    status = request.form['status']

    cursor.execute("""
        UPDATE attendance
        SET status = %s
        WHERE id = %s
    """, (status, attendance_id))

    db.commit()

    return '', 200


# ---------------- CHECK IN ----------------
@app.route('/check-in/<int:attendance_id>', methods=['POST'])
def check_in(attendance_id):

    check_in_time = datetime.now().strftime('%H:%M:%S')

    cursor.execute("""
        UPDATE attendance
        SET check_in = %s
        WHERE id = %s
    """, (check_in_time, attendance_id))

    db.commit()

    return redirect('/attendance')


# ---------------- CHECK OUT ----------------
@app.route('/check-out/<int:attendance_id>', methods=['POST'])
def check_out(attendance_id):

    check_out_time = datetime.now().strftime('%H:%M:%S')

    cursor.execute("""
        UPDATE attendance
        SET check_out = %s
        WHERE id = %s
    """, (check_out_time, attendance_id))

    db.commit()

    return redirect('/attendance')


# ---------------- EXPORT ATTENDANCE CSV ----------------
@app.route('/export-attendance')
def export_attendance():

    selected_date = request.args.get(
        'filter_date',
        datetime.now().strftime('%Y-%m-%d')
    )

    cursor.execute("""
        SELECT
        e.employee_code,
        e.first_name,
        e.last_name,
        d.dept_name AS department,
        a.attendance_date,
        a.status,
         a.check_in,
        a.check_out
        FROM attendance a
        JOIN employees e
            ON a.employee_id = e.id
        LEFT JOIN departments d
    ON e.dept_id = d.dept_id
        WHERE a.attendance_date = %s
        ORDER BY a.id DESC
    """, (selected_date,))

    records = cursor.fetchall()

    import csv
    from io import StringIO
    from flask import Response

    output = StringIO()

    writer = csv.writer(output)

    writer.writerow([
        'Employee ID',
        'Name',
        'Department',
        'Date',
        'Status',
        'Check In',
        'Check Out'
    ])

    for row in records:

        writer.writerow([
            row['employee_code'],
            row['first_name'] + ' ' + row['last_name'],
            row['department'],
            row['attendance_date'],
            row['status'],
            row['check_in'],
            row['check_out']
        ])

    response = Response(
        output.getvalue(),
        mimetype='text/csv'
    )

    response.headers['Content-Disposition'] = (
        f'attachment; filename=attendance_{selected_date}.csv'
    )

    return response
# =========================================================
# DEPARTMENT MANAGEMENT
# =========================================================

@app.route('/departments')
def departments():

    cursor.execute("""
        SELECT
            d.dept_id,
            d.dept_name,
            d.dept_head,
            d.description,
            d.created_date,
            COUNT(e.id) AS total_employees
        FROM departments d
        LEFT JOIN employees e
            ON d.dept_id = e.dept_id
        GROUP BY
            d.dept_id,
            d.dept_name,
            d.dept_head,
            d.description,
            d.created_date
        ORDER BY d.dept_name
    """)

    departments = cursor.fetchall()

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM employees
    """)

    total_employees = cursor.fetchone()['total']

    cursor.execute("""
        SELECT
            id,
            first_name,
            last_name
        FROM employees
        ORDER BY first_name
    """)

    employees = cursor.fetchall()

    return render_template(
        'departments.html',
        departments=departments,
        total_employees=total_employees,
        employees=employees
    )


# =========================================================
# DEPARTMENT TEAM
# =========================================================

@app.route('/department-team/<int:dept_id>')
def department_team(dept_id):

    cursor.execute("""
        SELECT dept_name
        FROM departments
        WHERE dept_id = %s
    """, (dept_id,))

    dept = cursor.fetchone()

    cursor.execute("""
        SELECT
            id,
            employee_code,
            first_name,
            last_name,
            role,
            email,
            phone,
            join_date,
            birth_date
        FROM employees
        WHERE dept_id = %s
        ORDER BY first_name, last_name
    """, (dept_id,))

    employees = cursor.fetchall()

    return {
        'department': dept['dept_name'] if dept else 'Team',
        'employees': employees
    }


# =========================================================
# ADD DEPARTMENT
# =========================================================

@app.route('/add-department', methods=['POST'])
def add_department():

    dept_name = request.form.get('dept_name', '').strip()
    dept_head = request.form.get('dept_head', '').strip()
    description = request.form.get('description', '').strip()

    created_date = request.form.get('created_date')

    cursor.execute("""
        INSERT INTO departments
        (
            dept_name,
            dept_head,
            description,
            created_date
        )
        VALUES (%s, %s, %s, %s)
    """, (
        dept_name,
        dept_head,
        description,
        created_date
    ))

    db.commit()

    return redirect('/departments')

# =========================================================
# DELETE DEPARTMENT
# =========================================================

@app.route('/delete-department/<int:dept_id>', methods=['POST'])
def delete_department(dept_id):

    cursor.execute("""
        DELETE FROM departments
        WHERE dept_id = %s
    """, (dept_id,))

    db.commit()

    return redirect('/departments')


# =========================================================
# EDIT DEPARTMENT
# =========================================================

@app.route('/edit-department/<int:dept_id>', methods=['POST'])
def edit_department(dept_id):

    dept_name = request.form.get('dept_name', '').strip()
    dept_head = request.form.get('dept_head', '').strip()
    description = request.form.get('description', '').strip()
    created_date = request.form.get('created_date')

    cursor.execute("""
        UPDATE departments
        SET
            dept_name = %s,
            dept_head = %s,
            description = %s,
            created_date = %s
        WHERE dept_id = %s
    """, (
        dept_name,
        dept_head,
        description,
        created_date,
        dept_id
    ))

    db.commit()

    return redirect('/departments')


@app.route('/salary')
def salary():

    # =========================================================
    # FILTER VALUES
    # =========================================================

    month = request.args.get('month', '').strip()
    department = request.args.get('department', '').strip()
    payment_status = request.args.get('payment_status', '').strip()
    search = request.args.get('search', '').strip()

    # =========================================================
    # EDIT SALARY
    # =========================================================

    edit_id = request.args.get('edit')
    edit_salary = None

    if edit_id:
        cursor.execute("""
            SELECT *
            FROM salary
            WHERE id = %s
        """, (edit_id,))

        edit_salary = cursor.fetchone()

    # =========================================================
    # EMPLOYEES
    # =========================================================

    cursor.execute("""
        SELECT
            id,
            employee_code,
            first_name,
            last_name,
            dept_id
        FROM employees
        ORDER BY first_name
    """)

    employees = cursor.fetchall()

    # =========================================================
    # DEPARTMENTS
    # =========================================================

    cursor.execute("""
        SELECT
            dept_id,
            dept_name
        FROM departments
        ORDER BY dept_name
    """)

    departments = cursor.fetchall()

    # =========================================================
    # SALARY RECORDS + FILTERS
    # =========================================================

    query = """
        SELECT
            s.id,
            e.employee_code,
            e.first_name,
            e.last_name,
            e.dept_id,
            d.dept_name AS department,
            s.salary_month,
            s.basic_salary,
            s.allowance,
            s.deduction,
            s.net_salary,
            s.payment_status,
            s.payment_date
        FROM salary s

        JOIN employees e
            ON s.employee_id = e.id

        LEFT JOIN departments d
            ON e.dept_id = d.dept_id

        WHERE 1 = 1
    """

    params = []

    # =========================================================
    # MONTH FILTER
    # =========================================================

    if month:
        query += """
            AND DATE_FORMAT(s.salary_month, '%Y-%m') = %s
        """
        params.append(month)

    # =========================================================
    # DEPARTMENT FILTER
    # =========================================================

    if department:
        query += """
            AND e.dept_id = %s
        """
        params.append(department)

    # =========================================================
    # PAYMENT STATUS FILTER
    # =========================================================

    if payment_status:
        query += """
            AND s.payment_status = %s
        """
        params.append(payment_status)

    # =========================================================
    # EMPLOYEE SEARCH
    # =========================================================

    if search:

        query += """
            AND (
                e.employee_code LIKE %s
                OR e.first_name LIKE %s
                OR e.last_name LIKE %s
                OR CONCAT(e.first_name, ' ', e.last_name) LIKE %s
            )
        """

        search_value = f"%{search}%"

        params.extend([
            search_value,
            search_value,
            search_value,
            search_value
        ])

    query += """
        ORDER BY s.id DESC
    """

    cursor.execute(query, params)

    salaries = cursor.fetchall()

    # =========================================================
    # SALARY CARDS
    # =========================================================

    cursor.execute("""
        SELECT COALESCE(SUM(net_salary), 0) AS total
        FROM salary
    """)

    total_payroll = cursor.fetchone()['total']

    cursor.execute("""
        SELECT COALESCE(SUM(net_salary), 0) AS total
        FROM salary
        WHERE payment_status = 'Paid'
    """)

    paid_salary = cursor.fetchone()['total']

    cursor.execute("""
        SELECT COALESCE(SUM(net_salary), 0) AS total
        FROM salary
        WHERE payment_status IN ('Pending', 'Initiated')
    """)

    pending_salary = cursor.fetchone()['total']

    cursor.execute("""
        SELECT COUNT(DISTINCT employee_id) AS total
        FROM salary
        WHERE payment_status = 'Paid'
    """)

    employees_paid = cursor.fetchone()['total']

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM employees
    """)

    total_employees = cursor.fetchone()['total']

    # =========================================================
    # RENDER
    # =========================================================

    return render_template(
        'salary.html',

        employees=employees,
        departments=departments,
        salaries=salaries,

        total_payroll=total_payroll,
        paid_salary=paid_salary,
        pending_salary=pending_salary,

        employees_paid=employees_paid,
        total_employees=total_employees,

        edit_salary=edit_salary,

        # Keep filters selected after Apply Filters
        selected_month=month,
        selected_department=department,
        selected_payment_status=payment_status,
        search_value=search
    )
# =========================================================
# SAVE SALARY
# =========================================================

@app.route('/save-salary', methods=['POST'])
def save_salary():

    employee_id = request.form.get('employee_id')
    salary_month = request.form.get('salary_month')

    basic_salary = request.form.get('basic_salary') or 0
    allowance = request.form.get('allowance') or 0
    deduction = request.form.get('deduction') or 0
    net_salary = request.form.get('net_salary') or 0

    payment_status = request.form.get('payment_status')
    payment_date = request.form.get('payment_date') or None

    # Convert YYYY-MM to YYYY-MM-01
    if salary_month and len(salary_month) == 7:
        salary_month = salary_month + '-01'

    sql = """
        INSERT INTO salary
        (
            employee_id,
            salary_month,
            basic_salary,
            allowance,
            deduction,
            net_salary,
            payment_status,
            payment_date
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(
        sql,
        (
            employee_id,
            salary_month,
            basic_salary,
            allowance,
            deduction,
            net_salary,
            payment_status,
            payment_date
        )
    )

    db.commit()

    return redirect('/salary')

# =========================================================
# UPDATE SALARY
# =========================================================
@app.route('/update-salary/<int:id>', methods=['POST'])
def update_salary(id):

    employee_id = request.form.get('employee_id')
    salary_month = request.form.get('salary_month')

    basic_salary = request.form.get('basic_salary') or 0
    allowance = request.form.get('allowance') or 0
    deduction = request.form.get('deduction') or 0
    net_salary = request.form.get('net_salary') or 0

    payment_status = request.form.get('payment_status')
    payment_date = request.form.get('payment_date') or None

    # Convert YYYY-MM to YYYY-MM-01
    if salary_month and len(salary_month) == 7:
        salary_month = salary_month + '-01'

    cursor.execute("""
        UPDATE salary
        SET
            employee_id = %s,
            salary_month = %s,
            basic_salary = %s,
            allowance = %s,
            deduction = %s,
            net_salary = %s,
            payment_status = %s,
            payment_date = %s
        WHERE id = %s
    """, (
        employee_id,
        salary_month,
        basic_salary,
        allowance,
        deduction,
        net_salary,
        payment_status,
        payment_date,
        id
    ))

    db.commit()

    return redirect('/salary')
@app.route('/export-salary-csv')
def export_salary_csv():

    month = request.args.get('month', '').strip()
    department = request.args.get('department', '').strip()
    payment_status = request.args.get('payment_status', '').strip()
    search = request.args.get('search', '').strip()


    # =========================================================
    # BUILD QUERY
    # =========================================================

    query = """
        SELECT
            e.employee_code,
            e.first_name,
            e.last_name,
            d.dept_name AS department,
            s.salary_month,
            s.basic_salary,
            s.allowance,
            s.deduction,
            s.net_salary,
            s.payment_status,
            s.payment_date

        FROM salary s

        JOIN employees e
            ON s.employee_id = e.id

        LEFT JOIN departments d
            ON e.dept_id = d.dept_id

        WHERE 1 = 1
    """

    params = []


    # =========================================================
    # MONTH
    # =========================================================

    if month:

        query += """
            AND DATE_FORMAT(s.salary_month, '%%Y-%%m') = %s
        """

        params.append(month)


    # =========================================================
    # DEPARTMENT
    # =========================================================

    if department:

        query += """
            AND e.dept_id = %s
        """

        params.append(department)


    # =========================================================
    # PAYMENT STATUS
    # =========================================================

    if payment_status:

        query += """
            AND s.payment_status = %s
        """

        params.append(payment_status)


    # =========================================================
    # SEARCH
    # =========================================================

    if search:

        query += """
            AND (
                e.employee_code LIKE %s
                OR e.first_name LIKE %s
                OR e.last_name LIKE %s
                OR CONCAT(e.first_name, ' ', e.last_name) LIKE %s
            )
        """

        search_value = "%" + search + "%"

        params.extend([
            search_value,
            search_value,
            search_value,
            search_value
        ])


    query += """
        ORDER BY s.id DESC
    """


    cursor.execute(query, params)

    salaries = cursor.fetchall()


    # =========================================================
    # CREATE CSV
    # =========================================================

    output = io.StringIO()

    writer = csv.writer(output)


    writer.writerow([
        "Employee ID",
        "Employee Name",
        "Department",
        "Salary Month",
        "Basic Salary",
        "Allowance",
        "Deduction",
        "Net Salary",
        "Payment Status",
        "Payment Date"
    ])


    for salary in salaries:

        writer.writerow([
            salary["employee_code"],

            f'{salary["first_name"]} {salary["last_name"]}',

            salary["department"] or "",

            salary["salary_month"],

            salary["basic_salary"],

            salary["allowance"],

            salary["deduction"],

            salary["net_salary"],

            salary["payment_status"],

            salary["payment_date"] or ""
        ])


    csv_data = output.getvalue()

    output.close()


    return Response(

        csv_data,

        mimetype="text/csv",

        headers={
            "Content-Disposition":
                "attachment; filename=salary_records.csv"
        }
    )

# --------- LEAVE MANAGEMENT ----------------

@app.route('/leave')
def leave_management():

    if session.get('role') != 'admin':
        return redirect('/')

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT
            lr.id,
            lr.employee_id,
            e.employee_code,
            e.first_name,
            e.last_name,
            e.email,
            d.dept_name AS department,
            lr.leave_type,
            lr.start_date,
            lr.end_date,
            lr.leave_duration,
            lr.reason,
            lr.priority,
            lr.attachment,
            lr.status,
            lr.admin_response,
            lr.applied_on
        FROM leave_requests lr
        JOIN employees e
            ON lr.employee_id = e.id
        LEFT JOIN departments d
            ON e.dept_id = d.dept_id
        ORDER BY lr.applied_on DESC
    """)

    leave_requests = cursor.fetchall()

    cursor.close()

    total_requests = len(leave_requests)

    pending_requests = sum(
        1 for leave in leave_requests
        if leave['status'] == 'Pending'
    )

    approved_requests = sum(
        1 for leave in leave_requests
        if leave['status'] == 'Approved'
    )

    rejected_requests = sum(
        1 for leave in leave_requests
        if leave['status'] == 'Rejected'
    )

    return render_template(
        'leave_management.html',
        leave_requests=leave_requests,
        total_requests=total_requests,
        pending_requests=pending_requests,
        approved_requests=approved_requests,
        rejected_requests=rejected_requests
    )

# =========================================================
# UPDATE LEAVE STATUS
# =========================================================

@app.route('/update-leave-status', methods=['POST'])
def update_leave_status():

    data = request.get_json()

    leave_id = data.get('leave_id')
    status = data.get('status')

    cursor = db.cursor()

    cursor.execute("""
        UPDATE leave_requests
        SET status=%s
        WHERE id=%s
    """, (status, leave_id))

    db.commit()

    cursor.close()

    return jsonify({
        "success": True,
        "message": f"Leave request {status.lower()} successfully."
    })

    
@app.route('/get-leave-details/<int:leave_id>')
def get_leave_details(leave_id):

    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM leave_requests
        WHERE id = %s
    """, (leave_id,))

    leave = cursor.fetchone()

    cursor.close()

    if leave:

        return jsonify({
            "success": True,
            "leave": leave
        })

    return jsonify({
        "success": False,
        "message": "Leave not found"
    })
@app.route('/save-leave-response', methods=['POST'])
def save_leave_response():

    data = request.get_json()

    leave_id = data.get('leave_id')
    remarks = data.get('remarks')

    cursor = db.cursor()

    cursor.execute("""
        UPDATE leave_requests
        SET admin_response = %s
        WHERE id = %s
    """, (remarks, leave_id))

    db.commit()

    cursor.close()

    return jsonify({
        "success": True
    })


# ---------------- EMPLOYEE DASHBOARD ----------------
@app.route('/employee-dashboard')
def employee_dashboard():

    # =====================================================
    # MAKE SURE EMPLOYEE IS LOGGED IN
    # =====================================================

    if session.get('role') != 'employee':
        return redirect('/')

    employee_id = session.get('employee_id')

    if not employee_id:
        return "Employee account is not linked to an employee record.", 404


    # =====================================================
    # EMPLOYEE INFORMATION
    # =====================================================

    cursor.execute("""
        SELECT
            e.id,
            e.employee_code,
            e.first_name,
            e.last_name,
            e.role,
            e.email,
            e.phone,
            e.join_date,
            e.birth_date,
            e.dept_id,
            d.dept_name AS department
        FROM employees e
        LEFT JOIN departments d
            ON e.dept_id = d.dept_id
        WHERE e.id = %s
    """, (employee_id,))

    employee = cursor.fetchone()

    if not employee:
        return "Employee record not found.", 404


    # =====================================================
    # CURRENT MONTH
    # =====================================================

    now = datetime.now()

    current_month = now.strftime('%Y-%m')

    month_start = now.replace(
        day=1,
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )

    if now.month == 12:

        next_month = now.replace(
            year=now.year + 1,
            month=1,
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

    else:

        next_month = now.replace(
            month=now.month + 1,
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )


    # =====================================================
    # PRESENT DAYS
    # =====================================================

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM attendance
        WHERE employee_id = %s
        AND status = 'Present'
        AND attendance_date >= %s
        AND attendance_date < %s
    """, (
        employee_id,
        month_start,
        next_month
    ))

    present_result = cursor.fetchone()

    present_days = int(
        present_result['total'] or 0
    )


    # =====================================================
    # ABSENT DAYS
    # =====================================================

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM attendance
        WHERE employee_id = %s
        AND status = 'Absent'
        AND attendance_date >= %s
        AND attendance_date < %s
    """, (
        employee_id,
        month_start,
        next_month
    ))

    absent_result = cursor.fetchone()

    absent_days = int(
        absent_result['total'] or 0
    )


    # =====================================================
    # LEAVE DAYS
    # =====================================================

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM attendance
        WHERE employee_id = %s
        AND status = 'Leave'
        AND attendance_date >= %s
        AND attendance_date < %s
    """, (
        employee_id,
        month_start,
        next_month
    ))

    leave_result = cursor.fetchone()

    leave_days = int(
        leave_result['total'] or 0
    )


    # =====================================================
    # ATTENDANCE RATE
    # =====================================================

    total_days = (
        present_days +
        absent_days +
        leave_days
    )

    if total_days > 0:

        attendance_rate = round(
            (present_days / total_days) * 100,
            2
        )

    else:

        attendance_rate = 0


    # =====================================================
    # RECENT ATTENDANCE
    # =====================================================

    cursor.execute("""
        SELECT
            attendance_date,
            status,
            check_in,
            check_out
        FROM attendance
        WHERE employee_id = %s
        ORDER BY attendance_date DESC
        LIMIT 10
    """, (employee_id,))

    recent_attendance = cursor.fetchall()


    # =====================================================
    # LATEST SALARY
    # =====================================================

    cursor.execute("""
        SELECT
            salary_month,
            basic_salary,
            allowance,
            deduction,
            net_salary,
            payment_status,
            payment_date
        FROM salary
        WHERE employee_id = %s
        ORDER BY salary_month DESC
        LIMIT 1
    """, (employee_id,))

    latest_salary = cursor.fetchone()




    # =====================================================
    # SEND DATA TO DASHBOARD
    # =====================================================

    return render_template(
        'employee_dashboard.html',

        employee=employee,

        # Attendance
        present_days=present_days,
        absent_days=absent_days,
        leave_days=leave_days,
        attendance_rate=attendance_rate,

        # Recent attendance
        recent_attendance=recent_attendance,

        # Current month
        current_month=current_month,

        # Salary
        latest_salary=latest_salary
    )
# ---------------- EMPLOYEE ATTENDANCE ----------------
@app.route('/employee-attendance')
def employee_attendance():

    # =====================================================
    # MAKE SURE EMPLOYEE IS LOGGED IN
    # =====================================================

    if session.get('role') != 'employee':
        return redirect('/')

    employee_id = session.get('employee_id')

    if not employee_id:
        return "Employee account is not linked to an employee record.", 404


    # =====================================================
    # EMPLOYEE INFORMATION
    # =====================================================

    cursor.execute("""
        SELECT
            e.id,
            e.employee_code,
            e.first_name,
            e.last_name,
            e.role,
            e.email,
            e.phone,
            e.join_date,
            e.birth_date,
            e.dept_id,
            d.dept_name AS department
        FROM employees e
        LEFT JOIN departments d
            ON e.dept_id = d.dept_id
        WHERE e.id = %s
    """, (employee_id,))

    employee = cursor.fetchone()

    if not employee:
        return "Employee record not found.", 404


    # =====================================================
    # SELECTED MONTH
    # =====================================================

    selected_month = request.args.get(
        'month',
        datetime.now().strftime('%Y-%m')
    )


    # =====================================================
    # CONVERT SELECTED MONTH TO DATE RANGE
    # =====================================================

    try:

        selected_date = datetime.strptime(
            selected_month,
            '%Y-%m'
        )

    except ValueError:

        selected_date = datetime.now()

        selected_month = selected_date.strftime('%Y-%m')


    month_start = selected_date.replace(
        day=1,
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )


    # Find first day of next month
    if selected_date.month == 12:

        next_month = selected_date.replace(
            year=selected_date.year + 1,
            month=1,
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

    else:

        next_month = selected_date.replace(
            month=selected_date.month + 1,
            day=1,
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )


    # =====================================================
    # ATTENDANCE RECORDS
    # =====================================================

    cursor.execute("""
        SELECT
            attendance_date,
            status,
            check_in,
            check_out
        FROM attendance
        WHERE employee_id = %s
        AND attendance_date >= %s
        AND attendance_date < %s
        ORDER BY attendance_date DESC
    """, (
        employee_id,
        month_start,
        next_month
    ))

    attendance_records = cursor.fetchall()


    # =====================================================
    # PRESENT COUNT
    # =====================================================

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM attendance
        WHERE employee_id = %s
        AND status = 'Present'
        AND attendance_date >= %s
        AND attendance_date < %s
    """, (
        employee_id,
        month_start,
        next_month
    ))

    present_result = cursor.fetchone()

    present_count = int(
        present_result['total'] or 0
    )


    # =====================================================
    # ABSENT COUNT
    # =====================================================

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM attendance
        WHERE employee_id = %s
        AND status = 'Absent'
        AND attendance_date >= %s
        AND attendance_date < %s
    """, (
        employee_id,
        month_start,
        next_month
    ))

    absent_result = cursor.fetchone()

    absent_count = int(
        absent_result['total'] or 0
    )


    # =====================================================
    # LEAVE COUNT
    # =====================================================

    cursor.execute("""
        SELECT COUNT(*) AS total
        FROM attendance
        WHERE employee_id = %s
        AND status = 'Leave'
        AND attendance_date >= %s
        AND attendance_date < %s
    """, (
        employee_id,
        month_start,
        next_month
    ))

    leave_result = cursor.fetchone()

    leave_count = int(
        leave_result['total'] or 0
    )


    # =====================================================
    # ATTENDANCE RATE
    # =====================================================

    total = (
        present_count +
        absent_count +
        leave_count
    )

    if total > 0:

        attendance_rate = round(
            (present_count / total) * 100,
            2
        )

    else:

        attendance_rate = 0




    # =====================================================
    # SEND DATA TO ATTENDANCE PAGE
    # =====================================================

    return render_template(
        'employee_attendance.html',

        employee=employee,

        selected_month=selected_month,

        present_count=present_count,

        absent_count=absent_count,

        leave_count=leave_count,

        attendance_rate=attendance_rate,

        attendance_records=attendance_records
    )
# ---------------- EMPLOYEE SALARY ----------------
@app.route('/employee-salary')
def employee_salary():

    # =====================================================
    # CHECK EMPLOYEE LOGIN
    # =====================================================

    if session.get('role') != 'employee':
        return redirect('/')

    employee_id = session.get('employee_id')

    if not employee_id:
        return "Employee account is not linked to an employee record.", 404


    # =====================================================
    # EMPLOYEE INFORMATION
    # =====================================================

    cursor.execute("""
        SELECT
            e.id,
            e.employee_code,
            e.first_name,
            e.last_name,
            e.role,
            e.email,
            e.phone,
            e.join_date,
            e.birth_date,
            e.dept_id,
            d.dept_name AS department
        FROM employees e
        LEFT JOIN departments d
            ON e.dept_id = d.dept_id
        WHERE e.id = %s
    """, (employee_id,))

    employee = cursor.fetchone()

    if not employee:
        return "Employee record not found.", 404


    # =====================================================
    # GET ALL SALARY RECORDS
    # =====================================================

    cursor.execute("""
        SELECT
            id,
            employee_id,
            salary_month,
            basic_salary,
            allowance,
            deduction,
            net_salary,
            payment_status,
            payment_date,
            notes
        FROM salary
        WHERE employee_id = %s
        ORDER BY salary_month DESC
    """, (employee_id,))

    salary_records = cursor.fetchall()


    # =====================================================
    # CHECK IF USER SELECTED A MONTH
    # =====================================================

    selected_month = request.args.get('month')


    # =====================================================
    # NO MONTH SELECTED
    # SHOW LATEST SALARY
    # =====================================================

    if not selected_month:

        if salary_records:
            latest_salary = salary_records[0]

            selected_month = latest_salary['salary_month'].strftime('%Y-%m')

        else:
            latest_salary = None

            selected_month = datetime.now().strftime('%Y-%m')


    # =====================================================
    # MONTH SELECTED
    # GET SALARY FOR THAT MONTH
    # =====================================================

    else:

        cursor.execute("""
            SELECT
                id,
                employee_id,
                salary_month,
                basic_salary,
                allowance,
                deduction,
                net_salary,
                payment_status,
                payment_date,
                notes
            FROM salary
            WHERE employee_id = %s
            AND salary_month >= %s
            AND salary_month < DATE_ADD(%s, INTERVAL 1 MONTH)
            ORDER BY salary_month DESC
            LIMIT 1
        """, (
            employee_id,
            selected_month + '-01',
            selected_month + '-01'
        ))

        latest_salary = cursor.fetchone()






    # =====================================================
    # SEND TO HTML
    # =====================================================

    return render_template(
        'employee_salary.html',

        employee=employee,

        salary_records=salary_records,

        latest_salary=latest_salary,

        selected_month=selected_month
    )

# =========================================================
# EMPLOYEE LEAVE REQUEST
# =========================================================

@app.route('/employee-leave')
def employee_leave():

    # Make sure employee is logged in
    if session.get('role') != 'employee':
        return redirect('/')

    employee_id = session.get('employee_id')

    if not employee_id:
        return "Employee account is not linked."

    cursor = db.cursor(dictionary=True)

    # -----------------------------------------------------
    # GET EMPLOYEE DETAILS
    # -----------------------------------------------------

    cursor.execute("""
        SELECT
            e.id,
            e.employee_code,
            e.first_name,
            e.last_name,
            e.role,
            e.email,
            e.phone,
            e.join_date,
            d.dept_name AS department
        FROM employees e
        LEFT JOIN departments d
            ON e.dept_id = d.dept_id
        WHERE e.id = %s
    """, (employee_id,))

    employee = cursor.fetchone()

    if not employee:
        cursor.close()
        return "Employee not found."

    # -----------------------------------------------------
    # GET LEAVE REQUESTS
    # -----------------------------------------------------

    cursor.execute("""
        SELECT *
        FROM leave_requests
        WHERE employee_id = %s
        ORDER BY applied_on DESC
    """, (employee_id,))

    leave_requests = cursor.fetchall()

    cursor.close()

    # -----------------------------------------------------
    # STATS
    # -----------------------------------------------------

    total_requests = len(leave_requests)

    approved_requests = sum(
        1 for leave in leave_requests
        if leave.get('status') == 'Approved'
    )

    pending_requests = sum(
        1 for leave in leave_requests
        if leave.get('status') == 'Pending'
    )

    rejected_requests = sum(
        1 for leave in leave_requests
        if leave.get('status') == 'Rejected'
    )

    # -----------------------------------------------------
    # RENDER PAGE
    # -----------------------------------------------------

    return render_template(
        'employee_leave.html',

        employee=employee,

        leave_requests=leave_requests,

        total_requests=total_requests,
        approved_requests=approved_requests,
        pending_requests=pending_requests,
        rejected_requests=rejected_requests
    )

# =========================================================
# SUBMIT EMPLOYEE LEAVE REQUEST
# =========================================================

@app.route('/submit-leave', methods=['POST'])
def submit_leave():

    # Make sure employee is logged in
    if session.get('role') != 'employee':
        return redirect('/')

    employee_id = session.get('employee_id')

    if not employee_id:
        return "Employee account is not linked."

    # -----------------------------------------------------
    # GET FORM DATA
    # -----------------------------------------------------

    leave_type = request.form.get('leave_type')
    priority = request.form.get('priority')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    leave_duration = request.form.get('leave_duration', 0)
    reason = request.form.get('reason')

    # -----------------------------------------------------
    # GET ATTACHMENT
    # -----------------------------------------------------

    attachment = request.files.get('attachment')

    filename = None

    if attachment and attachment.filename:

        filename = secure_filename(attachment.filename)

        upload_folder = os.path.join(
            app.root_path,
            'static',
            'uploads'
        )

        # Create uploads folder if it doesn't exist
        os.makedirs(upload_folder, exist_ok=True)

        # Save uploaded file
        attachment.save(
            os.path.join(upload_folder, filename)
        )

    # -----------------------------------------------------
    # INSERT LEAVE REQUEST
    # -----------------------------------------------------

    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO leave_requests
        (
            employee_id,
            leave_type,
            priority,
            start_date,
            end_date,
            leave_duration,
            reason,
            attachment,
            status
        )
        VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, 'Pending')
    """, (
        employee_id,
        leave_type,
        priority,
        start_date,
        end_date,
        leave_duration,
        reason,
        filename
    ))

    db.commit()

    cursor.close()

    return redirect('/employee-leave')


# ---------------- RUN APP ----------------
if __name__ == '__main__':
 app.run(host="0.0.0.0",port=5000,debug=True)

