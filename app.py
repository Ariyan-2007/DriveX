from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask import session

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/drivex'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    license = db.Column(db.String(50), nullable=True)
    nid = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    employee_id = db.Column(db.String(50), unique=True, nullable=False)
    position = db.Column(db.String(100), nullable=False)
    nid = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    admin_id = db.Column(db.String(50), unique=True, nullable=False)
    position = db.Column(db.String(100), nullable=False)
    nid = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(200), nullable=False)

# Initialize database tables
app.app_context().push()

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        nid = request.form['nid']
        password = generate_password_hash(request.form['password'])

        role = request.form['registration_type']
        if role == 'user':
            license = request.form['license']
            new_user = User(name=name, email=email, license=license, nid=nid, password=password)
            db.session.add(new_user)
        elif role == 'employee':
            employee_id = request.form['employee_id']
            position = request.form['e_position']
            new_employee = Employee(name=name,email=email, employee_id=employee_id, position=position, nid=nid, password=password)
            db.session.add(new_employee)
        elif role == 'admin':
            admin_id = request.form['admin_id']
            position = request.form['a_position']
            new_admin = Admin(name=name,email=email, admin_id=admin_id, position=position, nid=nid, password=password)
            db.session.add(new_admin)
        
        db.session.commit()
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']

        if role == 'user':
            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                session['username'] = user.name
                flash('Login successful!', 'success')
                return redirect(url_for('user_dashboard'))
    
        elif role == 'employee':
            employee = Employee.query.filter_by(email=email).first()  
            if employee and check_password_hash(employee.password, password):
                flash('Login successful!', 'success')
                return redirect(url_for('home'))
    
        elif role == 'admin':
            admin = Admin.query.filter_by(email=email).first()  
            if admin and check_password_hash(admin.password, password):
                flash('Login successful!', 'success')
                return redirect(url_for('home'))

        flash('Invalid credentials or role mismatch. Please try again.', 'danger')
        return redirect(url_for('login'))        
        
    return render_template('login.html')

# Route Page
@app.route('/route', methods=['GET'])
def route():
    pickup = request.args.get('pickup', '')
    dropoff = request.args.get('dropoff', '')
    return render_template('route.html', pickup=pickup, dropoff=dropoff)


#user_dashboard
@app.route('/user_dashboard')
def user_dashboard():
    username = session.get('username', 'Guest') 
    return render_template('user_dashboard.html', username=username)

if __name__ == '__main__':
    app.run(debug=True)
