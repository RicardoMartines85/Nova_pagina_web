import paramiko

host = "216.22.43.39"
port = 22
user = "root"
password = "fB79w8ePw8mEJxH2"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(host, port, user, password)
    
    # Grep all docker-compose.yml files for evolution-api
    stdin, stdout, stderr = client.exec_command("find /opt /var/lib/docker/volumes /data -name docker-compose.yml -exec grep -l 'evolution-api' {} + 2>/dev/null")
    out = stdout.read().decode('utf-8', errors='ignore')
    
    with open("evo_find_real_compose.txt", "w", encoding="utf-8") as f:
        f.write(out)
finally:
    client.close()
