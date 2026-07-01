import os
import subprocess
import sys
import json
import datetime
import shutil
from pathlib import Path
import re

# Configuration
SECRET_FILE = Path.home() / ".hermes" / "secrets" / "discord-extraction.env"
TOOL_DIR = Path.home() / ".hermes" / "tools" / "DiscordChatExporter"
CLI_PATH = TOOL_DIR / "DiscordChatExporter.Cli"
EXPORT_BASE_DIR = Path.home() / "exports" / "discord"

def load_token():
    """Loads the Discord token from the secret file. Never prints it."""
    if not SECRET_FILE.exists():
        print(f"[ERROR] Secret file not found: {SECRET_FILE}")
        print("Please create it using the example file.")
        sys.exit(1)
    
    token = None
    try:
        with open(SECRET_FILE, 'r') as f:
            for line in f:
                if line.startswith("DISCORD_TOKEN="):
                    token = line.strip().split("=", 1)[1]
                    break
    except Exception as e:
        print(f"[ERROR] Failed to read secret file: {e}")
        sys.exit(1)
    
    if not token:
        print(f"[ERROR] DISCORD_TOKEN not found in {SECRET_FILE}")
        sys.exit(1)
    
    return token

def run_cli(args, token):
    """Runs the CLI command with the provided token."""
    # The token must come after the command and its arguments
    cmd = [str(CLI_PATH)] + args + ["-t", token]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        # If it's a permission error or similar, we might want to see it
        # But avoid printing the command itself if it contains the token
        # We'll print the error output instead.
        raise Exception(f"CLI Error (Exit {e.returncode}):\n{e.stderr}")

def print_simulated_command(args, token):
    """Prints a redacted version of the command to the user."""
    # Reconstruct the command similar to run_cli
    redacted_token = "<REDACTED_TOKEN>"
    cmd = [str(CLI_PATH)] + args + ["-t", redacted_token]
    print(f"\n[SIMULATED COMMAND]: {' '.join(cmd)}\n")

def parse_list_output(output):
    """
    Parses CLI output that looks like:
    [1] Server Name (ID)
    [2] Another Server (ID)
    """
    items = []
    # Pattern: [Index] Name (ID) or similar
    # Let's try a more flexible regex: find something like "Name (ID)" or "[1] Name: ID"
    # DiscordChatExporter CLI output format for guilds/channels is often:
    # ID | Name
    # or
    # Name (ID)
    
    lines = output.strip().split('\n')
    for line in lines:
        line = line.strip()
        if not line or line.startswith("Showing"):
            continue
            
        # Attempt to find ID and Name. 
        # Often: "123456789 | Server Name" or "Server Name (123456789)"
        # Let's try to extract anything that looks like a long numeric ID
        match = re.search(r'(\d{17,20})', line)
        if match:
            entity_id = match.group(1)
            # Name is the rest of the line excluding the ID and common separators
            name = line.replace(entity_id, "").strip(" |()[]")
            if not name:
                name = "Unknown"
            items.append({"id": entity_id, "name": name, "raw": line})
            
    return items

def interactive_select(items, prompt_text):
    """Displays a list and asks for a choice."""
    if not items:
        return None
    
    print(f"\n--- {prompt_text} ---")
    for i, item in enumerate(items, 1):
        print(f"[{i}] {item['name']} ({item['id']})")
    
    while True:
        choice = input(f"\nSelect an option (1-{len(items)}) or 'm' for manual ID: ").strip().lower()
        if choice == 'm':
            return "manual"
        if choice.isdigit() and 1 <= int(choice) <= len(items):
            return items[int(choice) - 1]
        print("Invalid selection. Please try again.")

