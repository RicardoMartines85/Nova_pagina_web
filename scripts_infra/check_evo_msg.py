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
    
    # Payload for the message
    payload = {
        "number": "12036341054197321@g.us",
        "textMessage": {"text": "Teste de diagnóstico via SSH"}
    }
    payload_str = json.dumps(payload).replace('"', '\\"')
    
    # curl command to Evolution API
    curl_cmd = f"""curl -X POST 'http://127.0.0.1:8080/message/sendText/MartinesPS-3' \
-H 'apikey: rdo-evolution-secret-2026' \
-H 'Content-Type: application/json' \
-d "{payload_str}" --max-time 15"""
    
    stdin, stdout, stderr = client.exec_command(curl_cmd)
    
    output = stdout.read().decode('utf-8', errors='ignore')
    errs = stderr.read().decode('utf-8', errors='ignore')
    
    with open("evo_msg_test.txt", "w", encoding="utf-8") as f:
        f.write("=== OUTPUT ===\n" + output)
        f.write("\n=== ERRS ===\n" + errs)
finally:
    client.close()
