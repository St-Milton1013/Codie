



# Codie V2 User Correction Ledger

## 1. Status and constitutional basis

The attached Constitution is a comparison draft, not ratified implementation authority. This subsystem design is therefore a contract proposal. It does not authorize schema changes or production work until accepted through the normal governance chain.

The Constitution establishes the required foundation:

- User corrections are high-priority signals for Jin.
- Corrections must be applied at the narrowest valid scope.
- Corrections may change user context, reasoning, parsing, simulation assumptions, terminology, and presentation.
- Corrections may not override official rules, Oracle text, legality, canonical evidence, measured metrics, or persisted recommendations.
- Corrections implying architecture, schema, source-policy, or constitutional changes require governance review.
- Jin may create correction candidates but may not mutate canonical evidence. fileciteturn0file0

The Theory Corpus adds a separate contamination boundary: personal conclusions and corrections must remain distinct from theory attribution, empirical evidence, and author claims. A user preference must never be presented as something Menendian, Karsten, Rebell Lily, or another theorist established. fileciteturn0file1

---

# 2. Purpose

The User Correction Ledger is an append-only, versioned subsystem that converts user feedback into structured and reusable operational knowledge.

It answers six questions:

1. What was wrong, incomplete, misleading, or merely unsuitable?
2. What should replace it?
3. Who or what supports the correction?
4. Where does the correction apply?
5. When does it apply?
6. Which subsystem may act on it?

The ledger is an overlay on Codie behavior. It is not another truth database.

```text
Canonical authority and evidence
        +
Applicable correction overlay
        +
Current user and deck context
        =
Resolved behavior for this operation
```

A correction can alter how Codie interprets or presents information. It cannot alter what the underlying official card, rule, tournament record, or metric actually says.

---

# 3. Non-negotiable invariants

## 3.1 Authority barrier

No correction may override:

- official Comprehensive Rules;
- official Oracle text or official rulings;
- date-aware official legality;
- canonical Scryfall identity within its approved scope;
- canonical tournament records;
- Commander Spellbook records within their approved scope;
- approved measured metrics.

A conflicting correction becomes one of:

- an authority-verification request;
- a canonical-data incident;
- an unresolved dispute;
- a rejected correction.

It never becomes a silent replacement value.

## 3.2 Narrowest valid scope

Corrections apply only as broadly as their evidence establishes.

A correction about one WrongSi snapshot does not become a rule about all Rograkh/Silas Renn decks. A parser defect affecting one Hareruya field does not rewrite every provider. A user preference for expanded citations does not change another user’s interface.

## 3.3 No automatic promotion

Repeated user statements do not automatically become global truth.

Promotion from deck-specific or user-specific context to global behavior requires:

- evidence;
- review;
- explicit scope expansion;
- regression fixtures;
- an approved state transition.

## 3.4 Append-only semantic history

Corrections are never overwritten in place. Semantic changes create a new revision or a superseding correction. Prior states remain auditable.

## 3.5 Reproducible application

Every analysis, Jin answer, simulation, parser run, or recommendation packet affected by corrections must be able to identify the exact correction bundle used.

## 3.6 Separation from canonical storage

The correction subsystem may reference canonical records. It may not update them.

---

# 4. Correction categories

The top-level category enum should remain closed to the categories already named in the Constitution. More precise classification belongs in tags and affected-subsystem fields, not in a weekly proliferation of nearly identical categories.

| Category | Meaning | Typical effect |
|---|---|---|
| `factual_correction` | A prior non-rules factual claim was wrong | Replace or suppress a claim in Jin or reports |
| `rules_correction` | A rules interaction or legality explanation was wrong | Trigger authority verification and legality regression |
| `source_policy_correction` | A source was used outside its approved role | Change retrieval or evidence eligibility after governance review |
| `reasoning_failure` | Facts may be correct, but the conclusion or inference was defective | Change Jin or Decision Intelligence reasoning constraints |
| `missing_capability` | Codie could not represent or evaluate something required | Create governed backlog or unsupported-state handling |
| `simulator_model_correction` | Simulator behavior, trace interpretation, or modeled action was wrong | Filter traces, alter validators, or revise card support |
| `deck_specific_principle` | A strategic constraint applies to a deck or deck lineage | Modify deck-specific reasoning only |
| `ui_output_preference` | The user wants different presentation, detail, or workflow | Change display or export behavior |
| `acceptable_low_confidence_result` | A low-confidence answer was acceptable despite uncertainty | Prevent unnecessary rework; never raise factual confidence |
| `terminology_correction` | A name, alias, abbreviation, or preferred term was wrong | Change search/display terminology without changing identity |
| `data_parsing_correction` | An imported field, zone, quantity, or source structure was parsed incorrectly | Change provider-specific parser behavior and fixtures |

Additional dimensions use tags such as:

```text
analytics
canonicalization
interaction-legality
deck-evaluation
source-attribution
privacy
theory-attribution
zone-separation
card-role
local-meta
confidence-language
```

---

# 5. Authority levels

Authority and scope are separate. A very specific correction can outrank a broader correction inside its valid scope, but nothing outranks the official authority barrier.

| Level | Name | Description | Activation rule |
|---|---|---|---|
| `A5` | Constitutional or official authority gate | Official rules, Oracle, legality, ratified governance | Not authored by the ledger; referenced as a hard constraint |
| `A4` | Authority-backed operational correction | Correction directly established by Class 0 evidence | Requires evidence verification and review |
| `A3` | Project-validated correction | Reproducible parser, simulator, analytics, or reasoning correction | Requires fixtures, tests, and reviewer approval |
| `A2` | User-approved contextual correction | Deck, commander, local-meta, or strategic-context correction | User approval is sufficient within the defined private scope |
| `A1` | User preference or terminology | Presentation, alias, output, or workflow preference | May activate immediately for that user |
| `A0` | Candidate or inferred correction | Generated by Jin, detected by validators, or not yet reviewed | Never changes governed behavior |

