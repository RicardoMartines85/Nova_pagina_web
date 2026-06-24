import paramiko

host = "216.22.43.39"
port = 22
user = "root"
password = "fB79w8ePw8mEJxH2"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(host, port, user, password)
    
    # Stop and remove current api
    client.exec_command("docker stop opt-evolution-api-1 && docker rm opt-evolution-api-1")
    
    # Run v2.2.3
    api_cmd = """docker run -d --name=opt-evolution-api-1 --hostname=21b1ac0bf667 --volume /opt/evolution/instances:/evolution/instances --env=DATABASE_CONNECTION_CLIENT_NAME=evolution_api --env=DATABASE_PROVIDER=postgresql --env='DATABASE_CONNECTION_URI=postgresql://evouser:evopass@evolution-postgres:5432/evolutiondb?schema=public' --env=AUTHENTICATION_TYPE=apikey --env=LOG_LEVEL=ERROR --env=SERVER_URL=http://216.22.43.39:8080 --env=AUTHENTICATION_API_KEY=rdo-evolution-secret-2026 --env=REDIS_ENABLED=true --env=REDIS_URI=redis://evolution-redis:6379/1 --env=REDIS_PREFIX_KEY=evo2 --network=web_net --workdir=/evolution -p 8080:8080 --restart=always --label='com.docker.compose.depends_on=evolution-postgres:service_started:false,evolution-redis:service_started:false' --label='com.docker.compose.replace=evolution-api-1' --label='com.docker.compose.project=opt' --label='com.docker.compose.service=evolution-api' --label='com.docker.compose.container-number=1' evoapicloud/evolution-api:v2.2.3"""
    
    stdin, stdout, stderr = client.exec_command(api_cmd)
    out = stdout.read().decode('utf-8', errors='ignore')
    
    # Wait for container to start, then check logs
    client.exec_command("sleep 5")
    stdin, stdout, stderr = client.exec_command("docker logs --tail 40 opt-evolution-api-1")
    logs = stdout.read().decode('utf-8', errors='ignore')
    
    with open("evo_recreate_v223.txt", "w", encoding="utf-8") as f:
        f.write("OUT: " + out + "\nLOGS:\n" + logs)
finally:
    client.close()
