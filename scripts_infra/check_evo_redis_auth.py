import paramiko

host = "216.22.43.39"
port = 22
user = "root"
password = "fB79w8ePw8mEJxH2"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(host, port, user, password)
    
    # Try with password
    stdin, stdout, stderr = client.exec_command("docker exec opt-evolution-api-1 redis-cli -h evolution-redis -a evoredis PING")
    out1 = stdout.read().decode('utf-8', errors='ignore')
    err1 = stderr.read().decode('utf-8', errors='ignore')
    
    # Try without password
    stdin, stdout, stderr = client.exec_command("docker exec opt-evolution-api-1 redis-cli -h evolution-redis PING")
    out2 = stdout.read().decode('utf-8', errors='ignore')
    err2 = stderr.read().decode('utf-8', errors='ignore')
    
    with open("evo_redis_auth.txt", "w", encoding="utf-8") as f:
        f.write("=== WITH PASSWORD ===\nOUT: " + out1 + "\nERR: " + err1)
        f.write("\n=== WITHOUT PASSWORD ===\nOUT: " + out2 + "\nERR: " + err2)
finally:
    client.close()
