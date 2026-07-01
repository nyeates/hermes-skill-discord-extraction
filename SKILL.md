---
name: discord-extraction
category: social-media
description: Interactively exports Discord chat history to CSV using DiscordChatExporter.
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
python3 ~/.hermes/skills/social-media/discord-extraction/scripts/extractor.py
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
4. **Simulated Command:** The script will display a redacted version of the command to be executed for your review.
5. **Execution:** The script performs a CSV export to the organized directory.
6. **Simplification (Optional):** To remove excess noise (emojis, repetitive timestamps) from the raw CSV, run the local simplification utility:
    ```bash
    python3 ~/.hermes/skills/social-media/discord-extraction/scripts/simplify.py <path_to_csv>
    ```
7. **Hermes Chat Integration Planning:** When bringing this workflow into Hermes chat, keep the plan simple: Hermes should ask the user for guild/channel/date inputs itself, and the extraction script should act as a parameterized backend. Avoid trying to mirror `input()` prompts through a PTY unless you explicitly want terminal-emulation behavior. See `notes/hermes-chat-integration.md`.

## Outputs
Exports are organized cleanly in:
`~/exports/discord/<server-name>/<channel-name>/<date-range>/`

Each export folder contains:
- `export_<channel_id>.csv`: Machine-readable CSV data.
- `metadata.json`: Details about the extraction (timestamp, IDs, date range, etc.).

## Security & Safety
- **Read-Only:** This skill only uses "view" and "export" commands. It will **not** send, edit, or delete any messages.
- **Zero-Leak Policy:** The `DISCORD_TOKEN` is read strictly within the local Python script and is never exposed to the LLM or printed to the terminal.
- **Metadata Privacy:** The generated `metadata.json` contains all relevant IDs but **redacts the token**.

## Troubleshooting & Implementation Details
For specific troubleshooting steps regarding CLI argument ordering or format string requirements, refer to the [Debugging Notes](notes/debugging-notes.md).
For Hermes-facing integration design notes, refer to [Hermes Chat Integration](notes/hermes-chat-integration.md).

## Repo Content Scope
- Keep `SKILL.md` simple and functional.
- Do not embed private rationale, job-application framing, migration plans, or chat-specific troubleshooting into the repo artifact unless it directly helps future users of the skill.
- Prefer repo-relevant workflow guidance over meta-commentary about how the conversation unfolded.

## Pitfalls
- **Do not conflate progress-display planning with user-input integration planning.** Treat them as separate concerns.
- **Do not default to PTY relay for Hermes chat integration.** PTY can expose interactive prompts, but chat replies are not automatically wired to the subprocess stdin. That path requires output parsing plus `process submit` orchestration and is more brittle than necessary.
- **Prefer a split architecture for Hermes integration:**
  1. Keep DiscordChatExporter as the extraction engine.
  2. Refactor the Python wrapper into reusable functions / non-interactive arguments.
  3. Let Hermes ask the questions in chat (guild, channel, dates, media).
  4. Invoke the wrapper in non-interactive mode with those collected parameters.
- **Use PTY only when terminal-emulation behavior is specifically desired.** It is a fallback, not the default design.
- **For human-readable exports, prefer CSV plus a post-processing simplifier over raw JSON.** JSON exports are bulky and hard to skim for conversation-only review; keep the exporter focused on CSV when the downstream workflow is text simplification.
- **DiscordChatExporter format names are exact enums.** Use supported values such as `Csv`, `Json`, `HtmlDark`, or `HtmlLight`; plain `Html` is rejected.
