import paramiko

host = "216.22.43.39"
port = 22
user = "root"
password = "fB79w8ePw8mEJxH2"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(host, port, user, password)
    
    # Check the compose file
    stdin, stdout, stderr = client.exec_command("cat /opt/docker-compose.yml")
    compose_content = stdout.read().decode('utf-8', errors='ignore')
    
    with open("evo_compose_content.txt", "w", encoding="utf-8") as f:
        f.write(compose_content)
        
    # Replace REDIS_URI with REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_DB
    new_compose = compose_content.replace(
        "      - REDIS_URI=redis://:evoredis@evolution-redis:6379/1",
        "      - REDIS_HOST=evolution-redis\n      - REDIS_PORT=6379\n      - REDIS_PASSWORD=evoredis\n      - REDIS_DB=1"
    )
    
    # Write back to server and restart
    if new_compose != compose_content:
        import shlex
        escaped_compose = shlex.quote(new_compose)
        client.exec_command(f"echo {escaped_compose} > /opt/docker-compose.yml")
        client.exec_command("cd /opt && docker compose up -d")
        
        with open("evo_compose_update.txt", "w", encoding="utf-8") as f:
            f.write("Updated docker-compose and restarted!")
    else:
        with open("evo_compose_update.txt", "w", encoding="utf-8") as f:
            f.write("No changes made. REDIS_URI not found.")
            
finally:
    client.close()
