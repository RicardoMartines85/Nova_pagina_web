import paramiko

host = "216.22.43.39"
port = 22
user = "root"
password = "fB79w8ePw8mEJxH2"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(host, port, user, password)
    
    # Run curl from inside n8n to evolution's container name
    stdin, stdout, stderr = client.exec_command("docker inspect opt-evolution-api-1 | grep IPAddress")
    evo_ip = stdout.read().decode('utf-8', errors='ignore')
    
    stdin, stdout, stderr = client.exec_command("docker inspect n8n_standalone-n8n-1 | grep IPAddress")
    n8n_ip = stdout.read().decode('utf-8', errors='ignore')
    
    stdin, stdout, stderr = client.exec_command("docker network ls")
    networks = stdout.read().decode('utf-8', errors='ignore')
    
    with open("docker_net.txt", "w", encoding="utf-8") as f:
        f.write("=== EVO IP ===\n" + evo_ip)
        f.write("\n=== N8N IP ===\n" + n8n_ip)
        f.write("\n=== NETWORKS ===\n" + networks)
finally:
    client.close()
