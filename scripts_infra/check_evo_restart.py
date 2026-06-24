import paramiko

host = "216.22.43.39"
port = 22
user = "root"
password = "fB79w8ePw8mEJxH2"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(host, port, user, password)
    
    # Restart evolution API to fix Redis connection
    stdin, stdout, stderr = client.exec_command("docker restart opt-evolution-api-1")
    stdout.read()
    
    # Check logs after restart
    import time
    time.sleep(5)
    stdin, stdout, stderr = client.exec_command("docker logs --tail 20 opt-evolution-api-1")
    api_logs = stdout.read().decode('utf-8', errors='ignore')
    
    with open("evo_restart.txt", "w", encoding="utf-8") as f:
        f.write(api_logs)
finally:
    client.close()
