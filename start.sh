# cd ~/work/ufv/sacda-scripts-server/
cd backend && /bin/python3 -m uvicorn app:app --reload &
cd frontend && node build