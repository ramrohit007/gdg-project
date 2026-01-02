from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import List, Optional
import os
from datetime import datetime, timedelta
import uuid

from database import SessionLocal, engine, Base
from models import User, LoginCode, Syllabus, AnswerSheet, Topic, StudentTopicScore
from schemas import (
    UserLogin, UserResponse, CodeResponse, 
    SyllabusUpload, AnswerUpload, AnalyticsResponse
)
from auth import verify_password, get_password_hash, create_access_token, verify_token
from pdf_processor import PDFProcessor
from ai_analyzer import AIAnalyzer

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Performance Analyzer")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency to get current user
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = db.query(User).filter(User.id == payload.get("user_id")).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# Initialize processors
pdf_processor = PDFProcessor()
ai_analyzer = AIAnalyzer()

@app.get("/")
def root():
    return {"message": "Student Performance Analyzer API"}

@app.post("/api/auth/login", response_model=UserResponse)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """Login endpoint for students and teachers"""
    user = db.query(User).filter(User.username == user_data.username).first()
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if user.role == "student":
        # For students, check if they provided a valid code
        if not user_data.code:
            raise HTTPException(status_code=401, detail="Code required for student login")
        
        code_obj = db.query(LoginCode).filter(
            LoginCode.code == user_data.code,
            LoginCode.is_active == True,
            LoginCode.expires_at > datetime.utcnow()
        ).first()
        
        if not code_obj:
            raise HTTPException(status_code=401, detail="Invalid or expired code")
    
    if not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"user_id": user.id, "role": user.role})
    
    return {
        "id": user.id,
        "username": user.username,
        "role": user.role,
        "token": token
    }

@app.post("/api/teacher/generate-code", response_model=CodeResponse)
def generate_code(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Generate a unique login code for students (valid for 1 hour)"""
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can generate codes")
    
    # Deactivate old codes
    db.query(LoginCode).filter(LoginCode.is_active == True).update({"is_active": False})
    
    # Generate new code
    code = str(uuid.uuid4())[:8].upper()
    expires_at = datetime.utcnow() + timedelta(hours=1)
    
    login_code = LoginCode(
        code=code,
        created_by=current_user.id,
        expires_at=expires_at,
        is_active=True
    )
    
    db.add(login_code)
    db.commit()
    db.refresh(login_code)
    
    return {"code": code, "expires_at": expires_at.isoformat()}

@app.get("/api/teacher/current-code", response_model=Optional[CodeResponse])
def get_current_code(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get the current active code"""
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can view codes")
    
    code_obj = db.query(LoginCode).filter(
        LoginCode.is_active == True,
        LoginCode.expires_at > datetime.utcnow()
    ).first()
    
    if code_obj:
        return {"code": code_obj.code, "expires_at": code_obj.expires_at.isoformat()}
    return None

@app.post("/api/teacher/upload-syllabus")
def upload_syllabus(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload syllabus PDF and extract topics"""
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can upload syllabus")
    
    # Save file temporarily
    os.makedirs("uploads", exist_ok=True)
    file_path = f"uploads/syllabus_{datetime.utcnow().timestamp()}.pdf"
    
    with open(file_path, "wb") as f:
        content = file.file.read()
        f.write(content)
    
    try:
        # Convert PDF to text
        text = pdf_processor.pdf_to_text(file_path)
        
        # Extract topics using AI
        topics = ai_analyzer.extract_topics_from_syllabus(text)
        
        # Clear old syllabus and topics
        db.query(Topic).delete()
        db.query(Syllabus).delete()
        
        # Save syllabus
        syllabus = Syllabus(
            filename=file.filename,
            content=text,
            uploaded_by=current_user.id
        )
        db.add(syllabus)
        db.commit()
        db.refresh(syllabus)
        
        # Save topics
        for topic_name in topics:
            topic = Topic(name=topic_name, syllabus_id=syllabus.id)
            db.add(topic)
        
        db.commit()
        
        # Clean up file
        os.remove(file_path)
        
        return {"message": "Syllabus uploaded successfully", "topics": topics}
    
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Error processing syllabus: {str(e)}")

@app.post("/api/student/upload-answer")
def upload_answer(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Upload answer sheet PDF and analyze"""
    if current_user.role != "student":
        raise HTTPException(status_code=403, detail="Only students can upload answers")
    
    # Check if syllabus exists
    syllabus = db.query(Syllabus).first()
    if not syllabus:
        raise HTTPException(status_code=400, detail="No syllabus uploaded yet")
    
    # Save file temporarily
    os.makedirs("uploads", exist_ok=True)
    file_path = f"uploads/answer_{current_user.id}_{datetime.utcnow().timestamp()}.pdf"
    
    with open(file_path, "wb") as f:
        content = file.file.read()
        f.write(content)
    
    try:
        # Convert PDF to text
        text = pdf_processor.pdf_to_text(file_path)
        
        # Get topics
        topics = db.query(Topic).all()
        topic_names = [t.name for t in topics]
        
        # Analyze answer using AI
        topic_scores = ai_analyzer.analyze_answer_sheet(text, topic_names)
        
        # Save answer sheet
        answer_sheet = AnswerSheet(
            filename=file.filename,
            content=text,
            student_id=current_user.id
        )
        db.add(answer_sheet)
        db.commit()
        db.refresh(answer_sheet)
        
        # Save topic scores
        for topic_name, score in topic_scores.items():
            topic = db.query(Topic).filter(Topic.name == topic_name).first()
            if topic:
                # Delete old score if exists
                db.query(StudentTopicScore).filter(
                    StudentTopicScore.student_id == current_user.id,
                    StudentTopicScore.topic_id == topic.id
                ).delete()
                
                score_obj = StudentTopicScore(
                    student_id=current_user.id,
                    topic_id=topic.id,
                    answer_sheet_id=answer_sheet.id,
                    score=score
                )
                db.add(score_obj)
        
        db.commit()
        
        # Clean up file
        os.remove(file_path)
        
        return {"message": "Answer sheet uploaded and analyzed successfully"}
    
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Error processing answer sheet: {str(e)}")

@app.get("/api/teacher/analytics", response_model=AnalyticsResponse)
def get_analytics(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Get analytics for teacher dashboard - returns average scores per topic"""
    if current_user.role != "teacher":
        raise HTTPException(status_code=403, detail="Only teachers can view analytics")
    
    # Get all topics
    topics = db.query(Topic).all()
    
    # Get all students
    students = db.query(User).filter(User.role == "student").all()
    
    # Calculate average scores per topic
    topic_averages = []
    
    for topic in topics:
        # Get all scores for this topic from all students
        scores = []
        for student in students:
            score_obj = db.query(StudentTopicScore).filter(
                StudentTopicScore.student_id == student.id,
                StudentTopicScore.topic_id == topic.id
            ).order_by(StudentTopicScore.id.desc()).first()
            
            if score_obj:
                scores.append(score_obj.score)
        
        # Calculate average
        if scores:
            average_score = sum(scores) / len(scores)
        else:
            average_score = 0.0
        
        topic_averages.append({
            "topic_id": topic.id,
            "topic_name": topic.name,
            "average_score": round(average_score, 2)
        })
    
    return {"topic_averages": topic_averages}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

