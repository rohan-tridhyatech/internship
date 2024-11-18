from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Association table to link users and roles
user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.role_id'), primary_key=True)
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

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "full_name": self.full_name,
            "email": self.email,
            "gender": self.gender,
            "roles": [role.role_name for role in self.roles]  # Return role names as list
        }

@app.route("/")
def home():
    return jsonify({"message": "Welcome to the User API"})

@app.route("/register", methods=['POST'])
def register_user():
    data = request.get_json()
    full_name = data.get('full_name')
    email = data.get('email')
    gender = data.get('gender')
    selected_role_names = data.get('role_names', [])  # Expected list of role names

    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "Email already in use"}), 400

    # Get roles from the database based on role names
    selected_roles = Role.query.filter(Role.role_name.in_(selected_role_names)).all()

    # Create new user
    new_user = User(full_name=full_name, email=email, gender=gender)
    for role in selected_roles:
        new_user.roles.append(role)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "User could not be registered: " + str(e)}), 500

@app.route("/view", methods=['GET'])
def view_users():
    all_users = User.query.all()
    users_data = [user.to_dict() for user in all_users]
    return jsonify({"users": users_data})

@app.route("/view_user/<int:user_id>", methods=['GET'])
def view_user_details(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({"user": user.to_dict()})
    else:
        return jsonify({"error": "User not found"}), 404

@app.route("/edit_user/<int:user_id>", methods=['PUT'])
def edit_user(user_id):
    user = User.query.get(user_id)
    if user:
        data = request.get_json()
        user.full_name = data.get('full_name', user.full_name)
        user.email = data.get('email', user.email)
        user.gender = data.get('gender', user.gender)
        
        # Update roles if provided
        selected_role_names = data.get('role_names', [])
        selected_roles = Role.query.filter(Role.role_name.in_(selected_role_names)).all()
        user.roles = selected_roles

        try:
            db.session.commit()
            return jsonify({"message": "User updated successfully!"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Could not update user: " + str(e)}), 500
    else:
        return jsonify({"error": "User not found"}), 404

@app.route("/delete_user/<int:user_id>", methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        try:
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message": "User deleted successfully!"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Could not delete user: " + str(e)}), 500
    else:
        return jsonify({"error": "User not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
