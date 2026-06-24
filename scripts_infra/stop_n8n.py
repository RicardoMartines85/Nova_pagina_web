import paramiko

host = "216.22.43.39"
port = 22
user = "root"
password = "fB79w8ePw8mEJxH2"

setup_script = """#!/bin/bash
docker stop opt-n8n-1 || true
docker rm opt-n8n-1 || true
cd /opt/n8n_standalone
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
