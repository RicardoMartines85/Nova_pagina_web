import paramiko

host = "216.22.43.39"
port = 22
user = "root"
password = "fB79w8ePw8mEJxH2"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(host, port, user, password)
    # Procurar pelas variáveis de ambiente de autenticação no container
    stdin, stdout, stderr = client.exec_command("docker inspect opt-evolution-api-1 | grep -E 'AUTHENTICATION_API_KEY|AUTHENTICATION_GLOBAL_API_KEY|ADMIN_PASSWORD|MANAGER_PASSWORD|AUTHENTICATION_EXPOSE_IN_FETCH_INSTANCES'")
    print(stdout.read().decode('utf-8', errors='ignore'))
finally:
    client.close()
