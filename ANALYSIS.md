# ANALYSIS.md

## Purpose

This file describes a repeatable approach for analyzing large Discord community exports and turning raw chat into useful product, support, community, and documentation intelligence.

Use this after following `EXTRACT.md` to produce the export input for analysis.

The goal is not to summarize “what people talked about.” The goal is to identify durable patterns:

- who appears active and what informal or formal roles they play
- what users repeatedly ask, misunderstand, praise, or complain about
- where staff, moderators, or power users appear overloaded
- where documentation, onboarding, UX, pricing, support, or product communication may be unclear
- which user segments are underserved
- which quotes and examples best support the findings
- what caveats prevent overclaiming

This analysis should treat Discord as a directional community sample, not a complete view of an organization’s users, product, or operations.

## Input assumptions

Discord exports may vary widely. The analysis should adapt to the available structure.

The input may be a raw export or a simplified derivative, but it should preserve enough structure to trace findings back to source dates, channels, speakers, and raw references where possible.

Common useful fields include:

- date or timestamp
- channel name
- thread name
- speaker / username
- message text
- reply or mention markers
- attachments, links, or embeds
- reactions, if available

If the export lacks stable message links, time-of-day timestamps, channel metadata, or reply threading, state that limitation clearly. Do not invent precision that the source does not support.

If only day-level timestamps are available, cite by date plus raw reference and avoid response-lag claims more precise than the source allows.

## High-level workflow

Use a map → reduce → synthesize workflow.

1. **Parse and normalize** the export.
2. **Chunk** messages into manageable time windows.
3. **Extract** themes, user roles, issues, quotes, and signals from each chunk.
4. **Roll up** chunk findings into weekly or monthly summaries.
5. **Synthesize** durable cross-period patterns.
6. **Write** a concise, evidence-based report with caveats.

For large communities, avoid feeding the entire export into one prompt. Chunking reduces context loss, makes evidence easier to trace, and prevents one loud day from dominating the analysis.

## Parsing and normalization

Before analysis, normalize the export into a predictable structure.

Recommended message object:

```json
{
  "date": "YYYY-MM-DD",
  "time": "HH:MM:SS or null",
  "channel": "channel-name or null",
  "thread": "thread-name or null",
  "speaker": "username",
  "text": "message text",
  "links": [],
  "attachments": [],
  "raw_reference": "line number, message id, or source pointer"
}
```

Preserve raw references where possible. Later findings should be traceable back to dates, users, line numbers, or message links.

Normalize obvious export artifacts, but do not over-clean the text. Typos, repeated phrasing, and user frustration often contain useful signal.

Before close reading, it can help to generate lightweight scaffolding such as top speakers, question counts, keyword buckets, and response-like concentration. Use this to guide sampling, not as the conclusion.

## Chunking strategy

Choose chunk size based on volume.

Recommended options:

- **Daily chunks** for very active communities.
- **Weekly chunks** for medium-volume communities.
- **Monthly chunks** only for lower-volume communities.

Each chunk-level pass should extract:

- recurring questions or confusion
- repeated bugs, complaints, or workflow failures
- praise, delight, and signs of strong product/community fit
- staff/mod/power-user interventions
- support routing and escalation patterns
- documentation or onboarding gaps
- product, UX, pricing, API, reliability, or moderation issues
- notable quotes with date, speaker, and source reference
- unresolved or slow-response items
- evidence strength and uncertainty

Avoid treating every one-off complaint as a theme. A strong theme usually appears repeatedly, across multiple users or multiple time windows.

## User and role mapping

Build a map of visible community actors. Do not assume formal job titles unless directly supported.

Useful categories:

- **Official staff**: users with clear organizational usernames, explicit staff roles, or repeated “we/team” product statements.
- **Moderators**: users who enforce rules, route channels, warn about scams, manage conflict, or answer procedural questions.
- **Support responders**: users who direct people to support channels, ask for reproduction steps, handle account issues, or triage bugs.
- **Engineers / technical responders**: users who explain API behavior, integrations, infrastructure, tooling, or product internals.
- **Power users**: high-signal community members who answer questions, share workflows, explain tradeoffs, or test new features.
- **New users**: users asking basic onboarding, setup, pricing, permissions, or “how does this work?” questions.
- **Specialist segments**: builders, creators, moderators, investors, mobile users, enterprise users, roleplay users, privacy-sensitive users, etc., depending on the community.

For each important actor, capture:

- apparent function
- evidence for that function
- topics they commonly handle
- whether the role is direct evidence or inference
- caveats

Be careful with language. Prefer “appears to,” “seems to,” or “functions as” when formal status is uncertain. A prolific responder may still be a volunteer or power user, not staff.

