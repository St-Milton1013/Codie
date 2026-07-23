



# Codie V2 Theory Corpus and Attributed Knowledge Graph

## 1. Status and authority

This is a **proposed implementation specification**, not current project authority. The Codie V2 Constitution is explicitly a comparison draft that does not authorize implementation, while the Theory Corpus Compilation is a sourcebook draft that has not yet produced claim nodes, router weights, or a functioning graph. Any implementation phase must first receive an accepted contract through the normal governance chain. fileciteturn0file0 fileciteturn0file1

The system has one governing principle:

> Theory may explain, question, organize, or contextualize evidence. It may not replace rules authority, canonical observations, measured evidence, or user judgment.

Authors are provenance subjects. They are not truth authorities. Fame is not a data type.

---

# 2. System purpose

The Theory Corpus serves two consumers from one attributed graph:

1. **Jin-Gitaxias**, which retrieves documented strategic frameworks and applies them to approved Codie evidence.
2. **The curriculum system**, which teaches those same frameworks through readings, media, comparison, application, assessment, and reflection.

The corpus must support:

- durable Magic theory;
- native cEDH theory;
- translated Legacy, Vintage, competitive Constructed, Limited, and casual Commander theory;
- historical disagreements;
- source attribution chains;
- examples and counterexamples;
- format limitations;
- user-created applications;
- lessons and assessments;
- monitored but unverified source candidates.

The corpus must not:

- make authors canonical authorities;
- treat article popularity as evidentiary weight;
- infer a complete philosophy from one decklist or interview;
- convert historical card advice into current cEDH guidance without translation;
- allow Jin to fabricate an author’s opinion;
- ingest community discussion into tournament analytics;
- redistribute licensed or copyrighted source material;
- let Jin modify approved claims, graph structure, source records, or review status.

The shared-graph approach, source hierarchy, claim labels, disagreement preservation, topic routing, and curriculum architecture are already established in the corpus compilation. fileciteturn0file1

---

# 3. Trust boundaries

```text
External or local source
    |
    v
Source acquisition and rights gate
    |
    v
Immutable source version
    |
    v
Segment and citation-anchor creation
    |
    v
Candidate claim extraction
    |
    v
Human review and attribution audit
    |
    v
Approved theory graph
    |
    +--------------------+
    |                    |
    v                    v
Theory retrieval      Curriculum builder
    |                    |
    v                    v
Jin theory packet     Lesson packet
    |
    v
Jin writer
    |
    v
Legality, citation, and contradiction auditor
    |
    v
Final answer packet
```

### Boundary rules

| Component | May read | May write | Prohibited |
|---|---|---|---|
| Source acquirer | External source metadata and permitted content | Source candidate and immutable source version | Claims, recommendations |
| Extractor | Approved source versions and segments | Candidate claims and candidate links | Approving claims |
| Reviewer | Candidates, citations, rights, source identity | Review decisions and approved theory records | Canonical tournament evidence |
| Graph service | Approved theory objects | Versioned graph records | Raw provider records, recommendations |
| Retriever | Approved graph and query context | Ephemeral retrieval packet | Graph mutation |
| Jin writer | Theory packet, Codie evidence, user context | Draft answer, hypothesis, experiment proposal | Theory graph, metrics, recommendations |
| Jin auditor | Draft answer, cited evidence, legality results | Audit findings and corrected answer packet | Canonical or theory mutation |
| Curriculum service | Approved graph and lesson specifications | Curriculum progress and user reflections | Theory approval |
| Exporter | Approved records selected for export | Local export artifact | Unauthorized source text |

The Constitution already establishes that Jin may read the theory corpus but may not write canonical tournament evidence, measured metrics, confidence tables, commander staples, package statistics, or persisted recommendations. That prohibition extends here to approved theory claims and graph relationships. fileciteturn0file0

---

# 4. Supported source types

## 4.1 Source-role taxonomy

Source type and source role are separate. A podcast can be a primary statement, a later synthesis, or merely a discovery lead.

| Source type | Permitted roles | Default treatment |
|---|---|---|
| Book | Primary theory, synthesis, historical context | Rights-gated; edition-specific |
| Article or essay | Primary theory, synthesis, demonstrated application | Preserve publication and revision metadata |
| Primer | Deck-specific application, archetype explanation | Never universal by default |
| Video | Primary statement, lecture, interview, application | Timestamp anchors required |
| Podcast | Primary statement, discussion, synthesis | Speaker-level attribution required |
| Transcript | Searchable representation of media | Must identify transcript provenance and accuracy |
| Forum thread | Debate, historical development, demonstrated application | Preserve author, date, post hierarchy, edits |
| Reddit thread | Discovery, community hypothesis, disagreement | Candidate-only by default |
| Source map or bibliography | Discovery and attribution chain | Does not support the underlying claim itself |
| Decklist | Demonstrated application | Not proof of the author’s general theory |
| Tournament report | Demonstrated application and contextual evidence | Separate strategy statement from result |
| Curated user note | User interpretation or personal conclusion | Never attributed to an author |
| Official rules material | Rules authority, lesson support | Stored or linked through the Rules Layer |
| Judge article | Rules explanation or historical rules context | Current official rules remain authoritative |
| Design article | Design context, color-pie or system constraints | Not competitive authority |
| Adjacent non-Magic writing | Reasoning method, argument structure | Explicit invocation or validated topic match only |
| Generated transcription or summary | Processing artifact | Never treated as an original source |
| Screenshot | Discovery or preservation artifact | Not sufficient for claim approval when original is recoverable |

The sourcebook already identifies books, articles, primers, Substack posts, videos, podcasts, transcripts, forum threads, user notes, historical theory, Commander theory, and judge training as supported material. It also distinguishes primary theory, synthesis, discovery-only sources, and provisional monitored writers. fileciteturn0file0 fileciteturn0file1

## 4.2 Source-role values

```text
PRIMARY_THEORY
PRIMARY_DEFINITION
PRIMARY_APPLICATION
LATER_SYNTHESIS
HISTORICAL_RETELLING
FORMAT_BRIDGE
DESIGN_CONTEXT
RULES_EXPLANATION
COMMUNITY_CONTEXT
DEBATE_RECORD
DISCOVERY_MAP
USER_INTERPRETATION
ADJACENT_METHOD
EMPIRICAL_CONTEXT
UNKNOWN
```

A source may hold several roles, but each extracted claim must declare the role under which it is being used.

---

# 5. Storage rights and content handling

Copyright ownership, storage permission, processing permission, quotation permission, and export permission must be modeled separately. Treating “the user uploaded it” as blanket redistribution permission would be the sort of administrative hallucination humans usually reserve for license agreements.

## 5.1 Rights classes

| Rights class | Full local storage | Local indexing | Short quotation | Export source text | Cloud processing |
|---|---:|---:|---:|---:|---:|
| `USER_CREATED` | Yes | Yes | Yes | Yes | By explicit consent |
| `PUBLIC_DOMAIN` | Yes | Yes | Yes | Yes | By configuration |
| `OPEN_LICENSED` | Per license | Yes | Per license | Per license | By configuration |
| `PUBLIC_LINK_ONLY` | Metadata and permitted cache only | Metadata or permitted excerpts | Limited | No | Link metadata only |
| `USER_LICENSED_PRIVATE` | Local only | Local only | Minimal and private | No | No by default |
| `PLATFORM_TRANSCRIPT_LIMITED` | Only as permitted | Local if permitted | Limited | No | No by default |
| `COMMUNITY_PUBLIC` | Snapshot if permitted | Yes | Limited | No bulk republication | By explicit consent |
| `UNKNOWN_RESTRICTED` | Metadata only | No content index | No | No | No |
| `TAKEDOWN_OR_WITHDRAWN` | Existing local preservation only if lawful | Disabled | No new quotation | No | No |

## 5.2 Rights fields

Every source version requires:

```text
rights_class
copyright_holder_known
license_identifier
license_url_or_note
full_text_storage_allowed
local_processing_allowed
embedding_allowed
quotation_allowed
maximum_quote_policy
export_allowed
cloud_processing_allowed
retention_policy
reviewed_by
reviewed_at
```

