import paramiko

host = "216.22.43.39"
port = 22
user = "root"
password = "fB79w8ePw8mEJxH2"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(host, port, user, password)
    
    stdin, stdout, stderr = client.exec_command("docker inspect opt-npm-1 | grep -i network")
    out = stdout.read().decode('utf-8', errors='ignore')
    
    with open("evo_npm_net.txt", "w", encoding="utf-8") as f:
        f.write(out)
        
    # Also let's just connect them using IP internal if needed
finally:
    client.close()