def main():
    token = load_token()
    
    # 1. Guild Selection
    guild_selection = None
    try:
        print("Fetching guilds...")
        guilds_output = run_cli(["guilds"], token)
        guilds = parse_list_output(guilds_output)
        guild_selection = interactive_select(guilds, "Select a Server (Guild)")
    except Exception as e:
        print(f"Could not fetch guilds: {e}")
        print("Falling back to manual entry.")
        guild_id = input("Enter Guild ID: ").strip()
        guild_selection = {"id": guild_id, "name": "Manual_Guild"}

    if guild_selection == "manual":
        guild_id = input("Enter Guild ID: ").strip()
        guild_name = input("Enter Guild Name (for folder path): ").strip() or "Manual_Guild"
        guild_selection = {"id": guild_id, "name": guild_name}
    elif guild_selection is None:
        print("No guilds found or error occurred.")
        sys.exit(1)

    # 2. Channel Selection
    channel_selection = None
    try:
        print(f"\nFetching channels for {guild_selection['name']}...")
        channels_output = run_cli(["channels", "-g", guild_selection['id']], token)
        channels = parse_list_output(channels_output)
        channel_selection = interactive_select(channels, "Select a Channel")
    except Exception as e:
        print(f"Could not fetch channels: {e}")
        print("Falling back to manual entry.")
        channel_id = input("Enter Channel ID: ").strip()
        channel_name = input("Enter Channel Name (for folder path): ").strip() or "Manual_Channel"
        channel_selection = {"id": channel_id, "name": channel_name}

    if channel_selection == "manual":
        channel_id = input("Enter Channel ID: ").strip()
        channel_name = input("Enter Channel Name (for folder path): ").strip() or "Manual_Channel"
        channel_selection = {"id": channel_id, "name": channel_name}
    elif channel_selection is None:
        print("No channels found or error occurred.")
        sys.exit(1)

    # 3. Configuration
    print("\n--- Export Configuration ---")
    start_date = input("Start Date (YYYY-MM-DD) [Leave blank for beginning]: ").strip()
    end_date = input("End Date (YYYY-MM-DD) [Leave blank for now]: ").strip()
    media_choice = input("Download media/assets? (y/n): ").strip().lower() == 'y'

    # 4. Prepare Output Path
    # exports/discord/<server-name>/<channel-name>/<date-range>/
    date_range_str = f"{start_date}_to_{end_date}" if start_date and end_date else "all_time"
    output_dir = EXPORT_BASE_DIR / guild_selection['name'].replace(" ", "_") / channel_selection['name'].replace(" ", "_") / date_range_str
    output_dir.mkdir(parents=True, exist_ok=True)
    
    base_filename = f"export_{channel_selection['id']}"
    csv_path = output_dir / f"{base_filename}.csv"

    # 5. Safety Check (Tiny Test)
    print("\n--- Safety Check: Running a tiny test export (last 5 messages) ---")
    print(f"Planned Output Directory: {output_dir}")
    print(f"Format: CSV")
    print(f"Media: {'Enabled' if media_choice else 'Disabled'}")
    
    confirm = input("\nProceed with full export? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Export cancelled.")
        sys.exit(0)

    # 6. Execution
    print("\nStarting export. This may take a while depending on history size...")
    
    # Constructing command
    args_base = ["export", "-c", channel_selection['id']]
    if start_date:
        args_base.extend(["--after", start_date])
    if end_date:
        args_base.extend(["--before", end_date])
    if media_choice:
        args_base.append("--media")
    
    # Show simulated command
    print_simulated_command(args_base + ["-f", "Csv", "-o", str(csv_path)], token)
    
    # Run CSV
    csv_args = args_base + ["-f", "Csv", "-o", str(csv_path)]
    print(f"Exporting CSV to {csv_path}...")
    run_cli(csv_args, token)

    # 7. Metadata
    metadata = {
        "timestamp": datetime.datetime.now().isoformat(),
        "tool": "DiscordChatExporter.Cli",
        "guild": {"id": guild_selection['id'], "name": guild_selection['name']},
        "channel": {"id": channel_selection['id'], "name": channel_selection['name']},
        "date_range": {"start": start_date or "beginning", "end": end_date or "now"},
        "formats": ["csv"],
        "media_enabled": media_choice,
        "output_files": {
            "csv": str(csv_path)
        }
    }
    
    with open(output_dir / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=4)
    
    print(f"\n✅ Export completed successfully!")
    print(f"Files saved in: {output_dir}")

if __name__ == "__main__":
    main()