## 5.3 Required behavior

- Paid books supplied by the user may be analyzed privately but must not be redistributed.
- Full transcripts may not be generated, stored, or exported unless permitted.
- Search indexes derived from private licensed works remain local.
- Cloud-model prompts must not contain private source text unless the user explicitly authorizes that source and model profile.
- Exports should contain citations, metadata, short compliant excerpts where permitted, and original analysis. They should not reconstruct the source.
- A source without resolved rights remains metadata-only.
- Removal of an index entry must not falsify prior answer provenance. Historical answer records retain the source version identifier and a restricted-status marker.

This matches the corpus requirement that free access be favored, licensed private works not be redistributed, and acquisition mean legal access rather than bypassing paywalls. fileciteturn0file1

---

# 6. Source metadata

## 6.1 Work-level metadata

```yaml
work_id:
work_type:
title:
subtitle:
canonical_title:
creators:
publication:
original_publication_date:
date_precision:
language:
original_format_scope:
topics:
source_roles:
canonical_url:
local_reference:
access_status:
rights_profile_id:
acquisition_status:
authenticity_status:
source_stability:
notes:
created_at:
updated_at:
```

## 6.2 Edition or release metadata

```yaml
edition_id:
work_id:
edition_label:
revision_label:
release_date:
publisher_or_channel:
duration_or_page_count:
content_hash:
source_locator:
supersedes_edition_id:
is_complete:
is_authorized_copy:
transcript_status:
archived_at:
```

## 6.3 Person and identity metadata

```yaml
person_id:
display_name:
aliases:
pseudonyms:
identity_status:
identity_evidence:
do_not_merge_with:
roles:
notes:
```

Identity status:

```text
VERIFIED
PROBABLE
UNRESOLVED
SEPARATE_PENDING_REVIEW
PSEUDONYMOUS
ANONYMOUS
```

Rebell Lily and Rebell Son, for example, remain separate identities until continuity is verified. A Substack profile and a similarly named publication likewise remain separate until confirmed. The sourcebook explicitly identifies both as unresolved continuity risks. fileciteturn0file1

## 6.4 Source quality is not author quality

The corpus may score:

- source authenticity;
- directness;
- completeness;
- citation precision;
- format fit;
- review status;
- translation maturity.

It must not score “author prestige” or use fame to elevate a claim.

---

# 7. Typed knowledge graph

## 7.1 Node types

### Provenance nodes

| Node | Purpose |
|---|---|
| `Person` | Author, speaker, interviewer, editor, curator, commenter |
| `Organization` | Publisher, channel, website, project |
| `Work` | Intellectual work independent of edition |
| `Edition` | Specific version, release, episode, or revision |
| `SourceAsset` | File, page, audio, video, transcript, screenshot |
| `Segment` | Addressable passage, timestamp range, post, or section |
| `CitationAnchor` | Exact citation location and quotation metadata |

### Theory nodes

| Node | Purpose |
|---|---|
| `Claim` | Atomic attributed proposition |
| `Definition` | Source-specific definition of a term |
| `Concept` | Normalized topic such as tempo or inevitability |
| `Framework` | Structured analytical method |
| `QuestionPrompt` | Question a framework instructs the analyst to ask |
| `Example` | Source-supported illustration |
| `Counterexample` | Case showing failure or limitation |
| `Limitation` | Explicit or reviewed boundary |
| `Assumption` | Premise required for the claim |
| `FormatTranslation` | Controlled adaptation between formats |
| `Disagreement` | Structured conflict between claims or definitions |
| `AttributionChain` | Originator, expositor, synthesizer, later application |
| `Application` | Use of a claim on a deck, card, game, or scenario |
| `Hypothesis` | Testable but unapproved strategic proposition |
| `EmpiricalEvaluation` | Link to Codie evidence supporting or conflicting with theory |

### Curriculum nodes

| Node | Purpose |
|---|---|
| `Curriculum` | Versioned course structure |
| `Module` | Topic unit |
| `Lesson` | Individual learning packet |
| `LearningObjective` | Required competence |
| `Exercise` | Applied task |
| `Assessment` | Graded or self-checked task |
| `Rubric` | Evaluation criteria |
| `Prerequisite` | Required prior concept or skill |
| `Reflection` | User conclusion and change conditions |

### Governance nodes

| Node | Purpose |
|---|---|
| `ReviewDecision` | Approval, rejection, limitation, or deferral |
| `CorrectionRecord` | User or reviewer correction |
| `RightsProfile` | Storage and processing permissions |
| `IngestionRun` | Reproducibility and failure record |
| `GraphRelease` | Immutable approved graph snapshot |
| `RouterProfile` | Versioned retrieval configuration |

## 7.2 Edge types

### Authorship and provenance

```text
AUTHORED_BY
SPOKEN_BY
EDITED_BY
PUBLISHED_BY
INTERVIEWED_BY
CURATED_BY
HAS_EDITION
HAS_ASSET
HAS_SEGMENT
CITED_BY
DERIVED_FROM
TRANSCRIBED_FROM
SUMMARIZES
RESTATES
```

### Claim attribution

```text
ASSERTED_IN
DEFINED_IN
DEMONSTRATED_IN
ORIGINATED_BY
EXPOUNDED_BY
LATER_SYNTHESIZED_BY
ATTRIBUTED_TO
MISATTRIBUTED_TO
```

The Philosophy of Fire chain should therefore represent Adrian Sullivan as concept originator and Michael Flores as author of the canonical published exposition rather than flattening them into one ambiguous author field. fileciteturn0file1

### Conceptual relationships

```text
INSTANCE_OF
PART_OF
REQUIRES
ASSUMES
ENABLES
CONVERTS_TO
QUALIFIES
LIMITS
GENERALIZES
SPECIALIZES
OVERLAPS_WITH
DISTINCT_FROM
PRECEDES
FOLLOWS
```

### Evidence and disagreement

```text
SUPPORTS
CONTRADICTS
EMPIRICALLY_SUPPORTS
EMPIRICALLY_CONFLICTS
APPARENTLY_CONFLICTS
REFINES
SUPERSEDES
REJECTS
UNRESOLVED_WITH
```

### Translation and application

```text
APPLIES_TO_FORMAT
TRANSLATED_FROM
TRANSLATED_TO
VALIDATED_IN_FORMAT
REJECTED_IN_FORMAT
APPLIED_TO_DECK
APPLIED_TO_CARD
APPLIED_TO_PACKAGE
EXEMPLIFIES
COUNTEREXAMPLE_TO
```

### Curriculum relationships

```text
TEACHES
REQUIRES_PREREQUISITE
USES_SOURCE
USES_EXAMPLE
USES_COUNTEREXAMPLE
ASSESSES
HAS_RUBRIC
FOLLOWED_BY
```

## 7.3 Edge attributes

Every substantive edge must preserve:

```yaml
edge_id:
edge_type:
from_node_id:
to_node_id:
source_claim_id:
citation_anchor_ids:
scope:
format_scope:
deck_scope:
time_scope:
confidence:
review_status:
created_in_graph_version:
deprecated_in_graph_version:
reviewed_by:
reviewed_at:
```

An edge without provenance is merely a suggestion wearing a database costume.

---

# 8. Claim extraction

## 8.1 Claim labels

The extraction system must preserve the corpus labels:

```text
DIRECT_THEORY
DEMONSTRATED_APPLICATION
LATER_SYNTHESIS
JIN_INFERENCE
FORMAT_TRANSLATION
EMPIRICAL_SUPPORT
EMPIRICAL_CONFLICT
UNRESOLVED
```

These labels must remain distinct in storage and presentation. fileciteturn0file1

## 8.2 Atomic claim requirements

A claim must contain one independently reviewable proposition. It must not combine a definition, application, limitation, and conclusion into one paragraph-sized object.

Example:

```yaml
claim_id: claim_engine_001
claim_text: Engines should be analyzed through their inputs, outputs, repeatability, and conversion into a terminal objective.
claim_type: DIRECT_THEORY
polarity: AFFIRMATIVE
modality: SHOULD
subject_concept_ids:
  - engine-design
  - conversion-outlets
format_scope:
  - vintage
source_scope: GENERAL_FRAMEWORK
attributed_person_ids:
  - stephen_menendian
citation_anchor_ids:
  - anchor_understanding_gush_engine_section
limitations:
  - vintage_examples_not_directly_authoritative_for_cedh
review_status: APPROVED
```

A separate translation claim would address cEDH. A separate application claim would address a particular deck lacking a mana outlet.

## 8.3 Extraction procedure

```text
1. Identify source version.
2. Segment by stable location.
3. Identify speaker or writer for each segment.
4. Extract exact definitions before normalized concepts.
5. Split compound statements into atomic claims.
6. Record modality: is, may, usually, should, must, example only.
7. Record explicit assumptions.
8. Record source-provided examples.
9. Record source-provided limitations.
10. Distinguish argument from demonstrated deck application.
11. Attach exact citation anchors.
12. Identify attribution chains.
13. Generate candidate concepts and edges.
14. Flag possible contradiction or duplication.
15. Submit for review.
```

## 8.4 Extraction prohibitions

The extractor must not:

- rewrite an author into a stronger position;
- treat rhetorical questions as claims without context;
- infer universal rules from examples;
- merge distinct definitions of tempo;
- convert a decklist choice into an explicit author theory;
- use source-map descriptions as proof of the underlying article;
- approve claims from title-only sources;
- invent missing publication dates;
- merge pseudonyms without evidence;
- create direct quotations from machine summaries;
- assign cEDH applicability without a translation record.

## 8.5 Example and counterexample structure

```yaml
example_id:
claim_id:
description:
source_supported:
citation_anchor_ids:
format:
deck_or_card_refs:
conditions:
outcome:
example_status:
```

```yaml
counterexample_id:
claim_id:
description:
counterexample_type:
  # scope_failure, assumption_failure, empirical_conflict,
  # historical_obsolescence, multiplayer_failure, rules_failure
evidence_refs:
conditions:
review_status:
```

Counterexamples are not automatically refutations. They may merely identify scope.

---

# 9. Citations

## 9.1 Citation-anchor schema

```yaml
citation_anchor_id:
source_version_id:
segment_id:
locator_type:
  # page, paragraph, section, timestamp, post_id, comment_path
page_start:
page_end:
section_heading:
paragraph_start:
paragraph_end:
timestamp_start_ms:
timestamp_end_ms:
post_id:
comment_parent_id:
source_url:
accessed_at:
anchor_text_hash:
quotation_text:
quotation_storage_status:
quotation_length:
transcript_confidence:
notes:
```

## 9.2 Citation rules

- Claims require at least one exact anchor.
- Media claims require timestamp ranges.
- Forum and Reddit claims require post or comment identity and thread path.
- Transcripts must identify whether they are creator-provided, platform-generated, user-generated, or machine-generated.
- Paraphrases must cite the same anchor as the underlying claim.
- Direct quotations remain short and rights-compliant.
- Broken links do not erase a claim, but the source becomes `UNAVAILABLE` and the archived asset or verification record must remain.
- A later synthesis must cite both the synthesis source and the earlier source when the earlier attribution is material.
- Jin answer citations resolve through claim IDs to exact source anchors.
- Jin must not cite an author profile when the claim is supported only by one specific work.
- Curriculum summaries must preserve the original source list even when the learner sees a simplified lesson.

---

# 10. Concepts and definitions

Normalized concepts support retrieval. They do not erase source-specific definitions.

Example:

```text
Concept: Tempo
  |
  +-- Definition: Eric D. Taylor
  +-- Definition: Ian Lippert
  +-- Definition: Michael Devine
  +-- Definition: Patrick Chapin
  +-- Disagreement: Tempo vs Progress
  +-- Translation: 1v1 Tempo to cEDH
```

## 10.1 Concept schema

```yaml
concept_id:
preferred_name:
aliases:
description:
parent_concept_ids:
child_concept_ids:
router_tags:
definition_claim_ids:
disagreement_ids:
format_translation_ids:
status:
ontology_version:
```

## 10.2 Definition schema

```yaml
definition_id:
concept_id:
definition_text:
attributed_person_ids:
claim_id:
citation_anchor_ids:
format_scope:
time_scope:
distinguishing_features:
known_conflicts:
review_status:
```

The graph must never produce one blended definition merely because several writers use the same word. The corpus specifically identifies tempo as a family of distinct definitions and proposes disagreement nodes rather than premature merger. fileciteturn0file1

---

# 11. Transferability

## 11.1 Transfer states

```text
NATIVE
DIRECTLY_APPLICABLE
TRANSLATION_REQUIRED
TRANSLATION_PROPOSED
TRANSLATION_REVIEWED
EMPIRICALLY_SUPPORTED
EMPIRICALLY_CONFLICTED
REJECTED
INSUFFICIENT
```

## 11.2 Format-translation schema

```yaml
translation_id:
source_claim_id:
source_formats:
target_format:
translated_claim_text:
preserved_elements:
changed_assumptions:
new_assumptions:
multiplayer_effects:
commander_zone_effects:
singleton_effects:
mulligan_effects:
tutor_effects:
free_interaction_effects:
rules_or_card_pool_changes:
required_evidence:
supporting_evidence_refs:
conflicting_evidence_refs:
limitations:
review_status:
reviewed_by:
version:
```

## 11.3 Translation requirements

A cEDH translation must explicitly evaluate:

- four-player versus one-on-one incentives;
- three opponents rather than one;
- commander-zone access;
- singleton construction;
- free mulligan and Commander mulligan behavior;
- tutor density;
- free interaction;
- turn order;
- priority passing;
- shared policing burden;
- table politics;
- win-window creation;
- current legality and card pool;
- deck-specific conversion outlets.

The sourcebook already identifies translation targets such as Who’s the Beatdown into four-player role fragmentation, Turbo Xerox into singleton functional redundancy, Quadrant Theory into cEDH resource states, stax parity into multiplayer incentives, and mana probability into 99-card plus command-zone models. fileciteturn0file1

## 11.4 Transferability rule

No historical or cross-format claim may enter automatic cEDH retrieval at full relevance until it has an approved translation node.

---

# 12. Limitations

Limitations belong at several levels:

| Level | Example |
|---|---|
| Work | Article discusses an obsolete card pool |
| Claim | Assumes one opponent |
| Definition | Uses “tempo” only as mana development |
| Framework | Requires a stable aggressive and controlling role |
| Example | Demonstrates success in Limited, not cEDH |
| Translation | Does not account for commander recast access |
| Application | Depends on a mana outlet absent from the deck |
| Retrieval | Source identity unresolved |
| Rights | Full text cannot leave the local machine |
| Curriculum | Lesson source unavailable for free |

## 12.1 Limitation schema

```yaml
limitation_id:
limitation_type:
description:
applies_to_node_ids:
severity:
scope:
blocks_retrieval:
blocks_format_translation:
blocks_curriculum_use:
citation_anchor_ids:
review_status:
```

Severity:

```text
INFORMATIONAL
MATERIAL
BLOCKING
```

---

# 13. Reddit and community candidate handling

Reddit is useful for finding questions humans are arguing about. It is not useful as a magical authority generator.

## 13.1 Permitted uses

- discovery of primary sources;
- identification of emerging terminology;
- community hypotheses;
- matchup anecdotes;
- disputed interactions;
- historical source recovery;
- disagreement mapping;
- user-requested community context.

## 13.2 Prohibited uses

- tournament population evidence;
- canonical card or rules authority;
- automatic author-theory creation;
- causal claims;
- proof based on votes or comment score;
- promotion of screenshots into verified theory;
- identity inference across platforms;
- private subreddit or Discord ingestion without authorization.

## 13.3 Reddit candidate lifecycle

