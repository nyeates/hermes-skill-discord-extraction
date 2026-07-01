---
name: discord-extraction
category: social-media
description: Export Discord community data and analyze it for product, support, and community insights.
---
# Discord Community Export + Analysis Skill

## Purpose
This skill supports two related workflows:
1. **Discord extraction** — export server, channel, thread, or forum data locally using DiscordChatExporter.
2. **Community analysis** — turn exported Discord data into product, support, onboarding, moderation, and community insights.

## Which file to use
- **`EXTRACT.md`** — use for exporter setup, token setup, running exports, output structure, and extraction safety.
- **`ANALYSIS.md`** — use for interpreting exports, finding durable patterns, mapping visible roles, and writing evidence-based reports.

## Typical workflow
1. Use `EXTRACT.md` to produce a local export.
2. Simplify the export; detailed instructions are in `EXTRACT.md`.
3. Use `ANALYSIS.md` to analyze the resulting data.
   - Default to the cleaned text export for LLM analysis when it preserves enough evidence.
   - Keep the CSV beside it as a forensic fallback for exact timestamps, multiline attribution, links, reactions, and other dropped structure.

## Key repo structure
- `SKILL.md` — router and workflow entrypoint
- `EXTRACT.md` — extraction workflow
- `ANALYSIS.md` — community analysis workflow
- `references/date-range-and-simplify.md` — inclusive date filtering, safe test-export pattern, and `simplify.py` behavior
- `scripts/` — runnable Python helpers
- `notes/` — side notes and implementation notes

## Important boundaries
- Extraction is **read/export only**.
- Keep Discord tokens **local**.
- Do not confuse extraction mechanics with analysis methodology.
- Use `ANALYSIS.md` when the user wants **insights**, not just raw exported data.