## Distinguishing evidence from inference

Use three evidence levels.

### Direct evidence

A user explicitly says something or staff explicitly states something.

Example: “I cannot find the setting” is direct evidence of at least one user’s confusion.

### Pattern evidence

Multiple users ask similar questions or report similar issues across time.

Example: repeated questions about billing units across several weeks suggest a durable pricing-communication gap.

### Inference

The analysis interprets what the pattern may mean.

Example: repeated billing questions may imply that docs, UI labels, and onboarding are not aligned.

Reports should clearly separate these. Do not present inference as fact.

## Quote selection

Strong quotes should be:

- concise
- representative of a repeated pattern
- emotionally or operationally clear
- traceable to date, speaker, and source reference
- not needlessly embarrassing to an individual user or employee

Avoid overusing spicy quotes. A few strong quotes are better than a wall of drama.

When quoting users, preserve meaning but avoid exposing sensitive personal details. If the report will be public, consider anonymizing usernames or using role labels such as “new user,” “power user,” or “moderator.”

## Timeframe rollups

After chunk extraction, roll up by month or major product period.

Each rollup should include:

- top recurring pain points
- notable new issues
- issues that appear to improve or disappear
- active staff/mod/power-user functions
- strong quotes
- unresolved questions
- confidence level

Useful confidence labels:

- **High confidence**: repeated across users and time windows.
- **Medium confidence**: repeated, but concentrated in one period or user segment.
- **Low confidence**: plausible but based on limited evidence.

## Final synthesis

The final synthesis should answer:

- What does the community consistently value?
- What does the community consistently struggle to understand or use?
- Which user segments appear best served?
- Which user segments appear underserved?
- Where are staff, moderators, or power users repeatedly doing manual translation work?
- Which support, docs, product, or onboarding improvements would likely reduce repeated friction?
- What should not be overclaimed from this sample?

## Suggested report structure

The following structure is a suggested starting template, not a required format. Modify, remove, rename, or reorder sections based on what the data actually shows. The analysis should follow the evidence, not force the evidence into a predetermined report shape.

A general community-analysis report can use this structure:

```md
# Discord Community Analysis

## Executive summary

## Method and caveats

## Map of active users and visible roles

## What is handled well

## Top recurring pain points

## Other patterns and gaps

## Underserved user segments

## Potential leverage areas

## Risks, caveats, and uncertainties

## Appendix: representative evidence
```

For shorter reports, combine “method and caveats” with the executive summary and omit the appendix.

## Writing style

Aim for practical, concise, evidence-based analysis.

Use language that helps the organization improve without sounding accusatory. Prefer:

- “users repeatedly appear confused by…”
- “the community seems to rely on…”
- “this suggests a possible gap in…”
- “a likely leverage area is…”
- “this should be treated as directional, not definitive…”

Avoid:

- “the company failed to…”
- “nobody understands…”
- “staff are bad at…”
- “this proves…”
- “the community is toxic…”

The best report feels like product intelligence, not a dunk thread.

## Potential leverage areas

When proposing improvements, keep them concrete and tied to evidence.

Examples:

- a pricing / plan / credits explainer
- a privacy and data-flow matrix
- a model or feature capability matrix
- a “getting started” guide for new users
- integration quickstarts for common tools
- support macros for repeated questions
- improved incident/status messaging
- community office hours or onboarding sessions
- a recurring voice-of-community digest for product/support teams
- a release-readiness checklist syncing docs, UI labels, support macros, and status messaging

Phrase these as possible leverage areas, not demands.

## Ethics and privacy

Use only data the analyst is authorized to access.

If the community is public or semi-public, still treat users respectfully. Do not expose private personal details, dox users, or include sensitive material unless it is essential and appropriately anonymized.

For external publication, remove or anonymize usernames unless there is a strong reason to keep them. For internal team reports, include enough attribution for the team to trace evidence, but avoid unnecessary callouts.

## Common mistakes

Avoid these failure modes:

- treating Discord as the entire user base
- over-weighting the loudest users
- confusing jokes or memes for product feedback
- counting messages without reading context
- presenting one-off complaints as durable patterns
- ignoring what the community loves
- making staff or moderators look personally blamed for structural issues
- hiding uncertainty
- overloading the report with quotes instead of synthesis
- turning the report into a job pitch or sales deck

## Final checklist

Before publishing or sharing the analysis, confirm:

- the source scope is clearly stated
- the timeframe is clearly stated
- caveats are visible near the top
- direct evidence and inference are separated
- claims are supported by repeated patterns or strong examples
- sensitive details are removed or minimized
- usernames are handled appropriately for the audience
- the report includes both strengths and gaps
- recommendations are practical and proportionate
- the tone is useful rather than accusatory
