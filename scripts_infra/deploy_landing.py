import paramiko
import os
import subprocess

host = "216.22.43.39"
port = 22
user = "root"
password = "fB79w8ePw8mEJxH2"
base_dir = r"C:\Users\ricardo.matines\.gemini\antigravity-ide\scratch\gepeto\Projetos"
landing_dir = os.path.join(base_dir, "Pagina web")

print("Compactando os arquivos locais da Landing Page...")
tar_path = os.path.join(base_dir, "landing.tar.gz")
if os.path.exists(tar_path):
    os.remove(tar_path)
    
subprocess.run(["tar.exe", "-czf", "landing.tar.gz", "--exclude=node_modules", "--exclude=.git", "--exclude=.lovable", "Pagina web"], cwd=base_dir, shell=True)

setup_script = """#!/bin/bash
cd /opt

echo "Extraindo os arquivos na pasta /opt/landing-page..."
mkdir -p /opt/landing-page
tar -xzf /tmp/landing.tar.gz -C /opt/landing-page --strip-components=1

echo "Configurando docker-compose.yml para a Landing Page..."
sed -i '/networks:/,$d' docker-compose.yml
sed -i '/landing-page:/,$d' docker-compose.yml

echo "Criando pasta de cache estático para o Blog..."
mkdir -p /opt/blog_data
if [ ! -f /opt/blog_data/posts.json ]; then
    echo "[]" > /opt/blog_data/posts.json
fi

cat << 'EOF' >> docker-compose.yml

  landing-page:
    build: /opt/landing-page
    restart: always
    ports:
      - "8083:3000"
    volumes:
      - /opt/blog_data:/app/dist/client/blog_data
    networks:
      - web_net

networks:
  web_net:
    name: web_net
EOF

ufw allow 8083/tcp

echo "Iniciando build da Landing Page..."
docker compose rm -fs landing-page
docker compose build landing-page
docker compose up -d landing-page
"""

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    print("Conectando ao VPS...")
    client.connect(host, port, user, password)
    sftp = client.open_sftp()
    
    print("Transferindo arquivos compactados (Upload)...")
    sftp.put(tar_path, "/tmp/landing.tar.gz")
    
    with sftp.file('/tmp/deploy_landing.sh', 'w') as f:
        f.write(setup_script.replace("\\r\\n", "\\n"))
    sftp.close()
    
    print("Iniciando esteira de produção no servidor...")
    stdin, stdout, stderr = client.exec_command("bash /tmp/deploy_landing.sh")
    while not stdout.channel.exit_status_ready():
        if stdout.channel.recv_ready():
            text = stdout.channel.recv(1024).decode('utf-8', errors='ignore')
            print(text.encode('ascii', 'ignore').decode('ascii'), end="")
        if stderr.channel.recv_stderr_ready():
            text = stderr.channel.recv_stderr(1024).decode('utf-8', errors='ignore')
            print(text.encode('ascii', 'ignore').decode('ascii'), end="")
    text = stdout.read().decode('utf-8', errors='ignore')
    print(text.encode('ascii', 'ignore').decode('ascii'))
    print("Deploy finalizado! Landing Page rodando na porta 8082.")
finally:
    client.close()
