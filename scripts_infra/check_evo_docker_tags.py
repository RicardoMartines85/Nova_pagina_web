import paramiko
import json
import urllib.request

host = "216.22.43.39"
port = 22
user = "root"
password = "fB79w8ePw8mEJxH2"

# Get docker hub tags
url = "https://hub.docker.com/v2/repositories/evoapicloud/evolution-api/tags?page_size=50"
req = urllib.request.Request(url)
try:
    response = urllib.request.urlopen(req)
    data = json.loads(response.read().decode('utf-8'))
    tags = [tag['name'] for tag in data['results'] if tag['name'].startswith('v2.2')]
    tags2 = [tag['name'] for tag in data['results'] if tag['name'].startswith('v2')]
    
    with open("evo_docker_tags.txt", "w", encoding="utf-8") as f:
        f.write("v2.2 tags: " + str(tags) + "\nAll v2 tags: " + str(tags2))
except Exception as e:
    with open("evo_docker_tags.txt", "w", encoding="utf-8") as f:
        f.write("Error: " + str(e))
