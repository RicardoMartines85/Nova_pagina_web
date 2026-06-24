import paramiko

host = "216.22.43.39"
port = 22
user = "root"
password = "fB79w8ePw8mEJxH2"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(host, port, user, password)
    
    # Faz um curl na Evolution API localmente para ver se ela responde
    curl_cmd = """curl --location 'http://127.0.0.1:8080/instance/connectionState/Martines-Produtos-digitais' \
--header 'apikey: rdo-evolution-secret-2026'"""
    
    stdin, stdout, stderr = client.exec_command(curl_cmd)
    
    output = stdout.read().decode('utf-8', errors='ignore')
    errs = stderr.read().decode('utf-8', errors='ignore')
    
    with open("evo_test.txt", "w", encoding="utf-8") as f:
        f.write("=== OUTPUT ===\n" + output)
        f.write("\n=== ERRS ===\n" + errs)
    print("Teste CURL finalizado e salvo em evo_test.txt")
finally:
    client.close()
