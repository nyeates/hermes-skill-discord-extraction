---
name: discord-extraction
description: Interactively export Discord chat history using DiscordChatExporter.
---

# Discord Extraction Skill

## Purpose
A specialized skill for safely and interactively exporting Discord chat history using the open-source **DiscordChatExporter** engine. It provides a guided workflow to select servers, channels, and date ranges, ensuring your credentials remain local and secure.

## Installation & Setup

### 1. Requirement: DiscordChatExporter CLI
The skill requires the `DiscordChatExporter.Cli` executable.
- **Automatic Install:** Running the skill for the first time will attempt to detect if it's in your `PATH` or `~/.hermes/tools/DiscordChatExporter/`. If not found, it will download the correct macOS arm64 release from GitHub automatically.
- **Manual Install:** If you prefer to manage it yourself, place `DiscordChatExporter.Cli` in `~/.hermes/tools/DiscordChatExporter/`.

### 2. Credential Setup (Security First)
**Never hardcode your Discord token.** This skill uses a local environment file to keep your token out of chat logs and LLM prompts.

1. Navigate to `~/.hermes/secrets/`.
2. Create (or edit) a file named `discord-extraction.env`.
3. Add your token in the following format:
   ```env
   DISCORD_TOKEN=***   ```
4. Ensure the file permissions are restricted: `chmod 600 ~/.hermes/secrets/discord-extraction.env`.

## How to Use

To start an interactive export, run the following command from your terminal:

```bash
python3 ~/.hermes/skills/social-media/discord-extraction/extractor.py
```

### Workflow
1. **Auth Check:** The script verifies your token exists locally.
2. **Discovery:** 
   - It attempts to list your accessible **Guilds (Servers)**. Select one from the list.
   - It attempts to list **Channels** within that guild. Select one.
   - *Note: If discovery fails, you can enter IDs manually.*
3. **Configuration:**
   - Set a **Start Date** and **End Date** (`YYYY-MM-DD`).
   - Choose whether to download **Media/Assets** (Yes/No).
   - Choose the output format (JSON and HTML are both generated).
4. **Safety Check:** The script will summarize the planned export and ask for confirmation before proceeding.
5. **Execution:** The export runs. Large histories may take several minutes.

## Outputs
Exports are organized cleanly in:
`~/exports/discord/<server_name>/<channel_name>/<date_range>/`

Each export folder contains:
- `export_<channel_id>.json`: Machine-readable data.
- `export_<channel_id>.html`: Human-readable, styled chat view.
- `metadata.json`: Details about the extraction (timestamp, IDs, date range, etc.).

## Pitfalls
- **CLI Argument Ordering:** The `DiscordChatExporter.Cli` is sensitive to argument order. The authentication token (`-t` or `--token`) **must** follow the specific command (e.g., `discord-chat-exporter-cli guilds -t <token>`). Placing it before the command or as a global flag may result in an `Unrecognized option(s)` error.
- **Token Permissions:** If you encounter "Unauthorized" errors, ensure your token is a valid user token and that the account has access to the requested guilds/channels.

## Security & Safety
- **Read-Only:** This skill only uses "view" and "export" commands. It will **not** send, edit, or delete any messages.
- **Zero-Leak Policy:** The `DISCORD_TOKEN` is read strictly within the local Python script and is never exposed to the LLM or printed to the terminal.
- **Metadata Privacy:** The generated `metadata.json` files are automatically created with all relevant IDs but **redact the token**.
