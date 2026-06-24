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
    stdin, stdout, stderr = client.exec_command("docker inspect $(docker ps -q) | jq '[.[] | {Name: .Name, Config: .Config.Labels}]'")
    print(stdout.read().decode('utf-8', errors='ignore'))
finally:
    client.close()
