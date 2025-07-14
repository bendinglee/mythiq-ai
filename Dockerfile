FROM ubuntu:22.04

# 🛠️ System dependencies
RUN apt update && apt install -y \
  python3 \
  python3-pip \
  python3-venv

# 📁 Working directory
WORKDIR /app

# 📦 Dependency install
COPY requirements.txt ./
RUN python3 -m venv /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# 🔗 Add app files
COPY . /app

# ✅ Activate environment
ENV PATH="/opt/venv/bin:$PATH"

# 🚪 Expose port
ENV PORT=5000
EXPOSE 5000

# 🔮 Launch Mythiq
CMD ["gunicorn", "main:app", "-b", "0.0.0.0:$PORT"]
