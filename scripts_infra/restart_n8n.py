import paramiko

host = "216.22.43.39"
port = 22
user = "root"
password = "fB79w8ePw8mEJxH2"

setup_script = """#!/bin/bash
mkdir -p /opt/n8n_standalone
cd /opt/n8n_standalone

cat << 'EOF' > docker-compose.yml
services:
  n8n:
    image: docker.n8n.io/n8nio/n8n:latest
    restart: always
    environment:
      - N8N_HOST=216.22.43.39
      - N8N_PORT=5678
      - N8N_PROTOCOL=http
      - NODE_ENV=production
      - N8N_SECURE_COOKIE=false
      - WEBHOOK_URL=http://216.22.43.39:5678/
      - GENERIC_TIMEZONE=America/Sao_Paulo
    ports:
      - '5678:5678'
    volumes:
      - /opt/n8n/data:/home/node/.n8n
EOF

docker compose up -d n8n
"""

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(host, port, user, password)
    stdin, stdout, stderr = client.exec_command("cat > /tmp/setup_n8n.sh && bash /tmp/setup_n8n.sh")
    stdin.write(setup_script)
    stdin.close()
    
    print("STDOUT:", stdout.read().decode('utf-8', errors='ignore'))
    print("STDERR:", stderr.read().decode('utf-8', errors='ignore'))
finally:
    client.close()
