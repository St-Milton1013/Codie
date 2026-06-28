# Roadmap Patch - Deck Memory, Moxfield Export, Confidence Ratios, And Naming Assistance

Status: roadmap-only, implementation deferred

This patch records four useful product improvements. It does not authorize
schema changes, provider changes, recommendation output changes, or LLM usage
until each item has a contract and tests.

## Patch A - User Deck Analysis Memory

Purpose:

After a user analyzes a deck, Codie should preserve a retrievable copy of the
decklist and analysis context so the user can pull it up later.

Desired behavior:

```text
Import or paste deck.
Resolve cards.
Run evidence comparison.
Save decklist snapshot.
Group or filter saved decks by commander identity.
Display saved runs by date.
Allow the decklist and evidence report to be opened later.
```

Preferred implementation direction:

```text
Use existing user_decks, user_deck_cards, analysis_sessions, and saved_analysis first.
Persist raw_input or canonical exported deck text.
Index by deck_hash, commander_hash, created_at, and saved analysis id.
Treat imported user decks as user-local artifacts, not source/provider evidence.
```

Potential future schema only if existing tables are insufficient:

```text
user_deck_snapshots
user_deck_snapshot_cards
```

Required outputs:

```text
saved deck id
deck name
commander signature or commander hash
deck hash
analysis date
raw decklist text
resolved card rows
linked saved analysis ids
```

Acceptance tests:

```text
analyzed deck can be saved
saved deck can be listed by commander identity
saved deck can be listed by date
saved raw decklist can be retrieved
reimporting identical deck preserves deck_hash stability
unresolved import failure leaves no partial saved deck artifacts
saved deck retrieval does not read provider/source tables
```

Guardrails:

```text
Saved user decks are not tournament evidence.
Saved user decks are not source provider records.
Saved user decks do not alter canonical tournament analytics.
Private user decklists must not be exported or uploaded without explicit action.
```

## Patch B - Moxfield-Compatible Staples Export

Purpose:

When exporting commander staples or evidence card lists, Codie should provide an
option that helps the user upload or share that list through Moxfield.

Desired behavior:

```text
Generate a Moxfield-compatible deck/list export.
Group cards by Codie evidence categories.
Represent usage evidence through labels, sections, or tags where supported.
Preserve source metrics in a sidecar report.
Let the user share the list with others outside Codie.
```

Preferred V1 shape:

```text
Moxfield-compatible text export
JSON sidecar with Codie evidence metrics
Markdown explanation with source links and methodology
manual upload workflow
```

Possible later shape:

```text
Moxfield API upload only if a stable free method exists
explicit local auth/config
no hard-coded tokens
no automatic upload by default
```

Possible tag or section labels:

```text
High Usage
Medium Usage
Low Usage
Commander Specific
Generic Staple
Recent Innovation
Regional Signal
Low Sample Warning
```

Acceptance tests:

```text
staples export emits Moxfield-compatible text
cards are grouped deterministically
usage percentage is preserved in sidecar metadata
source deck/event ids are preserved in sidecar metadata
export does not claim cards should be played
manual upload export does not require network
API upload path is disabled unless explicitly configured
```

Guardrails:

```text
Moxfield exports are sharing artifacts, not evidence sources.
Do not treat uploaded Codie lists as tournament truth.
Do not store or expose Moxfield credentials in code.
Do not depend on Moxfield upload support for core exports.
```

## Patch C - Ratio-Aware Confidence Gating

Purpose:

Confidence should account for both absolute sample count and the percentage of
available data represented. Some commanders or regions have fewer tournament
results, so Codie should avoid hiding all outputs merely because the global
sample count is small.

Current problem:

```text
Minimum deck count alone can understate sparse-but-complete data.
Small metagames may have few tournaments but still have meaningful evidence.
```

Required confidence inputs:

```text
absolute matching deck count
eligible deck count for the selected scope
coverage ratio
event count
date window
region scope
commander scope
source completeness
dedupe completeness
```

Suggested display model:

```text
Show absolute sample size.
Show coverage ratio.
Show confidence tier.
Show a low-data warning when evidence is sparse.
Allow evidence display with warning instead of hard hiding when ratio is high.
```

Allowed wording:

```text
Card appears in 4 of 6 matching decks in the selected window.
The selected scope has limited data; treat this as low-sample evidence.
Coverage is 66.7% of available matching decks.
```

Forbidden wording:

```text
This is proven.
This is optimal despite low data.
The sample is small but definitely correct.
```

Acceptance tests:

```text
absolute sample threshold still works
coverage ratio influences confidence tier
small sample with high coverage shows low-data warning
small sample with low coverage remains anecdotal
confidence output includes numerator and denominator
confidence output includes date window and scope
recommendation scoring cannot hide missing sample warnings
```

## Patch D - LLM-Assisted Naming And Alias Review

Purpose:

Use an LLM as an optional assistant for reducing naming friction, especially
commander aliases, display names, and imported source-name cleanup.

Allowed uses:

```text
suggest possible commander aliases
cluster similar human-entered names for review
identify likely misspellings for review
propose display-name cleanup
draft candidate mappings for alias_registry review
summarize unresolved naming conflicts
```

Reliability model:

```text
LLM writer proposes candidate names, aliases, clusters, or cleanup mappings.
LLM auditor reviews the writer output against deterministic context.
Neither LLM may write directly to project tables.
Only reviewed outputs may enter a human/deterministic approval queue.
```

Writer responsibilities:

```text
produce candidate aliases
explain why each alias may match
identify source strings that triggered the suggestion
mark uncertainty and ambiguity
avoid strategic interpretation
```

Auditor responsibilities:

```text
check candidates against Scryfall-resolved names
check candidates against existing alias_registry entries
flag partner-pair ambiguity
flag single-commander vs partner-pair mismatch
flag unsupported or hallucinated names
reject candidates without source strings
return approve_for_review / reject / needs_human_review
```

Forbidden uses:

```text
LLM output as card identity truth
LLM output as commander identity truth
LLM output writing directly to alias_registry
LLM auditor output writing directly to alias_registry
LLM output bypassing Scryfall resolution
LLM output making strategic claims
LLM output sending private user decklists to cloud services without explicit consent
```

Required review workflow:

```text
source name observed
Scryfall exact or fuzzy resolution attempted
existing alias registry checked
LLM writer suggests candidate only if unresolved or ambiguous
LLM auditor reviews writer output against deterministic context
human or deterministic validator accepts/rejects candidate
accepted alias is persisted with provenance
rejected alias is logged to prevent repeated noise
```

Zero-cost and privacy rules:

```text
Local/free models are preferred.
Cloud LLM use is optional and must be explicitly configured.
Private user decklists must not be sent to a cloud LLM unless the user explicitly opts in.
LLM assistance must be disabled by default for sensitive inputs.
Writer and auditor roles must be independently logged.
The same response object must not be treated as both writer and auditor output.
```

Acceptance tests:

```text
LLM suggestion cannot directly write alias registry
LLM auditor cannot directly write alias registry
writer output without auditor review cannot be persisted
auditor rejection blocks candidate persistence
auditor needs_human_review status requires explicit approval
accepted alias records provenance
rejected alias does not resolve future imports
Scryfall exact match outranks LLM suggestion
ambiguous commander pair requires review
partner order normalization remains deterministic
no private raw deck text is sent when LLM assistance is disabled
```

## Placement

Suggested phase placement:

```text
Deck memory: Phase 11/12 user workflow expansion
Moxfield-compatible staples export: Phase 9 export expansion
Ratio-aware confidence gating: Phase 8 analytics/recommendation confidence patch
LLM-assisted naming review: alias/registry maintenance tooling after deterministic resolver is stable
```

## Shared Non-Goals

```text
Do not generate final strategic recommendations from these patches.
Do not treat user deck memory as tournament evidence.
Do not make Moxfield a required dependency.
Do not make LLMs a source of truth.
Do not add schema before a contract proves it is needed.
```