```text
DISCOVERED
    ->
SNAPSHOTTED
    ->
THREAD_CONTEXT_VERIFIED
    ->
SOURCE_LEADS_EXTRACTED
    ->
COMMUNITY_CLAIMS_CANDIDATE
    ->
CORROBORATION_REVIEW
    +----------------------+
    |                      |
    v                      v
COMMUNITY_CONTEXT      DISCOVERY_ONLY
    |                      |
    v                      v
INDEXED_WITH_LIMITS    ARCHIVED_OR_REJECTED
```

## 13.4 Reddit candidate schema

```yaml
community_candidate_id:
platform:
subreddit_or_forum:
thread_title:
thread_url:
thread_created_at:
retrieved_at:
author_handle:
author_identity_status:
post_or_comment_id:
parent_path:
edited_status:
deleted_status:
score_at_capture:
candidate_type:
  # source_lead, hypothesis, anecdote, terminology, disagreement
claim_text:
source_leads:
corroborating_sources:
contradicting_sources:
recency_class:
review_status:
privacy_status:
```

## 13.5 Recency

- Jin community retrieval defaults to the most recent 90 days.
- Older material may be used when it is the sole useful context, historically important, or part of an attribution chain.
- Source-recovery threads do not become irrelevant merely because they are old.
- Scores and awards are preserved as platform metadata, not credibility.

The Constitution and corpus both classify Reddit as community or discovery context rather than tournament evidence, and require date, author, context, attribution, and corroboration. fileciteturn0file0 fileciteturn0file1

---

# 14. Versioning

## 14.1 Versioned objects

Codie must version:

- source works;
- editions;
- assets;
- transcripts;
- segments;
- citation anchors;
- claims;
- concepts;
- definitions;
- edges;
- format translations;
- disagreement records;
- rights profiles;
- router profiles;
- graph releases;
- curriculum structures;
- lessons;
- answer packets.

## 14.2 Immutable history

A correction creates a new version. It does not overwrite the old version.

```text
claim_engine_001@1
    ->
SUPERSEDED_BY
    ->
claim_engine_001@2
```

Prior answers retain the graph release and claim versions they used.

## 14.3 Version identifiers

```text
source_schema_version
claim_schema_version
graph_ontology_version
graph_release_id
router_profile_version
curriculum_version
jin_theory_packet_version
```

## 14.4 Graph release

```yaml
graph_release_id:
ontology_version:
included_claim_versions:
included_edge_versions:
source_snapshot_ids:
router_compatibility:
created_at:
review_summary:
validation_artifact:
status:
```

Status:

```text
DRAFT
REVIEW
ACCEPTED
DEPRECATED
REVOKED
```

---

# 15. Ingestion states

## 15.1 Source ingestion state machine

```text
DISCOVERED
    ->
RIGHTS_REVIEW
    ->
ACQUISITION_PENDING
    ->
ACQUIRED
    ->
AUTHENTICITY_REVIEW
    ->
VERIFIED
    ->
SEGMENTATION_PENDING
    ->
SEGMENTED
    ->
EXTRACTION_PENDING
    ->
EXTRACTED
    ->
CLAIM_REVIEW
    ->
APPROVED
    ->
INDEXED
```

Failure and alternate states:

```text
METADATA_ONLY
UNAVAILABLE
QUARANTINED
REJECTED
DUPLICATE
SUPERSEDED
WITHDRAWN
RIGHTS_BLOCKED
IDENTITY_UNRESOLVED
```

## 15.2 Claim state machine

```text
CANDIDATE
    ->
ATTRIBUTION_REVIEW
    ->
CITATION_REVIEW
    ->
SCOPE_REVIEW
    ->
TRANSLATION_REVIEW
    ->
CONTRADICTION_REVIEW
    ->
APPROVED
    ->
PUBLISHED_IN_GRAPH
```

Alternate states:

```text
NEEDS_SOURCE
NEEDS_PRIMARY_SOURCE
NEEDS_RIGHTS_CLEARANCE
LIMITED
REJECTED
SUPERSEDED
WITHDRAWN
```

## 15.3 State invariants

- `ACQUIRED` does not imply permission to index.
- `EXTRACTED` does not imply truth or approval.
- `APPROVED` does not imply cEDH transferability.
- `INDEXED` does not imply automatic Jin routing.
- `SUPERSEDED` records remain queryable for historical provenance.
- `DISCOVERY_ONLY` material cannot support a direct-theory claim.

---

# 16. Review workflow

## 16.1 Logical reviewer roles

The project may have one human performing several roles, but the records must remain distinct.

| Role | Responsibility |
|---|---|
| Rights reviewer | Storage, processing, quotation, and export permissions |
| Source verifier | Authenticity, completeness, authorship, edition |
| Extractor | Candidate claims, definitions, examples, limitations |
| Attribution reviewer | Originator, expositor, synthesizer, application chain |
| Theory reviewer | Claim accuracy and scope |
| Format reviewer | Translation into cEDH or another target format |
| Rules reviewer | Current rules and legality dependencies |
| Contradiction reviewer | Conflicting definitions and claims |
| Curriculum reviewer | Pedagogical ordering and assessment quality |
| Release auditor | Graph determinism, privacy, and acceptance criteria |

## 16.2 Review sequence

```text
1. Register source.
2. Resolve rights.
3. Verify identity and completeness.
4. Create immutable source version.
5. Segment and anchor.
6. Extract candidate claims.
7. Review wording against source.
8. Review attribution chain.
9. Add examples, counterexamples, assumptions, and limitations.
10. Create or link normalized concepts.
11. Review format applicability.
12. Scan contradictions and duplicates.
13. Approve or limit.
14. Publish in a graph release.
15. Build retrieval index.
16. Run regression and privacy tests.
```

## 16.3 Review decision schema

```yaml
review_id:
reviewed_object_type:
reviewed_object_id:
review_type:
decision:
  # approve, approve_with_limits, reject, defer, supersede
reason:
required_changes:
reviewer:
reviewed_at:
source_version_ids:
graph_version_target:
```

---

# 17. Retrieval

## 17.1 Retrieval inputs

```yaml
question:
intent:
topics:
target_format:
deck_snapshot_id:
cards:
commanders:
packages:
rules_dependencies:
requested_theorists:
excluded_theorists:
requested_mode:
  # automatic, explicit_lens, council, debate, curriculum
time_scope:
community_recency:
theory_opt_out:
```

Substantive Jin strategy answers should retrieve relevant theory by default unless theory is explicitly disabled. That remains a presentation policy, not permission for theory to override evidence.

## 17.2 Retrieval stages

```text
Intent resolution
    ->
Topic and format tagging
    ->
Exact concept and claim lookup
    ->
Format-transfer eligibility filter
    ->
Rights and privacy filter
    ->
Deck-context applicability filter
    ->
Contradiction expansion
    ->
Diversity and duplication control
    ->
Theory packet assembly
```

## 17.3 Router scoring

Proposed initial router profile: `theory-router-v0.1`.

For candidate claim \(c\):

\[
R(c)=
0.30T+
0.20F+
0.15S+
0.15A+
0.10Q+
0.10D
\]

Where:

- \(T\): topic match;
- \(F\): format fit;
- \(S\): source-role and review fitness;
- \(A\): application fit to the deck, card, or question;
- \(Q\): citation and review quality;
- \(D\): contribution to framework diversity or material contradiction coverage.

All components are normalized from 0 to 1.

### Format-fit defaults

| Condition | \(F\) |
|---|---:|
| Native target-format claim | 1.00 |
| Approved translation with empirical support | 0.90 |
| Approved translation | 0.80 |
| Directly applicable general method | 0.75 |
| Translation proposed but unreviewed | 0.40 |
| Historical application only | 0.25 |
| Explicitly rejected in format | 0.00 |

### Source-role defaults

| Source role | Base \(S\) |
|---|---:|
| Reviewed primary theory | 1.00 |
| Reviewed primary definition | 1.00 |
| Reviewed later synthesis | 0.80 |
| Reviewed demonstrated application | 0.70 |
| Reviewed format bridge | 0.75 |
| Community context | 0.35 |
| Discovery map | 0.10 |
| Unverified candidate | 0.00 |

