# 🌍 Use Railway's Nixpacks-compatible base image
FROM ghcr.io/railwayapp/nixpacks:ubuntu-1745885067@sha256:d45c89d80e13d7ad0fd555b5130f22a866d9dd10e861f589932303ef2314c7de

# 📁 Set working directory
WORKDIR /app

# 📦 Copy requirements and source code
COPY requirements.txt ./
COPY . /app/

# ⚙️ Install dependencies in virtualenv and activate
RUN python -m venv --copies /opt/venv && \
    . /opt/venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# 🛠️ Ensure PATH includes venv binaries
RUN printf '\nPATH=/opt/venv/bin:$PATH' >> /root/.profile

# 🚪 Expose port for Railway healthcheck
ENV PORT=5000
EXPOSE 5000

# 🚀 Start app using Gunicorn and your dynamic port detection
CMD ["gunicorn", "main:app", "-b", "0.0.0.0:$PORT"]
