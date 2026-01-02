from pydantic import BaseModel
from typing import Optional, List

class UserLogin(BaseModel):
    username: str
    password: str
    code: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    role: str
    token: str

class CodeResponse(BaseModel):
    code: str
    expires_at: str

class SyllabusUpload(BaseModel):
    message: str
    topics: List[str]

class AnswerUpload(BaseModel):
    message: str
    scores: dict

class TopicScore(BaseModel):
    student_id: int
    student_name: str
    score: float

class TopicAnalytics(BaseModel):
    topic_id: int
    topic_name: str
    student_scores: List[TopicScore]

class AnalyticsResponse(BaseModel):
    topics: List[TopicAnalytics]

