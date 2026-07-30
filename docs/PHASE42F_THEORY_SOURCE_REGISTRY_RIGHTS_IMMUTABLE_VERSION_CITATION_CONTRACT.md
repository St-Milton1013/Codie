# Phase 42F - Theory Source Registry, Rights, Immutable Source Version, and Citation Contract

Status: contract only; implementation not authorized

## Validation Tuple

```text
phase_id: Phase42F
phase_part: outside-validation
gate_scope: INTERMEDIATE_PACKET
next_phase_id: Phase42G
next_phase_part: outside-validation
next_gate_scope: INTERMEDIATE_PACKET
```

Phase 42G is reserved for the Reviewed Claim, Typed Graph, Contradiction,
Translation, and Retrieval Contract. It remains blocked until Phase 42F
outside validation returns PASS or PASS WITH REVIEW NOTES.

## Purpose

Phase 42F defines the provenance and rights foundation that must exist before
the Theory Corpus may create approved claims or retrieval packets.

This contract governs:

```text
person and organization identity
work identity
edition and release identity
source asset identity
source role
rights and access state
immutable source versions
segments
exact citation anchors
quotation handling
source availability and takedown state
attribution-chain inputs
```

It does not create claims, concepts, graph edges, translations, retrieval
packets, curriculum, embeddings, or Jin output.

## Authority

This contract is governed by:

1. `docs/CODIE_V2_CONSTITUTION.md`;
2. `docs/ROADMAP_PATCH_V2_INTELLIGENCE_PROGRAM_INTAKE.md`;
3. the accepted Phase 42A cross-specification boundary;
4. the accepted Phase 42C Rules authority contract;
5. the accepted Phase 42D model-profile and privacy contract;
6. the accepted Phase 42E Correction Ledger core contract;
7. `docs/design_inputs/v2_intelligence_program/CODIE_V2_THEORY_CORPUS_ATTRIBUTED_KNOWLEDGE_GRAPH_PROPOSAL.md`
   as preserved design input only.

## Governing Invariants

```text
Theory contextualizes evidence; it does not replace authority or measurement.
Authors are provenance subjects, not truth authorities.
Source type and source role remain separate.
Every approved future claim requires an immutable source version and exact anchor.
Rights to store, process, quote, export, and transmit are separate decisions.
Unknown rights fail closed.
Private licensed content remains local by default.
Discovery material does not prove the discovered claim.
Machine summaries and transcripts are processing artifacts, not originals.
Historical versions are never silently rewritten.
Identity ambiguity remains visible.
```

## Trust Boundary

The future governed sequence is:

```text
source candidate
-> identity review
-> source-role classification
-> access and rights review
-> permitted acquisition
-> immutable source version
-> stable segmentation
-> exact citation anchors
-> attribution review inputs
-> future candidate claim extraction
```

Phase 42F stops at citation anchors.

## Supported Source Types

```text
book
article
essay
primer
newsletter_or_substack
video
podcast
transcript
forum_thread
community_thread
source_map_or_bibliography
decklist
tournament_report
curated_user_note
official_rules_material
judge_article
design_article
adjacent_non_magic_work
generated_transcription
generated_summary
screenshot
```

A source type describes its medium. It does not determine evidentiary role,
authority, rights, or strategic quality.

## Source Roles

Each source version declares one or more roles:

```text
primary_theory
primary_definition
primary_application
later_synthesis
historical_retelling
format_bridge
design_context
rules_explanation
community_context
debate_record
discovery_map
user_interpretation
adjacent_method
empirical_context
unknown
```

Each future claim must name the role under which its anchor is used.

Rules:

```text
a primer is deck-specific by default
a decklist demonstrates an application but not a complete philosophy
a source map discovers material but does not support the underlying claim
a Reddit or community item is candidate or community context by default
official rules material routes to the Rules Layer for authority use
a judge article is explanation, while current official rules remain authority
a generated summary cannot become primary theory
```

## Work Identity

A work is the intellectual item independent of a particular edition or asset.

