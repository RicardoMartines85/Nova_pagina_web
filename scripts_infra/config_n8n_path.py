import paramiko

host = "216.22.43.39"
port = 22
user = "root"
password = "fB79w8ePw8mEJxH2"

setup_script = """#!/bin/bash
cd /opt

# Adicionar N8N_PATH se não existir
if ! grep -q "N8N_PATH=/n8n/" docker-compose.yml; then
    sed -i '/N8N_PORT=5678/a \      - N8N_PATH=/n8n/' docker-compose.yml
fi

# Mudar o N8N_HOST para o domínio
sed -i 's/N8N_HOST=216.22.43.39/N8N_HOST=martines.halftech.com/g' docker-compose.yml
sed -i 's/N8N_PROTOCOL=http/N8N_PROTOCOL=https/g' docker-compose.yml
sed -i 's|WEBHOOK_URL=http://216.22.43.39:5678/|WEBHOOK_URL=https://martines.halftech.com/n8n/|g' docker-compose.yml

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
