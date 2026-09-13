import subprocess
import re
import sys

print("[INFO] Starting cloudflared tunnel to http://127.0.0.1:5000...")
proc = subprocess.Popen(
    ['.\\cloudflared.exe', 'tunnel', '--url', 'http://127.0.0.1:5000'],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1
)

url_found = False
for line in iter(proc.stdout.readline, ''):
    sys.stdout.write(line)
    sys.stdout.flush()
    m = re.search(r'https://[a-zA-Z0-9-]+\.trycloudflare\.com', line)
    if m and not url_found:
        tunnel_url = m.group(0)
        with open('tunnel_url.txt', 'w', encoding='utf-8') as f:
            f.write(tunnel_url)
        print(f"\n[OK] TUNNEL_ESTABLISHED: {tunnel_url}\n", flush=True)
        url_found = True

proc.wait()
