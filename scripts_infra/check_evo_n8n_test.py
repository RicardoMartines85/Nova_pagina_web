import paramiko

host = "216.22.43.39"
port = 22
user = "root"
password = "fB79w8ePw8mEJxH2"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(host, port, user, password)
    
    stdin, stdout, stderr = client.exec_command("docker exec n8n_standalone-n8n-1 curl -I http://evolution-api:8080/instance/connectionState/MartinesPS-3 --header 'apikey: rdo-evolution-secret-2026'")
    out = stdout.read().decode('utf-8', errors='ignore')
    err = stderr.read().decode('utf-8', errors='ignore')
    
    with open("evo_n8n_test.txt", "w", encoding="utf-8") as f:
        f.write("=== OUTPUT ===\n" + out)
        f.write("\n=== ERRS ===\n" + err)
finally:
    client.close()
