import paramiko

host = "216.22.43.39"
port = 22
user = "root"
password = "fB79w8ePw8mEJxH2"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(host, port, user, password)
    
    # Check if redis is running
    stdin, stdout, stderr = client.exec_command("docker ps -a | grep redis")
    ps_out = stdout.read().decode('utf-8', errors='ignore')
    
    # Check redis logs
    stdin, stdout, stderr = client.exec_command("docker logs --tail 30 opt-evolution-redis-1")
    logs_out = stdout.read().decode('utf-8', errors='ignore')
    
    with open("evo_redis_status.txt", "w", encoding="utf-8") as f:
        f.write("=== PS ===\n" + ps_out + "\n=== LOGS ===\n" + logs_out)
finally:
    client.close()
