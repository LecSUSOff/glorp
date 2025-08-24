import sys
import base64
import requests
import os
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

SERVER_URL = "https://lecsusoff.pythonanywhere.com/"
console = Console()

def upload_file(module_name: str):
    filename = f"{module_name}.glorp"
    if not os.path.isfile(filename):
        console.print(f"[bold red][!] File '{filename}' not found.[/]")
        return

    with open(filename, 'rb') as f:
        content = f.read()

    content_b64 = base64.b64encode(content).decode()

    with Progress(
        SpinnerColumn(),
        "[progress.description]{task.description}",
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Uploading...", total=len(content))

        # Fake progress bar (for UX), since upload is one request
        for i in range(0, len(content), max(1, len(content)//50)):
            progress.update(task, advance=i)
        response = requests.post(f"{SERVER_URL}/upload", json={
            "filename": filename,
            "content": content_b64
        })
        progress.update(task, completed=len(content))

    if response.ok:
        console.print(f"[bold green][+] {response.json().get('message', 'Upload complete')}[/]")
    else:
        console.print(f"[bold red][!] {response.json().get('error', 'Upload failed')}[/]")


def download_file(module_name: str):
    filename = f"{module_name}.glorp"
    url = f"{SERVER_URL}/get/{filename}"

    with console.status(f"[cyan]Downloading {filename}..."):
        response = requests.get(url, stream=True)

    if response.status_code != 200:
        console.print(f"[bold red][!] Error: {response.text}[/]")
        return

    total_size = int(response.headers.get("Content-Length", 0))
    chunk_size = 1024

    with open(filename, 'w', encoding='utf-8') as f, Progress(
        SpinnerColumn(),
        "[progress.description]{task.description}",
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Downloading...", total=total_size)

        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk.decode("utf-8"))
                progress.update(task, advance=len(chunk))

    console.print(f"[bold green][+] File '{filename}' downloaded successfully.[/]")


def main():
    if len(sys.argv) != 3:
        console.print("[yellow]Usage:[/]\n  glorppkg upload <module>\n  glorppkg get <module>")
        return

    command, module_name = sys.argv[1], sys.argv[2]

    if command == "upload":
        upload_file(module_name)
    elif command == "get":
        download_file(module_name)
    else:
        console.print("[bold red]Unknown command. Use 'upload' or 'get'.")


if __name__ == "__main__":
    main()
