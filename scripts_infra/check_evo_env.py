import paramiko
import json

host = "216.22.43.39"
port = 22
user = "root"
password = "fB79w8ePw8mEJxH2"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(host, port, user, password)
    
    stdin, stdout, stderr = client.exec_command("docker inspect opt-evolution-api-1")
    out = stdout.read().decode('utf-8', errors='ignore')
    data = json.loads(out)
    env_vars = data[0]["Config"]["Env"]
    
    with open("evo_env.txt", "w", encoding="utf-8") as f:
        for e in env_vars:
            f.write(e + "\n")
finally:
    client.close()
