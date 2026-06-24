import paramiko

host = "216.22.43.39"
port = 22
user = "root"
password = "fB79w8ePw8mEJxH2"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(host, port, user, password)
    
    # Verifica o status dos containers e os logs do Redis
    stdin, stdout, stderr = client.exec_command("docker ps -a | grep evolution")
    ps_output = stdout.read().decode('utf-8', errors='ignore')
    
    stdin, stdout, stderr = client.exec_command("docker logs --tail 20 opt-evolution-redis-1")
    redis_logs = stdout.read().decode('utf-8', errors='ignore')
    redis_errs = stderr.read().decode('utf-8', errors='ignore')
    
    with open("evo_logs.txt", "w", encoding="utf-8") as f:
        f.write("=== DOCKER PS ===\n")
        f.write(ps_output)
        f.write("\n=== REDIS LOGS ===\n")
        f.write(redis_logs)
        f.write(redis_errs)
    print("Dados salvos em evo_logs.txt")
finally:
    client.close()
