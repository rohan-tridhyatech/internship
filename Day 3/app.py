from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Association table to link users and roles
user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id', ondelete='CASCADE'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.role_id', ondelete='CASCADE'), primary_key=True)
)

# Define the Role model    
class Role(db.Model):
    role_id = db.Column(db.Integer, primary_key=True) 
    role_name = db.Column(db.String(50), nullable=False)

    # One-to-many relationship: One role can be assigned to multiple users
    user = db.relationship('User',secondary=user_roles, backref=db.backref('roles_assigned', lazy=True))  

    def __repr__(self):
        return f"{self.role_id} - {self.role_name}"

# Define the User model
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    
    roles = db.relationship('Role', secondary=user_roles, backref=db.backref('users_with_role', lazy=True))


    def __repr__(self):
        return f"{self.user_id} - {self.full_name}"

# Function to get user by ID
def get_user_by_id(user_id):
    user = User.query.get(user_id)  # SQLAlchemy query
    return user

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/register", methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        # Extract data from form submission
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        gender = request.form.get('gender')
        selected_role_names = request.form.getlist('role_name')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"error": "Email already in use"}), 400

        selected_roles = Role.query.filter(Role.role_name.in_(selected_role_names)).all()

        # Create a new user instance
        new_user = User(full_name=full_name, email=email, gender=gender)
        for role in selected_roles:
            new_user.roles_assigned.append(role)

        try:
            db.session.add(new_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "User could not be registered. " + str(e)}), 500
    return render_template("register.html", roles=Role.query.all())

@app.route("/view")
def view_user():
    # Retrieve all users with their associated roles
    all_users = User.query.all()

    # Iterate over the users to gather user data along with their roles
    users_with_roles = []
    for user in all_users:
        roles = [role.role_name for role in user.roles]  # Get role names for each user
        users_with_roles.append({
            "user_id":user.user_id,
            "full_name": user.full_name,
            "email": user.email,
            "gender": user.gender,
            "roles": roles  # List of role names
        })

    return render_template("view.html",  users_with_roles=users_with_roles)

@app.route('/view_user/<user_id>')
def view_user_details(user_id):
    user = get_user_by_id(user_id)
    if user:
        return render_template('view_user.html', user=user)
    else:
        return "User not found", 404
    
@app.route("/update/<int:user_id>", methods=['GET', 'POST'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        # Get updated data from form submission
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        gender = request.form.get('gender')
        selected_role_names = request.form.getlist('role_name')

        # Check if the email is already used by another user
        existing_user = User.query.filter_by(email=email).first()
        if existing_user and existing_user.user_id != user_id:
            return jsonify({"error": "Email already in use by another user"}), 400

        # Update user fields
        user.full_name = full_name
        user.email = email
        user.gender = gender

        # Clear existing roles and assign new ones
        user.roles.clear()  # Clear the existing roles
        selected_roles = Role.query.filter(Role.role_name.in_(selected_role_names)).all()
        for role in selected_roles:
            user.roles.append(role)

        try:
            db.session.commit()
            return jsonify({"success": "User updated successfully"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "User could not be updated. " + str(e)}), 500

    return render_template("update.html", user=user, roles=Role.query.all())
            
@app.route("/delete/<int:user_id>", methods=['GET', 'POST'])
def delete_user(user_id):
    # Fetch the user by ID
    user = User.query.get_or_404(user_id)
    if user:
        try:
            # Before deleting the user, let's clear any roles assigned to avoid issues with foreign key constraints
            user.roles.clear()
            db.session.commit()

            # Now delete the user from the database
            db.session.delete(user)
            db.session.commit()

            # Return a success message
            return jsonify({"success": f"User with ID {user_id} has been deleted successfully."}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"An error occurred while deleting the user. {str(e)}"}), 500

    return render_template("delete.html", user=user)

if __name__ == "__main__":
    app.run(debug=True)

  