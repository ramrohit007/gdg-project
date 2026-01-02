# Backend - Student Performance Analyzer

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up PostgreSQL database:
- Create a database named `student_performance`
- Update `DATABASE_URL` in `.env` file

3. Create `.env` file:
```bash
cp .env.example .env
# Edit .env with your database credentials and OpenAI API key
```

4. Initialize database with demo accounts:
```bash
python init_db.py
```

5. Run the server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

- `POST /api/auth/login` - Login for students and teachers
- `POST /api/teacher/generate-code` - Generate student login code
- `GET /api/teacher/current-code` - Get current active code
- `POST /api/teacher/upload-syllabus` - Upload syllabus PDF
- `GET /api/teacher/analytics` - Get analytics data
- `POST /api/student/upload-answer` - Upload answer sheet PDF

## Demo Accounts

- Teacher: username: `teacher`, password: `teacher123`
- Students: username: `student1`, `student2`, `student3`, password: `student123`