### Authority rules

`A5` is a gate rather than an editable ledger record.

`A4` and `A3` may alter shared subsystem behavior.

`A2` may alter user and deck behavior but not shared evidence.

`A1` may alter presentation and lookup convenience only.

`A0` is review material.

An `A2` deck-specific correction can outrank an `A3` general reasoning rule for that deck, provided it does not conflict with `A5` or change canonical evidence.

---

# 6. Scope model

Each correction has exactly one primary scope and may include additional predicates.

| Scope | Example | Revalidation behavior |
|---|---|---|
| `system_global` | Mainboard analytics never count sideboard-only copies | Revalidate on analytics or schema change |
| `subsystem_global` | Simulator target-turn runs are not presumed cumulative | Revalidate on simulator semantic-version change |
| `provider` | Hareruya parser field mapping | Revalidate on source schema or parser version change |
| `format_and_date` | Legality handling for Commander during a date range | Revalidate on rules or ban-history update |
| `card_identity` | A particular card requires special parser or simulator handling | Revalidate on Oracle, ruling, or card-definition change |
| `interaction_signature` | Springleaf Drum plus Valley Floodcaller interaction | Revalidate on rules or simulator action-model change |
| `commander_signature` | Exact partner-pair strategic principle | Revalidate when commander identity changes |
| `archetype` | Rule of Law parity analysis | Revalidate on archetype-definition change |
| `deck_lineage` | Chekhov’s-gun profile for the user’s Rograkh/Ishai deck | Revalidate after material deck diff |
| `deck_snapshot` | Current WrongSi list lacks a usable mana sink | Applies only to one immutable deck hash |
| `user_profile` | Always show explicit source attribution | Isolated to that user |
| `experiment` | Treat a test card as locked for one comparison run | Expires with experiment |
| `session` | Temporary conversational assumption | Never persisted as durable behavior without promotion |

## 6.1 Deck lineage versus deck snapshot

A `deck_snapshot` correction applies only to the exact deck hash.

A `deck_lineage` correction persists across snapshots, but each material deck change triggers revalidation.

Examples:

- “This current WrongSi list has no useful generic mana sink” belongs to `deck_snapshot`.
- “Evaluate this Rograkh/Ishai lineage using the Chekhov’s-gun profile” belongs to `deck_lineage`.
- “Flash Photography is locked during this testing program” may be `deck_lineage` with an explicit effective period.
- “Tataru Taru is not a clear failure in this list” belongs to the relevant snapshot or lineage, not to all decks containing the card.

---

# 7. Correction record

A correction must contain enough information to be understood without reconstructing an old conversation from archaeological debris.

```yaml
correction_id: uuid
stable_key: string
category: enum
title: string

original_claim: string
corrected_claim: string
supporting_reason: string
reusable_rule: string | null

authority_level: A0-A4
state: enum

scope_type: enum
scope_selector:
  user_id: string | null
  deck_lineage_id: string | null
  deck_snapshot_id: string | null
  deck_hash: string | null
  commander_signature_id: string | null
  provider_id: string | null
  oracle_id: string | null
  interaction_signature: string | null
  format: string | null
  valid_date_predicates: object | null

subject_type: string
subject_id: string | null

affected_subsystems:
  - jin
  - simulator
  - parser
  - terminology
  - ui
  - user_context
  - analytics
  - decision_intelligence
  - theory_router

application_modes:
  jin: annotate
  simulator: filter
  parser: enforce
  ui: prefer

exceptions: []
dependencies: []
supporting_evidence_ids: []

valid_from: datetime | null
valid_until: datetime | null
effective_from: datetime | null
effective_until: datetime | null

revalidation_policy_id: string
current_revision: integer
created_at: datetime
created_by: actor
sensitivity: enum
```

---

# 8. Lifecycle

## 8.1 States

```text
DRAFT
  ->
SUBMITTED
  ->
TRIAGED
  ->
UNDER_REVIEW
  ->
APPROVED_PENDING_EFFECTIVE
  ->
ACTIVE
```

Alternate transitions:

```text
UNDER_REVIEW -> REJECTED
UNDER_REVIEW -> EVIDENCE_REQUIRED
ACTIVE -> REVALIDATION_REQUIRED
REVALIDATION_REQUIRED -> ACTIVE
REVALIDATION_REQUIRED -> SUSPENDED
ACTIVE -> SUPERSEDED
ACTIVE -> EXPIRED
ACTIVE -> WITHDRAWN
SUSPENDED -> ACTIVE
SUSPENDED -> SUPERSEDED
```

## 8.2 State meanings

| State | Meaning | May affect behavior |
|---|---|---:|
| `DRAFT` | Incomplete record | No |
| `SUBMITTED` | User, Jin, validator, or subsystem submitted it | No |
| `TRIAGED` | Category, scope, and owner assigned | No |
| `EVIDENCE_REQUIRED` | Insufficient support for requested authority or scope | No |
| `UNDER_REVIEW` | Evidence and implications being evaluated | No |
| `APPROVED_PENDING_EFFECTIVE` | Approved but effective date has not arrived | No |
| `ACTIVE` | Eligible for resolution and application | Yes |
| `REVALIDATION_REQUIRED` | A dependency changed | Normally no |
| `SUSPENDED` | Temporarily disabled because correctness is uncertain | No |
| `SUPERSEDED` | Replaced by another correction | No |
| `REJECTED` | Did not meet evidence, authority, or scope requirements | No |
| `WITHDRAWN` | User or owner withdrew it | No |
| `EXPIRED` | Effective period ended | No |

Preferences may move from `SUBMITTED` directly to `ACTIVE` when they are `A1`, private, and do not affect shared behavior.

