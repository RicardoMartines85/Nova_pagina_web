import paramiko

host = "216.22.43.39"
port = 22
user = "root"
password = "fB79w8ePw8mEJxH2"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(host, port, user, password)
    stdin, stdout, stderr = client.exec_command("cat /opt/landing-page/vite.config.ts")
    print("STDOUT:", stdout.read().decode('utf-8', errors='ignore'))
    
    stdin, stdout, stderr = client.exec_command("docker run --rm --entrypoint cat opt-landing-page /app/vite.config.ts")
    print("DOCKER STDOUT:", stdout.read().decode('utf-8', errors='ignore'))
finally:
    client.close()