These values are router configuration, not constitutional truth. They must be versioned, inspectable, and testable.

## 17.4 Retrieval invariants

- No automatic fame weighting.
- No routing from title-only or discovery-only material.
- No cEDH routing from untranslated historical theory.
- At least one materially different framework should be included when available.
- Material known contradictions must be retrieved.
- Duplicate restatements should be collapsed into an attribution chain.
- Explicit user invocation may retrieve a low-confidence lens, but the limitation remains visible.
- Failure to find applicable theory must produce `INSUFFICIENT_CORPUS_COVERAGE`, not invented commentary.

The corpus already requires topic-based routing, relevance thresholds, independent frameworks, explicit invocation, preservation of disagreement, and no voice imitation. fileciteturn0file1

---

# 18. Contradiction handling

## 18.1 Disagreement types

```text
DEFINITIONAL
CONTEXTUAL
EMPIRICAL
FORMAT_SPECIFIC
PRIORITY_BASED
APPARENT
ATTRIBUTION
TEMPORAL
UNRESOLVED
```

The first six come directly from the corpus design; attribution and temporal conflicts are necessary implementation additions. fileciteturn0file1

## 18.2 Disagreement schema

```yaml
disagreement_id:
topic_id:
claim_a_id:
claim_b_id:
conflict_type:
overlapping_scope:
differing_assumptions:
format_scope:
time_scope:
materiality:
resolution_status:
resolution_note:
supporting_evidence_refs:
review_status:
```

Resolution status:

```text
PRESERVED
SCOPE_PARTITIONED
APPARENTLY_RECONCILED
EMPIRICALLY_FAVORS_A
EMPIRICALLY_FAVORS_B
SUPERSEDED
UNRESOLVED
```

## 18.3 Resolution rules

1. **Rules authority defeats theory on rules facts.**
2. **Current Oracle text defeats historical card interpretation.**
3. **Primary source outranks synthesis for attribution, not automatically for strategic correctness.**
4. **Native cEDH evidence does not automatically invalidate a durable cross-format concept. It may limit its translation.**
5. **Empirical support applies only to its population, deck, time, and metric scope.**
6. **Author count is irrelevant.**
7. **A contradiction caused by different definitions must remain definitional.**
8. **A contradiction caused by different game states should be scope-partitioned.**
9. **A famous framework does not receive a tie-breaker.**
10. **Unresolved conflicts remain visible in Jin and curriculum output.**

## 18.4 Contradiction scanner

The scanner should flag candidates when:

- claims share a concept but opposite polarity;
- definitions have incompatible necessary conditions;
- one claim generalizes where another supplies a counterexample;
- a later source attributes a concept differently;
- two translations alter different assumptions;
- empirical evidence supports opposing conclusions under overlapping scope;
- a current rules reference invalidates an older example.

The scanner proposes conflicts. It does not resolve them autonomously.

---

# 19. Jin integration

## 19.1 Theory packet

```yaml
theory_packet_id:
question:
intent:
target_format:
deck_snapshot_id:
graph_release_id:
router_profile_version:
selected_claims:
selected_frameworks:
selected_definitions:
examples:
counterexamples:
format_translations:
limitations:
disagreements:
community_context:
coverage:
missing_topics:
rights_restrictions:
generated_at:
```

## 19.2 Jin answer flow

```text
User question
    ->
Codie evidence retrieval
    ->
Theory packet retrieval
    ->
Independent framework memoranda
    ->
Evidence comparison
    ->
Answer draft
    ->
Rules and legality check
    ->
Citation check
    ->
Contradiction check
    ->
Unsupported-claim removal
    ->
Final answer packet
```

## 19.3 Writer boundary

The writer may:

- summarize approved claims;
- apply approved frameworks;
- produce explicitly labeled inference;
- compare theory against Codie evidence;
- generate a hypothesis;
- propose an experiment;
- explain why a translation may fail.

The writer may not:

- attribute new opinions to an author;
- promote a Jin inference into an approved claim;
- hide contradictory frameworks;
- treat theory as measured evidence;
- alter a citation;
- mutate a correction;
- persist a recommendation outside Decision Intelligence.

## 19.4 Auditor boundary

The auditor checks:

- every attributed statement resolves to an approved claim;
- every claim has an allowed citation;
- format translations are approved;
- material disagreements are represented;
- rules dependencies were checked;
- deck-specific claims use the correct snapshot;
- community claims are labeled;
- unsupported author imitation has been removed;
- confidence does not exceed corpus and evidence coverage;
- private source text was not exposed.

## 19.5 Final Jin answer packet

```yaml
direct_answer:
evidence_level:
theory_coverage:
speculation_level:
frameworks_used:
claims_used:
material_sources:
contradictory_frameworks:
format_transfer_warnings:
legality_status:
deck_snapshot_id:
unsupported_claims_removed:
illegal_suggestions_blocked:
confidence_ceiling:
suggested_experiment:
graph_release_id:
analysis_date:
```

This extends the Constitution’s required Jin safety fields with graph release and format-transfer provenance. fileciteturn0file0

---

# 20. Initial curriculum

## 20.1 Lesson format

Each lesson uses the sourcebook’s shared structure:

```text
Listen
Read
Compare
Apply
Assess
Reflect
```

The graph supplies the content. The curriculum determines order, difficulty, examples, and assessment. fileciteturn0file1

## 20.2 Curriculum structure

### Module 0: Evidence, attribution, and reasoning hygiene

**Objectives**

- Distinguish rules truth, tournament observation, measured evidence, theory, inference, and user judgment.
- Identify primary sources, synthesis, demonstrated application, and discovery material.
- Recognize when reputation is substituting for evidence.
- State what evidence would change a conclusion.

**Core frameworks**

Chapin, Sasser, Karsten, Sam Black, source-map and attribution-chain material.

**Assessment**

Given five statements, classify each by evidence layer, source role, and confidence limit.

---

### Module 1: cEDH fundamentals

**Topics**

- terminal and intermediate objectives;
- commander-zone value;
- singleton redundancy;
- mulligans;
- interaction burden;
- free interaction;
- turn order;
- win attempts;
- conversion outlets;
- local versus tournament context.

**Application**

Map a deck’s intended terminal state, intermediate objectives, primary interaction pattern, and failure states.

**Counterexample**

A deck containing an infinite-mana line but no present mana sink or conversion outlet.

---

### Module 2: Resource theory

**Topics**

- card advantage;
- virtual card advantage;
- mana;
- life;
- tempo;
- option value;
- Philosophy of Fire;
- resource conversion;
- one-shot resources;
- dead outputs;
- engine inputs and outputs.

**Primary lenses**

Taylor, Flores, Sullivan, Chapin, Menendian, Tait, Pierce.

**Assessment**

For a sequence, identify every resource consumed, produced, denied, delayed, or converted.

---

### Module 3: Tempo, progress, critical turns, and windows

**Topics**

- distinct definitions of tempo;
- progress theory;
- fundamental turn;
- critical turn;
- temporary win windows;
- developmental advantage;
- role-dependent tempo;
- multiplayer timing.

**Primary lenses**

Taylor, Devine, Zvi, Rebell Lily, Flores, Chapin, Lippert when recovered.

**Required disagreement**

Tempo as development differential versus tempo as role-dependent value versus progress toward terminal state.

**Application**

Rograkh/Ishai sequencing and free-protection windows.

---

### Module 4: Roles, table politics, and incentives

**Topics**

- Who’s the Beatdown;
- fragmented multiplayer roles;
- free riders;
- table incentives;
- threat presentation;
- political commitments;
- stax-removal incentives;
- hidden information;
- delayed commitment;
- rhetorical pressure.

**Primary lenses**

Flores, Reid Duke, Charles Zhuang, Rebell Lily, Peter Jahn after source recovery.

**Assessment**

Assign the role of each player against each opponent rather than giving every player one table-wide label.

