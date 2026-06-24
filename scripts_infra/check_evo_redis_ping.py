import paramiko

host = "216.22.43.39"
port = 22
user = "root"
password = "fB79w8ePw8mEJxH2"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(host, port, user, password)
    
    # Run a temporary redis container to test connection
    stdin, stdout, stderr = client.exec_command("docker run --rm --network web_net redis:alpine redis-cli -h evolution-redis -a evoredis PING")
    out1 = stdout.read().decode('utf-8', errors='ignore')
    err1 = stderr.read().decode('utf-8', errors='ignore')
    
    # Run a temporary redis container to test connection without password
    stdin, stdout, stderr = client.exec_command("docker run --rm --network web_net redis:alpine redis-cli -h evolution-redis PING")
    out2 = stdout.read().decode('utf-8', errors='ignore')
    err2 = stderr.read().decode('utf-8', errors='ignore')
    
    with open("evo_redis_ping_test.txt", "w", encoding="utf-8") as f:
        f.write("=== WITH PASSWORD ===\n" + out1 + "\nERR:\n" + err1 + "\n")
        f.write("=== WITHOUT PASSWORD ===\n" + out2 + "\nERR:\n" + err2)
finally:
    client.close()
