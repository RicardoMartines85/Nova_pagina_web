import paramiko
import re

host = "216.22.43.39"
port = 22
user = "root"
password = "fB79w8ePw8mEJxH2"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(host, port, user, password)
    
    # Recreate Redis without password
    stdin, stdout, stderr = client.exec_command("docker run --rm -v /var/run/docker.sock:/var/run/docker.sock assaflavie/runlike opt-evolution-redis-1")
    redis_cmd = stdout.read().decode('utf-8', errors='ignore')
    
    if redis_cmd.strip() != "":
        redis_cmd = redis_cmd.replace("docker run ", "docker run -d ")
        # Remove --requirepass evoredis
        redis_cmd = redis_cmd.replace("--requirepass evoredis", "")
        redis_cmd = redis_cmd.replace("--requirepass 'evoredis'", "")
        redis_cmd = redis_cmd.replace("--requirepass=\"evoredis\"", "")
        
        full_redis = f"docker stop opt-evolution-redis-1 && docker rm opt-evolution-redis-1 && {redis_cmd}"
        client.exec_command(full_redis)
        
    # Recreate API without REDIS_PASSWORD
    stdin, stdout, stderr = client.exec_command("docker run --rm -v /var/run/docker.sock:/var/run/docker.sock assaflavie/runlike opt-evolution-api-1")
    api_cmd = stdout.read().decode('utf-8', errors='ignore')
    
    if api_cmd.strip() != "":
        api_cmd = api_cmd.replace("docker run ", "docker run -d ")
        # Remove REDIS_PASSWORD
        api_cmd = re.sub(r'--env=REDIS_PASSWORD=[^\s]+', '', api_cmd)
        
        full_api = f"docker stop opt-evolution-api-1 && docker rm opt-evolution-api-1 && {api_cmd}"
        
        # We need to wait a few seconds for redis to start
        final_cmd = f"{full_redis} && sleep 5 && {full_api}"
        
        stdin, stdout, stderr = client.exec_command(final_cmd)
        out = stdout.read().decode('utf-8', errors='ignore')
        err = stderr.read().decode('utf-8', errors='ignore')
        
        with open("evo_recreate_both.txt", "w", encoding="utf-8") as f:
            f.write("OUT: " + out + "\nERR: " + err)
            
finally:
    client.close()