---

### Module 5: Threat assessment and interaction allocation

**Topics**

- threat versus answer theory;
- permanent engines versus immediate wins;
- interaction burden;
- protected windows;
- priority order;
- false positives;
- tablewide consequences;
- stopping progress versus stopping timing.

**Application**

Construct a threat map for a four-player board, including which player is responsible for acting and why.

**Counterexample**

A permanent that appears dominant but does not improve its controller’s conversion path.

---

### Module 6: Sequencing, stack discipline, and priority

**Topics**

- action ordering;
- preserving options;
- hidden information;
- passing priority;
- casting windows;
- cost payment;
- targets;
- replacement effects;
- commander access;
- tutor-pile opponent choices;
- recovery sequencing.

**Primary lenses**

Menendian, Reid Duke, PVDDR, Chapin, judge-style rules material.

**Assessment**

Compare three legal lines, identify the information each exposes, and explain which options are lost.

---

### Module 7: Packages, engines, redundancy, and outlets

**Topics**

- deck versus pile;
- engine, support, and payload;
- packages;
- slot budgeting;
- functional overlap;
- tutors;
- conversion outlets;
- commander dependency;
- opportunity cost;
- Chekhov’s-gun analysis;
- template exceptions.

**Primary lenses**

Verhey, Menendian, Chapin, Comer, Sasser, Sam Black, Salubrious Snail, 8x8 as a limited heuristic.

**Assessment**

For each card in a package, identify required role, overlap, failure state, and minimum viable package size.

---

### Module 8: Probability, testing, and evidence

**Topics**

- hypergeometric models;
- colored sources;
- acceptable failure rates;
- sample size;
- simulation versus exact calculation;
- theory-driven, experience-driven, and data-driven development;
- gauntlet design;
- reproducibility;
- memorable-result bias.

**Primary lenses**

Karsten, Sasser, PVDDR, Chapin.

**Assessment**

Choose whether a question needs exact calculation, simulation, tournament evidence, or controlled playtesting.

---

### Module 9: Fallacies and argument analysis

**Topics**

- appeal to authority;
- popularity fallacy;
- survivorship bias;
- confirmation bias;
- base-rate neglect;
- false equivalence;
- moving the goalposts;
- post hoc reasoning;
- cherry-picking;
- anecdotal overreach;
- false dilemma;
- equivocation;
- motte-and-bailey;
- sunk-cost reasoning;
- attachment bias;
- the danger of strategically irrelevant “cool things.”

**Application**

Analyze deckbuilding arguments and table-political claims. Identify the fallacy, the valid underlying concern, and the evidence required to repair the argument.

**Boundary**

The course may teach recognition and defensive use of rhetoric. It must not present deceptive claims as evidence.

---

### Module 10: Judge-style reasoning

**Method**

1. Identify objects and zones.
2. Identify current Oracle text.
3. Identify relevant rules.
4. Identify costs, modes, choices, and targets.
5. Identify timing and priority.
6. Identify replacement and continuous effects.
7. Identify timestamps and dependencies where applicable.
8. Apply effects in order.
9. Check state-based actions and triggers.
10. Explain the result with authority citations.

**Fixtures**

- Paradise Mantle equip and creature-tap sequencing.
- Springleaf Drum object ownership and untap behavior.
- Commander recast and summoning sickness.
- Tutor-pile choice branches.
- Priority during win attempts.
- Historical judge article conflicting with current rules.

The judge-style sequence is already recognized in the Constitution’s Rules Layer design. fileciteturn0file0

---

### Module 11: Synthesis capstone

The learner receives:

- a deck snapshot;
- a tournament population;
- a disputed card;
- a rules interaction;
- two conflicting theory claims;
- one Reddit hypothesis;
- incomplete simulation evidence.

The learner must produce:

- an evidence map;
- theory comparison;
- format-translation analysis;
- legality finding;
- recommendation limits;
- experiment plan;
- list of facts that remain unresolved.

---

# 21. Core schemas

## 21.1 Claim

```yaml
claim_id:
claim_version:
claim_text:
claim_type:
polarity:
modality:
concept_ids:
framework_ids:
attributed_person_ids:
source_role:
citation_anchor_ids:
format_scope:
deck_scope:
time_scope:
assumption_ids:
example_ids:
counterexample_ids:
limitation_ids:
translation_ids:
disagreement_ids:
empirical_evaluation_ids:
confidence:
review_status:
created_at:
reviewed_at:
supersedes_claim_version:
```

## 21.2 Framework

```yaml
framework_id:
name:
description:
attributed_person_ids:
origin_claim_ids:
core_claim_ids:
definition_ids:
question_prompt_ids:
applicable_topics:
native_formats:
translation_requirements:
limitations:
minimum_source_threshold:
review_status:
```

## 21.3 Disagreement

```yaml
disagreement_id:
topic_id:
claim_ids:
conflict_type:
scope_overlap:
assumption_difference:
materiality:
resolution_status:
resolution_note:
evidence_refs:
review_status:
```

## 21.4 Application

```yaml
application_id:
claim_or_framework_ids:
target_type:
target_id:
deck_snapshot_id:
application_text:
source_or_inference:
evidence_refs:
conditions:
limitations:
outcome:
review_status:
```

## 21.5 Lesson

```yaml
lesson_id:
curriculum_version:
module_id:
title:
learning_objectives:
prerequisite_ids:
concept_ids:
claim_ids:
source_ids:
listen_assets:
read_assets:
comparison_ids:
exercise_ids:
assessment_ids:
reflection_prompt:
format_scope:
estimated_duration:
rights_constraints:
review_status:
```

## 21.6 Retrieval packet

```yaml
packet_id:
query_hash:
graph_release_id:
router_profile_version:
intent:
topic_ids:
format:
deck_snapshot_id:
claim_ids:
framework_ids:
definition_ids:
translation_ids:
disagreement_ids:
limitations:
community_candidate_ids:
coverage:
missing_coverage:
generated_at:
```

---

# 22. Fixtures

The initial test corpus should contain hand-reviewable fixtures rather than thousands of undifferentiated articles.

| Fixture | Purpose |
|---|---|
| Primary article with exact claims | Basic extraction and citation |
| Book with multiple editions | Edition and source-version handling |
| Licensed private book | Rights and local-only indexing |
| Video with creator transcript | Timestamp and speaker attribution |
| Video with machine transcript | Transcript-confidence limitations |
| Podcast with several speakers | Speaker-level attribution |
| Philosophy of Fire chain | Originator versus published expositor |
| Tempo definitions from multiple authors | Definitional contradiction |
| Turbo Xerox cEDH translation | Cross-format translation |
| Native cEDH Window claim | Native format routing |
| Rule of Law parity framework | Specialist routing and limits |
| 8x8 Theory | Heuristic limitation |
| Quadrant Theory | Limited-to-cEDH translation |
| Decklist without explicit essay | Demonstrated application only |
| Source-map article | Discovery-only enforcement |
| Missing historical article | Metadata-only and source-recovery state |
| Reddit screenshot | Discovery-only handling |
| Reddit thread with recoverable original source | Source-lead promotion |
| Edited or deleted Reddit post | Snapshot and status handling |
| Rebell identity ambiguity | Non-merge behavior |
| Tali profile ambiguity | Adjacent-source routing exclusion |
| Historical judge article | Current-rules override |
| User-created Chekhov application | User-context separation |
| Empirical conflict with theory | Scoped conflict attachment |
| Superseded claim | Immutable version history |
| Private deck application | Privacy and graph separation |

The corpus compilation already names tempo as the ideal pilot because it exposes definitional disagreement, role assignment, sequencing, resource theory, and multiplayer translation. That remains the correct pilot. fileciteturn0file1

---

# 23. Tests

## 23.1 Schema tests

- Reject unknown node and edge types.
- Reject substantive edges without provenance.
- Reject claims without citation anchors.
- Reject duplicate immutable version identifiers.
- Verify deterministic serialization.
- Verify migration forward and rollback behavior.

## 23.2 Rights tests

