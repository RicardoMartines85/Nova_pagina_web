import paramiko

host = "216.22.43.39"
port = 22
user = "root"
password = "fB79w8ePw8mEJxH2"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(host, port, user, password)
    
    # Testa o envio direto para a nova instância 'num_MartinesPS' via CURL interno
    curl_cmd = """curl --location 'http://127.0.0.1:8080/message/sendText/num_MartinesPS' \
--header 'apikey: rdo-evolution-secret-2026' \
--header 'Content-Type: application/json' \
--data '{
    "number": "120363410541197321@g.us",
    "text": "🤖 Oi! Teste direto do Servidor Central pela instância nova!"
}'"""
    
    print("Enviando requisição CURL...")
    stdin, stdout, stderr = client.exec_command(curl_cmd)
    
    output = stdout.read().decode('utf-8', errors='ignore')
    errs = stderr.read().decode('utf-8', errors='ignore')
    
    with open("evo_send_2.txt", "w", encoding="utf-8") as f:
        f.write("=== OUTPUT ===\n" + output)
        f.write("\n=== ERRS ===\n" + errs)
    print("Teste CURL de envio finalizado.")
finally:
    client.close()
