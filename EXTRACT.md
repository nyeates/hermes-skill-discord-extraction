# EXTRACT.md

## Purpose
This file covers the operational extraction workflow for exporting Discord data with **DiscordChatExporter**.

Use this file when you need to:
- install or verify the exporter CLI
- configure the local Discord token
- run an interactive export
- understand output files and folder structure
- troubleshoot extraction-specific issues

## Requirement: DiscordChatExporter CLI
The workflow requires the `DiscordChatExporter.Cli` executable.

### Install detection
The local workflow should first check standard locations such as:
- current `PATH`
- `DiscordChatExporter.Cli`
- `discord-chat-exporter-cli`
- `~/tools/DiscordChatExporter`
- `~/tools/DiscordChatExporter.Cli`
- `~/.hermes/tools/DiscordChatExporter`

### Local install location
Preferred install location:
`~/.hermes/tools/DiscordChatExporter/`

### Install behavior
- If the CLI is already present and working, reuse it.
- If it is missing, install the correct official CLI release for the current OS and CPU architecture.
- Prefer the CLI zip release, not the GUI build.

## Credential setup
**Never hardcode the Discord token.** Keep it in a local env file.

Recommended file:
`~/.hermes/secrets/discord-extraction.env`

Format:
```env
DISCORD_TOKEN=***
```

Also keep an example file for setup guidance.

Recommended permissions:
```bash
chmod 600 ~/.hermes/secrets/discord-extraction.env
```

## Run the interactive exporter
Run:
```bash
python3 ~/.hermes/skills/social-media/discord-extraction/scripts/extractor.py
```

## Interactive workflow
1. **Auth check**
   - Verify that `DISCORD_TOKEN` exists locally.
2. **Guild discovery**
   - List accessible guilds/servers.
   - Let the user choose from the list.
3. **Channel discovery**
   - List channels for the selected guild.
   - Let the user choose a channel/thread/forum target.
   - If discovery fails, allow manual ID entry.
4. **Export configuration**
   - Ask for start date and end date (`YYYY-MM-DD` at minimum).
   - Ask whether to download media/assets.
5. **Command preview**
   - Show a redacted version of the command before execution.
6. **Export execution**
   - Run the export and save results into the organized output folder.
7. **Optional simplification**
   - Post-process the CSV if a cleaner human-readable artifact is needed.

## Optional post-processing
To simplify raw CSV output:
```bash
python3 ~/.hermes/skills/social-media/discord-extraction/scripts/simplify.py <path_to_csv>
```

## Outputs
Save exports under a structure like:
`~/exports/discord/<server-name>/<channel-name>/<date-range>/`

Typical files:
- `export_<channel_id>.csv` — exported chat data
- `metadata.json` — extraction metadata

## Metadata expectations
`metadata.json` should include:
- extraction timestamp
- DiscordChatExporter version, if available
- server name and ID
- channel name and ID
- date range
- output formats and paths
- approximate message counts if easy to determine
- executed command with token redacted

## Safety and reliability
- Extraction is **read-only**.
- Do not send, edit, delete, or react to messages.
- Do not print the token.
- Keep token handling local to the script.
- Redact token values from command previews and metadata.
- Avoid overwriting old exports unless explicitly approved.
- Prefer resumable/reusable export behavior where practical.
- Before a large export, prefer a small safe test export.

## Extraction-specific pitfalls
- Prefer **CSV plus simplification** for readable review when raw JSON is too bulky.
- DiscordChatExporter format names are exact enums; unsupported names like plain `Html` can fail.
- Discovery may fail in some cases; manual guild/channel IDs should remain a fallback.

## Related files
- `ANALYSIS.md` — use after export when the goal is interpretation rather than extraction
- `notes/debugging-notes.md` — extraction troubleshooting details
- `notes/hermes-chat-integration.md` — notes on future Hermes-native interaction design
