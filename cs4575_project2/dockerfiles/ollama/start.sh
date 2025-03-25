ollama serve &

echo "Starting Ollama service..."
sleep 15 

echo "Starting prompt processing..."
python3 /app/ollama_library.py
