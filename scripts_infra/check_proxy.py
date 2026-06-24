import paramiko

host = "216.22.43.39"
port = 22
user = "root"
password = "fB79w8ePw8mEJxH2"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(host, port, user, password)
    
    stdin, stdout, stderr = client.exec_command("docker ps")
    ps_output = stdout.read().decode('utf-8', errors='ignore')
    
    stdin, stdout, stderr = client.exec_command("ufw status")
    ufw_output = stdout.read().decode('utf-8', errors='ignore')

    with open("proxy_check.txt", "w", encoding="utf-8") as f:
        f.write("=== DOCKER PS ===\n")
        f.write(ps_output)
        f.write("\n=== UFW STATUS ===\n")
        f.write(ufw_output)
finally:
    client.close()
