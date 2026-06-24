import paramiko

host = "216.22.43.39"
port = 22
user = "root"
password = "fB79w8ePw8mEJxH2"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(host, port, user, password)
    
    # Restart NPM to flush DNS cache
    stdin, stdout, stderr = client.exec_command("docker restart opt-npm-1")
    out = stdout.read().decode('utf-8', errors='ignore')
    
    with open("evo_restart_npm.txt", "w", encoding="utf-8") as f:
        f.write(out)
finally:
    client.close()
