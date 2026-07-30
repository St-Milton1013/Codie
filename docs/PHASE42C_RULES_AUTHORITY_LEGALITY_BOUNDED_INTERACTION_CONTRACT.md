# Phase 42C - Rules Authority, Legality, and Bounded Interaction Contract

Status: contract only

## Validation Tuple

```text
phase_id: Phase42C
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase42D
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

Phase 42D is reserved for the Local-First Model Profile, Redaction, Consent,
and Routing Contract. It remains blocked until Phase 42C outside validation
returns PASS or PASS WITH REVIEW NOTES.

## Purpose

Phase 42C defines the deterministic Rules Layer boundary for:

```text
versioned rules authority
date-aware card and deck legality
bounded interaction explanations
bounded continuous-effect and dependency analysis
future simulator trace validation
rules citations
explicit unknown and conflict handling
```

The Rules Layer determines whether an official, versioned authority package
supports a conclusion. It does not decide whether a legal line is
strategically desirable.

Phase 42C is documentation-only. It does not acquire rules, parse rules text,
create snapshots, implement legality or interaction services, add schema,
call models, validate live simulator traces, build lessons, or integrate Jin.

## Authority

```text
docs/CODIE_V2_CONSTITUTION.md, Sections 5, 6, 24, 27, and 32 through 35
docs/ROADMAP_PATCH_V2_INTELLIGENCE_PROGRAM_INTAKE.md, Program B
docs/PHASE42A_JIN_THEORY_RULES_CORRECTIONS_CROSS_SPECIFICATION_BOUNDARY_CONTRACT.md
docs/PHASE42B_FIXED_JIN_REGRESSION_CORPUS_SCHEMA_DETERMINISTIC_EVALUATION_CONTRACT.md
```

The preserved
`docs/design_inputs/v2_intelligence_program/CODIE_V2_RULES_LAYER_JUDGE_TRAINING_PROPOSAL.md`
is a design input only.

## Rules Layer Ownership

The Rules Layer owns:

```text
authority package identities and compatibility
rules and Oracle citation resolution
date-aware legality verdict packets
bounded interaction verdict packets
bounded continuous-effect traces
future simulator legality-validation packets
explicit unsupported, stale, missing, and conflict states
```

It does not own:

```text
canonical card identity storage
tournament evidence
analytics or confidence scores
strategic evaluation
recommendations
Theory Corpus claims
Correction Ledger activation
Jin answer wording
arbitrary game-state execution
```

## Domain-Aware Authority Lattice

Authority depends on the question's domain.

| Source class | Governing domain | Final verdict permitted |
|---|---|---:|
| Current official Comprehensive Rules | General procedures, objects, zones, timing, costs, effects, state-based actions, multiplayer rules | Yes |
| Current official Oracle text | Current card wording, characteristics, card-specific instructions | Yes |
| Official format rules, policy, and ban announcements | Format and event legality within effective dates | Yes |
| Official rulings and release notes | Clarification, examples, and transition guidance consistent with current authority | Yes within scope |
| Synchronized Scryfall canonical cache | Local identity, Oracle mirror, legalities, faces, and ruling linkage | Provisional or final only under accepted freshness policy |
| Approved community tools | Discovery, comparison, differential testing, regression candidates | No |
| Community articles, forums, videos, and discussions | Discovery and examples | No |
| User corrections | Issue discovery, supplied facts, regression candidates | No |
| Model output | Explanation draft after deterministic verdict | No |

The lattice is not a numeric popularity score.

## Domain Precedence

### Card Wording

```text
current official Oracle text
then synchronized Scryfall Oracle snapshot
then printed wording as historical or identification context only
```

### General Procedure

```text
current Comprehensive Rules
then current official release notes or rulings
then non-authoritative explanations
```

### Card-Specific Application

```text
current Oracle text plus current Comprehensive Rules
then current official ruling or release note
then community tool output as a validation reference only
```

### Format Legality

```text
official format or tournament authority effective on the evaluation date
then a synchronized Scryfall legality cache
then provider claims as observations only
```

Historical questions use the authority package effective on the requested
date. They never silently use current legality.

## Authority Conflict Rules

Oracle text and the Comprehensive Rules are complementary rather than
automatically conflicting. A bounded analyzer must determine whether:

```text
card text creates a permitted exception
the general rule still controls
material facts are missing
one source snapshot is stale or incompatible
```

An official ruling inconsistent with newer Oracle text or rules is
`STALE_OR_SUPERSEDED_RULING`.

Apparently irreconcilable current official sources produce
`UNKNOWN_OFFICIAL_SOURCE_CONFLICT`, preserve both citations, and block a
definitive verdict.

Community disagreement may create a warning, source-sync request, regression
candidate, or human-review item. It never changes an official verdict.

## Versioned Authority Package Contract

Every future authority package must bind compatible:

```text
ruleset snapshot
Oracle snapshot set
official ruling set
format and legality-policy snapshots
release-note and ban-announcement references
package manifest
```

The package manifest preserves:

```text
authority_package_id
authority_package_version
effective_from
effective_until
ruleset_snapshot_id and content hash
Oracle snapshot-set ID and content hash
ruling snapshot-set ID and content hash
legality-policy snapshot IDs and content hashes
release-note reference IDs
ban-announcement reference IDs
parser and index versions
compatibility status
freshness status
superseded package ID
created_at supplied by the release process
provenance references
caveats
```

An answer may not combine incompatible snapshot versions silently.

## Ruleset Snapshot

A future ruleset snapshot preserves:

```text
ruleset_snapshot_id
source type
official source locator
effective date
retrieved timestamp
content hash
parser version
section-index version
superseded snapshot ID
status
```

This contract does not choose the acquisition location, parser, refresh
cadence, retention policy, or persistence owner.

## Oracle And Ruling References

Rules packets consume accepted canonical card identities and versioned Oracle
references. They do not redefine card identity.

Oracle references preserve:

```text
oracle_id
Oracle snapshot ID
Oracle text and card-face identity reference
effective or retrieved timestamp
content hash
ruling snapshot-set ID
```

Official ruling references preserve publication date, official locator,
related Oracle identity, related ruleset snapshot, status, and supersession.

## Legality-Policy Snapshot

Every legality-policy snapshot preserves:

```text
legality_policy_id
format_id
effective_from
effective_until
banned and restricted entries
deck-construction rules
commander-selection rules
source references
content hash
```

Local event deviations remain separately labeled supplied context and never
become official policy.

## Rules Status Model

Every operation returns one primary categorical status:

```text
CONFIRMED
CONFIRMED_WITH_ASSUMPTIONS
INVALID
LEGAL
ILLEGAL
PARTIALLY_SUPPORTED
UNKNOWN_INSUFFICIENT_FACTS
UNKNOWN_UNRESOLVED_CARD
UNKNOWN_UNSUPPORTED_MECHANIC
UNKNOWN_STALE_RULESET
UNKNOWN_OFFICIAL_SOURCE_CONFLICT
UNKNOWN_DEPENDENCY_CYCLE
UNKNOWN_UNMODELED_CONTINUOUS_EFFECT
UNKNOWN_HISTORICAL_POLICY
NOT_APPLICABLE
```

Rules truth does not receive a percentage confidence score. Coverage,
freshness, assumptions, and unsupported portions remain separate fields.

## Rules Answer Packet

A future rules answer packet preserves:

```text
rules_answer_packet_id and version
request ID
question
format and evaluation date
deck snapshot ID where applicable
game-state snapshot ID where applicable
primary status
verdict
structured explanation
supplied, inferred, missing, and disputed facts
object identities, zones, controllers, owners, and timestamps
issue spots and materiality
ordered analysis steps
official citations
official rulings considered
non-authoritative references considered
assumptions
unknowns
blocked claims
simulator implications
Jin constraints
authority package ID
ruleset, Oracle, and legality-policy snapshot IDs
analyzer version
generated_at supplied by the caller
```

Identical inputs, authority packages, and analyzer versions produce identical
substantive serialization.

## Citation Contract

Material rules conclusions cite applicable:

```text
Oracle snapshot and oracle_id
Comprehensive Rules section or subsection
official ruling and publication date
official release note
format policy section
ban announcement and effective date
```

Every citation preserves source class, authority domain, snapshot ID, exact
locator, subject, effective date, retrieved date, and content hash.

Community references appear under a separate non-authoritative collection.
They never appear as verdict authority.

## Date-Aware Legality

Future legality validation supports:

```text
card legality
historical card legality
card availability by date
commander and color-identity eligibility
partner, background, companion, and related commander configuration
deck size and singleton rules
zone composition
banned and restricted cards
sideboard, companion, and auxiliary-zone handling where supported
event-date policy
explicitly supplied local deviations
```

Required inputs include format ID, evaluation date, commander identities, all
relevant deck zones, and the selected authority package.

A present-day query may explicitly request the active date. Historical deck
or event analysis requires an explicit date and matching policy snapshot.

## Legality Pipeline

```text
resolve canonical card identities
-> select the effective authority package
-> validate commander configuration
-> validate zones and quantities
-> validate color identity
-> validate banned or restricted status
-> validate release and availability date
-> return errors, warnings, unknowns, and citations
```

Legality returns `UNKNOWN`, not `LEGAL`, when identity, historical policy,
required local rules, supported mechanics, or acceptable freshness is
missing.

## Legality Report

A future report preserves:

```text
LEGAL, ILLEGAL, or UNKNOWN
errors with code, card, zone, explanation, and citations
warnings
unknowns
evaluated and unresolved card counts
authority package ID
policy snapshot ID
Oracle snapshot-set ID
evaluation date
validator version
```

Illegal and unknown are distinct. A warning may not silently downgrade an
illegal result to legal.

## Bounded Interaction Analyzer

The analyzer explains a supported interaction from supplied facts. It does
not simulate an arbitrary game.

Required issue-spotting order:

```text
identify objects and zones
identify rules and effects
identify timestamps and dependencies
identify choices, costs, modes, targets, timing, stack, and priority
apply supported replacement and prevention logic
resolve supported spells or abilities
apply supported continuous effects
check supported state-based actions
identify supported triggered abilities
produce the resulting state and unresolved branches
cite authority
```

The analyzer must distinguish supplied, inferred, missing, disputed, hidden,
and unsupported facts.

## Required Interaction Facts

As applicable:

```text
card identities
format and evaluation date
active player and priority holder
turn, phase, and step
owners and controllers
zones and timestamps
tapped and summoning-sickness state
counters and attachments
copied values
stack objects
prior events
choices, costs, modes, and targets
```

Missing a material fact returns a specific unknown state and lists what is
needed to resolve it.

## Bounded Continuous Effects

Future first-scope analysis may cover curated, explicitly represented:

```text
copy effects
control-changing effects
text-changing effects
type-changing effects
color-changing effects
ability-adding or ability-removing effects
power/toughness setting and modification
counters and power/toughness switching
timestamps
same-layer or same-sublayer dependencies
```

Layer and sublayer definitions come from the selected ruleset snapshot. They
are not permanently hardcoded.

The first bounded capability does not parse arbitrary Oracle text into formal
effects, execute unrestricted copy chains, resolve arbitrary linked
abilities, or reproduce a complete game state.

## Continuous-Effect Representation

An accepted future effect representation preserves:

```text
effect ID
source object and Oracle identity
duration
affected-object selector
layer and sublayer
timestamp
approved deterministic operation
dependency predicates
support status
official citations
```

Allowed operations must be enumerated by a later implementation contract.
An LLM may not invent or execute effect operations.

Dependency follows the selected Comprehensive Rules definition. A dependency
cycle produces `UNKNOWN_DEPENDENCY_CYCLE`; it is never broken by an arbitrary
ordering.

## Simulator Validation Boundary

The Rules Layer may later validate simulator action and trace packets. It
does not choose plays or calculate strategic success.

Future trace statuses:

```text
SUPPORTED_VALID
SUPPORTED_INVALID
PARTIAL_NONMATERIAL
PARTIAL_MATERIAL
UNSUPPORTED
UNVERIFIABLE
```

Only `SUPPORTED_VALID` enters clean simulator evidence.
`PARTIAL_NONMATERIAL` remains separate and caveated.

No trace validation is implemented or authorized in Phase 42C.

## Mandatory Future Regression Cases

Future Rules and simulator validation must retain at least these known
corrections:

```text
Paradise Mantle mana traces identify the equipped creature as ability source
and validate equip, tapping, and summoning-sickness requirements
Springleaf Drum remains the mana-ability source; untapping the assisting
creature does not untap the Drum
copy effects validate exact object eligibility rather than functional similarity
separate target-turn experiments are not relabeled as cumulative by-turn results
```

These are regression requirements, not general-purpose behavior
implementations in Phase 42C.

## Jin Boundary

Future Jin may read validated Rules packets. It may not:

```text
edit authority snapshots
create official rulings
change Oracle text
mark a trace legal
override UNKNOWN or conflict
bypass legality
draft the underlying verdict before Rules responds
persist strategic conclusions into Rules storage
```

Theory may supply pedagogical or strategic framing after a rules verdict. It
cannot change the verdict.

## Decision Boundary

Decision Intelligence must reject or withhold a candidate whose required
premise is:

```text
INVALID
ILLEGAL
materially unsupported
UNKNOWN where the conclusion depends on it
missing a required dated legality policy
```

An unknown interaction may become a research or experiment item. It may not
become a supported recommendation.

## Unknown And Partial Answers

Refusing certification does not require refusing all assistance.

Future packets must separate:

```text
confirmed facts
assumptions
unknown or unsupported portions
blocked conclusion
exact facts or authority needed to resolve it
```

The system must not replace unknown with likely, conceal unsupported
mechanics, trust model confidence as authority, or let community consensus
outvote official material.

## Community And Reference Implementations

MTG Layer Inspector, Forge, XMage, judge sites, forums, videos, articles, and
other models may be used for:

```text
case discovery
explanation comparison
differential testing
architecture reference
```

Any admitted regression case rewrites its expected outcome from official
authority. Reference conclusions remain discovery provenance, never verdict
authority.

Licensing, access terms, adapters, scraping, and runtime integration require
separate accepted contracts.

## Security And Privacy

Authority source content and external references are untrusted inputs.
Parsers must eventually enforce type, size, encoding, locator, content-hash,
and unexpected-content checks.

No rules source, card text, ruling, local rule, user correction, or community
reference may contain executable instructions for Codie or a model.

Private deck context remains local unless explicitly allowed by a later model
profile. Rules packets expose only the minimum deck or game-state projection
needed for the requested verdict.

## Reproducibility

Every future rules verdict binds:

```text
request identity and facts
evaluation date
authority package and snapshot hashes
analyzer and capability versions
canonical card identity versions
assumptions and unknowns
generated timestamp
```

Historical verdicts are not silently reinterpreted under newer authority.

## Implementation Deferral

Phase 42C does not authorize:

```text
source acquisition or download
rules parsing or indexing
authority storage
schema or repositories
legality implementation
interaction implementation
continuous-effect implementation
simulator integration
Jin integration
judge-training lessons
```

Future implementation requires separately accepted contracts naming exact
paths, capability manifests, public packet interfaces, persistence ownership,
fixtures, tests, source licensing, refresh policy, and rollback behavior.

## Phase 42D Boundary

Phase 42D may define only the Local-First Model Profile, Redaction, Consent,
and Routing Contract.

It must remain contract-only and may not download or invoke models, admit
cloud providers, transmit data, store secrets, implement redaction, build UI,
write profile repositories, produce Jin answers, or change dependencies.

## Forbidden Phase 42C Work

Phase 42C must not add production code, implementation tests, fixtures,
schemas, repositories, migrations, providers, rules source files, source
downloads, parsers, indexes, live network calls, model invocation, LLM
prompts, Jin answers, correction or Theory behavior, simulator behavior,
judge lessons, UI, file writing, dependencies, workflow changes, active-scope
changes, or constitution changes.

## Gate

Phase 42D may begin only after Phase 42C outside validation returns PASS or
PASS WITH REVIEW NOTES.
