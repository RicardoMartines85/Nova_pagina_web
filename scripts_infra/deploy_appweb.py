import paramiko
import os
import subprocess

host = "216.22.43.39"
port = 22
user = "root"
password = "fB79w8ePw8mEJxH2"
base_dir = r"C:\Users\ricardo.matines\.gemini\antigravity-ide\scratch\Projeto_RDO"

print("Compactando os arquivos locais do RDO Inteligente...")
tar_path = os.path.join(base_dir, "app.tar.gz")
if os.path.exists(tar_path):
    os.remove(tar_path)
    
subprocess.run(["tar.exe", "-czf", "app.tar.gz", "--exclude=node_modules", "--exclude=.git", "--exclude=.wrangler", "rdo-inteligente-source"], cwd=base_dir, shell=True)

setup_script = """#!/bin/bash
cd /opt

echo "Extraindo os arquivos na pasta /opt/rdo-app..."
mkdir -p /opt/rdo-app
tar -xzf /tmp/app.tar.gz -C /opt/rdo-app --strip-components=1

echo "Configurando docker-compose.yml..."
if ! grep -q "rdo-app:" docker-compose.yml; then
    sed -i '/networks:/,$d' docker-compose.yml
    cat << 'EOF' >> docker-compose.yml

  rdo-app:
    build: /opt/rdo-app
    restart: always
    ports:
      - "8081:80"
    networks:
      - web_net

networks:
  web_net:
    name: web_net
EOF
fi

ufw allow 8081/tcp

echo "Iniciando build do RDO Inteligente..."
docker compose build rdo-app
docker compose up -d rdo-app
"""

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    print("Conectando ao VPS...")
    client.connect(host, port, user, password)
    sftp = client.open_sftp()
    
    print("Transferindo arquivos compactados (Upload)...")
    sftp.put(tar_path, "/tmp/app.tar.gz")
    
    with sftp.file('/tmp/deploy_app.sh', 'w') as f:
        f.write(setup_script.replace("\\r\\n", "\\n"))
    sftp.close()
    
    print("Iniciando esteira de produção no servidor...")
    stdin, stdout, stderr = client.exec_command("bash /tmp/deploy_app.sh")
    while not stdout.channel.exit_status_ready():
        if stdout.channel.recv_ready():
            print(stdout.channel.recv(1024).decode('utf-8', errors='ignore'), end="")
        if stderr.channel.recv_stderr_ready():
            print(stderr.channel.recv_stderr(1024).decode('utf-8', errors='ignore'), end="")
    print(stdout.read().decode('utf-8', errors='ignore'))
    print("Deploy finalizado! App disponível na porta 8081.")
finally:
    client.close()
