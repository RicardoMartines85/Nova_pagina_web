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
    
    # Get current run command
    stdin, stdout, stderr = client.exec_command("docker run --rm -v /var/run/docker.sock:/var/run/docker.sock assaflavie/runlike opt-evolution-api-1")
    api_cmd = stdout.read().decode('utf-8', errors='ignore')
    
    if api_cmd.strip() != "":
        api_cmd = api_cmd.replace("docker run ", "docker run -d ")
        
        # Disable Redis
        api_cmd = api_cmd.replace("--env=REDIS_ENABLED=true", "--env=REDIS_ENABLED=false")
        
        # Remove any lingering Redis env vars just in case
        api_cmd = re.sub(r'--env=REDIS_URI=[^\s]+', '', api_cmd)
        api_cmd = re.sub(r'--env=REDIS_HOST=[^\s]+', '', api_cmd)
        api_cmd = re.sub(r'--env=REDIS_PORT=[^\s]+', '', api_cmd)
        api_cmd = re.sub(r'--env=REDIS_PASSWORD=[^\s]+', '', api_cmd)
        api_cmd = re.sub(r'--env=REDIS_DB=[^\s]+', '', api_cmd)
        api_cmd = re.sub(r'--env=REDIS_PREFIX_KEY=[^\s]+', '', api_cmd)
        
        full_api = f"docker stop opt-evolution-api-1 && docker rm opt-evolution-api-1 && {api_cmd}"
        
        stdin, stdout, stderr = client.exec_command(full_api)
        out = stdout.read().decode('utf-8', errors='ignore')
        
        with open("evo_recreate_api_no_redis.txt", "w", encoding="utf-8") as f:
            f.write(out)
finally:
    client.close()
