import paramiko

host = "216.22.43.39"
port = 22
user = "root"
password = "fB79w8ePw8mEJxH2"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    print("Conectando ao VPS para reiniciar TODA a stack da Evolution API...")
    client.connect(host, port, user, password)
    
    # Reinicia o Redis, Postgres e a Evolution API
    print("Enviando comando de restart massivo...")
    stdin, stdout, stderr = client.exec_command("docker restart opt-evolution-redis-1 opt-evolution-postgres-1 opt-evolution-api-1")
    
    print("Saída do comando:", stdout.read().decode('utf-8'))
    print("Erros (se houver):", stderr.read().decode('utf-8'))
    
    print("Stack inteira da Evolution API reiniciada com sucesso!")
finally:
    client.close()
