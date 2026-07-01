# DiscordChatExporter date-range + simplify notes

## Inclusive date ranges
For a user-requested inclusive range like `2026-06-20` through `2026-06-30`, use:

```bash
--after 2026-06-20 --before 2026-07-01
```

Why:
- `--before` is safer when treated as the day *after* the requested end date.
- This avoids ambiguity around whether `--before 2026-06-30` excludes most of June 30.
- Record both the requested inclusive range and the exact CLI filters used in `metadata.json`.

## Safe export pattern
Before a larger export, run a small same-channel test export for a narrow window (for example one day) to verify:
- auth works
- the target channel is correct
- output paths are correct
- CSV format is readable downstream

## simplify.py contract
The simplify helper should be invoked as:

```bash
python3 ~/.hermes/skills/social-media/discord-extraction/scripts/simplify.py <path_to_csv>
```

Expected behavior:
- accept the CSV path as argv[1]
- write a sibling file named `<csv_stem>_clean.txt`
- preserve date-grouped readable text output for quick review

Analysis note:
- prefer the cleaned `.txt` as the first-pass LLM input when it preserves enough evidence
- keep the CSV alongside it as the source of truth for exact timestamps, links, reactions, and multiline message boundaries if the simplifier is lossy

This matches the documented workflow better than hardcoded `raw.csv` / `clean.txt` paths.
