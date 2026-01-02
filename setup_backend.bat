@echo off
echo Setting up backend...
cd backend

echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Please create a .env file in the backend directory with the following content:
echo DATABASE_URL=postgresql://postgres:postgres@localhost:5432/student_performance
echo SECRET_KEY=your-secret-key-change-in-production
echo OPENAI_API_KEY=your-openai-api-key-here
echo.
pause

echo Initializing database...
python init_db.py

echo.
echo Backend setup complete!
echo To start the server, run: uvicorn main:app --reload
pause

