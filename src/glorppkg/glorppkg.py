import sys
import base64
import requests
import os

SERVER_URL = "https://lecsusoff.pythonanywhere.com/"

def upload_file(module_name):
    filename = f"{module_name}.glorp"
    if not os.path.isfile(filename):
        print(f"[!] File '{filename}' not found.")
        return

    with open(filename, 'rb') as f:
        content_b64 = base64.b64encode(f.read()).decode()

    response = requests.post(f"{SERVER_URL}/upload", json={
        "filename": filename,
        "content": content_b64
    })

    print(response.json().get('message') or response.json().get('error'))

def download_file(module_name):
    filename = f"{module_name}.glorp"
    response = requests.get(f"{SERVER_URL}/get/{filename}")

    if response.status_code != 200:
        print(f"[!] Error: {response.json().get('error')}")
        return

    content_b64 = response.json().get('content')
    if not content_b64:
        print("[!] Missing content in server response.")
        return

    with open(filename, 'wb') as f:
        f.write(base64.b64decode(content_b64))

    print(f"[+] File '{filename}' downloaded successfully.")

def main():
    if len(sys.argv) != 3:
        print("Usage:\n  glorppkg upload <module>\n  glorppkg get <module>")
        return

    command, module_name = sys.argv[1], sys.argv[2]

    if command == "upload":
        upload_file(module_name)
    elif command == "get":
        download_file(module_name)
    else:
        print("Unknown command. Use 'upload' or 'get'.")

if __name__ == "__main__":
    main()
