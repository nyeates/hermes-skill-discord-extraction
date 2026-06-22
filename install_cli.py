import os
import subprocess
import sys
import shutil
import urllib.request
import zipfile
from pathlib import Path

TOOL_DIR = Path.home() / ".hermes" / "tools" / "DiscordChatExporter"
CLI_NAME = "DiscordChatExporter.Cli"

def check_cli():
    # Check PATH
    if shutil.which(CLI_NAME):
        print(f"Found {CLI_NAME} in PATH.")
        return Path(shutil.which(CLI_NAME))
    
    # Check tool dir
    cli_path = TOOL_DIR / CLI_NAME
    if cli_path.exists():
        print(f"Found {CLI_NAME} in {TOOL_DIR}.")
        return cli_path
    
    return None

def install_cli():
    print(f"Installing {CLI_NAME} to {TOOL_DIR}...")
    TOOL_DIR.mkdir(parents=True, exist_ok=True)
    
    # Get latest release URL for macOS arm64
    try:
        cmd = 'curl -s https://api.github.com/repos/Tyrrrz/DiscordChatExporter/releases/latest | grep "browser_download_url" | grep "Cli" | grep "osx-arm64" | cut -d \'"\' -f 4'
        url = subprocess.check_output(cmd, shell=True).decode().strip()
        if not url:
            raise Exception("Could not find macOS arm64 release URL.")
        print(f"Downloading from {url}...")
    except Exception as e:
        print(f"Error fetching release info: {e}")
        sys.exit(1)

    zip_path = TOOL_DIR / "cli.zip"
    try:
        urllib.request.urlretrieve(url, zip_path)
        print("Unzipping...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(TOOL_DIR)
        zip_path.unlink() # Remove zip
        
        # Ensure executable
        cli_path = TOOL_DIR / CLI_NAME
        if cli_path.exists():
            os.chmod(cli_path, 0o755)
            print(f"Installation complete: {cli_path}")
            return cli_path
        else:
            print("Installation failed: CLI not found in expected directory after unzipping.")
            sys.exit(1)
    except Exception as e:
        print(f"Error during installation: {e}")
        sys.exit(1)

if __name__ == "__main__":
    found = check_cli()
    if found:
        print(f"CLI already installed: {found}")
        # Verify it works
        try:
            subprocess.check_output([str(found), "--help"], stderr=subprocess.STDOUT)
            print("Verification successful.")
        except Exception as e:
            print(f"Verification failed: {e}")
            sys.exit(1)
    else:
        install_path = install_cli()
        # Verify it works
        try:
            subprocess.check_output([str(install_path), "--help"], stderr=subprocess.STDOUT)
            print("Verification successful.")
        except Exception as e:
            print(f"Verification failed: {e}")
            sys.exit(1)
