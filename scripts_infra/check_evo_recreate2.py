import paramiko

host = "216.22.43.39"
port = 22
user = "root"
password = "fB79w8ePw8mEJxH2"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(host, port, user, password)
    
    # Get run command
    stdin, stdout, stderr = client.exec_command("docker run --rm -v /var/run/docker.sock:/var/run/docker.sock assaflavie/runlike opt-evolution-api-1")
    run_cmd = stdout.read().decode('utf-8', errors='ignore')
    
    if run_cmd.strip() != "":
        # Add -d for detached mode since runlike might not include it
        run_cmd = run_cmd.replace("docker run ", "docker run -d ")
        
        # Remove REDIS_URI
        import re
        run_cmd = re.sub(r'--env=REDIS_URI=[^\s]+', '', run_cmd)
        
        # Add new redis variables
        new_env = " --env=REDIS_HOST=evolution-redis --env=REDIS_PORT=6379 --env=REDIS_PASSWORD=evoredis --env=REDIS_DB=1 "
        run_cmd = run_cmd.replace("--env=REDIS_ENABLED=true", "--env=REDIS_ENABLED=true" + new_env)
        
        # Execute stop, rm and run sequentially
        full_cmd = f"docker stop opt-evolution-api-1 && docker rm opt-evolution-api-1 && {run_cmd}"
        
        stdin, stdout, stderr = client.exec_command(full_cmd)
        out = stdout.read().decode('utf-8', errors='ignore')
        err = stderr.read().decode('utf-8', errors='ignore')
        
        with open("evo_recreate2.txt", "w", encoding="utf-8") as f:
            f.write("CMD: " + full_cmd + "\nOUT: " + out + "\nERR: " + err)
            
finally:
    client.close()
