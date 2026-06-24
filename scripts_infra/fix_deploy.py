import paramiko

host = "216.22.43.39"
port = 22
user = "root"
password = "fB79w8ePw8mEJxH2"

setup_script = """#!/bin/bash
cd /opt

echo "Corrigindo docker-compose.yml..."
# Remove as redes e tudo depois
sed -i '/networks:/,$d' docker-compose.yml

# Garante que a landing-page não ficou presa
sed -i '/landing-page:/,$d' docker-compose.yml

# Re-adiciona a landing page e a rede corretamente
cat << 'EOF' >> docker-compose.yml

  landing-page:
    build: /opt/landing-page
    restart: always
    ports:
      - "8082:3000"
    networks:
      - web_net

networks:
  web_net:
    name: web_net
EOF

echo "Iniciando build da Landing Page..."
docker compose build landing-page
docker compose up -d landing-page
"""

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    print("Conectando ao VPS...")
    client.connect(host, port, user, password)
    sftp = client.open_sftp()
    
    with sftp.file('/tmp/fix_deploy.sh', 'w') as f:
        f.write(setup_script.replace("\\r\\n", "\\n"))
    sftp.close()
    
    print("Corrigindo deploy...")
    stdin, stdout, stderr = client.exec_command("bash /tmp/fix_deploy.sh")
    while not stdout.channel.exit_status_ready():
        if stdout.channel.recv_ready():
            print(stdout.channel.recv(1024).decode('utf-8', errors='ignore'), end="")
        if stderr.channel.recv_stderr_ready():
            print(stderr.channel.recv_stderr(1024).decode('utf-8', errors='ignore'), end="")
    print(stdout.read().decode('utf-8', errors='ignore'))
    print("Correção Finalizada!")
finally:
    client.close()