Required work fields:

```text
work_id
work_type
title
canonical_title
subtitle, when any
creator_refs
publication_or_channel
original_publication_date
date_precision
language
original_format_scope
topic_tags
source_roles
canonical_locator
rights_profile_id
access_status
authenticity_status
identity_status
created_at
record_version
metadata
```

Titles, URLs, display names, and topic similarity are not sufficient to merge
works.

## Person And Organization Identity

Required person identity fields:

```text
person_id
display_name
aliases
pseudonyms
identity_status
identity_evidence_refs
do_not_merge_with
roles
record_version
```

Allowed identity states:

```text
verified
probable
unresolved
separate_pending_review
pseudonymous
anonymous
```

Uncertain identities remain separate. A similarly named profile, publication,
channel, or pen name is not merged without evidence.

Organizations and publications receive separate identities from people.

Author reputation, follower count, tournament success, and popularity are not
truth scores.

## Edition And Release Identity

An edition is a specific release, revision, episode, post revision, or
published version of a work.

Required fields:

```text
edition_id
work_id
edition_label
revision_label
release_date
publisher_or_channel
duration_or_page_count
source_locator
supersedes_edition_id, when any
is_complete
is_authorized_copy
transcript_status
identity_status
created_at
record_version
```

A later edition does not mutate or replace the historical content of an
earlier edition.

## Source Asset

A source asset is one permitted local or remote representation:

```text
source_asset_id
edition_id
asset_type
locator
media_type
encoding
language
content_length
content_hash
acquired_at
accessed_at
acquisition_method
authenticity_status
completeness_status
rights_profile_id
retention_state
record_version
```

Credentials, session tokens, paywall bypass data, and private account
identifiers are never stored in source assets.

## Rights Model

Rights decisions are independent:

```text
full local storage
local processing
local indexing or embeddings
short quotation
source-text export
cloud processing
retention
```

One permission does not imply another.

Required rights classes:

| Class | Default handling |
|---|---|
| `user_created` | local use and export per user ownership and consent |
| `public_domain` | allowed subject to verified status |
| `open_licensed` | follow the exact license |
| `public_link_only` | metadata, link, and permitted excerpts only |
| `user_licensed_private` | local private use; no redistribution or cloud by default |
| `platform_transcript_limited` | only the platform-permitted handling |
| `community_public` | permitted snapshot or index; no bulk republication |
| `unknown_restricted` | metadata only |
| `takedown_or_withdrawn` | no new processing, quoting, export, or transmission |

Every rights profile preserves:

```text
rights_profile_id
rights_class
copyright_holder_known
license_identifier
license_locator_or_note
full_text_storage_allowed
local_processing_allowed
indexing_allowed
embedding_allowed
quotation_allowed
maximum_quote_policy
export_allowed
cloud_processing_allowed
retention_policy
review_status
reviewed_by
reviewed_at
effective_from
record_version
```

Unknown or conflicting rights are restrictive.

User upload or possession is not blanket redistribution permission.

## Access And Acquisition States

```text
candidate
metadata_verified
access_permitted
acquired
unavailable
access_revoked
takedown_or_withdrawn
revalidation_required
rejected
```

Acquisition means lawful permitted access. It does not include bypassing
paywalls, access controls, robots restrictions, or platform terms.

Phase 42F does not implement acquisition.

## Immutable Source Version

Each permitted acquired representation creates an immutable version:

```text
source_version_id
work_id
edition_id
source_asset_id
source_version_number
content_hash
normalized_content_hash
source_role_set
rights_profile_id
language
completeness_status
transcript_provenance
created_at
supersedes_source_version_id, when any
record_version
```

Changing content, segmentation inputs, transcript provenance, or rights
identity creates a new version or rights event. It never edits historical
content in place.

Source versions preserve hashes even when content retention later becomes
restricted, so historical provenance can identify the exact unavailable
version without reconstructing it.

## Transcript Provenance

Transcript states:

```text
creator_provided
publisher_provided
platform_generated
user_transcribed
machine_generated
reviewed_machine_transcript
unavailable
```

