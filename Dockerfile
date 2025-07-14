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

# 🧪 Copy requirements for faster layer caching
COPY requirements.txt ./

# 🎯 Create virtual environment and install dependencies
RUN python3 -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 🔗 Add full app source
COPY . /app

# ✅ Activate environment
ENV PATH="/opt/venv/bin:$PATH"

# 🚪 Dynamic port from Railway
ENV PORT=5000
EXPOSE 5000

# 🧠 Sanity check: print version and active port before launch
RUN python3 -V && echo "Mythiq container ready for port $PORT"

# 🚀 Launch Mythiq via Gunicorn with worker resilience