Global parser, simulator, source-policy, or rules corrections must pass review.

---

# 9. Supporting evidence

Evidence objects are independent records because one fixture, trace, or source citation may support multiple corrections.

```yaml
evidence_id: uuid
evidence_type: enum
title: string
source_class: class_0 | canonical | measured | user_context | test_artifact
source_reference: string
content_digest: sha256
captured_at: datetime
observed_at: datetime | null
deck_snapshot_id: string | null
simulator_run_id: string | null
jin_answer_packet_id: string | null
parser_fixture_id: string | null
authority_status: verified | unverified | disputed
storage_rights: enum
privacy_class: enum
retention_policy: string
```

Supported evidence types include:

- official rule reference;
- Oracle or official ruling snapshot;
- canonical card record;
- raw provider payload;
- parser fixture;
- simulator trace;
- simulator reconstruction;
- deck snapshot;
- Jin answer packet;
- user statement;
- user test note;
- screenshot;
- validation report;
- regression test;
- theory source citation;
- metric packet.

## 9.1 Evidence thresholds

| Correction type | Minimum support |
|---|---|
| Rules or canonical-card claim | Verified Class 0 evidence |
| Global simulator correction | Reproducible failing trace, corrected interpretation, regression fixture |
| Global parser correction | Raw source fixture, current output, expected output |
| Source-policy correction | Source-role analysis and governance approval |
| Reasoning failure | Original answer packet, identified failure, corrected reasoning rule |
| Deck-specific principle | User statement and applicable deck identity |
| UI preference | User statement |
| Terminology preference | User statement, with canonical term preserved |
| Missing capability | Demonstrated unsupported case |
| Acceptable low-confidence result | User acceptance linked to the original answer packet |

A user statement is sufficient evidence for the user’s own preference. It is not sufficient evidence for changing the rules engine. Apparently this distinction needs machinery because software has repeatedly demonstrated that context is optional until the damage report arrives.

---

# 10. Effective dates and temporal model

The ledger uses bitemporal history.

## 10.1 Valid time

Valid time answers: “When was this correction true or applicable in the domain?”

Fields:

```text
valid_from
valid_until
```

Examples:

- A legality correction may apply only after a ban announcement.
- A local-meta observation may apply only during a specified season.
- A deck correction may apply only while a particular snapshot was current.

## 10.2 System time

System time answers: “When did Codie know about and store this correction?”

Fields:

```text
recorded_at
activated_at
superseded_at
```

This permits historical replay:

```text
Reproduce the answer Codie would have produced
using knowledge available on 2026-07-20
for a deck legal on 2026-05-01.
```

## 10.3 Effective time

Effective time controls actual application:

```text
effective_from
effective_until
```

An approved correction with a future effective date remains `APPROVED_PENDING_EFFECTIVE`.

---

# 11. Supersession and revision

## 11.1 Revision versus new correction

Create a new revision when changing:

- spelling;
- formatting;
- evidence links;
- non-semantic explanation;
- metadata that does not alter behavior.

Create a new correction and supersession relation when changing:

- corrected claim;
- scope;
- authority;
- exceptions;
- application mode;
- effective period;
- reusable operational rule.

## 11.2 Supersession relationships

```text
FULL_REPLACEMENT
PARTIAL_REPLACEMENT
SCOPE_NARROWING
SCOPE_EXPANSION
EXCEPTION_ADDED
REFINEMENT
REVOCATION
DUPLICATE_OF
```

A superseding correction must state:

- which prior correction it supersedes;
- whether supersession is full or partial;
- the affected scopes;
- the effective date;
- the reason;
- whether prior application receipts remain valid historically.

## 11.3 No latest-wins shortcut

The newest correction does not automatically win.

Resolution considers:

1. official authority barrier;
2. active state;
3. valid and effective dates;
4. exact scope match;
5. explicit exceptions;
6. authority level;
7. scope specificity;
8. supersession relationship;
9. revision;
10. unresolved contradictions.

Two incompatible corrections at the same authority and scope produce a conflict. They do not get averaged into a confident sentence.

---

# 12. Exceptions

Exceptions are structured predicates, not prose appended to the end of a correction and forgotten.

```yaml
exception_id: uuid
parent_correction_id: uuid
predicate_type: enum
predicate:
  simulator_version: string | null
  card_definition_version: string | null
  deck_contains_oracle_ids: []
  deck_lacks_tags: []
  action_trace_fields_present: []
  date_range: object | null
  provider_version: string | null
effect: bypass | modify | downgrade | require_review
reason: string
```

Rules:

- An exception may narrow or condition a correction.
- An exception may not grant authority beyond the parent correction.
- More-specific exceptions outrank the parent correction.
- Ambiguous legality exceptions fail closed.
- Ambiguous UI preferences fall back to the user default.
- Exceptions are independently versioned and audited.

Example:

```text
Base correction:
Paradise Mantle mana traces are invalid.

Exception:
A trace remains eligible when it records equip payment,
the equipped creature, legal timing, the creature's tap action,
summoning-sickness legality, and resulting mana.
```

---

# 13. Revalidation triggers

Corrections declare dependencies. A changed dependency emits a revalidation request.

| Trigger | Corrections affected |
|---|---|
| Oracle text or ruling change | Card, interaction, simulator, terminology |
| Comprehensive Rules update | Rules and simulator corrections |
| Ban or legality update | Date-aware legality corrections |
| Simulator engine version change | Simulator-model corrections |
| Simulator card-definition change | Card-specific trace corrections |
| Parser version change | Parser corrections |
| Provider schema or payload change | Provider-specific corrections |
| Tagger ontology update | Terminology, role, and functional-tag corrections |
| Commander Spellbook update | Combo-related contextual corrections |
| Deck hash change | Snapshot corrections |
| Material deck-lineage diff | Deck-lineage principles |
| Commander signature change | Commander-scoped corrections |
| Theory source acquisition or attribution change | Theory-routing and terminology corrections |
| Constitution ratification or amendment | Source-policy and governance corrections |
| Contradictory new evidence | Any correction at or below the evidence level |
| User withdrawal | User-context and preference corrections |
| Effective period expiration | Time-bounded corrections |
| Privacy classification change | Export and cloud-retrieval eligibility |

