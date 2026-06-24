import paramiko

host = "216.22.43.39"
port = 22
user = "root"
password = "fB79w8ePw8mEJxH2"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(host, port, user, password)
    
    # Faz um curl na Evolution API localmente para mandar a mensagem direto
    curl_cmd = """curl --location 'http://127.0.0.1:8080/message/sendText/Martines-Produtos-digitais' \
--header 'apikey: rdo-evolution-secret-2026' \
--header 'Content-Type: application/json' \
--data '{
    "number": "120363410541197321@g.us",
    "text": "🤖 Oi! Esse é um teste direto do Servidor Central. Se você leu isso, a Evolution está 100% perfeita!"
}'"""
    
    stdin, stdout, stderr = client.exec_command(curl_cmd)
    
    output = stdout.read().decode('utf-8', errors='ignore')
    errs = stderr.read().decode('utf-8', errors='ignore')
    
    with open("evo_send.txt", "w", encoding="utf-8") as f:
        f.write("=== OUTPUT ===\n" + output)
        f.write("\n=== ERRS ===\n" + errs)
    print("Teste CURL de envio finalizado.")
finally:
    client.close()
