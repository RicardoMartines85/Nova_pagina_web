import paramiko

host = "216.22.43.39"
port = 22
user = "root"
password = "fB79w8ePw8mEJxH2"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(host, port, user, password)
    
    stdin, stdout, stderr = client.exec_command("ip -4 addr show docker0")
    ip_output = stdout.read().decode('utf-8', errors='ignore')
    
    with open("docker_ip.txt", "w", encoding="utf-8") as f:
        f.write(ip_output)
finally:
    client.close()