- Block indexing when rights are unresolved.
- Block cloud retrieval of private licensed text.
- Block export of prohibited full text.
- Permit citation metadata export.
- Preserve prior provenance after source withdrawal.
- Prevent private embeddings from entering shared indexes.

## 23.3 Attribution tests

- Preserve originator and expositor as different relationships.
- Refuse to infer author beliefs from decklists.
- Refuse to merge unresolved identities.
- Label later synthesis separately.
- Reject title-only claim extraction.
- Detect source-map material used improperly as primary support.

## 23.4 Claim-extraction tests

- Split compound statements into atomic claims.
- Preserve modality.
- Preserve explicit limitations.
- Distinguish example from general claim.
- Distinguish direct theory from Jin inference.
- Reject paraphrases that materially strengthen the source.
- Reject quotation text not found in the source version.

## 23.5 Translation tests

- Block unreviewed historical theory from full cEDH routing.
- Require multiplayer assumptions.
- Require singleton and commander-zone analysis where relevant.
- Attach translation limits.
- Preserve the original claim unchanged.
- Mark empirical support as population-specific.

## 23.6 Contradiction tests

- Detect opposite claims with overlapping scope.
- Avoid false conflict when scopes differ.
- Preserve distinct tempo definitions.
- Partition 1v1 and multiplayer claims.
- Never resolve by author count.
- Surface material contradictions in retrieval packets.

## 23.7 Retrieval tests

- Route by topic rather than author fame.
- Respect explicit theorist invocation.
- Exclude provisional writers from automatic routing.
- Include a materially different lens where available.
- Collapse duplicate syntheses.
- Respect format-transfer status.
- Return insufficient coverage rather than fabrication.
- Produce identical results for identical graph, router, and query inputs.

## 23.8 Jin boundary tests

- Jin cannot create or approve graph claims.
- Jin cannot mutate canonical evidence.
- Jin inference is labeled.
- Unsupported author attribution is removed.
- Material contradictions remain visible.
- Legality failures block the affected application.
- Private source text does not appear in the final answer.
- Deck-specific conclusions remain attached to the deck snapshot.
- Theory is omitted when explicitly disabled.
- Community context remains labeled.

## 23.9 Curriculum tests

- Every lesson has objectives, sources, application, assessment, and reflection.
- Prerequisite graph contains no cycles.
- Paid-only material is not required for the free curriculum.
- Lessons preserve disagreements.
- Rules lessons cite current authority.
- Assessments have deterministic rubrics where possible.

## 23.10 Privacy tests

- User notes cannot become author claims.
- Private deck applications cannot enter global theory.
- Cloud profiles reject disallowed sources.
- Logs omit source text and secrets.
- Deleted user notes are removed from curriculum and Jin indexes.
- Reddit usernames are not linked to external identities.

---

# 24. Privacy rules

1. Full source text, private annotations, user reflections, private decks, correction records, and embeddings remain local by default.
2. User-created applications are stored separately from the approved global theory graph.
3. A deck-specific conclusion must contain its deck snapshot ID.
4. Personal curriculum progress must not affect global claim confidence.
5. Public usernames remain source metadata only. Codie must not infer real identity or correlate identities across sites.
6. Prompt injection or executable instructions found inside a source are treated as quoted data.
7. Cloud model profiles must declare which source-rights classes they may receive.
8. Local model profiles may read permitted local indexes but cannot write approved graph state.
9. Export requires an explicit selection of private notes or reflections.
10. Source text must not be written to diagnostic logs.
11. Secrets, tokens, cookies, and authenticated source URLs must not be stored in graph records.
12. A user deletion request removes local content and indexes while preserving only non-content audit facts required for integrity.
13. Community screenshots supplied by the user remain private unless explicitly exported.
14. Private licensed works must never be included in a distributable fixture set.

These rules follow Codie’s local-first requirement for private decks, notes, theory annotations, prompts, traces, and tokens. fileciteturn0file0

---

# 25. Proposed modules

```text
codie/theory/
    models/
        person.py
        source.py
        segment.py
        citation.py
        claim.py
        concept.py
        framework.py
        translation.py
        disagreement.py
        curriculum.py

    repositories/
        source_repository.py
        claim_repository.py
        graph_repository.py
        review_repository.py
        curriculum_repository.py

    rights/
        rights_models.py
        rights_policy.py
        export_policy.py
        cloud_policy.py

    ingestion/
        source_registry.py
        acquisition_service.py
        authenticity_service.py
        segmenter.py
        transcript_service.py
        ingestion_state_machine.py

    extraction/
        claim_candidate_service.py
        definition_extractor.py
        example_extractor.py
        attribution_chain_service.py
        limitation_extractor.py

    review/
        review_service.py
        attribution_review.py
        format_review.py
        rules_review.py
        release_service.py

    graph/
        ontology.py
        edge_service.py
        graph_builder.py
        graph_validator.py
        graph_release_service.py

    contradictions/
        contradiction_scanner.py
        disagreement_service.py
        scope_comparator.py

    translation/
        format_translation_service.py
        cedh_translation_checks.py

    retrieval/
        intent_mapper.py
        topic_router.py
        claim_ranker.py
        diversity_selector.py
        theory_packet_builder.py

    community/
        reddit_candidate_service.py
        community_snapshot_service.py
        corroboration_service.py

    curriculum/
        curriculum_builder.py
        lesson_builder.py
        assessment_service.py
        progress_repository.py

    jin/
        theory_context_adapter.py
        theory_answer_auditor.py
        theory_citation_renderer.py

    exports/
        obsidian_exporter.py
        markdown_exporter.py
        json_exporter.py
```

## 25.1 Proposed public functions

```text
register_source_candidate(...)
review_source_rights(...)
record_source_version(...)
verify_source_identity(...)
segment_source_version(...)
create_citation_anchor(...)
extract_claim_candidates(...)
review_claim_candidate(...)
approve_claim(...)
create_format_translation(...)
record_disagreement(...)
publish_graph_release(...)
retrieve_theory_packet(...)
scan_answer_theory_support(...)
build_lesson_packet(...)
export_theory_graph(...)
```

All writes pass through repositories. Providers and Jin never write directly to graph tables.

---

# 26. Failure behavior

| Failure | Required behavior |
|---|---|
| Rights unresolved | Store metadata only; block content processing |
| Source unavailable | Preserve discovery record; do not extract claims |
| Author identity unresolved | Keep identities separate |
| Transcript unreliable | Lower citation usability; require manual verification |
| Claim lacks anchor | Block approval |
| Claim overstates source | Reject or rewrite as candidate |
| Primary source missing | Keep as synthesis or discovery only |
| Format translation missing | Exclude from automatic target-format routing |
| Contradictory claims | Preserve both and create disagreement candidate |
| Rules conflict | Current authority blocks outdated application |
| Source updated | Create a new immutable version |
| Source deleted | Preserve legal local archive or mark unavailable |
| Private source requested by cloud model | Block or substitute metadata-only packet |
| No relevant theory | Return insufficient corpus coverage |
| Graph release invalid | Do not publish or update retrieval index |
| Jin attempts mutation | Reject operation and record boundary violation |
| Curriculum source becomes unavailable | Substitute an approved source or mark lesson incomplete |
| Reddit original cannot be recovered | Retain discovery-only status |
| Empirical evidence conflicts with theory | Attach scoped conflict; do not rewrite the theory claim |

---

# 27. Implementation phases

Building ingestion, extraction, a graph database, contradiction logic, Jin retrieval, and an educational platform in one pull request would produce exactly the kind of half-working monument the no-stubs rule exists to prevent.

## Phase TC-A: Constitutional and ontology contract

**Deliverables**

- approved source-role taxonomy;
- node and edge enums;
- rights classes;
- ingestion states;
- review roles;
- schema ownership;
- exclusions;
- migration plan.

**No production ingestion.**

## Phase TC-B: Source registry and rights foundation

**Deliverables**

- source, edition, asset, rights, and identity schemas;
- repositories;
- immutable version hashes;
- rights enforcement;
- metadata-only ingestion;
- fixtures and migrations.

