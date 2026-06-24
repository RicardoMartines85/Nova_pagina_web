import paramiko

host = "216.22.43.39"
port = 22
user = "root"
password = "fB79w8ePw8mEJxH2"

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    client.connect(host, port, user, password)
    
    # Install runlike
    client.exec_command("pip3 install runlike || pip install runlike")
    
    # Get run command
    stdin, stdout, stderr = client.exec_command("runlike opt-evolution-api-1")
    run_cmd = stdout.read().decode('utf-8', errors='ignore')
    
    with open("evo_run_cmd.txt", "w", encoding="utf-8") as f:
        f.write(run_cmd)
finally:
    client.close()
