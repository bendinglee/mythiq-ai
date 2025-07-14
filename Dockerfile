FROM ubuntu:22.04

# 🛠️ System dependencies
RUN apt update && apt install -y \
  python3 \
  python3-pip \
  python3-venv \
  curl \
  lsof \
  net-tools \
  ca-certificates

# 📁 Working directory
WORKDIR /app

# 🧪 Copy requirements first for caching
COPY requirements.txt ./

# 🎯 Set up Python virtual environment and install dependencies
RUN python3 -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 🔗 Copy full app source code
COPY . /app

# ✅ Activate environment path
ENV PATH="/opt/venv/bin:$PATH"

# 🚪 Expose dynamic Railway port
ENV PORT=5000
EXPOSE 5000

# 🧠 Print version and verify entrypoint file
RUN python3 -V && \
    echo "Mythiq container ready for port $PORT" && \
    echo "📂 Contents of /app:" && \
    ls -al /app

# 🚀 Launch Mythiq directly with Python for full log visibility
CMD ["python3", "main.py"]
