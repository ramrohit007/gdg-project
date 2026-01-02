from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)  # "student" or "teacher"
    created_at = Column(DateTime, default=datetime.utcnow)

class LoginCode(Base):
    __tablename__ = "login_codes"
    
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    is_active = Column(Boolean, default=True)

class Syllabus(Base):
    __tablename__ = "syllabus"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    content = Column(Text)
    uploaded_by = Column(Integer, ForeignKey("users.id"))
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    topics = relationship("Topic", back_populates="syllabus")

class Topic(Base):
    __tablename__ = "topics"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    syllabus_id = Column(Integer, ForeignKey("syllabus.id"))
    
    syllabus = relationship("Syllabus", back_populates="topics")
    scores = relationship("StudentTopicScore", back_populates="topic")

class AnswerSheet(Base):
    __tablename__ = "answer_sheets"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    content = Column(Text)
    student_id = Column(Integer, ForeignKey("users.id"))
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    scores = relationship("StudentTopicScore", back_populates="answer_sheet")

class StudentTopicScore(Base):
    __tablename__ = "student_topic_scores"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    topic_id = Column(Integer, ForeignKey("topics.id"))
    answer_sheet_id = Column(Integer, ForeignKey("answer_sheets.id"))
    score = Column(Float)  # 0-100 percentage
    created_at = Column(DateTime, default=datetime.utcnow)
    
    topic = relationship("Topic", back_populates="scores")
    answer_sheet = relationship("AnswerSheet", back_populates="scores")

