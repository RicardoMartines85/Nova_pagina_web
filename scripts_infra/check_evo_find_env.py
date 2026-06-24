import paramiko

host = "216.22.43.39"
port = 22
user = "root"
password = "fB79w8ePw8mEJxH2"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(host, port, user, password)
    
    # Check for .env file inside instances or evolution directory
    stdin, stdout, stderr = client.exec_command("find /opt/evolution -name '.env'")
    find_out = stdout.read().decode('utf-8', errors='ignore')
    
    # Also dump exactly the environment variables inside the container
    stdin, stdout, stderr = client.exec_command("docker exec opt-evolution-api-1 env")
    env_out = stdout.read().decode('utf-8', errors='ignore')
    
    with open("evo_find_env.txt", "w", encoding="utf-8") as f:
        f.write("=== FIND .ENV ===\n" + find_out + "\n=== CONTAINER ENV ===\n" + env_out)
finally:
    client.close()
