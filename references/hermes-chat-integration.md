# Hermes chat integration notes

## Goal
Bring the existing `extractor.py` workflow into Hermes chat without forcing the user to manually launch the Python script and answer `input()` prompts in a terminal.

## Key lesson
Do not treat this as a PTY/terminal problem first. Treat it as an interface split:
- Hermes chat should own user interaction.
- `extractor.py` (or a refactored successor) should own local execution against DiscordChatExporter.

## Why PTY is not the default answer
A PTY can show the existing guild list, channel list, and prompt text, but Hermes chat replies are not automatically connected to the subprocess stdin. To make PTY mirroring work, the agent would have to:
1. start the script as an interactive process,
2. read terminal output,
3. detect when input is requested,
4. ask the user in chat,
5. map the reply back into the process via stdin submission,
6. repeat for every prompt.

This is possible, but it is brittle and unnecessarily complex for this workflow.

## Preferred architecture
### 1. Refactor the script into backend functions
Suggested logical split:
- `list_guilds()`
- `list_channels(guild_id)`
- `run_export(guild_id, channel_id, after, before, media)`

### 2. Support non-interactive arguments
Add a mode that accepts arguments such as:
- `--guild-id`
- `--channel-id`
- `--after`
- `--before`
- `--media`

The current interactive CLI can remain as a local convenience mode.

### 3. Let Hermes collect inputs in chat
Hermes should:
1. list guilds,
2. ask the user which guild to use,
3. list channels for that guild,
4. ask which channel to use,
5. ask for dates/media,
6. run the backend mode with those answers.

## Recommendation
Keep PTY as a fallback only if terminal-emulation behavior is explicitly desired. For normal Hermes usage, the simplest and most robust design is:
- chat-native questions in Hermes,
- parameterized backend execution in Python.

## Planning hygiene
Do not conflate:
- progress-bar/display questions, and
- user-input / interface-design questions.

Plan them separately.