import paramiko

host = '216.22.43.39'
port = 22
user = 'root'
password = 'fB79w8ePw8mEJxH2'

try:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(host, port, user, password)

    stdin, stdout, stderr = client.exec_command('echo "[]" > /opt/blog_data/posts.json')
    stdout.read()
    print('Posts apagados com sucesso no VPS!')
finally:
    client.close()