## 13.1 Revalidation behavior

Safety-sensitive corrections move immediately to `REVALIDATION_REQUIRED` and stop enforcing behavior.

Presentation preferences may remain active unless their meaning became ambiguous.

Deck-snapshot corrections do not require review when a new snapshot appears. They simply stop matching.

---

# 14. Retrieval and resolution

## 14.1 Resolution request

```yaml
user_id:
operation:
subsystem:
analysis_time:
domain_time:
format:
provider_id:
oracle_ids:
interaction_signature:
commander_signature_id:
deck_lineage_id:
deck_snapshot_id:
deck_hash:
simulator_version:
parser_version:
analysis_profile:
```

## 14.2 Resolution algorithm

```text
1. Establish the Class 0 and canonical authority barrier.
2. Retrieve corrections matching subject, subsystem, user, scope, and time.
3. Remove non-active, expired, suspended, and incompatible-version records.
4. Mark revalidation-required records as unavailable.
5. Evaluate structured exceptions.
6. Group corrections by conflict key.
7. Apply explicit supersession relations.
8. Rank remaining records by:
      authority
      scope specificity
      effective date
      revision
9. Detect incompatible equal-rank corrections.
10. Return applied, shadowed, blocked, and conflicting records.
11. Generate a deterministic correction bundle hash.
```

## 14.3 Resolution packet

```yaml
correction_bundle_id:
bundle_hash:
resolution_policy_version:
generated_at:

applied:
  - correction_id
    revision
    application_mode
    scope_match
    reason

shadowed:
  - correction_id
    shadowed_by
    reason

blocked:
  - correction_id
    reason

revalidation_required:
  - correction_id
    trigger

conflicts:
  - conflict_id
    correction_ids
    required_action

authority_barrier_refs: []
```

Every affected operation records the bundle hash.

---

# 15. Application modes

A correction does not merely “apply.” It applies through an explicit mode.

| Mode | Behavior |
|---|---|
| `ENFORCE` | Changes deterministic subsystem behavior |
| `BLOCK` | Stops an operation or excludes an invalid result |
| `FILTER` | Removes invalid traces, claims, or candidates |
| `ANNOTATE` | Adds correction context without changing underlying evidence |
| `WARN` | Continues with a visible caveat |
| `PREFER` | Selects a presentation or terminology preference |
| `ROUTE` | Changes retrieval or theory routing |
| `SUPPRESS` | Prevents repetition of a known bad claim |
| `DOWNGRADE_CONFIDENCE` | Lowers confidence because a known limitation remains |
| `CREATE_REVIEW_ITEM` | Produces a queue item but does not alter behavior |

No correction may raise measured-evidence confidence. An `acceptable_low_confidence_result` record can prevent needless repair work, but it cannot convert weak evidence into strong evidence.

---

# 16. Subsystem effects

## 16.1 Jin-Gitaxias

Jin retrieves corrections after intent and deck-scope resolution, before drafting the answer.

```text
Question
  ->
Intent and scope
  ->
Canonical evidence
  ->
Applicable correction bundle
  ->
Theory retrieval
  ->
Answer draft
  ->
Authority check
  ->
Contradiction scan
  ->
Final packet
```

Jin must:

- apply active user and deck corrections;
- suppress previously corrected reasoning failures;
- identify corrections as user context where appropriate;
- preserve scope in its language;
- expose material conflicting corrections;
- include correction IDs and bundle hash in the answer packet;
- keep user conclusions separate from theory attribution;
- avoid turning correction frequency into confidence.

Jin may create `A0` correction candidates.

Jin may not:

- activate a global correction;
- change canonical evidence;
- change metrics;
- change official legality;
- persist a recommendation by writing through the ledger;
- reinterpret a deck correction as format-wide knowledge.

### Jin answer fields

```text
applied_correction_ids
correction_bundle_hash
correction_scope
correction_conflicts
user_context_claims
authority_conflicts_blocked
```

## 16.2 Simulator

Only `A3` or `A4` active corrections may alter shared simulator behavior.

Simulator corrections may:

- reject invalid traces;
- require additional action fields;
- change trace post-processing;
- mark a card unsupported;
- disable a broken behavior model;
- alter scenario assumptions;
- lower result confidence.

They may not alter official rules without Class 0 support.

The simulator resolves one immutable correction bundle at run start. It does not query the ledger during individual games. The run record stores:

```text
correction_bundle_hash
applied_simulator_corrections
simulator_version
card_definition_version
```

Deck-specific corrections may change test targets or interpretation. They may not alter the shared legal-action engine.

## 16.3 Parsers

Parser corrections require provider-scoped or system-global fixtures.

They may change:

- field extraction;
- zone classification;
- quantity handling;
- commander recognition;
- provider-specific date parsing;
- auxiliary-object handling;
- alias normalization.

They may not guess unresolved card identities.

A parser correction becomes enforceable only when:

1. the raw failing fixture is retained;
2. expected candidate output is declared;
3. canonicalization behavior is unchanged or separately reviewed;
4. regression tests pass.

## 16.4 Terminology

Terminology corrections operate through an alias and display layer.

They may:

- recognize `PVDDR` as an alias;
- preserve the preferred spelling of a theorist;
- map partner shorthand;
- change a user-facing label;
- improve natural-language retrieval.