Every transcript records:

```text
source media version
generator or contributor
generation or capture time
language
confidence or review state
known omissions
speaker attribution state
content hash
```

A generated transcript is a representation of the media, not a replacement
for the original source.

## Segments

A segment is an addressable portion of one source version.

```text
segment_id
source_version_id
segment_type
sequence
speaker_or_author_ref
page range, section, paragraph, timestamp, post, or comment path
segment_text_hash
transcript_confidence, when applicable
created_at
segment_version
```

Stable source-native locators are preferred. Segment boundaries must be
deterministic for the same source version and segmentation policy.

## Citation Anchors

Every future approved claim requires at least one exact citation anchor.

Required fields:

```text
citation_anchor_id
source_version_id
segment_id
locator_type
page_start and page_end
section_heading
paragraph_start and paragraph_end
timestamp_start_ms and timestamp_end_ms
post_id
comment_parent_id
source_locator
accessed_at
anchor_text_hash
quotation_storage_status
quotation_length
transcript_confidence
anchor_version
notes
```

Only fields applicable to the locator type are populated.

Rules:

```text
books and documents use edition-aware page or section anchors
media uses timestamp ranges and speaker identity
forums use post or comment identity plus thread path
transcripts declare provenance
paraphrases cite the anchor supporting the paraphrase
direct quotations remain short and rights-compliant
author profile pages do not substitute for the cited work
source maps do not substitute for the underlying source
```

Anchor text hashes support verification. They do not authorize retaining or
exporting disallowed quotation text.

## Quotation Handling

Quotation state:

```text
not_stored
hash_only
short_excerpt_permitted
private_local_excerpt
restricted
withdrawn
```

The maximum quote policy is rights-profile specific.

No export may reconstruct a restricted source through many small excerpts.

Jin and future curriculum output cite and paraphrase by default. Quotation
requires explicit rights eligibility and output policy.

## Availability, Takedown, And Withdrawal

A broken locator does not erase historical provenance.

When a source is unavailable or withdrawn:

```text
new extraction stops
new quotation stops unless independently lawful and permitted
new export and cloud transmission stop
approved future claims become unavailable or revalidation-required according
to the later claim contract
historical answer packets retain source-version identity and restriction state
```

A takedown does not falsify prior usage history.

## Attribution Inputs

Phase 42F stores only provenance facts needed by a future attribution chain:

```text
creator or speaker
editor, interviewer, translator, or curator
work and source version
explicit cited predecessor work
declared adaptation or synthesis role
identity uncertainty
```

It does not decide that one author originated a concept merely because the
earliest locally known source belongs to that author.

The future claim contract must distinguish originator, expositor, synthesizer,
and later application.

## Community And Discovery Boundary

Community and RSS material may create candidate source records.

It may not directly create:

```text
approved theory claims
tournament observations
measured evidence
canonical truth
recommendations
authoritative Rules records
```

Promotion requires review of the linked work, author, attribution, relevance,
rights, and transferability.

## Rules Material Boundary

Official rules and legality material remain governed by Phase 42C.

The Theory source registry may reference a Rules authority package for
curriculum provenance. It may not duplicate or override Rules authority.

Judge articles and historical rules discussions remain explanatory context.

## Model And Cloud Boundary

Phase 42D controls every model route.

```text
restricted theory content remains local
unknown-rights content cannot enter a model packet
cloud use requires rights permission plus profile-specific consent
source text is minimized before any eligible external request
model output cannot change source identity, rights, versions, or review state
```

No live model use is authorized in Phase 42F.

## Privacy

Private source locators, user-owned files, notes, and licensed content are
local by default.

The registry may preserve non-sensitive source identity separately from
private content. Logs and exports must not expose absolute paths, account
identifiers, tokens, or private source text.

## Required Validation States

