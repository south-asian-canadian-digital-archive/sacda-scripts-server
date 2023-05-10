echo "Starting app"
npx kill-port 8000 && npx kill-port 3000
cd backend && /bin/python3 -m uvicorn app:app --reload &
cd frontend && node build