import paramiko

host = "216.22.43.39"
port = 22
user = "root"
password = "fB79w8ePw8mEJxH2"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(host, port, user, password)
    
    # 2. Recreate API with CACHE_REDIS_ENABLED=false
    client.exec_command("docker rm -f opt-evolution-api-1")
    
    api_cmd = """docker run -d --name=opt-evolution-api-1 --hostname=21b1ac0bf667 --volume /opt/evolution/instances:/evolution/instances --env=DATABASE_CONNECTION_CLIENT_NAME=evolution_api --env=DATABASE_PROVIDER=postgresql --env='DATABASE_CONNECTION_URI=postgresql://evouser:evopass@evolution-postgres:5432/evolutiondb?schema=public' --env=AUTHENTICATION_TYPE=apikey --env=LOG_LEVEL=ERROR --env=SERVER_URL=http://216.22.43.39:8080 --env=AUTHENTICATION_API_KEY=rdo-evolution-secret-2026 --env=REDIS_ENABLED=false --env=CACHE_REDIS_ENABLED=false --network=web_net --network-alias=evolution-api --workdir=/evolution -p 8080:8080 --restart=always evoapicloud/evolution-api:v2.3.7"""
    
    stdin, stdout, stderr = client.exec_command(api_cmd)
    out = stdout.read().decode('utf-8', errors='ignore')
    err = stderr.read().decode('utf-8', errors='ignore')
    
    client.exec_command("sleep 5")
    stdin, stdout, stderr = client.exec_command("docker logs --tail 40 opt-evolution-api-1")
    logs = stdout.read().decode('utf-8', errors='ignore')
    
    with open("evo_logs_cache_redis_false_fixed.txt", "w", encoding="utf-8") as f:
        f.write("OUT: " + out + "\nERR: " + err + "\nLOGS:\n" + logs)
finally:
    client.close()