```text
IDENTITY_UNRESOLVED
ROLE_UNRESOLVED
RIGHTS_UNRESOLVED
ACCESS_NOT_PERMITTED
SOURCE_UNAVAILABLE
SOURCE_INCOMPLETE
HASH_MISMATCH
TRANSCRIPT_PROVENANCE_UNRESOLVED
SPEAKER_UNRESOLVED
ANCHOR_INVALID
ANCHOR_STALE
QUOTATION_BLOCKED
EXPORT_BLOCKED
CLOUD_BLOCKED
TAKEDOWN_OR_WITHDRAWN
REVALIDATION_REQUIRED
```

Unknown states remain visible and fail closed for promotion.

## Required Regression Cases

A future implementation contract must cover:

```text
same work with two editions remains one work and two editions
revised article creates a new immutable source version
similar person names remain separate without identity evidence
pseudonymous creator remains labeled pseudonymous
source map cannot support the discovered claim
Reddit RSS item remains candidate-only
user-licensed book remains local and non-exportable
unknown rights retain metadata only
open license follows its exact quotation and export limits
generated transcript preserves media and generator provenance
podcast anchor requires timestamp and speaker
forum anchor requires post or comment path
anchor hash mismatch creates a stale or invalid state
takedown blocks new processing without erasing historical identity
short excerpts cannot be composed into source reconstruction
provider profile cannot override rights denial
model output cannot mutate rights or source identity
```

## Resolved Decisions

Phase 42F resolves:

```text
source type and source role separation
work, edition, asset, source-version, segment, and anchor identities
person and organization identity ambiguity
independent rights permissions
restrictive handling for unknown rights
immutable content and provenance versions
transcript provenance states
exact anchor requirements by medium
quotation-state handling
takedown without provenance erasure
community and discovery candidate-only defaults
```

## Deferred Decisions

Later accepted contracts must decide:

```text
schema, migrations, repositories, and indexes
acquisition adapters and allowed source-specific mechanisms
transcription tools
embedding storage
claim extraction and review
graph relationships
translation and contradiction policy
retrieval weights
curriculum storage
export rendering and file writing
initial source set
```

## Future Implementation Boundary

A later implementation contract may first authorize pure packets and
validators:

```text
TheoryPerson
TheoryOrganization
TheoryWork
TheoryEdition
TheoryRightsProfile
TheorySourceAsset
TheorySourceVersion
TheorySegment
TheoryCitationAnchor
TheorySourceValidationReport
```

No acquisition, storage, claim extraction, graph, model, UI, or export work is
authorized without explicit later contracts.

## Phase 42G Boundary

Phase 42G may define only reviewed atomic claims, typed graph relationships,
contradiction records, format translations, and retrieval packets using
approved Phase 42F source versions and anchors.

It must not implement the graph, extraction, embeddings, retrieval, models,
Jin, curriculum, UI, exports, or network behavior.

## Forbidden Phase 42F Work

Phase 42F must not add:

```text
production Theory Corpus code
implementation tests or fixtures
schema, migrations, or repositories
source acquisition or scraping
paywall or access-control bypass
transcription or embeddings
claim extraction or approval
graph nodes or relationships
translation or retrieval
Jin, model, or curriculum behavior
Rules duplication
Correction Ledger mutation
Decision Intelligence or recommendations
UI, CLI, export, or file-writing behavior
live network calls
dependency changes
workflow or validator changes
active-scope changes in the PR
constitution changes
```

## Acceptance Gate

Phase 42F passes only when outside validation confirms that it:

1. remains contract-only;
2. records Phase 42E artifact-backed acceptance;
3. keeps theory contextual and authors non-authoritative;
4. separates source type, role, identity, and rights;
5. models each rights permission independently;
6. fails closed on unknown rights or identity;
7. requires immutable source versions;
8. requires exact medium-appropriate citation anchors;
9. preserves transcript and speaker provenance;
10. blocks unauthorized quotation, export, and cloud processing;
11. preserves historical identity after unavailability or takedown; and
12. keeps Phase 42G blocked.

Phase 42G may begin only after Phase 42F outside validation returns PASS or
PASS WITH REVIEW NOTES.
