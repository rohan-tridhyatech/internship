from app import db, app
from app import Role

# Function to add default data
def add_default_roles():
    default_roles = [
    "Software Developer",
    "System Administrator",
    "DevOps Engineer",
    "Quality Assurance (QA) Engineer",
    "Data Scientist/Analyst",
    "IT Support Specialist",
    "Project Manager",
    "Cybersecurity Specialist",
    "UI/UX Designer",
    "Human Executive",
    "Cloud Architect",
    "Business Analyst",
    "Database Administrator (DBA)",
    "Product Manager",
    "Network Engineer",
    "Marketing Executive"
]


    for role_name in default_roles:
        # Check if the role already exists to avoid duplicates
        existing_role = Role.query.filter_by(role_name = role_name).first()
        if not existing_role:
            new_role = Role(role_name=role_name)
            db.session.add(new_role)

    db.session.commit()
    print("Default roles added successfully!")

if __name__ == "__main__":
    with app.app_context():
        add_default_roles()
