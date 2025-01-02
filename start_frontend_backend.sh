#!/bin/bash

# Function to clean up processes on exit
cleanup() {
    echo "Cleaning up..."
    kill $front_pid $back_pid
    wait $front_pid $back_pid
    echo "All processes stopped."
    exit 0
}

# Set up a trap to catch SIGINT (Ctrl+C) and call the cleanup function
trap cleanup SIGINT

# Start the frontend
cd flask-vue-app/frontend

echo "Installing frontend dependencies..."
npm install

echo "Starting frontend server..."
npm run dev &
front_pid=$!

# Start the backend
cd ../backend-server

echo "Starting backend server..."
flask run --port=5000 --debug &
back_pid=$!

# Wait for processes to finish
wait $front_pid $back_pid
