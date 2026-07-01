# DiscordChatExporter CLI Troubleshooting & Implementation Notes

This file contains specific implementation details and pitfalls encountered during the development of the `discord-extraction` skill.

## Command Argument Ordering
The `DiscordChatExporter.Cli` tool is sensitive to argument order. The authentication token (`-t` or `--token`) must be provided **after** the specific command and its associated arguments.

**Incorrect:**
`DiscordChatExporter.Cli -t <token> guilds`

**Correct:**
`DiscordChatExporter.Cli guilds -t <token>`

## Format String Requirements
When using the `export` command, the format flag `-f` is case-sensitive and requires specific strings. 
- Using `Html` will result in a `System.ArgumentException: Requested value 'Html' was not found.`
- Use `HtmlDark` for the standard dark-themed HTML export.
- Use `Csv` for comma-separated value exports.
- Use `Json` for machine-readable JSON.

## Post-Processing Workflow
While the CLI provides raw exports, the data can be noisy (excessive timestamps, emojis, etc.). 
- Use the local `simplify.py` script to transform the raw CSV output into a cleaner, more readable format.
