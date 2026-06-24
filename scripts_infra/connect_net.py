import paramiko

host = "216.22.43.39"
port = 22
user = "root"
password = "fB79w8ePw8mEJxH2"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(host, port, user, password)
    
    # Connect n8n to the web_net network
    stdin, stdout, stderr = client.exec_command("docker network connect web_net n8n_standalone-n8n-1")
    out = stdout.read().decode('utf-8', errors='ignore')
    err = stderr.read().decode('utf-8', errors='ignore')
    
    with open("connect_net.txt", "w", encoding="utf-8") as f:
        f.write("OUT: " + out + "\nERR: " + err)
finally:
    client.close()
