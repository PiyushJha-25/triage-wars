import subprocess
import sys
import os
import time

def install_pyngrok():
    print("Installing pyngrok...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyngrok"])

if __name__ == "__main__":
    install_pyngrok()
    
    from pyngrok import ngrok
    
    token = os.environ.get("NGROK_AUTH_TOKEN")
    if not token:
        print("Error: NGROK_AUTH_TOKEN environment variable not set.")
        sys.exit(1)
        
    print("Authenticating with ngrok...")
    ngrok.set_auth_token(token)
    
    print("Starting HTTP tunnel on port 8080...")
    tunnel = ngrok.connect(8080)
    
    print(f"\n{'='*40}")
    print(f"TUNNEL URL: {tunnel.public_url}")
    print(f"{'='*40}\n")
    print("Press Ctrl+C to shut down the tunnel.")
    
    try:
        # Keep the script running to keep the tunnel alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down tunnel...")
        ngrok.kill()
