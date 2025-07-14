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

# 💥 Add alias so 'python' maps to 'python3'
RUN ln -s /usr/bin/python3 /usr/bin/python

# 📁 Working directory
WORKDIR /app

# 🔗 Copy requirements first
COPY requirements.txt ./

# ⚙️ Install dependencies in virtualenv and activate
RUN python -m venv --copies /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 📦 Copy full app
COPY . /app

# ✅ Activate virtualenv on startup
ENV PATH="/opt/venv/bin:$PATH"

# 🚪 Expose port
ENV PORT=5000
EXPOSE 5000

# 🚀 Launch using Gunicorn
CMD ["gunicorn", "main:app", "-b", "0.0.0.0:$PORT"]
