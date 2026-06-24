import paramiko
import json

host = "216.22.43.39"
port = 22
user = "root"
password = "fB79w8ePw8mEJxH2"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(host, port, user, password)
    
    # Busca configurações do container
    stdin, stdout, stderr = client.exec_command("docker inspect opt-evolution-api-1")
    output = stdout.read().decode('utf-8', errors='ignore')
    
    try:
        data = json.loads(output)
        envs = data[0]['Config']['Env']
        mounts = data[0]['Mounts']
        
        with open("evo_analysis.txt", "w", encoding="utf-8") as f:
            f.write("=== ENVIRONMENT VARIABLES ===\n")
            for env in envs:
                f.write(env + "\n")
            
            f.write("\n=== MOUNTS ===\n")
            for mount in mounts:
                f.write(f"{mount.get('Source')} -> {mount.get('Destination')}\n")
    except Exception as e:
        with open("evo_analysis.txt", "w", encoding="utf-8") as f:
            f.write("Erro ao fazer parse do docker inspect: " + str(e))
            f.write("\n\n" + output)
            
    print("Análise salva em evo_analysis.txt")
finally:
    client.close()
