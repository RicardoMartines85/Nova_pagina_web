import paramiko

host = "216.22.43.39"
port = 22
user = "root"
password = "fB79w8ePw8mEJxH2"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(host, port, user, password)
    
    # Check Evolution API logs
    stdin, stdout, stderr = client.exec_command("docker logs --tail 50 opt-evolution-api-1")
    api_logs = stdout.read().decode('utf-8', errors='ignore')
    
    # Ping evolution-api from n8n
    stdin, stdout, stderr = client.exec_command("docker exec n8n_standalone-n8n-1 ping -c 2 evolution-api")
    ping_out = stdout.read().decode('utf-8', errors='ignore')
    ping_err = stderr.read().decode('utf-8', errors='ignore')
    
    with open("evo_diag.txt", "w", encoding="utf-8") as f:
        f.write("=== API LOGS ===\n" + api_logs)
        f.write("\n=== PING TEST ===\n" + ping_out + "\n" + ping_err)
finally:
    client.close()