They may not:

- replace canonical card names;
- merge uncertain author identities;
- rewrite source quotations;
- change Oracle identity;
- attribute a user term to an author.

The Theory Corpus explicitly requires source identities and attribution chains to remain distinct until verified. fileciteturn0file1

## 16.5 UI preferences

User-interface corrections may activate immediately at `A1`.

Examples:

- show source attribution beside each material claim;
- default to expanded correction provenance;
- collapse low-priority audit detail;
- display deck-snapshot scope prominently;
- prefer a specific export format.

UI preferences are isolated by user and device profile. They never affect analytics, source eligibility, or recommendation confidence.

## 16.6 User context

Deck principles, local-meta observations, locked cards, testing goals, and corrections remain Class 4 user context.

They may personalize:

- Jin discussion;
- Decision Intelligence profiles;
- experiment generation;
- deck-health interpretation;
- candidate ranking.

They may not enter:

- tournament populations;
- global inclusion rates;
- commander averages;
- source-agreement calculations;
- canonical deck records.

## 16.7 Decision Intelligence

Decision Intelligence may consume applicable corrections through Unified Evidence or an approved correction-context attachment.

Corrections may:

- block a known-invalid recommendation path;
- apply a locked-card constraint;
- identify missing conversion outlets;
- preserve a deck-specific analysis profile;
- downgrade confidence.

The ledger may not directly write or revise persisted recommendations.

## 16.8 Theory Corpus

Corrections may fix:

- author identity;
- attribution;
- source status;
- terminology;
- format-transfer warnings;
- user conclusions mistakenly attributed to a theorist.

User corrections remain linked user-context nodes. They are not converted into theorist claim nodes.

---

# 17. Realistic correction examples

| Correction | Category | Scope | Authority | Application |
|---|---|---|---|---|
| Paradise Mantle traces require equip payment, equipped creature, legal tapping, and summoning-sickness checks | `simulator_model_correction` | Simulator global, card-specific | A3 after validation | Block invalid traces |
| Springleaf Drum does not become repeatable merely because the creature used for its cost untaps | `rules_correction` and `simulator_model_correction` | Interaction signature | A4 with rules support | Block illegal loop reasoning |
| Target-turn runs are separate experiments unless cumulative semantics are proven | `simulator_model_correction` | Simulator global | A3 | Change labels and interpretation |
| The current WrongSi snapshot has no useful generic mana sink | `deck_specific_principle` | Exact deck snapshot | A2 | Downgrade abstract infinite-mana value |
| Chekhov’s-gun evaluation applies to the user’s Rograkh/Ishai lineage, not every deck | `deck_specific_principle` | Deck lineage | A2 | Route deck-health analysis |
| Tataru Taru should not be treated as a clear failure in this shell | `reasoning_failure` | Rograkh/Ishai snapshot or lineage | A2 | Suppress prior blanket conclusion |
| Wan Shi Tong should receive credit where frequent library searching supports it | `reasoning_failure` | Relevant deck snapshot | A2 | Modify deck-specific card analysis |
| Sideboard-only copies do not inflate mainboard frequency | `data_parsing_correction` | Parser and analytics global | A3 | Enforce zone separation |
| Always expose which source supports each material research claim | `ui_output_preference` | User profile | A1 | Presentation preference |
| A prior low-confidence answer was useful and does not require repair | `acceptable_low_confidence_result` | Answer packet | A2 | Close review item without raising confidence |
| A user-supplied nickname should resolve in search but display the canonical card name | `terminology_correction` | User profile or approved alias registry | A1 or A3 | Search alias only |

The first three examples are already treated as project-level simulator constraints in the Constitution. fileciteturn0file0

---

# 18. Conflicting-correction resolution

## 18.1 Deck change invalidates a snapshot correction

Correction A:

```text
WrongSi snapshot X has no meaningful mana sink.
```

A later snapshot adds a reliable outlet.

Resolution:

- Correction A remains historically valid for snapshot X.
- It does not match snapshot Y.
- The deck-lineage revalidation queue may propose a new correction.
- No global “WrongSi lacks sinks” rule is created.

## 18.2 Global rule versus deck-specific exception

Correction A:

```text
Cards with narrow utility should be flagged.
Scope: general Jin reasoning.
Authority: A3.
```

Correction B:

```text
Tataru Taru has sufficient long-game and replacement value in this Rograkh/Ishai list.
Scope: exact deck lineage.
Authority: A2.
```

Resolution:

- Correction A remains the general lens.
- Correction B is more specific and changes the conclusion within that deck.
- The final answer may still mention the general concern, but must not call the card a clear failure.

## 18.3 User correction conflicts with official truth

Correction candidate:

```text
Treat the card as having different Oracle text.
```

Resolution:

- Class 0 barrier blocks activation.
- Candidate moves to authority verification.
- If official evidence confirms a canonical data lag, create a canonical-data incident.
- If official evidence contradicts the user claim, reject the correction.
- Preserve the user report and resolution history.

## 18.4 Equal-scope reasoning conflict

Two active project corrections claim opposite interpretations for the same interaction and simulator version.

Resolution:

- Neither receives automatic precedence.
- A `correction_conflict` record is created.
- Shared enforcement is suspended.
- Existing results receive a visible caveat.
- Review must supersede or narrow one correction.

## 18.5 User preference conflicts

User A wants full provenance expanded. User B wants a compact view.

Resolution:

- Both remain active because their `user_profile` scopes do not overlap.
- There is no system conflict.

---

# 19. Database design

SQLite remains appropriate. The ledger should use normalized append-only history with derived current-state views.

## 19.1 Tables

### `corrections`

Stable identity only.

```text
correction_id PK
tenant_id
category
stable_key
subject_type
subject_id
created_at
created_by
sensitivity
```

