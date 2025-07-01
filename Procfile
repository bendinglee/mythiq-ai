web: gunicorn mythiq_ai_backend_optimized:app -w 1 --bind 0.0.0.0:$PORT --timeout 120 --worker-class eventlet --max-requests 1000 --preload

