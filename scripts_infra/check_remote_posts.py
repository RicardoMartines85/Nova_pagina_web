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
    stdin, stdout, stderr = client.exec_command("cat /opt/blog_data/posts.json")
    content = stdout.read().decode('utf-8', errors='ignore')
    
    print("--- CONTEÚDO BRUTO ---")
    print(content[:1000] + "\n..." if len(content) > 1000 else content)
    
    print("\n--- VALIDAÇÃO JSON ---")
    try:
        data = json.loads(content)
        posts = data if isinstance(data, list) else data.get("posts", [])
        print(f"Total de posts encontrados: {len(posts)}")
        if len(posts) > 0:
            print("Último post inserido:")
            for k, v in posts[0].items():
                print(f"  {k}: {str(v)[:50]}")
    except Exception as e:
        print(f"Erro ao parsear o JSON: {e}")
        
    # Verificar também se o new_post.json falhou
    stdin, stdout, stderr = client.exec_command("cat /tmp/new_post.json")
    new_post = stdout.read().decode('utf-8', errors='ignore')
    if new_post:
        print("\n--- CONTEÚDO DO /tmp/new_post.json ---")
        print(new_post[:1000])

finally:
    client.close()