### `correction_revisions`

Append-only semantic content.

```text
revision_id PK
correction_id FK
revision_number
title
original_claim
corrected_claim
supporting_reason
reusable_rule
authority_level
valid_from
valid_until
effective_from
effective_until
revalidation_policy_id
payload_hash
created_at
created_by
```

Unique constraint:

```text
UNIQUE(correction_id, revision_number)
```

### `correction_scopes`

```text
scope_id PK
revision_id FK
scope_type
user_id
deck_lineage_id
deck_snapshot_id
deck_hash
commander_signature_id
provider_id
oracle_id
interaction_signature
format
selector_json
```

Frequently queried fields remain columns. Rare predicates may use validated JSON.

### `correction_targets`

```text
target_id PK
revision_id FK
subsystem
application_mode
priority_hint
```

`priority_hint` may organize presentation but must not override authority resolution.

### `correction_exceptions`

```text
exception_id PK
revision_id FK
predicate_type
predicate_json
effect
reason
created_at
```

### `correction_evidence`

```text
evidence_id PK
evidence_type
title
source_class
source_reference
content_digest
authority_status
captured_at
observed_at
storage_rights
privacy_class
retention_policy
```

### `correction_evidence_links`

```text
revision_id FK
evidence_id FK
support_role
```

Support roles:

```text
supports
contradicts
illustrates
authority_basis
regression_fixture
user_assertion
```

### `correction_state_events`

```text
event_id PK
correction_id FK
revision_id FK
from_state
to_state
actor_type
actor_id
reason
occurred_at
request_id
```

Current state is a view derived from the latest valid event.

### `correction_relations`

```text
relation_id PK
source_correction_id FK
target_correction_id FK
relation_type
scope_selector_json
effective_from
reason
created_at
```

### `correction_dependencies`

```text
dependency_id PK
revision_id FK
dependency_type
dependency_key
version_constraint
```

### `correction_revalidation_events`

```text
revalidation_event_id PK
correction_id FK
trigger_type
trigger_reference
detected_at
status
reviewed_at
reviewed_by
resolution
```

### `correction_conflicts`

```text
conflict_id PK
conflict_key
status
detected_at
resolved_at
resolution_revision_id
```

### `correction_conflict_members`

```text
conflict_id FK
correction_id FK
revision_id FK
```

### `correction_application_receipts`

```text
receipt_id PK
operation_type
operation_id
bundle_hash
resolution_policy_version
applied_at
result_digest
```

Receipts may store correction IDs in a child table rather than duplicating full content.

### `correction_audit_events`

Security and administrative audit distinct from state history.

```text
audit_event_id PK
actor_type
actor_id
action
object_type
object_id
request_id
timestamp
metadata_json
previous_hash
event_hash
```

## 19.2 Derived views

```text
active_corrections
correction_current_revision
correction_current_state
corrections_requiring_revalidation
unresolved_correction_conflicts
correction_usage_summary
```

---

# 20. Repository and trust boundaries

## 20.1 Repository ownership

`CorrectionLedgerRepository` is the sole writer for correction identities, revisions, scopes, evidence links, and state events.

`CorrectionQueryRepository` provides read-only contextual retrieval.

`CorrectionReviewRepository` manages review queues and state transitions through domain services.

`CorrectionAuditRepository` writes append-only audit events.

No other subsystem writes correction tables directly.

## 20.2 Service boundaries

```text
Jin
Simulator
Parser
UI
Decision Intelligence
        |
        v
CorrectionResolverService
        |
        v
CorrectionQueryRepository
        |
        v
SQLite correction tables
```

Write flow:

```text
User / Jin candidate / Validator
        |
        v
CorrectionCommandService
        |
        v
Validation and authorization
        |
        v
CorrectionLedgerRepository
```

## 20.3 Prohibited access

The correction subsystem may not write to:

- canonical card tables;
- Oracle or legality tables;
- canonical tournament records;
- source observation records;
- measured metric tables;
- recommendation history;
- simulator historical outputs;
- theory claim provenance.

A subsystem needing a canonical change must open the appropriate incident or review command.

## 20.4 Jin boundary

Jin may call:

```text
submit_correction_candidate
retrieve_applicable_corrections
explain_applied_correction
```

Jin may not call:

```text
activate_global_correction
supersede_project_correction
modify_canonical_record
raise_evidence_confidence
```

---

# 21. Privacy requirements

The correction ledger is private and local by default because it may reveal:

- private decklists;
- local metagame observations;
- user habits;
- strategic preferences;
- conversation excerpts;
- simulator traces;
- source links;
- mistakes and review history.

## 21.1 Privacy classifications

```text
PUBLIC_REFERENCE
PROJECT_INTERNAL
USER_PRIVATE
DECK_PRIVATE
SECRET_REFERENCE
```

`SECRET_REFERENCE` may identify that protected material exists but may not store tokens, credentials, or secret contents.

## 21.2 Cloud processing

Corrections are excluded from cloud-model prompts unless:

- cloud processing is enabled;
- the relevant user has consented;
- the correction’s privacy class permits it;
- private evidence attachments are minimized or redacted;
- the outgoing packet is logged.

## 21.3 Exports

Default exports include:

- correction ID;
- category;
- state;
- corrected rule;
- scope summary;
- non-private evidence references;
- audit summary.

Default exports exclude:

- raw conversation text;
- private decklists;
- full simulator traces;
- local file paths;
- user identity;
- hidden source attachments;
- credentials.

## 21.4 Multi-user isolation

Every user-specific correction includes a tenant and user boundary.

Deck-private corrections may be shared only through explicit permissions.

One user’s terminology or interface preference must never leak into another user’s profile.

## 21.5 Deletion and redaction

A user may delete user-authored private content.

Audit integrity is preserved through a redaction tombstone containing:

```text
correction_id
deletion_time
deletion_actor
prior_content_digest
deletion_reason
```

The content itself is removed. Hashes must not permit practical reconstruction.

---

# 22. Audit requirements

Every meaningful action records:

- actor;
- timestamp;
- request ID;
- operation;
- affected correction and revision;
- prior state;
- resulting state;
- reason;
- evidence added or removed;
- scope changes;
- authority changes;
- supersession relationships;
- validation result.

Audit history must answer:

```text
Who created this correction?
What evidence existed at activation?
Who approved it?
Which version applied to this answer or simulation?
What later caused revalidation?
Why was it superseded?
Did it ever affect shared behavior?
```

Audit logs are append-only.

Administrative read access does not permit mutation.

---

# 23. Failure behavior

| Failure | Required behavior |
|---|---|
| Ledger unavailable | Continue only when safe; disclose correction context unavailable |
| Resolver timeout | Do not silently assume no corrections exist |
| Ambiguous global correction | Block enforcement and create conflict |
| Ambiguous UI preference | Fall back to user default |
| Revalidation-required rules correction | Fail closed for legality-dependent behavior |
| Missing evidence attachment | Mark correction incomplete; do not activate |
| Unknown deck snapshot | Do not broaden to deck lineage |
| Invalid scope selector | Reject write |
| Bundle hash mismatch | Reject replay or mark result non-reproducible |
| Canonical conflict | Block correction and open authority review |
| Privacy policy failure | Exclude correction from cloud/export operation |
| Migration failure | Roll back migration and preserve existing ledger |

---

# 24. Test plan

## 24.1 Unit tests

1. Category enum validation.
2. Authority comparison.
3. Scope matching.
4. Scope-specificity ordering.
5. Effective-date filtering.
6. Valid-time historical queries.
7. Exception evaluation.
8. Supersession resolution.
9. Conflict-key construction.
10. Bundle-hash determinism.
11. State-transition validation.
12. Revalidation-trigger matching.
13. Privacy-class enforcement.
14. Revision hash verification.

## 24.2 Hand-verifiable fixtures

### Fixture A: Snapshot isolation

- Correction applies to deck hash `AAA`.
- Analysis uses deck hash `BBB`.
- Expected: correction does not apply.

### Fixture B: Deck specificity

- Global reasoning rule flags narrow cards.
- Deck-specific correction protects one card in one deck.
- Expected: general rule remains active elsewhere; specific correction applies only in matching deck.

### Fixture C: Authority barrier

- User correction conflicts with verified Oracle text.
- Expected: blocked, authority review created, canonical data unchanged.

### Fixture D: Simulator filtering

- Trace uses Paradise Mantle without equip details.
- Expected: trace excluded.
- Second trace includes all required fields.
- Expected: correction exception permits normal legality evaluation.

### Fixture E: Springleaf Drum interaction

- Trace assumes untapping the creature untaps the Drum.
- Expected: trace rejected.

### Fixture F: Target-turn semantics

- Turn-two rate exceeds turn-three rate.
- Expected: UI does not label results cumulative.

### Fixture G: Parser zone separation

- Card appears only in sideboard.
- Expected: zero mainboard inclusion contribution.

### Fixture H: Equal-rank conflict

- Two active corrections have equal authority, subject, scope, and incompatible rules.
- Expected: conflict returned; neither enforced.

### Fixture I: UI isolation

- Two users have opposite provenance-display preferences.
- Expected: each receives their own setting.

### Fixture J: Low-confidence acceptance

- User accepts an answer with low confidence.
- Expected: review item closes; confidence remains unchanged.

## 24.3 Integration tests

- Jin retrieves deck-specific corrections and exposes bundle hash.
- Jin does not apply corrections belonging to another deck.
- Simulator stores correction bundle with the run.
- Parser fixtures activate only after approved correction state.
- Decision Intelligence receives correction context without canonical mutation.
- Theory routing keeps user correction separate from theorist claims.
- Export redacts private evidence.
- Historical replay resolves the correction set active at the requested time.
- Canonical repositories receive zero writes during all correction workflows.

## 24.4 Adversarial tests

- Repeated user assertion does not auto-promote authority.
- Newer low-authority correction does not override older authority-backed correction.
- Deck-lineage correction does not leak into commander-wide analysis.
- User terminology does not alter canonical identity.
- Jin cannot activate its own correction candidate.
- Malformed exception JSON cannot bypass safety checks.
- Revalidation-required correction cannot remain silently active.
- Deleted private content is absent from exports and cloud packets.
- A correction cannot raise measured confidence.
- Source-policy correction cannot activate without governance approval.

---

# 25. Contract-ready Codex handoff

## Phase name

**Codie V2 User Correction Ledger Core Contract**

## Objective

Implement the governed storage, lifecycle, resolution, audit, and retrieval foundation for user corrections without integrating uncontrolled behavior changes into Jin, simulation, parsing, analytics, or canonical repositories.

## Authorized scope

- SQLite migrations for ledger tables.
- Correction domain models and enums.
- Append-only revisions and state events.
- Scope and authority resolution.
- Supporting-evidence metadata.
- Supersession and exception handling.
- Revalidation dependency tracking.
- Deterministic correction bundle generation.
- Read and write repositories.
- Local privacy enforcement.
- Audit history.
- Fixtures and tests.
- Read-only adapter contracts for future consumers.

## Prohibited scope

- No canonical card or rules mutation.
- No tournament evidence mutation.
- No metric recalculation.
- No recommendation creation.
- No automatic global activation from Jin.
- No simulator engine rewrite.
- No provider parser rewrite beyond test adapters.
- No theory-node mutation.
- No cloud synchronization.
- No UI redesign.
- No automatic correction extraction from every conversation.
- No constitutional ratification.

## Proposed modules

