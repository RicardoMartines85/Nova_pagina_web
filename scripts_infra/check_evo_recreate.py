import paramiko

host = "216.22.43.39"
port = 22
user = "root"
password = "fB79w8ePw8mEJxH2"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(host, port, user, password)
    
    # Run assaflavie/runlike to get the exact docker run command
    stdin, stdout, stderr = client.exec_command("docker run --rm -v /var/run/docker.sock:/var/run/docker.sock assaflavie/runlike opt-evolution-api-1")
    run_cmd = stdout.read().decode('utf-8', errors='ignore')
    
    with open("evo_run_cmd2.txt", "w", encoding="utf-8") as f:
        f.write(run_cmd)
        
    # Now we modify the command
    if run_cmd.strip() != "":
        # Remove REDIS_URI
        import re
        run_cmd = re.sub(r'--env=REDIS_URI=[^\s]+', '', run_cmd)
        
        # Add new redis variables
        new_env = " --env=REDIS_HOST=evolution-redis --env=REDIS_PORT=6379 --env=REDIS_PASSWORD=evoredis --env=REDIS_DB=1 "
        run_cmd = run_cmd.replace("--env=REDIS_ENABLED=true", "--env=REDIS_ENABLED=true" + new_env)
        
        # We need to stop and rm the old container
        client.exec_command("docker stop opt-evolution-api-1")
        client.exec_command("docker rm opt-evolution-api-1")
        
        # We also need to make sure we don't mess up the network if it was connected to multiple
        # runlike usually handles it, but let's just run it!
        stdin, stdout, stderr = client.exec_command(run_cmd)
        out = stdout.read().decode('utf-8', errors='ignore')
        err = stderr.read().decode('utf-8', errors='ignore')
        
        with open("evo_recreate.txt", "w", encoding="utf-8") as f:
            f.write("CMD: " + run_cmd + "\nOUT: " + out + "\nERR: " + err)
            
finally:
    client.close()