## Phase TC-C: Segments and citations

**Deliverables**

- stable segment model;
- page, section, timestamp, post, and comment anchors;
- transcript provenance;
- citation validation;
- local source storage boundaries.

## Phase TC-D: Claim candidates and review

**Deliverables**

- claim, definition, example, limitation, assumption, and attribution-chain models;
- candidate workflow;
- approval workflow;
- direct theory versus synthesis enforcement.

## Phase TC-E: Graph and contradiction system

**Deliverables**

- concept ontology;
- typed edges;
- disagreement records;
- contradiction scanner;
- graph release snapshots;
- deterministic export.

## Phase TC-F: Format translation

**Deliverables**

- translation schema;
- cEDH-specific assumption checklist;
- translation review;
- transferability filters;
- empirical support and conflict links.

## Phase TC-G: Retrieval and routing

**Deliverables**

- topic mapping;
- deterministic candidate ranking;
- diversity selection;
- contradiction expansion;
- rights filtering;
- theory packet contract.

## Phase TC-H: Jin integration

**Deliverables**

- theory context adapter;
- writer boundary;
- auditor;
- citation rendering;
- final-answer packet;
- mutation-block tests.

## Phase TC-I: Curriculum foundation

**Deliverables**

- curriculum, module, lesson, exercise, assessment, rubric, and progress models;
- initial modules;
- free-access checks;
- Obsidian and Markdown output.

## Phase TC-J: Tempo pilot

**Deliverables**

- recovered and verified tempo sources;
- distinct definitions;
- disagreement graph;
- 1v1-to-cEDH translations;
- Rograkh/Ishai application;
- curriculum lessons;
- end-to-end Jin retrieval tests.

## Phase TC-K: Initial corpus expansion

Add resource theory, roles, windows, packages, probability, fallacies, and judge-style reasoning only after the tempo pilot passes.

---

# 28. Codex implementation handoff

## Task name

**Codie V2 Theory Corpus and Attributed Knowledge Graph Foundation**

## Authority

Implementation requires an accepted phase contract. Neither the V2 comparison draft nor this specification alone authorizes repository changes. fileciteturn0file0

## Objective

Create the governed local-first foundation for attributed theory sources, immutable source versions, rights controls, exact citations, reviewed claims, typed graph relationships, format translations, contradictions, retrieval packets, and curriculum records.

## Authorized initial scope

Phase TC-A only:

- ontology specification;
- schema proposal;
- rights model;
- ingestion-state model;
- repository ownership;
- migration design;
- interface contracts;
- fixtures;
- tests;
- failure behavior;
- validation packet.

## Explicit exclusions

- no bulk source acquisition;
- no web scraping;
- no embedding model;
- no vector database;
- no automatic claim approval;
- no LLM-generated production graph;
- no Jin integration;
- no curriculum UI;
- no Obsidian vault generation;
- no cloud processing;
- no Reddit monitoring;
- no source-text redistribution;
- no changes to canonical evidence or Decision Intelligence;
- no author authority score;
- no final router weights beyond a documented draft profile;
- no theory-driven recommendations.

## Required data models

```text
TheoryPerson
TheoryWork
TheoryEdition
TheorySourceAsset
TheoryRightsProfile
TheorySegment
TheoryCitationAnchor
TheoryClaim
TheoryConcept
TheoryFramework
TheoryExample
TheoryCounterexample
TheoryLimitation
TheoryAssumption
TheoryFormatTranslation
TheoryDisagreement
TheoryEdge
TheoryReviewDecision
TheoryGraphRelease
TheoryCurriculum
TheoryModule
TheoryLesson
TheoryAssessment
TheoryCommunityCandidate
```

## Repository ownership

```text
TheorySourceRepository
TheoryClaimRepository
TheoryGraphRepository
TheoryReviewRepository
TheoryCurriculumRepository
```

No generic repository may bypass type validation or version rules.

## Required interfaces

```text
SourceRegistry.register_candidate
RightsService.evaluate
SourceVersionService.create_immutable_version
CitationService.create_anchor
ClaimReviewService.submit_candidate
ClaimReviewService.record_decision
GraphService.add_typed_edge
GraphReleaseService.build_release
ContradictionService.scan
TranslationService.validate_target_format
TheoryRetrievalService.build_packet
```

Only contracts and test doubles are permitted in TC-A. Runnable production behavior belongs to later authorized phases. The project’s no-stubs rule means TC-A should not pretend interfaces are implemented merely because empty files exist.

## Required fixtures

At minimum:

1. Primary theory article.
2. Licensed private book.
3. Multi-speaker podcast.
4. Machine transcript.
5. Originator/expositor attribution chain.
6. Tempo-definition conflict.
7. Untranslated historical claim.
8. Native cEDH claim.
9. Source map.
10. Reddit discovery thread.
11. Unresolved pseudonym.
12. Current-rules conflict.
13. Superseded source edition.
14. User-created deck application.

## Required tests

- enum and schema validation;
- immutable versioning;
- rights policy;
- citation-anchor validation;
- source-role enforcement;
- author non-authority enforcement;
- unresolved identity separation;
- discovery-only restrictions;
- translation gate;
- contradiction preservation;
- deterministic graph serialization;
- privacy boundaries;
- Jin mutation boundary contract;
- migration and rollback plan validation.

## Acceptance criteria

1. Every approved claim requires a source version and exact citation anchor.
2. Authors cannot be marked as canonical authorities.
3. Source type and source role are separate fields.
4. Rights determine storage, indexing, quotation, export, and cloud processing independently.
5. Discovery-only sources cannot support approved direct-theory claims.
6. Source versions are immutable and hash-addressed.
7. Claim corrections produce new versions.
8. Definitions remain source-specific.
9. Cross-format claims require translation records before automatic cEDH routing.
10. Contradictions are stored, classified, and surfaced rather than averaged.
11. User notes cannot be attributed to theorists.
12. Private licensed content cannot enter cloud packets or exports.
13. Reddit content cannot enter tournament analytics.
14. Graph releases are deterministic and versioned.
15. Jin has no graph mutation interface.
16. No source text, token, or secret appears in logs or validation artifacts.
17. All required failure states have negative-path tests.
18. The phase contains no hidden manual database edits.
19. Standard deterministic, architecture, adversarial, and aggregate validators pass.
20. The next authorized phase is explicitly designated.

## Validation packet

The implementation handoff must include:

```text
phase identifier
authorized contract
commit SHA
changed files
schema diff
migration plan
repository ownership map
public interfaces
fixture inventory
test commands
test results
rights-boundary results
privacy-boundary results
deterministic serialization hash
architecture verdict
adversarial verdict
aggregate verdict
unresolved findings
next-phase designation
```

## Unresolved decisions requiring governance approval

1. Whether the canonical graph lives only in SQLite or also exports to an Obsidian mirror.
2. Whether source assets are stored in the database, filesystem, or content-addressed local vault.
3. Whether embeddings are permitted for private licensed works.
4. Which transcript generators are acceptable.
5. Whether user review alone is sufficient for claim approval or selected claims require a second reviewer.
6. Whether empirical support edges are stored in the theory database or resolved through external evidence references.
7. Final router weight profile.
8. Minimum primary-source threshold for automatic framework routing.
9. Whether community snapshots may retain deleted public posts.
10. Whether curriculum progress belongs in the main Codie database or a separate private learning store.
11. Exact quotation limits by rights class.
12. Whether adjacent non-Magic reasoning sources remain in the same graph or a segregated namespace.
13. Whether corrections to approved claims require full graph rerelease or can enter a patch release.
14. The approved initial tempo source set.
15. The ratification status required before TC-B may begin.
> [!IMPORTANT]
> Repository intake note: This is a preserved pre-ratification design
> proposal. `docs/CODIE_V2_CONSTITUTION.md` is now ratified and is the
> governing authority. Statements below that call V2 a non-authoritative
> comparison draft are historical. This proposal does not authorize
> implementation.
