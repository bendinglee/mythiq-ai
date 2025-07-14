# ✅ Use a base image that includes build tools
FROM ubuntu:22.04

# 🔧 System setup
RUN apt update && apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    git

# 📁 Set working directory
WORKDIR /app

# 📦 Copy requirements first (for layer caching)
COPY requirements.txt ./

# ⚙️ Install dependencies
RUN python3 -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# 🧠 Add rest of the app
COPY . /app

# ⚙️ Activate venv at runtime
ENV PATH="/opt/venv/bin:$PATH"

# 🚪 Expose port for Railway compatibility
ENV PORT=5000
EXPOSE 5000

# 🚀 Launch Mythiq
CMD ["gunicorn", "main:app", "-b", "0.0.0.0:$PORT"]