```text
src/codie/corrections/
    __init__.py
    enums.py
    models.py
    commands.py
    queries.py
    authority.py
    scope.py
    lifecycle.py
    resolver.py
    supersession.py
    exceptions.py
    revalidation.py
    bundles.py
    privacy.py
    audit.py
    errors.py

src/codie/repositories/
    correction_ledger_repository.py
    correction_query_repository.py
    correction_review_repository.py
    correction_audit_repository.py

src/codie/db/migrations/
    <next>_create_correction_ledger.sql

src/codie/integrations/corrections/
    jin_read_adapter.py
    simulator_read_adapter.py
    parser_read_adapter.py
    ui_preference_adapter.py

tests/corrections/
    test_authority.py
    test_scope.py
    test_lifecycle.py
    test_supersession.py
    test_exceptions.py
    test_revalidation.py
    test_resolution.py
    test_bundle_hash.py
    test_privacy.py
    test_audit.py
    test_repository_boundaries.py
    test_historical_replay.py

tests/fixtures/corrections/
    paradise_mantle_invalid_trace.json
    paradise_mantle_valid_trace.json
    springleaf_drum_invalid_loop.json
    target_turn_nonmonotonic.json
    wrongsi_snapshot_no_sink.json
    wrongsi_snapshot_with_sink.json
    rograkh_ishai_chekhov_profile.json
    sideboard_frequency_fixture.json
    equal_rank_conflict.json
    private_export_redaction.json
```

Package roots may be adjusted to the repository’s existing layout. Module responsibilities and boundaries remain fixed.

## Required public interfaces

```text
submit_correction(command) -> CorrectionIdentity
add_correction_revision(command) -> CorrectionRevision
transition_correction_state(command) -> StateTransitionReceipt
attach_correction_evidence(command) -> EvidenceLink
supersede_correction(command) -> SupersessionReceipt
record_correction_exception(command) -> ExceptionIdentity

resolve_corrections(context) -> CorrectionResolutionPacket
get_correction(correction_id, as_of=None) -> CorrectionRecord
list_corrections(filter) -> CorrectionPage
get_correction_history(correction_id) -> CorrectionHistory
list_revalidation_queue(filter) -> RevalidationPage
list_conflicts(filter) -> ConflictPage

record_application_receipt(command) -> ApplicationReceipt
```

## Required domain errors

```text
InvalidCorrectionCategory
InvalidAuthorityTransition
InvalidLifecycleTransition
InvalidScopeSelector
AuthorityBarrierViolation
CanonicalMutationAttempt
CorrectionConflictUnresolved
CorrectionRequiresRevalidation
CorrectionNotActive
EvidenceRequirementUnsatisfied
PrivacyBoundaryViolation
BundleHashMismatch
SupersessionCycleDetected
```

## Migration requirements

- Migration must be transactional.
- Foreign keys must be enabled.
- Every common retrieval path must have an index.
- Rollback or recovery instructions must be documented.
- Existing canonical and analytics tables must remain unchanged.
- Schema documentation must identify repository ownership.
- Migration tests must run against empty and populated databases.

## Required indexes

At minimum:

```text
correction_revisions(correction_id, revision_number)
correction_state_events(correction_id, occurred_at)
correction_scopes(scope_type, user_id)
correction_scopes(deck_snapshot_id)
correction_scopes(deck_lineage_id)
correction_scopes(provider_id)
correction_scopes(oracle_id)
correction_scopes(interaction_signature)
correction_targets(subsystem, application_mode)
correction_dependencies(dependency_type, dependency_key)
correction_conflicts(status, detected_at)
correction_application_receipts(operation_type, operation_id)
```

## Acceptance criteria

1. All listed top-level categories exist exactly as governed enums.
2. Only active, temporally valid, version-compatible corrections can apply.
3. Official authority conflicts are blocked.
4. Deck-snapshot corrections never leak to other snapshots.
5. User-profile corrections never leak to other users.
6. Equal-rank incompatible corrections produce an explicit conflict.
7. Supersession is deterministic and cannot form cycles.
8. Every semantic revision remains historically retrievable.
9. Historical replay returns the correction set valid at the requested system and domain times.
10. Every resolution packet has a deterministic bundle hash.
11. Jin, simulator, and parser adapters are read-only.
12. No correction operation writes to canonical, source, metric, or recommendation tables.
13. Privacy classifications control exports and cloud eligibility.
14. Deleted private content is replaced by a non-reconstructive tombstone.
15. Audit history identifies every activation, rejection, supersession, and revalidation.
16. The Paradise Mantle, Springleaf Drum, target-turn, sideboard, and deck-scope fixtures pass.
17. `acceptable_low_confidence_result` never raises confidence.
18. Jin-generated candidates remain `A0` and non-active.
19. Revalidation triggers reliably suspend safety-sensitive corrections.
20. Deterministic, architecture, adversarial, and aggregate validation all return an allowed passing result with no unresolved blocking finding.

## Completion report requirements

The implementation report must include:

```text
phase name
commit SHA
migration identity
files created
files modified
public interfaces
schema changes
repository ownership
fixtures added
tests executed
test results
boundary checks
privacy checks
known limitations
unresolved findings
next permitted phase
```

## Next permitted phase

**Codie V2 Correction Ledger Consumer Integration Contract**

That later phase may integrate the resolver with Jin, simulator trace validation, provider parsers, terminology lookup, user-context assembly, and UI preference presentation. It may not alter the core ledger contract without a separately reviewed amendment.
> [!IMPORTANT]
> Repository intake note: This is a preserved pre-ratification design
> proposal. `docs/CODIE_V2_CONSTITUTION.md` is now ratified and is the
> governing authority. Statements below that call V2 a non-authoritative
> comparison draft are historical. This proposal does not authorize
> implementation.
