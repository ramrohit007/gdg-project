# Student Performance Analyzer

A comprehensive tool for analyzing student performance and understanding of topics using AI-powered analysis of exam answer sheets.

## Features

- **Authentication System**: Separate login for students and teachers with demo accounts
- **Student Login Codes**: Teachers can generate time-limited codes (1 hour validity) for student access
- **PDF Processing**: Converts PDF answer sheets and syllabus to text
- **AI-Powered Analysis**: Uses AI to extract topics from syllabus and analyze student answers
- **Performance Analytics**: Visual bar graphs showing student understanding per topic
- **Database Storage**: PostgreSQL database for storing all data

## Tech Stack

### Backend
- FastAPI (Python)
- PostgreSQL
- SQLAlchemy (ORM)
- OpenAI API (for AI analysis)
- PDF processing libraries (pdfplumber, PyPDF2)

### Frontend
- React 18
- TypeScript
- Vite
- React Router
- Axios
- Recharts (for visualizations)

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL database

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Set up PostgreSQL database:
- Create a database named `student_performance`
- Update `DATABASE_URL` in `.env` file

4. Create `.env` file:
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/student_performance
SECRET_KEY=your-secret-key-change-in-production
OPENAI_API_KEY=your-openai-api-key-here
```

5. Initialize database with demo accounts:
```bash
python init_db.py
```

6. Run the backend server:
```bash
uvicorn main:app --reload
```

Backend will run on `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```

Frontend will run on `http://localhost:3000`

## Demo Accounts

### Teacher
- Username: `teacher`
- Password: `teacher123`

### Students
- Username: `student1`, `student2`, or `student3`
- Password: `student123`

## Usage

1. **Teacher Login**:
   - Login with teacher credentials
   - Generate a login code for students (valid for 1 hour)
   - Upload syllabus PDF (topics will be automatically extracted)
   - View analytics dashboard with student performance

2. **Student Login**:
   - Get login code from teacher
   - Login with student credentials and the code
   - Upload answer sheet PDF
   - View your topic scores

## API Endpoints

- `POST /api/auth/login` - Login
- `POST /api/teacher/generate-code` - Generate student login code
- `GET /api/teacher/current-code` - Get current active code
- `POST /api/teacher/upload-syllabus` - Upload syllabus PDF
- `GET /api/teacher/analytics` - Get analytics data
- `POST /api/student/upload-answer` - Upload answer sheet PDF

## Project Structure

```
gdg1/
├── backend/
│   ├── main.py              # FastAPI application
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── auth.py              # Authentication utilities
│   ├── pdf_processor.py     # PDF to text conversion
│   ├── ai_analyzer.py       # AI analysis functions
│   ├── init_db.py           # Database initialization
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── pages/           # Page components
│   │   ├── components/      # Reusable components
│   │   ├── context/         # React context
│   │   └── App.tsx          # Main app component
│   ├── package.json
│   └── vite.config.ts
└── README.md
```

## Notes

- The AI analyzer uses OpenAI API. If no API key is provided, it will use mock responses for development.
- PDF files are temporarily stored during processing and then deleted.
- Login codes expire after 1 hour.
- The system supports multiple answer sheet uploads per student (latest scores are used).

