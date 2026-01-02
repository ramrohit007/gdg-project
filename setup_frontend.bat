@echo off
echo Setting up frontend...
cd frontend

echo Installing dependencies...
call npm install

echo.
echo Frontend setup complete!
echo To start the development server, run: npm run dev
pause

