import paramiko

host = "216.22.43.39"
port = 22
user = "root"
password = "fB79w8ePw8mEJxH2"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(host, port, user, password)
    
    stdin, stdout, stderr = client.exec_command("docker inspect opt-evolution-api-1 | grep -i redis")
    redis_env = stdout.read().decode('utf-8', errors='ignore')
    
    with open("evo_redis.txt", "w", encoding="utf-8") as f:
        f.write(redis_env)
finally:
    client.close()
