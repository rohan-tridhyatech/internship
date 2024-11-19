from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///user.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# *****************************  DATA TABLES (MODELS)  *****************************
# Association table to link users and roles
user_roles = db.Table('user_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id', ondelete="CASCADE"), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.role_id', ondelete="CASCADE"), primary_key=True)
)

# Define the Role model
class Role(db.Model):
    role_id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(50), nullable=False)

    # One-to-many relationship: One role can be assigned to multiple users
    user = db.relationship('User',secondary=user_roles, backref=db.backref('roles_assigned', lazy=True))

    def __repr__(self):
        return f"{self.role_id} - {self.role_name}"

    def to_dict(self):
        return {
            "role_id": self.role_id,
            "role_name": self.role_name
        }

# Define the User model
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(10), nullable=False)

    roles = db.relationship('Role', secondary=user_roles, backref=db.backref('users_with_role', lazy=True))

    def __repr__(self):
        return f"{self.user_id} - {self.name}"

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
            "gender": self.gender,
            "roles": [role.role_name for role in self.roles]  # Return role names as list
        }



# *****************************  PROFILE APIs  *****************************
# Create User
@app.route("/profile", methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get('name')
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
    new_user = User(name=name, email=email, gender=gender)
    for role in selected_roles:
        new_user.roles.append(role)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "User could not be registered: " + str(e)}), 500

# View All Users
@app.route("/profile", methods=['GET'])
def view_users():
    all_users = User.query.all()
    users_data = [user.to_dict() for user in all_users]
    return jsonify({"users": users_data})

# View Single User through User ID
@app.route("/profile/<int:user_id>", methods=['GET'])
def view_user_details(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({"user": user.to_dict()})
    else:
        return jsonify({"error": "User not found"}), 404

# Update User
@app.route("/profile/<int:user_id>", methods=['PUT'])
def edit_user(user_id):
    user = User.query.get(user_id)
    if user:
        data = request.get_json()
        user.name = data.get('name', user.name)
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

# Delete User
@app.route("/profile/<int:user_id>", methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        try:
            # Clear relationships in the association table
            user.roles.clear()
            db.session.commit()

            # Delete the user
            db.session.delete(user)
            db.session.commit()
            return jsonify({"message": "User deleted successfully!"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Could not delete user: " + str(e)}), 500
    else:
        return jsonify({"error": "User not found"}), 404


# *****************************  ROLES APIs  *****************************
# Create Role
@app.route("/roles", methods=['POST'])
def create_role():
    data = request.get_json()
    role_name = data.get('role_name')

    # Check if role already exists
    existing_role = Role.query.filter_by(role_name = role_name).first()
    if existing_role:
        return jsonify({"error": "Role already exists"}), 400

    # Create a new role
    new_role = Role(role_name=role_name)
    try:
        db.session.add(new_role)
        db.session.commit()
        return jsonify({"message": "Role created successfully!"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Role could not be created: " + str(e)}), 500

# View All Roles
@app.route("/roles", methods=['GET'])
def view_roles():
    all_roles = Role.query.all()
    role_data = [role.to_dict() for role in all_roles]
    return jsonify({"roles": role_data})

# View Single Role through Role ID
@app.route("/roles/<int:role_id>", methods=['GET'])
def view_role_details(role_id):
    role = Role.query.get(role_id)
    if role:
        return jsonify({"role": role.to_dict()})
    else:
        return jsonify({"error": "Role not found"}), 404

# Update Role
@app.route("/roles/<int:role_id>", methods=['PUT'])
def update_role(role_id):
    role = Role.query.get(role_id)
    if role:
        data = request.get_json()
        role.role_name = data.get('role_name', role.role_name)

        try:
            db.session.commit()
            return jsonify({"message": "Role updated successfully!"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Could not update role: " + str(e)}), 500
    else:
        return jsonify({"error": "Role not found"}), 404

# Delete Role
@app.route("/roles/<int:role_id>", methods=['DELETE'])
def delete_role(role_id):
    role = Role.query.get(role_id)
    if role:
        try:
            # Clear relationships in the association table
            for user in role.users_with_role:
                user.roles.remove(role)

            db.session.commit()

            # Delete the role
            db.session.delete(role)
            db.session.commit()
            return jsonify({"message": "Role deleted successfully!"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Could not delete role: " + str(e)}), 500
    else:
        return jsonify({"error": "Role not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)
