import sys
from app import create_app, db
from app.models import User

app = create_app()

def delete_user(identifier: str):
    """
    Deletes a user based on their phone number, email, or ID.
    """
    with app.app_context():
        # Try to find the user by phone or email
        user = User.query.filter(
            (User.phone == identifier) | 
            (User.email == identifier)
        ).first()

        # If not found by phone or email, try by ID if it's an integer
        if not user and identifier.isdigit():
            user = User.query.get(int(identifier))

        if user:
            print(f"Found user: {user.full_name} (Phone: {user.phone}, Email: {user.email})")
            try:
                db.session.delete(user)
                db.session.commit()
                print(f"User '{identifier}' deleted successfully.")
            except Exception as e:
                db.session.rollback()
                print(f"Failed to delete user '{identifier}'. Error: {e}")
        else:
            print(f"User '{identifier}' not found.")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python seed.py <phone_number_or_email_or_id>")
        print("Example: python seed.py user@example.com")
        print("Example: python seed.py 9876543210")
        sys.exit(1)

    user_identifier = sys.argv[1]
    delete_user(user_identifier)
