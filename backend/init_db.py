"""Initialize database with demo accounts"""
from database import SessionLocal, engine, Base
from models import User
from auth import get_password_hash

# Create tables
Base.metadata.create_all(bind=engine)

def init_demo_accounts():
    db = SessionLocal()
    
    try:
        # Check if users already exist
        if db.query(User).count() > 0:
            print("Demo accounts already exist. Skipping initialization.")
            return
        
        # Create teacher account
        teacher = User(
            username="teacher",
            hashed_password=get_password_hash("teacher123"),
            role="teacher"
        )
        db.add(teacher)
        
        # Create student accounts
        students = [
            {"username": "student1", "password": "student123"},
            {"username": "student2", "password": "student123"},
            {"username": "student3", "password": "student123"}
        ]
        
        for student_data in students:
            student = User(
                username=student_data["username"],
                hashed_password=get_password_hash(student_data["password"]),
                role="student"
            )
            db.add(student)
        
        db.commit()
        print("Demo accounts created successfully!")
        print("\nLogin credentials:")
        print("Teacher - Username: teacher, Password: teacher123")
        print("Students - Username: student1/student2/student3, Password: student123")
        
    except Exception as e:
        print(f"Error creating demo accounts: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_demo_accounts()

