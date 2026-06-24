import paramiko

host = "216.22.43.39"
port = 22
user = "root"
password = "fB79w8ePw8mEJxH2"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(host, port, user, password)
    
    # 1. Recreate Redis with alias
    client.exec_command("docker stop opt-evolution-redis-1 && docker rm opt-evolution-redis-1")
    redis_cmd = "docker run -d --name=opt-evolution-redis-1 --network=web_net --network-alias=evolution-redis -p 6379:6379 --restart=always redis:6-alpine"
    client.exec_command(redis_cmd)
    
    # 2. Recreate API with alias
    client.exec_command("docker stop opt-evolution-api-1 && docker rm opt-evolution-api-1")
    api_cmd = """docker run -d --name=opt-evolution-api-1 --hostname=21b1ac0bf667 --volume /opt/evolution/instances:/evolution/instances --env=DATABASE_CONNECTION_CLIENT_NAME=evolution_api --env=DATABASE_PROVIDER=postgresql --env='DATABASE_CONNECTION_URI=postgresql://evouser:evopass@evolution-postgres:5432/evolutiondb?schema=public' --env=AUTHENTICATION_TYPE=apikey --env=LOG_LEVEL=ERROR --env=SERVER_URL=http://216.22.43.39:8080 --env=AUTHENTICATION_API_KEY=rdo-evolution-secret-2026 --env=REDIS_ENABLED=true --env=REDIS_URI=redis://evolution-redis:6379/1 --env=REDIS_PREFIX_KEY=evo2 --network=web_net --network-alias=evolution-api --workdir=/evolution -p 8080:8080 --restart=always --label='com.docker.compose.depends_on=evolution-postgres:service_started:false,evolution-redis:service_started:false' --label='com.docker.compose.replace=evolution-api-1' --label='com.docker.compose.project=opt' --label='com.docker.compose.service=evolution-api' --label='com.docker.compose.container-number=1' evoapicloud/evolution-api:v2.3.7"""
    client.exec_command(api_cmd)
    
    client.exec_command("docker restart opt-npm-1")
    
    client.exec_command("sleep 5")
    stdin, stdout, stderr = client.exec_command("docker logs --tail 40 opt-evolution-api-1")
    logs = stdout.read().decode('utf-8', errors='ignore')
    
    with open("evo_logs_final_aliases.txt", "w", encoding="utf-8") as f:
        f.write(logs)
finally:
    client.close()
