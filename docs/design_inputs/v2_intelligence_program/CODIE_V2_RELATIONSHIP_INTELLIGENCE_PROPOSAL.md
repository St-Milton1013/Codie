



The attached document is a non-authoritative comparison draft. This design is therefore a proposed implementation contract, not authorization to change Codie. It follows the constitution’s separation of canonical data, Class 2 measurement, Evidence Fusion, Decision Intelligence, theory context, and Jin; its requirements for visible formulas, populations, coverage, uncertainty, conflicts, and provenance; and its prohibition against treating observational association as causal proof. fileciteturn0file0

:::writing{variant="document" id="58317"}
# Codie V2 Relationship Intelligence Subsystem
## Proposed Architecture and Contract-Ready Codex Handoff

**Status:** Proposed design
**Authority:** Non-authoritative until separately approved and contracted
**Subsystem class:** Class 2 Measured Evidence, with separate structural-authority and theory-context projections
**Primary storage:** SQLite through approved repositories
**Recommendation authority:** None
**LLM execution:** None inside Relationship Intelligence

---

# 1. Purpose

Relationship Intelligence measures, records, and explains typed relationships among:

- cards;
- functional tags;
- recognized combos;
- curated packages;
- commander signatures;
- deck snapshots;
- tournament deck instances;
- events;
- regions;
- theory claims.

The subsystem answers:

1. Which relationships are explicitly declared by authoritative or curated sources?
2. Which elements occur together in a defined population?
3. How much more or less often does one element appear when another is present?
4. How similar are two elements, decks, packages, or populations?
5. Which apparent relationships may instead result from commander identity, color identity, region, time, generic staples, package definitions, source duplication, or low sample size?
6. Which evidence may Jin describe without transforming association into causation or recommendation?

Relationship Intelligence does not decide whether a card should be played. It produces evidence that may later enter Unified Evidence and, only after that boundary, Decision Intelligence.

---

# 2. Constitutional Boundaries

## 2.1 Authorized responsibilities

Relationship Intelligence may:

- resolve approved populations from canonical records;
- project entities into deterministic population predicates;
- calculate approved relationship metrics;
- create explicit structural relationships from authoritative and curated definitions;
- calculate deck-level co-occurrence;
- calculate directional and symmetric association metrics;
- calculate deck-list similarity;
- aggregate card relationships into functional-tag relationships;
- compare global, regional, commander, event-size, and placement scopes;
- identify likely confounders;
- expose low-sample and coverage limitations;
- preserve metric provenance;
- create references suitable for Unified Evidence;
- provide read-only evidence to Jin.

## 2.2 Prohibited responsibilities

Relationship Intelligence may not:

- fetch raw provider data;
- canonicalize source records;
- deduplicate events or deck instances;
- approve aliases;
- infer Oracle functionality;
- create Commander Spellbook combo authority;
- invent package definitions;
- persist recommendations;
- generate replacement proposals;
- assign strategic value;
- claim rules interactions from co-occurrence;
- claim causal effects;
- call an LLM;
- write to Jin’s theory notes or correction ledger;
- place private user decks into global evidence without explicit authorization;
- combine structural, measured, and theory relationships into an unlabeled edge.

## 2.3 Required evidence separation

Every relationship belongs to exactly one assertion class:

| Assertion class | Meaning | Evidence class |
|---|---|---|
| `AUTHORITY_DECLARED` | Imported from an approved authority | Class 0 |
| `CURATED_DECLARED` | Defined by a versioned package or correction registry | Class 0C or governed context |
| `OBSERVED_STRUCTURAL` | Directly represented by a canonical observation | Class 1 |
| `DERIVED_STRUCTURAL` | Deterministically projected from declared structure | Class 1 or Class 2 derivation |
| `MEASURED_ASSOCIATION` | Calculated from a defined population | Class 2 |
| `THEORY_CONTEXT` | Attributed human strategic claim | Context layer |
| `USER_CONTEXT` | User-supplied deck or local hypothesis | Class 4 |

No assertion may be silently promoted from one class to another.

Examples:

- “Card A has Tag T” is an ontology assertion.
- “Card A and Card B appear together in 18% of eligible decks” is measured association.
- “Combo C requires Card A” is an authority assertion.
- “Author X argues that Card A enables Card B” is theory context.
- “Card A makes Card B better” is not established by any of those statements.

---

# 3. Logical Graph Model

Relationship Intelligence is a logical graph implemented over SQLite tables. It does not require a graph database. Humanity has survived long enough without turning every adjacency list into an infrastructure religion.

## 3.1 Node types

### `CARD`

Canonical functional card identity.

Required identity:

- Oracle ID;
- canonical name;
- card-face handling where applicable;
- legality reference;
- ontology mapping version.

Oracle ID is the default relationship identity. Printing IDs do not create separate analytical nodes unless the relationship concerns a printing-specific property.

### `TAG`

Versioned functional tag.

Required identity:

- canonical tag ID;
- display name;
- source type;
- source record ID;
- ontology version;
- alias lineage;
- correction status.

### `COMBO`

Commander Spellbook-recognized combo record.

Required identity:

- Spellbook combo ID;
- combo version or retrieval snapshot;
- required cards;
- optional or variant cards;
- outcomes;
- constraints;
- source link.

Combo presence in a deck means that the declared list contains the recognized pieces. It does not prove that the deck can execute the combo under a particular game state.

### `PACKAGE`

Versioned curated package definition.

Required identity:

- package ID;
- version;
- name;
- author or curator;
- required members;
- optional members;
- enablers;
- payoffs;
- substitutes;
- outputs;
- constraints;
- source provenance.

A package definition is not generated merely because several cards co-occur. Measured co-occurrence may create a package candidate for review, but may not create an approved package.

### `COMMANDER_SIGNATURE`

Canonical commander identity.

A commander signature is:

- one commander; or
- an exact unordered partner pair; or
- another explicitly legal multi-commander identity.

A partner pair is a separate node from either individual card.

Partial-partner populations require an explicit population option.

### `DECK_SNAPSHOT`

Immutable normalized deck content.

Required identity:

- snapshot ID;
- deck hash;
- commander signature;
- normalized zones;
- import source;
- import time;
- source modification time where available;
- private or public classification;
- support status;
- analysis version.

### `TOURNAMENT_DECK_INSTANCE`

One canonical deck entry in one canonical event.

Required identity:

- deck-instance ID;
- event ID;
- pilot identity where retained;
- deck snapshot or deck hash;
- commander signature;
- placement;
- record;
- region inherited from event;
- provider lineage.

The same deck hash played in two events creates two tournament deck instances. Duplicate provider records for the same event entry create one canonical instance.

### `EVENT`

Canonical tournament event.

Required identity:

- event ID;
- name;
- date;
- organizer;
- store;
- attendance;
- event-size class;
- format;
- location;
- source lineage;
- deduplication rationale.

### `REGION`

Hierarchical geographic or organizational scope.

Permitted levels:

- global;
- continent;
- country;
- state or province;
- city;
- store;
- organizer;
- tournament series.

A store and organizer are region-like analytical scopes even where they are not geographic regions.

### `THEORY_CLAIM`

One attributed claim extracted from a theory source.

Required identity:

- claim ID;
- source ID;
- author;
- exact or summarized claim text;
- publication date;
- applicable format;
- stated scope;
- limitations;
- extraction provenance;
- confidence that the extraction represents the source;
- user annotations.

Theory claims remain context. The number of authors repeating a claim does not turn the claim into measured tournament evidence.

---

# 4. Relationship Type Registry

## 4.1 Card and tag relationships

| Relationship | Direction | Class | Meaning |
|---|---|---|---|
| `CARD_HAS_TAG` | Card → Tag | Authority or curated | Card is mapped to the tag |
| `CARD_TAG_CORRECTED_BY` | Card → correction | User context or governed correction | User or curator corrected a mapping |
| `CARD_ASSOCIATED_WITH_TAG` | Card → Tag | Measured | Decks containing the card also contain other cards with the tag |
| `TAG_CO_OCCURS_WITH_TAG` | Symmetric | Measured | Both tags appear in the same eligible decks |
| `TAG_CROSS_CARD_CO_OCCURS_WITH_TAG` | Symmetric | Measured | Tags appear on separate card identities in the same deck |

`CARD_HAS_TAG` and `CARD_ASSOCIATED_WITH_TAG` are different relationships. The first is ontology. The second is population evidence.

## 4.2 Combo relationships

| Relationship | Direction | Class |
|---|---|---|
| `COMBO_REQUIRES_CARD` | Combo → Card | Class 0B |
| `COMBO_OPTIONALLY_USES_CARD` | Combo → Card | Class 0B |
| `COMBO_HAS_OUTCOME` | Combo → outcome | Class 0B |
| `DECK_LIST_CONTAINS_COMBO` | Deck → Combo | Derived structural |
| `COMBO_CO_OCCURS_WITH_CARD` | Combo ↔ Card | Measured |
| `COMBO_CO_OCCURS_WITH_COMBO` | Symmetric | Measured |

Relationship metrics between a combo and one of its required cards are structural tautologies and must be suppressed or explicitly labeled as such.

## 4.3 Package relationships

| Relationship | Direction | Class |
|---|---|---|
| `PACKAGE_REQUIRES_CARD` | Package → Card | Curated declared |
| `PACKAGE_OPTIONALLY_USES_CARD` | Package → Card | Curated declared |
| `PACKAGE_ENABLED_BY_CARD` | Package → Card | Curated declared |
| `PACKAGE_HAS_PAYOFF_CARD` | Package → Card | Curated declared |
| `PACKAGE_ACCEPTS_SUBSTITUTE` | Package → Card | Curated declared |
| `PACKAGE_PRODUCES_OUTPUT` | Package → output | Curated declared |
| `DECK_SATISFIES_PACKAGE` | Deck → Package | Derived structural |
| `PACKAGE_CO_OCCURS_WITH_ELEMENT` | Package ↔ element | Measured |

Package presence must be calculated from the package definition version that was active for the analysis. Definitions may not mutate historical measurements.

## 4.4 Commander relationships

| Relationship | Direction | Class |
|---|---|---|
| `COMMANDER_SIGNATURE_CONTAINS_CARD` | Signature → Card | Authority-derived |
| `DECK_HAS_COMMANDER_SIGNATURE` | Deck → Signature | Observed structural |
| `ELEMENT_PREVALENT_WITH_COMMANDER` | Signature → element | Measured |
| `COMMANDER_SIGNATURE_SIMILAR_TO` | Symmetric | Measured |

Commander similarity is not part of the first implementation unless its comparison basis is explicitly contracted. Card-frequency-vector similarity must not be silently substituted for strategic similarity.

## 4.5 Deck relationships

| Relationship | Direction | Class |
|---|---|---|
| `DECK_CONTAINS_CARD` | Deck → Card | Observed structural |
| `DECK_CONTAINS_TAG` | Deck → Tag | Derived structural |
| `DECK_LIST_CONTAINS_COMBO` | Deck → Combo | Derived structural |
| `DECK_SATISFIES_PACKAGE` | Deck → Package | Derived structural |
| `DECK_HAS_COMMANDER_SIGNATURE` | Deck → Commander | Observed structural |
| `DECK_ENTERED_EVENT` | Tournament deck → Event | Observed structural |
| `DECK_DERIVED_FROM_SNAPSHOT` | Tournament deck → snapshot | Observed structural |
| `DECK_CARD_JACCARD_SIMILAR_TO` | Deck ↔ Deck | Measured |
| `DECK_TAG_JACCARD_SIMILAR_TO` | Deck ↔ Deck | Measured |

A private deck may be compared to a population without becoming a population member.

## 4.6 Event and region relationships

| Relationship | Direction | Class |
|---|---|---|
| `EVENT_LOCATED_IN_REGION` | Event → Region | Observed structural |
| `EVENT_ORGANIZED_BY_SCOPE` | Event → Organizer | Observed structural |
| `REGION_CHILD_OF_REGION` | Region → Region | Curated structural |
| `EVENT_CONTAINS_DECK_INSTANCE` | Event → deck instance | Observed structural |
| `ELEMENT_PREVALENT_IN_EVENT` | Event → element | Measured |
| `ELEMENT_PREVALENT_IN_REGION` | Region → element | Measured |
| `REGION_DIFFERS_FROM_PARENT_FOR_ELEMENT` | Region → element | Measured |

Region and event nodes normally define populations or prevalence contexts. Generic pair metrics must not be calculated between an event and a card unless both have been explicitly projected onto the same observational unit.

## 4.7 Theory relationships

| Relationship | Direction | Class |
|---|---|---|
| `THEORY_CLAIM_ABOUT_ENTITY` | Claim → entity | Context |
| `THEORY_CLAIM_ASSERTS_RELATIONSHIP` | Claim → relationship assertion | Context |
| `THEORY_CLAIM_SUPPORTS_CLAIM` | Claim → Claim | Context |
| `THEORY_CLAIM_CONTRADICTS_CLAIM` | Claim → Claim | Context |
| `THEORY_CLAIM_QUALIFIES_CLAIM` | Claim → Claim | Context |
| `THEORY_CLAIM_PROVIDES_EXAMPLE` | Claim → entity | Context |
| `THEORY_CLAIM_PROVIDES_COUNTEREXAMPLE` | Claim → entity | Context |

Theory relationships must never alter tournament counts, measured relationship metrics, or metric confidence.

---

# 5. Observation Units and Predicate Projection

## 5.1 Default observational unit

The default unit is one canonical `TOURNAMENT_DECK_INSTANCE`.

Every eligible deck instance contributes at most one observation to a deck-presence relationship, regardless of card quantity.

The population definition must declare its unit:

- tournament deck instance;
- approved deck snapshot;
- event;
- user-selected manual deck;
- another separately approved unit.

Metrics from different units may not be combined.

## 5.2 Three-state predicates

Each endpoint is projected onto every population unit as:

- `TRUE`;
- `FALSE`;
- `UNKNOWN`.

Unknown must not be treated as false.

Examples of `UNKNOWN`:

- incomplete decklist;
- unresolved card identity;
- missing tag mapping version;
- package definition unavailable;
- combo record unavailable;
- zone information missing;
- deck content blocked by privacy boundaries.

Only units where both endpoint predicates are known enter the pair contingency table.

## 5.3 Endpoint projection rules

### Card predicate

For card \(c\) and deck \(d\):

\[
I_c(d)=
\begin{cases}
1 & \text{if eligible zone contains Oracle ID } c \\
0 & \text{if the complete eligible zone does not contain } c \\
\text{unknown} & \text{if content is incomplete or unresolved}
\end{cases}
\]

Default eligible zone: mainboard only.

Commander-zone inclusion requires an explicit relationship mode.

### Tag predicate

For tag \(t\):

\[
I_t(d)=1
\]

when at least one eligible card in the deck carries tag \(t\) under the selected ontology version.

### Combo predicate

For combo \(k\):

\[
I_k(d)=1
\]

when all required card identities are represented in the zones permitted by the combo projection policy.

This means “list contains recognized pieces.” It does not mean:

- the line is legal from every game state;
- the pieces are simultaneously accessible;
- the deck can pay the costs;
- the combo is strategically appropriate.

### Package predicate

Package presence is calculated under one declared mode:

1. `REQUIRED_COMPLETE`: all required cards are present.
2. `THRESHOLD_COMPLETE`: all required cards plus the declared optional threshold.
3. `ROLE_COMPLETE`: all required package roles have at least one accepted member.

The package definition must declare which mode applies.

### Commander predicate

Default:

\[
I_K(d)=1
\]

only when the deck’s exact commander signature equals \(K\).

Partial partner matching is a separate population option.

### Region predicate

A deck belongs to region \(R\) through its canonical event lineage.

A deck may satisfy several hierarchical region predicates, such as store, city, state, country, and global.

### Theory claim predicate

Theory claims are not projected onto tournament deck populations. Claim counts may be analyzed in a separate theory-corpus population, but those results must be labeled bibliographic or contextual rather than tournament evidence.

---

# 6. Population Specification

Every relationship measurement must consume an immutable `PopulationSpec`.

## 6.1 Required fields

- population ID;
- observational unit;
- approved source pool;
- canonical-data snapshot;
- date start;
- date end;
- region scope;
- store or organizer scope;
- event-size classes;
- attendance bounds;
- placement scope;
- commander scope;
- partner matching mode;
- zones;
- legality date policy;
- release-date policy;
- source-completeness requirements;
- duplicate handling;
- pilot-repeat handling;
- deck-hash-repeat handling;
- weighting profile;
- private-data inclusion status;
- ontology version;
- combo snapshot version;
- package-definition version;
- population-spec version.

## 6.2 Default relationship population

Proposed default:

- canonical tournament deck instances;
- exact commander or exact partner pair when a commander scope is selected;
- last six months;
- all placements unless explicitly changed;
- mainboard presence;
- deduplicated canonical event entries;
- legal and released cards as of each event date;
- private user decks excluded;
- unweighted;
- global region unless selected otherwise.

This default differs from the commander-staples default, which uses Top 16 decks. The UI must not silently reuse one population for the other.

## 6.3 Candidate, usable, and unknown counts

For a pair \(A,B\):

- \(N_{candidate}\): units matching the population filters before endpoint evaluation.
- \(N_{usable}\): units where both predicates are known.
- \(N_{unknown}\): candidate units excluded because either predicate is unknown.

\[
N_{candidate}=N_{usable}+N_{unknown}
\]

Coverage:

\[
coverage=\frac{N_{usable}}{N_{candidate}}
\]

when \(N_{candidate}>0\).

A relationship with 20 matches among 20 usable decks is not equivalent to 20 matches among 2,000 candidate decks with 1,980 unresolved records.

## 6.4 Deduplication requirements

The population resolver must:

- count one canonical tournament entry once;
- collapse mirrored provider records;
- preserve all provider lineage;
- reject source records not linked to a canonical deck instance;
- exclude private decks unless explicitly authorized;
- preserve repeated legitimate event appearances;
- identify repeated deck hashes and pilots as dependence warnings.

---

# 7. Contingency Table

For two projected predicates \(A\) and \(B\), define:

| | \(B=1\) | \(B=0\) | Total |
|---|---:|---:|---:|
| \(A=1\) | \(a\) | \(b\) | \(n_A=a+b\) |
| \(A=0\) | \(c\) | \(d\) | \(N-n_A=c+d\) |
| Total | \(n_B=a+c\) | \(N-n_B=b+d\) | \(N\) |

Where:

- \(a\): both A and B present;
- \(b\): A present, B absent;
- \(c\): A absent, B present;
- \(d\): neither present;
- \(N=N_{usable}=a+b+c+d\).

All primary relationship metrics are derived from these stored integer counts.

Counts are canonical. Displayed floating-point values are reproducible derivatives.

---

# 8. Exact Metric Formulas

Metric versions must be persisted. Proposed initial versions use the suffix `.v1`.

## 8.1 Marginal prevalence

\[
P(A)=\frac{n_A}{N}
\]

\[
P(B)=\frac{n_B}{N}
\]

Metric IDs:

- `prevalence.a.v1`
- `prevalence.b.v1`

## 8.2 Support

Support measures the proportion of eligible units containing both endpoints.

\[
support(A,B)=P(A\cap B)=\frac{a}{N}
\]

Metric ID:

`support.v1`

Properties:

- symmetric;
- range \([0,1]\);
- strongly affected by endpoint prevalence;
- not evidence of dependence by itself.

## 8.3 Directional confidence

Directional confidence is association-rule confidence, not confidence that a claim is true.

\[
confidence(A\rightarrow B)=P(B\mid A)=\frac{a}{a+b}
\]

Defined only when \(a+b>0\).

Reverse direction:

\[
confidence(B\rightarrow A)=P(A\mid B)=\frac{a}{a+c}
\]

Metric ID:

`directional_confidence.v1`

UI label:

**Conditional rate**

Tooltip:

“Traditionally called association-rule confidence. This is the observed rate of B among units containing A, not epistemic confidence and not causal confidence.”

## 8.4 Dependence delta

Codie shall reserve `dependence_delta` for the directional observed prevalence contrast between units where A is present and units where A is absent.

\[
dependence\_delta(A\rightarrow B)
=
P(B\mid A)-P(B\mid \neg A)
\]

\[
=
\frac{a}{a+b}-\frac{c}{c+d}
\]

Defined only when:

\[
a+b>0
\]

and:

\[
c+d>0
\]

Metric ID:

`dependence_delta.v1`

Properties:

- directional;
- range \([-1,1]\);
- displayed in percentage points;
- positive means B is more prevalent among A-present units;
- negative means B is less prevalent among A-present units;
- zero means equal observed prevalence in the two groups;
- remains observational and noncausal.

Codie must not alias this to:

\[
P(B\mid A)-P(B)
\]

That separate quantity may later be implemented as `baseline_delta`, but it is not the V1 dependence-delta definition.

## 8.5 Lift

\[
lift(A,B)
=
\frac{P(A\cap B)}{P(A)P(B)}
\]

Equivalent form:

\[
lift(A,B)
=
\frac{P(B\mid A)}{P(B)}
\]

Expanded:

\[
lift(A,B)
=
\frac{aN}{(a+b)(a+c)}
\]

Defined only when \(n_A>0\) and \(n_B>0\).

Metric ID:

`lift.v1`

Interpretation:

- \(lift=1\): observed joint rate equals the independence expectation;
- \(lift>1\): positive association;
- \(lift<1\): negative association;
- \(lift=0\): both marginals are positive but no joint observations exist.

Lift is symmetric even though one equivalent formula is directional.

Rare endpoints can produce extreme lift from trivial counts. Lift may not be ranked without passing low-sample gates.

## 8.6 Leverage

\[
leverage(A,B)
=
P(A\cap B)-P(A)P(B)
\]

Expanded:

\[
leverage(A,B)
=
\frac{a}{N}
-
\frac{(a+b)(a+c)}{N^2}
\]

Metric ID:

`leverage.v1`

Interpretation:

- positive: joint presence exceeds independence expectation;
- negative: joint presence falls below independence expectation;
- zero: observed joint support equals independence expectation.

Leverage expresses absolute population difference rather than a ratio. It is less explosive than lift for rare elements but remains population-dependent.

## 8.7 Population Jaccard similarity

For two endpoint membership sets:

\[
Jaccard(A,B)
=
\frac{|A\cap B|}{|A\cup B|}
\]

Expanded:

\[
Jaccard(A,B)
=
\frac{a}{a+b+c}
\]

Defined when \(a+b+c>0\).

Metric ID:

`jaccard.population.v1`

Jaccard ignores units containing neither endpoint. It measures overlap, not expected overlap and not dependence.

## 8.8 Deck-list Jaccard similarity

For two deck snapshots with eligible Oracle-ID sets \(C_1\) and \(C_2\):

\[
Jaccard_{cards}(D_1,D_2)
=
\frac{|C_1\cap C_2|}{|C_1\cup C_2|}
\]

Metric ID:

`jaccard.deck_cards.v1`

Commander cards are excluded from the mainboard comparison unless the selected mode includes commanders.

A tag-set variant may be implemented as:

`jaccard.deck_tags.v1`

The two Jaccard variants must never share an unlabeled result field.

## 8.9 Pointwise mutual information

Natural-log PMI:

\[
PMI(A,B)
=
\ln\left(
\frac{P(A\cap B)}{P(A)P(B)}
\right)
\]

Therefore:

\[
PMI(A,B)=\ln(lift(A,B))
\]

Expanded:

\[
PMI(A,B)
=
\ln\left(
\frac{aN}{(a+b)(a+c)}
\right)
\]

Defined only when:

- \(a>0\);
- \(n_A>0\);
- \(n_B>0\).

Metric ID:

`pmi_ln.v1`

Interpretation:

- positive: positive association;
- zero: independence expectation;
- negative: negative association;
- undefined when joint support is zero.

Codie must store `null` with reason `ZERO_JOINT_PMI_UNDEFINED` rather than storing negative infinity.

No additive smoothing is permitted in the measured V1 metric. A future exploratory smoothed PMI must use a different metric name and must not replace raw PMI.

## 8.10 Weighted variants

Weighted metrics are optional and must remain separate from raw metrics.

For nonnegative fixed unit weights \(w_i\):

\[
W=\sum_i w_i
\]

\[
W_A=\sum_i w_i I_A(i)
\]

\[
W_B=\sum_i w_i I_B(i)
\]

\[
W_{AB}=\sum_i w_i I_A(i)I_B(i)
\]

Weighted formulas substitute:

- \(W\) for \(N\);
- \(W_A\) for \(n_A\);
- \(W_B\) for \(n_B\);
- \(W_{AB}\) for \(a\).

Weighted outputs must use metric IDs such as:

- `support.weighted.v1`;
- `lift.weighted.v1`;
- `leverage.weighted.v1`.

Unweighted counts must always remain visible beside weighted results.

Effective sample size for weighting gates:

\[
N_{eff}
=
\frac{\left(\sum_i w_i\right)^2}
{\sum_i w_i^2}
\]

Placement weighting may introduce selection bias and must trigger a confounder notice.

---

# 9. Confidence Handling

## 9.1 Distinguish three meanings of confidence

Codie must display three different concepts separately:

1. **Directional confidence:** \(P(B\mid A)\), a relationship metric.
2. **Sampling interval:** uncertainty around an observed proportion.
3. **Evidence stability:** a gate based on sample size, coverage, conflicts, and confounders.

No field named only `confidence` is permitted in pair-detail serialization.

## 9.2 Wilson interval for proportions

Support and directional conditional rates use a two-sided 95% Wilson interval.

For \(k\) successes in \(n\) observations:

\[
\hat p=\frac{k}{n}
\]

\[
denominator=1+\frac{z^2}{n}
\]

\[
center=
\frac{
\hat p+\frac{z^2}{2n}
}{
1+\frac{z^2}{n}
}
\]

\[
halfwidth=
\frac{
z
\sqrt{
\frac{\hat p(1-\hat p)}{n}
+
\frac{z^2}{4n^2}
}
}{
1+\frac{z^2}{n}
}
\]

Where:

\[
z=1.96
\]

The interval is:

\[
[center-halfwidth,\ center+halfwidth]
\]

Metric version:

`wilson_95.v1`

Wilson intervals apply only to unweighted integer observations.

## 9.3 Dependence-delta interval

V1 may expose a conservative component interval:

- Wilson interval for \(P(B\mid A)\): \([L_1,U_1]\);
- Wilson interval for \(P(B\mid\neg A)\): \([L_0,U_0]\).

Conservative delta envelope:

\[
[L_1-U_0,\ U_1-L_0]
\]

This must be labeled:

`conservative_component_envelope`

It is not a causal interval and not a formal significance test.

## 9.4 Proposed low-sample gates

These thresholds are proposed defaults and require approval before implementation.

### `UNAVAILABLE`

Any of:

- \(N_{usable}=0\);
- endpoint unit mismatch;
- structural tautology;
- \(n_A=0\) for an A→B directional metric;
- \(n_A=N\) for dependence delta;
- coverage below 0.50;
- unresolved canonical identity;
- private-data violation.

### `DESCRIPTIVE_ONLY`

Any of:

- \(N_{usable}<20\);
- \(a<3\);
- either marginal count below 5;
- material source conflict unresolved.

Display counts and formulas. Do not rank.

### `LOW_STABILITY`

All metrics are calculable, but any of:

- \(N_{usable}<50\);
- \(n_A<10\);
- \(n_B<10\);
- \(a<5\);
- coverage below 0.70;
- high-risk confounder unresolved.

May be displayed with a warning. Do not place in default top-relationship rankings.

### `MODERATE_STABILITY`

Minimum:

- \(N_{usable}\ge100\);
- \(n_A\ge25\);
- \(n_B\ge25\);
- \(a\ge10\);
- coverage at least 0.85;
- no blocking confounder.

Eligible for ranking.

### `HIGH_STABILITY`

Minimum:

- \(N_{usable}\ge250\);
- \(n_A\ge50\);
- \(n_B\ge50\);
- \(a\ge20\);
- coverage at least 0.90;
- at least two independent provider lineages where applicable;
- no blocking confounder;
- no material unresolved conflict.

“High stability” means that the measured association is comparatively stable under the selected population. It does not mean that the relationship is causal, strategically correct, or universally transferable.

## 9.5 Confidence ceiling downstream

When Relationship Intelligence is included in Unified Evidence:

- `DESCRIPTIVE_ONLY` evidence cannot support a high-confidence recommendation.
- `LOW_STABILITY` evidence cannot independently support more than low recommendation confidence.
- `MODERATE_STABILITY` or `HIGH_STABILITY` still cannot independently authorize a recommendation.
- Theory agreement cannot raise measured stability.
- Class 0 structural authority may establish requirements, but does not establish strategic desirability.

---

# 10. Population Controls

## 10.1 Mandatory controls

Every measurement must show:

- observational unit;
- source pool;
- date range;
- region;
- event-size scope;
- placement scope;
- commander scope;
- zones;
- candidate count;
- usable count;
- unknown count;
- coverage;
- legality policy;
- weighting status;
- duplicate policy.

## 10.2 Exact commander control

Card relationships are heavily determined by commander identity and color identity.

Default card-pair analysis should support:

- global;
- exact commander signature;
- exact partner pair;
- explicitly selected partial-partner population;
- user-selected commander group.

A global relationship must not be presented as though it necessarily applies within a selected commander.

## 10.3 Color-eligibility control

For card-to-card relationships, an optional color-eligible population may restrict the denominator to decks legally capable of playing both cards as of the event date.

This population must be labeled:

`COLOR_ELIGIBLE`

It must not replace the unfiltered population silently.

Color eligibility reduces one structural confounder but does not control for commander strategy.

## 10.4 Time and legality control

Each deck instance must evaluate cards against:

- release date;
- format legality;
- ban status;
- event date.

Decks from before an endpoint was released or legal are excluded from that endpoint’s time-valid population rather than counted as endpoint absence.

## 10.5 Region control

Relationship metrics must be recomputable for:

- global;
- continent;
- country;
- state or province;
- city;
- store;
- organizer;
- tournament series.

Regional comparison must use identical nonregional filters.

For relationship metric \(M\):

\[
regional\_delta_M=M_R-M_{parent}
\]

This is a difference between observed populations, not a claim that region caused the relationship.

## 10.6 Placement control

Supported placement scopes:

- all submitted canonical deck instances;
- winner;
- Top 4;
- Top 16;
- made cut;
- custom placement band.

Placement filtering can create selection bias. Any non-all-placement population must display:

`PLACEMENT_SELECTION_CONFOUNDER`

## 10.7 Event-size control

Event-size thresholds must be versioned. A relationship result must store the actual attendance bounds, not merely a label such as “major.”

## 10.8 Repeated pilot and deck control

Repeated observations may not be independent.

Required disclosures:

- unique pilots where available;
- unique deck hashes;
- maximum appearances by one pilot;
- maximum appearances by one deck hash;
- percentage of units represented by the five most repeated pilots;
- percentage represented by the five most repeated deck hashes.

V1 does not remove legitimate repeat appearances by default. It flags concentration and supports a sensitivity view using one observation per pilot or deck hash.

---

# 11. Confounders and Required Handling

| Confounder | Detection | Required handling |
|---|---|---|
| Color identity | One or both cards illegal in many population decks | Offer color-eligible comparison |
| Exact commander | Relationship concentrated in one commander signature | Show commander distribution and exact-commander strata |
| Partner identity | Partial-partner population mixes distinct shells | Require explicit partial matching |
| Archetype | Pair concentrated in one known archetype | Show archetype or package concentration where available |
| Package definition | One endpoint structurally contains the other | Mark tautology; suppress association interpretation |
| Combo definition | Card is required by combo endpoint | Mark tautology |
| Tag self-membership | Card itself creates tag presence | Use leave-one-out tag aggregation |
| Multi-tag card | One card creates both tag predicates | Show same-card bridge and cross-card result |
| Generic staple | High marginal prevalence creates high raw support | Display lift, leverage, and marginal prevalence |
| Rare endpoints | Tiny joint count creates extreme lift or PMI | Apply low-sample gate |
| Release date | Older decks could not contain a card | Restrict to time-valid population |
| Ban status | Card unavailable during some events | Apply date-aware legality |
| Region | Pair concentrated in one region or store | Show regional strata |
| Event size | Local and major-event populations differ | Display event-size comparison |
| Placement selection | Top-cut filter conditions on performance | Label selection bias |
| Provider duplication | Same event entry appears from multiple sources | Canonical deduplication required |
| Source incompleteness | Decklists or mappings missing | Use unknown state and coverage |
| Repeated pilot | One pilot contributes many observations | Show concentration and sensitivity |
| Repeated deck hash | Same list repeated across events | Show concentration and sensitivity |
| Deck-size constraint | Including one card necessarily displaces another | Explain that negative association may reflect finite slots |
| Private data | User deck included unintentionally | Block measurement |
| Theory contamination | Human claims used as metric inputs | Block calculation |
| Circular package discovery | Package defined from the same measurement being used to validate it | Mark circularity and reject validation claim |

## 11.1 Stratified dependence delta

For an approved confounder divided into strata \(s\), calculate within each estimable stratum:

\[
\Delta_s
=
P_s(B\mid A)-P_s(B\mid\neg A)
\]

A stratum is estimable only when both A-present and A-absent units exist.

Reference weight:

\[
q_s=
\frac{N_s}{\sum_{j\in S^*}N_j}
\]

where \(S^*\) contains estimable strata.

Standardized delta:

\[
\Delta_{standardized}
=
\sum_{s\in S^*}q_s\Delta_s
\]

Metric ID:

`dependence_delta.stratified_standardized.v1`

Required disclosures:

- stratification variable;
- number of total strata;
- number of estimable strata;
- excluded strata;
- retained population share;
- each stratum’s counts and delta.

If less than 70% of the usable population remains in estimable strata, the standardized result is `DESCRIPTIVE_ONLY`.

The result remains observational. Stratification reduces measured imbalance; it does not create a causal design.

---

# 12. Card-to-Tag Aggregation

## 12.1 Direct ontology mapping

`CARD_HAS_TAG` is a declared ontology edge.

It carries:

- card Oracle ID;
- tag ID;
- source;
- source record;
- ontology version;
- correction lineage;
- import time.

It carries no support, lift, PMI, or dependence delta.

## 12.2 Deck-level tag presence

For deck \(d\) and tag \(t\):

\[
TagPresent(d,t)=
\mathbb{1}
\left[
\sum_c I_c(d)I_{c,t}>0
\right]
\]

where \(I_{c,t}=1\) when card \(c\) has tag \(t\).

## 12.3 Tag slot count

\[
TagSlotCount(d,t)
=
\sum_c quantity(d,c)I_{c,t}
\]

## 12.4 Distinct tagged-card count

\[
TagDistinctCount(d,t)
=
\sum_c \mathbb{1}[quantity(d,c)>0]I_{c,t}
\]

## 12.5 Tag density

\[
TagDensity(d,t)
=
\frac{TagSlotCount(d,t)}
{EligibleMainboardSlots(d)}
\]

Tags may overlap. A card with three tags contributes to all three tag counts. Tag densities are not compositional percentages and need not sum to 100%.

## 12.6 Leave-one-out card-to-tag association

A direct card-to-tag association would otherwise be tautological when the card itself owns the tag.

For source card \(x\):

\[
TagPresent^{-x}(d,t)
=
\mathbb{1}
\left[
\sum_{c\ne x}I_c(d)I_{c,t}>0
\right]
\]

Measured card-to-tag affinity uses:

- \(A=I_x(d)\);
- \(B=TagPresent^{-x}(d,t)\).

This answers:

> When decks contain card X, how often do they also contain another card serving tag T?

The UI must show both:

- direct ontology tags on X;
- leave-one-out measured tag associations.

## 12.7 Tag-to-tag same-card bridge

Inclusive tag co-occurrence can be produced by one multifunction card.

For tags \(t_1,t_2\), store:

- inclusive deck co-occurrence;
- cross-card deck co-occurrence;
- same-card bridge count.

Cross-card presence requires distinct card identities:

\[
CrossCardTags(d,t_1,t_2)=1
\]

only if there exist \(c_1\ne c_2\) such that:

\[
I_{c_1,t_1}=1
\]

and:

\[
I_{c_2,t_2}=1
\]

This prevents one card tagged both “draw” and “discard outlet” from being mistaken for evidence that the deck supports a multi-card package.

## 12.8 Package-to-tag aggregation

Two modes must be exposed:

1. `INCLUSIVE`: package members contribute to tag presence.
2. `EXTERNAL_SUPPORT`: package members are excluded before tag presence is measured.

`EXTERNAL_SUPPORT` answers whether decks using the package tend to include additional support outside the package itself.

---

# 13. Combo and Package Tautology Rules

Metrics must be suppressed when endpoint definitions mechanically entail joint presence.

Examples:

- package P requires card A;
- combo C requires card B;
- commander signature K contains commander card C;
- tag presence is calculated from the source card itself;
- deck snapshot is compared to a card known to be in that same immutable snapshot.

Required output:

- relationship status: `STRUCTURAL_TAUTOLOGY`;
- declared relationship;
- source and version;
- no lift ranking;
- no PMI ranking;
- explanation of why statistical association would be meaningless.

A user may inspect the raw contingency counts, but the UI must not interpret them as discovered affinity.

---

# 14. Pair-Detail Output

Every pair-detail record must contain the following sections.

## 14.1 Identity

- endpoint A type and canonical ID;
- endpoint A display label;
- endpoint B type and canonical ID;
- endpoint B display label;
- relationship direction;
- relationship assertion classes;
- structural relationships already known;
- metric bundle version.

## 14.2 Population

- population ID;
- human-readable population summary;
- observational unit;
- source pool;
- date range;
- region;
- commander scope;
- event-size scope;
- placement scope;
- zones;
- legality policy;
- weighting profile;
- candidate count;
- usable count;
- unknown count;
- coverage.

## 14.3 Contingency counts

- \(a\): both;
- \(b\): A only;
- \(c\): B only;
- \(d\): neither;
- \(n_A\);
- \(n_B\);
- \(N\).

The UI must display the full 2×2 table.

## 14.4 Metrics

- support;
- support Wilson interval;
- confidence A→B;
- confidence A→B Wilson interval;
- confidence B→A;
- confidence B→A Wilson interval;
- dependence delta A→B;
- dependence delta B→A;
- lift;
- leverage;
- population Jaccard;
- PMI;
- metric undefined reasons;
- weighted variants where selected.

## 14.5 Stability

- stability band;
- gate failures;
- coverage status;
- provider diversity;
- source agreement where applicable;
- unresolved conflicts;
- concentration warnings;
- low-sample warning;
- ranking eligibility.

## 14.6 Confounders

- detected confounders;
- severity;
- detection evidence;
- available controlled comparisons;
- strata summary;
- standardized dependence delta where requested;
- interpretation limits.

## 14.7 Provenance

- canonical dataset snapshot;
- canonical deck-instance IDs or reproducible population manifest;
- source provider records;
- population-spec hash;
- formula IDs;
- metric version;
- ontology version;
- package version;
- combo snapshot;
- generated timestamp;
- software commit;
- exclusions;
- unknown-resolution reasons.

## 14.8 Contributing evidence

Expandable lists:

- decks containing both;
- decks containing A only;
- decks containing B only;
- events contributing most observations;
- commander signatures contributing most observations;
- regions contributing most observations;
- repeated pilots or deck hashes;
- direct structural relationships;
- relevant theory claims.

Private content remains hidden unless explicitly authorized.

## 14.9 Interpretation

The measured interpretation may state:

- whether association is positive, neutral, or negative;
- whether the direction differs;
- whether the result survives a selected stratification;
- whether the result is dominated by a commander, region, package, or multifunction card;
- whether sample or coverage prevents ranking.

It may not state:

- that A caused B;
- that A improves B;
- that A is strategically necessary;
- that the user should add or remove either endpoint.

---

# 15. Provenance Model

## 15.1 No metric without lineage

Every persisted measurement must expose:

- numerator and denominator;
- raw counts;
- formula identifier;
- metric version;
- population specification;
- canonical source records;
- date range;
- region;
- placement scope;
- sample size;
- coverage;
- generated time;
- exclusions;
- caveats.

## 15.2 Population manifest

Each calculation creates or references an immutable population manifest containing:

- manifest ID;
- sorted canonical unit IDs;
- population-spec hash;
- canonical-data snapshot ID;
- creation timestamp;
- privacy classification.

The same manifest and metric versions must reproduce the same integer counts.

## 15.3 Relationship measurement identity

Proposed deterministic identity:

\[
measurement\_id=
hash(
endpoint_A,
endpoint_B,
direction_mode,
population\_manifest,
metric\_bundle\_version
)
\]

Endpoint ordering must be canonicalized for symmetric metrics and preserved for directional metrics.

## 15.4 Source lineage

Measurement provenance points to canonical records. Canonical records point to provider records. Provider records point to raw payloads or preserved fixtures where allowed.

Provider records are not counted separately once canonicalized.

## 15.5 Conflict preservation

Conflicting source fields must remain attached to canonical records and surface in pair details when they could affect:

- population inclusion;
- event date;
- commander identity;
- deck content;
- placement;
- region;
- attendance;
- legality.

---

# 16. Jin Discussion Policy

## 16.1 Permitted relationship language

Jin may say:

- “In the selected 120-deck population, A and B appeared together in 18% of decks.”
- “Among decks containing A, 60% also contained B.”
- “B appeared 28.6 percentage points more often in A-present decks than in A-absent decks.”
- “The observed lift was 1.5, meaning the joint rate was 1.5 times the rate expected from the two marginal frequencies under an independence baseline.”
- “This association was concentrated in Commander K.”
- “After exact-commander stratification, the relationship weakened.”
- “This is consistent with the package claim made by Source X.”
- “That interpretation is an inference rather than measured evidence.”
- “The data does not establish that A causes better performance.”
- “The pair is too rare for reliable ranking.”

## 16.2 Restricted language

Jin may not derive the following solely from Relationship Intelligence:

- “A makes B better.”
- “B depends on A.”
- “A is required.”
- “A is the correct inclusion.”
- “You should play A.”
- “You should cut B.”
- “This package wins more because of A.”
- “This theory is proven.”
- “Players use these together because…”
- “The relationship will apply in your local metagame.”

The word “depends” may be used only in one of these forms:

- “The package definition declares B as required.”
- “The observed directional dependence delta was…”
- “The available data is consistent with dependence, but does not establish functional or causal dependence.”

## 16.3 Structural authority

Jin may state a structural requirement when supported by authority:

- a Spellbook combo requires a listed card;
- a curated package definition marks a card required;
- a commander signature contains a commander card;
- a card carries a versioned Tagger label.

Jin must name the source class.

## 16.4 Theory discussion

Jin may connect measured evidence to theory only through attributed wording:

> “Author X describes A as an enabler for B. In the selected tournament population, the pair also has positive lift. The theory claim and the measured association agree, but the tournament data does not test the claimed mechanism.”

Contradictory theory claims must remain visible.

Theory-source agreement does not change Class 2 metric values or stability bands.

## 16.5 Recommendation boundary

When asked whether to add or remove a card, Jin must:

1. retrieve Relationship Intelligence as measured evidence;
2. retrieve other approved evidence;
3. build or retrieve Unified Evidence;
4. use an approved Decision Intelligence result for a persisted recommendation;
5. label any nonpersisted strategic discussion as inference or experiment design.

Relationship Intelligence may support a recommendation. It may never generate one.

## 16.6 Required Jin answer metadata

A substantive relationship answer must be able to expose:

- direct answer;
- population;
- metric values;
- evidence level;
- stability band;
- source coverage;
- structural authority;
- theory context;
- confounders;
- contradictory evidence;
- explicit inference;
- causation warning;
- recommendation boundary;
- deck snapshot used;
- analysis date.

## 16.7 Language guard tests

The Jin relationship-language guard must reject or rewrite unsupported causal verbs, including:

- caused;
- improved;
- enabled, unless structurally declared;
- required, unless structurally declared;
- led to;
- produced better results;
- proves;
- demonstrates that players chose;
- should include;
- should cut.

The guard must not ban those words when they are used in quotations, source attribution, rules descriptions, or Decision Intelligence output with proper classification.

---

# 17. Regional and Local Comparisons

For endpoint pair \(A,B\), the pair-detail surface should compare:

- selected region;
- parent region;
- global population;
- selected store or organizer where available.

Required comparison fields:

- identical nonregional filters;
- \(N\), \(n_A\), \(n_B\), and \(a\);
- support;
- directional confidence;
- dependence delta;
- lift;
- coverage;
- stability;
- date range;
- event-size distribution.

No regional comparison may compare different date windows without a visible warning.

A store-level relationship based on five decks remains five decks, even if the user finds it personally compelling. Software does not turn anecdotes into census data merely because the chart is attractive.

---

# 18. UI Requirements

## 18.1 Relationship Explorer

Required controls:

- endpoint A selector;
- endpoint B selector;
- entity-type filter;
- direction toggle;
- population selector;
- date window;
- region;
- store or organizer;
- commander signature;
- exact or partial partner mode;
- event-size class;
- placement scope;
- zone scope;
- weighting toggle;
- confounder stratification;
- inclusive or leave-one-out tag mode.

## 18.2 Graph view

The graph may display typed nodes and edges, but every edge must show:

- relationship type;
- assertion class;
- direction;
- stability;
- population scope where measured.

Structural, measured, and theory edges require:

- distinct line patterns;
- text labels;
- accessible icons or prefixes;
- non-color-only differentiation.

Measured edges may not be reduced to one opaque “relationship score.”

## 18.3 Pair-detail drawer

Required default summary:

1. direct relationship statement;
2. population;
3. joint count;
4. support;
5. conditional rates;
6. dependence deltas;
7. lift;
8. stability;
9. strongest confounder;
10. structural or theory relationships.

Expandable sections expose the complete pair-detail output.

## 18.4 Contingency table

The 2×2 table is mandatory.

Users must be able to verify every metric with the displayed counts.

## 18.5 Metric explanations

Each metric requires a tooltip with:

- formula;
- plain-language interpretation;
- major failure mode.

Examples:

- Lift: unstable for rare endpoints.
- PMI: strongly favors rare pairings.
- Support: rewards common cards.
- Jaccard: ignores decks containing neither element.
- Directional confidence: not epistemic confidence.
- Dependence delta: observational contrast, not causal effect.

## 18.6 Population visibility

A persistent population bar must show:

- source pool;
- date range;
- region;
- commander;
- placement;
- event size;
- candidate count;
- usable count;
- coverage.

The population cannot be hidden inside an information icon.

## 18.7 Provenance panel

The user must be able to inspect:

- formula IDs;
- metric versions;
- source manifests;
- canonical record IDs;
- provider lineage;
- ontology versions;
- package versions;
- exclusions;
- conflicts.

## 18.8 Ranking views

Default ranking requires at least `MODERATE_STABILITY`.

Users may reveal low-stability results through an explicit control.

Rankings must support separate sort keys:

- support;
- directional confidence;
- dependence delta;
- lift;
- leverage;
- Jaccard;
- PMI.

A blended relationship score is excluded from core V2.

## 18.9 Jin integration

The pair-detail surface must support opening Jin with:

- endpoint identities;
- population ID;
- relationship measurement ID;
- selected deck snapshot;
- visible confounders;
- structural relationships;
- relevant theory claims.

Jin must link back to the exact pair-detail measurement.

## 18.10 Export

Supported exports:

- Markdown;
- CSV;
- JSON;
- Obsidian Markdown;
- static HTML where approved.

Exports must preserve filters, counts, formulas, versions, stability, caveats, and provenance.

---

# 19. Failure States

| Code | Condition | Required behavior |
|---|---|---|
| `REL_ENTITY_UNRESOLVED` | Endpoint identity cannot be canonicalized | Stop calculation |
| `REL_UNIT_MISMATCH` | Endpoints cannot be projected onto the same unit | Stop calculation |
| `REL_POPULATION_EMPTY` | No candidate units | Return empty result |
| `REL_NO_USABLE_RECORDS` | All endpoint evaluations unknown | Return unavailable |
| `REL_COVERAGE_CRITICAL` | Coverage below 0.50 | Descriptive counts only or unavailable |
| `REL_DIRECTION_ZERO_DENOMINATOR` | Directional antecedent absent | Return null directional metric |
| `REL_DELTA_NO_COMPLEMENT` | A is present in all usable units | Return null dependence delta |
| `REL_PMI_ZERO_JOINT` | No joint observations | Return null PMI |
| `REL_STRUCTURAL_TAUTOLOGY` | One endpoint definition entails the other | Suppress association interpretation |
| `REL_TAG_SELF_INCLUSION` | Direct tag mapping creates tautology | Force leave-one-out mode |
| `REL_PACKAGE_CIRCULARITY` | Package definition derived from same metric used for validation | Reject validation interpretation |
| `REL_SOURCE_CONFLICT` | Canonical conflict may change membership | Surface conflict and lower stability |
| `REL_ONTOLOGY_VERSION_MISSING` | Required tag map unavailable | Mark affected predicates unknown |
| `REL_PACKAGE_VERSION_MISSING` | Package definition unavailable | Stop package projection |
| `REL_COMBO_VERSION_MISSING` | Combo snapshot unavailable | Stop combo projection |
| `REL_PRIVATE_POPULATION_BLOCKED` | Private deck would enter global pool | Block operation |
| `REL_WEIGHT_INVALID` | Negative, missing, or nonfinite weight | Reject weighted calculation |
| `REL_TIME_ILLEGAL` | Endpoint unavailable in part of historical window | Apply time-valid exclusion |
| `REL_DUPLICATE_CANONICAL_UNIT` | Population manifest repeats canonical ID | Reject manifest |
| `REL_NONDETERMINISTIC_SERIALIZATION` | Same input serializes differently | Validation failure |

No failure may silently replace unknown with absence or silently broaden the population.

---

# 20. Example Calculation

Assume 100 eligible canonical deck instances.

- Card A appears in 30.
- Card B appears in 40.
- Both appear in 18.

Contingency table:

| | B present | B absent | Total |
|---|---:|---:|---:|
| A present | 18 | 12 | 30 |
| A absent | 22 | 48 | 70 |
| Total | 40 | 60 | 100 |

## Support

\[
support=\frac{18}{100}=0.18
\]

Result: **18%**

## Directional confidence A→B

\[
P(B\mid A)=\frac{18}{30}=0.60
\]

Result: **60%**

Approximate 95% Wilson interval:

\[
[42.32\%,75.41\%]
\]

## Directional confidence B→A

\[
P(A\mid B)=\frac{18}{40}=0.45
\]

Result: **45%**

## Dependence delta A→B

\[
P(B\mid A)=\frac{18}{30}=0.60
\]

\[
P(B\mid\neg A)=\frac{22}{70}\approx0.314286
\]

\[
dependence\_delta(A\rightarrow B)
=
0.60-0.314286
=
0.285714
\]

Result: **+28.57 percentage points**

## Dependence delta B→A

\[
P(A\mid B)=\frac{18}{40}=0.45
\]

\[
P(A\mid\neg B)=\frac{12}{60}=0.20
\]

\[
dependence\_delta(B\rightarrow A)=0.25
\]

Result: **+25 percentage points**

## Lift

\[
lift
=
\frac{0.18}{0.30\times0.40}
=
\frac{0.18}{0.12}
=
1.5
\]

Result: **1.5**

The pair occurs 1.5 times as often as the independence baseline predicts.

## Leverage

\[
leverage=0.18-(0.30\times0.40)
\]

\[
=0.18-0.12=0.06
\]

Result: **+6 percentage points of population support**

## Jaccard

\[
Jaccard
=
\frac{18}{30+40-18}
=
\frac{18}{52}
\approx0.346154
\]

Result: **34.62% overlap**

## PMI

\[
PMI=\ln(1.5)\approx0.405465
\]

Result: **0.4055 natural-log units**

## Permitted interpretation

> A and B have positive observed association in this population. B appears 28.57 percentage points more often among A-present decks than among A-absent decks. The result does not establish that A causes B to be included or that either card improves the other.

---

# 21. Edge Cases

## 21.1 No joint observations

Given:

- \(N=100\);
- \(n_A=20\);
- \(n_B=30\);
- \(a=0\).

Results:

- support = 0;
- directional confidence = 0 where antecedent exists;
- dependence delta is negative;
- lift = 0;
- leverage is negative;
- Jaccard = 0;
- PMI = null with `ZERO_JOINT_PMI_UNDEFINED`.

## 21.2 Antecedent never appears

If \(n_A=0\):

- support may be zero;
- confidence A→B is null;
- dependence delta A→B is null;
- lift is null;
- PMI is null;
- Jaccard may be zero if B appears.

The UI must not display zero for undefined directional metrics.

## 21.3 Antecedent appears everywhere

If \(n_A=N\):

- confidence A→B is defined;
- dependence delta A→B is undefined because no A-absent comparison exists;
- lift may be defined but is necessarily 1 where B has positive prevalence;
- the result should be treated as structurally uninformative.

## 21.4 Rare pair with extreme lift

If:

- \(N=1{,}000\);
- \(n_A=2\);
- \(n_B=2\);
- \(a=2\);

then:

\[
lift=500
\]

This does not justify first-place ranking. The pair is `DESCRIPTIVE_ONLY` because its counts fail minimum gates.

## 21.5 Generic staples

Two cards each appearing in 90% of decks can have enormous support and Jaccard while lift remains near 1.

The UI must show marginal prevalence so commonness is not mistaken for special affinity.

## 21.6 Card mapped to tested tag

If Card A carries Tag T:

- inclusive confidence A→T is mechanically 100%;
- this is an ontology fact, not discovered affinity;
- measured A→T uses leave-one-out tag presence.

## 21.7 Package contains endpoint

If Package P requires Card A:

- P→A association metrics are tautological;
- the pair-detail view shows `PACKAGE_REQUIRES_CARD`;
- no lift or PMI ranking is allowed.

## 21.8 Multifunction tag bridge

If one card is tagged both “draw engine” and “discard outlet,” inclusive tag co-occurrence rises.

The pair detail must show how much co-occurrence comes from:

- the same card;
- separate cards.

## 21.9 Historical release boundary

A card released halfway through the date window must not be counted absent in earlier decks.

The relationship population begins when both endpoints were legal and available, unless the user explicitly requests historical absence analysis.

## 21.10 Simpson-style confounding

Global association may appear even when no within-stratum association exists.

Fixture:

### Stratum 1

- \(N=50\);
- \(n_A=40\);
- \(n_B=30\);
- \(a=24\).

\[
P(B\mid A)=0.60
\]

\[
P(B\mid\neg A)=0.60
\]

Delta: 0.

### Stratum 2

- \(N=50\);
- \(n_A=10\);
- \(n_B=20\);
- \(a=4\).

\[
P(B\mid A)=0.40
\]

\[
P(B\mid\neg A)=0.40
\]

Delta: 0.

### Global

- \(N=100\);
- \(n_A=50\);
- \(n_B=50\);
- \(a=28\).

\[
P(B\mid A)=0.56
\]

\[
P(B\mid\neg A)=0.44
\]

Global delta: +12 percentage points.

The stratified standardized delta is zero. The global relationship is confounded by stratum composition.

---

# 22. Hand-Verifiable Integration Fixture

## 22.1 Entities

Cards:

- A;
- B;
- C.

Tags:

- A has `draw`;
- B has `tutor`;
- C has `draw`.

Commander signatures:

- K1;
- K2.

Regions:

- R1;
- R2.

Events:

- E1 and E2 in R1;
- E3 and E4 in R2.

Package:

- P1 requires A and B.

Combo:

- C1 requires A, B, and C.

Theory claim:

- T1 states that A supports B in K1.
- T1 is context only.

## 22.2 Deck instances

| Deck | Commander | Event | Region | Cards |
|---|---|---|---|---|
| D1 | K1 | E1 | R1 | A, B, C |
| D2 | K1 | E1 | R1 | A, B |
| D3 | K1 | E1 | R1 | A, B |
| D4 | K1 | E2 | R1 | A, C |
| D5 | K1 | E2 | R1 | A |
| D6 | K2 | E3 | R2 | B, C |
| D7 | K2 | E3 | R2 | B |
| D8 | K2 | E3 | R2 | C |
| D9 | K2 | E4 | R2 | A, B |
| D10 | K2 | E4 | R2 | C |

## 22.3 Expected A/B counts

- \(N=10\);
- \(n_A=6\);
- \(n_B=6\);
- \(a=4\);
- \(b=2\);
- \(c=2\);
- \(d=2\).

Expected metrics:

\[
support=0.4
\]

\[
confidence(A\rightarrow B)=\frac{4}{6}=0.666667
\]

\[
confidence(B\rightarrow A)=\frac{4}{6}=0.666667
\]

\[
dependence\_delta(A\rightarrow B)
=
\frac{4}{6}-\frac{2}{4}
=
0.166667
\]

\[
lift
=
\frac{0.4}{0.6\times0.6}
=
1.111111
\]

\[
leverage=0.4-0.36=0.04
\]

\[
Jaccard=\frac{4}{8}=0.5
\]

\[
PMI=\ln(1.111111)\approx0.105361
\]

Stability: `DESCRIPTIVE_ONLY`.

## 22.4 Expected package results

P1 is present in:

- D1;
- D2;
- D3;
- D9.

Count: 4.

P1→A and P1→B must be marked structural tautologies.

## 22.5 Expected combo results

C1 is list-complete only in D1.

Count: 1.

Any measured association involving C1 is `DESCRIPTIVE_ONLY`.

## 22.6 Expected leave-one-out card-to-tag result

A itself has the `draw` tag.

Among the six A decks, another draw-tagged card C appears in:

- D1;
- D4.

Therefore:

\[
confidence(A\rightarrow draw^{-A})
=
\frac{2}{6}
=
0.333333
\]

Inclusive A→draw would be 1.0 and must be identified as tautological ontology overlap.

## 22.7 Theory separation

T1 must appear in pair detail as:

- attributed theory context;
- applicable to K1;
- not counted in \(a,b,c,d\);
- not used to increase stability;
- not treated as proof of mechanism.

---

# 23. Proposed Data Models

## 23.1 `EntityRef`

Fields:

- entity type;
- canonical ID;
- display name;
- version reference;
- privacy classification.

## 23.2 `RelationshipAssertion`

Fields:

- assertion ID;
- subject entity;
- relationship type;
- object entity;
- directionality;
- assertion class;
- source references;
- scope;
- valid-from;
- valid-to;
- version;
- conflict status.

## 23.3 `PopulationSpec`

Fields defined in Section 6.

## 23.4 `PopulationManifest`

Fields:

- manifest ID;
- population-spec hash;
- canonical snapshot ID;
- ordered unit IDs;
- candidate count;
- privacy classification;
- generated timestamp.

## 23.5 `PredicateProjection`

Fields:

- manifest ID;
- endpoint;
- unit ID;
- result: true, false, or unknown;
- unknown reason;
- projection version.

## 23.6 `ContingencyTable`

Fields:

- \(a,b,c,d\);
- \(n_A,n_B,N\);
- candidate count;
- unknown count;
- coverage.

## 23.7 `RelationshipMetricBundle`

Fields:

- measurement ID;
- endpoints;
- population manifest;
- contingency counts;
- metric values;
- undefined reasons;
- Wilson intervals;
- weighted values;
- metric versions;
- stability band;
- ranking eligibility.

## 23.8 `ConfounderAssessment`

Fields:

- confounder type;
- severity;
- detection evidence;
- affected interpretation;
- suggested controlled view;
- blocking status.

“Suggested controlled view” is an analytical operation, not a card recommendation.

## 23.9 `RelationshipProvenance`

Fields:

- canonical snapshot;
- provider lineage;
- population-spec hash;
- formula versions;
- ontology version;
- combo version;
- package version;
- software commit;
- generation timestamp;
- exclusions;
- conflicts.

## 23.10 `PairDetail`

Fields:

- identity;
- structural assertions;
- measured metrics;
- population;
- stability;
- confounders;
- provenance;
- contributing records;
- theory context;
- interpretation limits.

---

# 24. Proposed SQLite Persistence

A governed migration would be required.

Proposed logical tables:

- `relationship_assertion`;
- `relationship_assertion_source`;
- `relationship_population_spec`;
- `relationship_population_manifest`;
- `relationship_population_member`;
- `relationship_measurement`;
- `relationship_measurement_metric`;
- `relationship_measurement_stratum`;
- `relationship_confounder`;
- `relationship_provenance`;
- `relationship_theory_link`.

Requirements:

- one repository owner per table family;
- foreign keys to canonical entities;
- no provider writes;
- no LLM writes;
- deterministic uniqueness constraints;
- historical measurements remain immutable;
- recalculation creates a new measurement version;
- raw counts persist even when a display metric is null.

---

# 25. Proposed Modules

## Core domain

- `codie/relationship_intelligence/entity_types.py`
- `codie/relationship_intelligence/relationship_types.py`
- `codie/relationship_intelligence/models.py`
- `codie/relationship_intelligence/errors.py`

## Population and projection

- `codie/relationship_intelligence/population.py`
- `codie/relationship_intelligence/population_manifest.py`
- `codie/relationship_intelligence/predicates.py`
- `codie/relationship_intelligence/entity_projection.py`

## Measurement

- `codie/relationship_intelligence/contingency.py`
- `codie/relationship_intelligence/metrics.py`
- `codie/relationship_intelligence/intervals.py`
- `codie/relationship_intelligence/stability.py`
- `codie/relationship_intelligence/stratification.py`
- `codie/relationship_intelligence/confounders.py`

## Entity-specific aggregation

- `codie/relationship_intelligence/tag_aggregation.py`
- `codie/relationship_intelligence/combo_projection.py`
- `codie/relationship_intelligence/package_projection.py`
- `codie/relationship_intelligence/commander_projection.py`
- `codie/relationship_intelligence/regional_comparison.py`
- `codie/relationship_intelligence/deck_similarity.py`
- `codie/relationship_intelligence/theory_projection.py`

## Provenance and service

- `codie/relationship_intelligence/provenance.py`
- `codie/relationship_intelligence/pair_detail.py`
- `codie/relationship_intelligence/serialization.py`
- `codie/relationship_intelligence/service.py`

## Repository

- `codie/repositories/relationship_repository.py`
- `codie/repositories/relationship_population_repository.py`

## Evidence Fusion integration

- `codie/evidence_fusion/relationship_reference_builder.py`

This adapter may reference completed Relationship Intelligence measurements. It may not recalculate them.

## Jin integration

- `codie/jin/relationship_retrieval.py`
- `codie/jin/relationship_claim_guard.py`
- `codie/jin/relationship_answer_packet.py`

Jin modules remain read-only against Relationship Intelligence repositories.

## UI

- `codie/ui/relationship_explorer/`
- `codie/ui/relationship_pair_detail/`
- `codie/ui/relationship_graph/`
- `codie/ui/relationship_population_bar/`
- `codie/ui/relationship_provenance_panel/`

Exact paths remain subordinate to the accepted repository structure.

---

# 26. Proposed Public Functions

## Population

- `resolve_population(spec) -> PopulationManifest`
- `validate_population_spec(spec) -> ValidationResult`
- `compare_population_specs(left, right) -> PopulationDiff`

## Projection

- `project_entity(endpoint, manifest) -> PredicateProjectionSet`
- `project_card(card, manifest, zone_mode)`
- `project_tag(tag, manifest, exclusion_mode)`
- `project_combo(combo, manifest)`
- `project_package(package, manifest)`
- `project_commander_signature(signature, manifest)`

## Measurement

- `build_contingency(left_projection, right_projection) -> ContingencyTable`
- `calculate_relationship_metrics(table) -> RelationshipMetricBundle`
- `calculate_weighted_relationship_metrics(projections, weights)`
- `calculate_wilson_interval(successes, observations)`
- `classify_stability(metric_bundle, provenance, confounders)`
- `calculate_stratified_dependence_delta(strata)`

## Aggregation

- `aggregate_card_to_tags(card, manifest, leave_one_out=True)`
- `aggregate_tag_to_tag(left_tag, right_tag, cross_card_mode)`
- `calculate_deck_card_jaccard(left_deck, right_deck)`
- `calculate_deck_tag_jaccard(left_deck, right_deck)`

## Output

- `build_pair_detail(measurement_id) -> PairDetail`
- `serialize_pair_detail(pair_detail, format_version)`
- `build_relationship_evidence_reference(measurement_id)`

## Jin guard

- `validate_relationship_claim(claim, pair_detail)`
- `classify_relationship_language(claim)`
- `build_jin_relationship_packet(pair_detail, theory_context)`

No public function returns a card recommendation.

---

# 27. Fixtures

Required fixtures:

1. `relationship_counts_100`
   - verifies all exact formulas.

2. `relationship_entities_10`
   - verifies integration across cards, tags, packages, combos, commanders, events, and regions.

3. `relationship_zero_joint`
   - verifies PMI null handling.

4. `relationship_zero_antecedent`
   - verifies directional denominator handling.

5. `relationship_full_antecedent`
   - verifies dependence-delta complement handling.

6. `relationship_rare_extreme_lift`
   - verifies low-sample gating.

7. `relationship_tag_self_inclusion`
   - verifies leave-one-out aggregation.

8. `relationship_tag_same_card_bridge`
   - verifies inclusive and cross-card tag relationships.

9. `relationship_package_tautology`
   - verifies structural suppression.

10. `relationship_combo_tautology`
    - verifies required-piece suppression.

11. `relationship_simpson_strata`
    - verifies standardized delta.

12. `relationship_region_comparison`
    - verifies identical-filter regional comparison.

13. `relationship_release_boundary`
    - verifies time-valid populations.

14. `relationship_ban_boundary`
    - verifies event-date legality.

15. `relationship_duplicate_provider_lineage`
    - verifies one canonical observation from several sources.

16. `relationship_repeated_pilot`
    - verifies concentration warnings.

17. `relationship_repeated_deck_hash`
    - verifies sensitivity population.

18. `relationship_unknown_tag_mapping`
    - verifies unknown state and coverage.

19. `relationship_private_deck_exclusion`
    - verifies privacy boundary.

20. `relationship_theory_claim_separation`
    - verifies context isolation.

21. `relationship_deterministic_serialization`
    - verifies byte-equivalent serialization.

22. `relationship_weighted_effective_sample`
    - verifies weighted formulas and \(N_{eff}\).

---

# 28. Test Requirements

## 28.1 Formula unit tests

For every metric:

- exact hand-calculated fixture;
- zero case;
- one case;
- undefined denominator;
- symmetric-property test where applicable;
- directional reversal test where applicable;
- decimal tolerance;
- metric version assertion.

Required invariants:

- support is symmetric;
- lift is symmetric;
- leverage is symmetric;
- Jaccard is symmetric;
- PMI is symmetric;
- directional confidence may differ by direction;
- dependence delta may differ by direction;
- PMI equals natural log of lift when both are defined;
- leverage equals support minus marginal-product expectation;
- Jaccard denominator excludes neither-present units.

## 28.2 Property tests

For valid contingency tables:

- support lies in \([0,1]\);
- directional confidence lies in \([0,1]\);
- dependence delta lies in \([-1,1]\);
- Jaccard lies in \([0,1]\);
- lift is nonnegative;
- leverage is bounded by valid probability limits;
- swapping endpoints preserves symmetric metrics;
- swapping endpoints swaps directional fields;
- no metric returns NaN or infinity in serialized output.

## 28.3 Population tests

- private decks excluded by default;
- source records cannot enter without canonical IDs;
- mirrored records count once;
- event-date legality applied;
- unresolved content creates unknown status;
- commander and mainboard zones remain separate;
- exact partner matching requires both commanders;
- partial matching requires explicit mode;
- population manifest contains no duplicate unit IDs.

## 28.4 Confounder tests

- exact-commander concentration detected;
- color-eligibility warning detected;
- generic-staple warning detected;
- release-boundary warning detected;
- placement-selection warning detected;
- repeated-pilot warning detected;
- repeated-deck warning detected;
- tag self-inclusion detected;
- package and combo tautologies detected;
- Simpson fixture produces nonzero global delta and zero standardized delta.

## 28.5 Provenance tests

Every measurement must expose:

- population manifest;
- canonical snapshot;
- counts;
- formula IDs;
- metric versions;
- source lineage;
- date window;
- region;
- sample;
- coverage;
- exclusions;
- generated timestamp.

Missing required provenance invalidates the measurement.

## 28.6 Theory-boundary tests

- adding a theory claim does not change counts;
- removing a theory claim does not change counts;
- theory agreement does not change stability;
- contradictory theory claims remain visible;
- theory claims cannot create package definitions;
- theory claims cannot create authoritative rules interactions.

## 28.7 Jin adversarial tests

Jin must not convert:

- lift into causation;
- confidence into epistemic certainty;
- package co-occurrence into a recommendation;
- regional association into universal format truth;
- theory agreement into measured evidence;
- a required combo piece into a universal deck requirement;
- high support into a claim that a card is correct.

## 28.8 UI tests

- full population remains visible;
- 2×2 table displayed;
- metric tooltips use correct formulas;
- undefined metrics display reasons;
- low-sample results cannot enter default rankings;
- structural and measured edges are distinguishable without color;
- pair detail links to provenance;
- Jin links back to exact measurement;
- private records are not exposed in exports.

## 28.9 Determinism tests

Equivalent:

- canonical snapshot;
- population spec;
- ontology version;
- combo version;
- package version;
- formula version;

must produce equivalent:

- population manifest;
- contingency counts;
- metric values;
- stability gates;
- serialization.

---

# 29. Contract-Ready Codex Handoff

## 29.1 Phase name

**Codie V2 Relationship Intelligence Core Contract**

## 29.2 Objective

Implement the deterministic core required to represent typed structural relationships and calculate reproducible Class 2 relationship evidence across canonical deck populations.

## 29.3 Authorized scope

- relationship entity references;
- typed relationship registry;
- population specifications and manifests;
- three-state endpoint projection;
- card presence;
- tag presence;
- combo list-completeness;
- package satisfaction;
- exact commander signatures;
- event and region lineage;
- contingency-table construction;
- support;
- directional confidence;
- dependence delta;
- lift;
- leverage;
- population Jaccard;
- deck-card Jaccard;
- natural-log PMI;
- Wilson intervals;
- proposed stability gates;
- confounder flags;
- card-to-tag leave-one-out aggregation;
- same-card versus cross-card tag aggregation;
- structural-tautology suppression;
- pair-detail output;
- provenance;
- deterministic serialization;
- read-only Evidence Fusion references;
- read-only Jin relationship packets;
- required fixtures and tests.

## 29.4 Prohibited scope

- recommendations;
- replacement proposals;
- deck-health conclusions;
- LLM calls inside analytics;
- automated package invention;
- automated theory-claim generation;
- causal inference;
- significance claims;
- logistic regression;
- Bayesian recommendation scoring;
- hidden blended relationship scores;
- graph database adoption;
- provider fetching;
- canonicalization changes;
- event-deduplication changes;
- rules-engine expansion;
- simulator changes;
- UI redesign outside Relationship Intelligence surfaces;
- cloud services;
- paid dependencies.

## 29.5 Dependencies

Required existing or separately accepted dependencies:

- canonical card identity;
- canonical commander signatures;
- canonical deck instances;
- canonical event and region records;
- repository layer;
- date-aware legality;
- functional-tag registry;
- Commander Spellbook snapshot;
- curated package registry;
- immutable deck snapshots;
- source-lineage records.

The implementation must fail explicitly when a required dependency is unavailable.

## 29.6 Schema impact

A governed migration is required for:

- assertions;
- population specs;
- population manifests;
- measurements;
- metric values;
- strata;
- confounders;
- provenance;
- theory links.

The migration requires:

- rollback or recovery plan;
- foreign-key review;
- index review;
- repository ownership;
- schema documentation;
- migration tests.

## 29.7 Data flow

```text
Canonical entities
    ->
PopulationSpec
    ->
PopulationManifest
    ->
Three-state endpoint projection
    ->
Contingency table
    ->
Metric calculation
    ->
Stability and confounder assessment
    ->
Provenance assembly
    ->
PairDetail
    ->
Unified Evidence reference
    ->
Read-only Jin retrieval
```

No arrow returns data to canonical source tables.

## 29.8 Required completion report

The implementation report must record:

- task name;
- objective;
- scope;
- files created;
- files modified;
- schema migration;
- repositories;
- formulas implemented;
- formula versions;
- fixtures added;
- tests added;
- commands run;
- deterministic validation result;
- architecture validation result;
- adversarial validation result;
- aggregate validation result;
- unresolved findings;
- exclusions;
- next permitted phase.

## 29.9 Exclusions

The contract does not approve:

- a general knowledge graph;
- automatic package discovery;
- theory-corpus ingestion;
- strategic recommendations;
- relationship-based replacement ranking;
- performance-causation analysis;
- match-win analysis;
- exposure modeling;
- full advanced UI;
- cloud synchronization;
- public sharing.

## 29.10 Unresolved decisions requiring approval

1. Whether the proposed stability thresholds become defaults.
2. Whether relationship populations default to all placements or Top 16 for commander-scoped exploration.
3. Whether color-eligible populations appear by default or only as comparison views.
4. Whether pilot and deck-hash sensitivity views enter core implementation or a later phase.
5. Whether weighted relationship metrics are included in the first implementation.
6. Whether theory links are persisted in the first schema migration or added later.
7. Whether package `ROLE_COMPLETE` definitions are authorized immediately.
8. Whether store and organizer remain `REGION` subtypes or receive separate entity types.
9. Whether pair-detail provenance stores all unit IDs or references a compressed immutable manifest.
10. Whether standardized dependence delta is core V2 or a follow-on controlled-analysis phase.
11. Whether `baseline_delta=P(B|A)-P(B)` should be added as a separately named metric.
12. Whether low-stability results are exportable by default.
13. Whether the relationship graph is part of the core implementation or only the pair-detail table.
14. Whether the comparison draft must be ratified before any Relationship Intelligence implementation contract can be accepted.

# 30. Codex Acceptance Criteria

Implementation is accepted only when all applicable criteria pass.

1. Every endpoint resolves to a typed canonical entity reference.
2. Structural, observed, measured, theory, and user-context relationships remain separately classified.
3. Raw provider records never enter calculations directly.
4. Every population is represented by an immutable `PopulationSpec` and `PopulationManifest`.
5. Private user decks are excluded unless explicitly authorized.
6. Endpoint projection supports true, false, and unknown.
7. Unknown values are excluded and reported rather than treated as absence.
8. Every relationship calculation stores \(a,b,c,d,n_A,n_B,N\).
9. Support exactly equals \(a/N\).
10. Directional confidence A→B exactly equals \(a/(a+b)\).
11. Directional confidence B→A exactly equals \(a/(a+c)\).
12. Dependence delta A→B exactly equals \(a/(a+b)-c/(c+d)\).
13. Lift exactly equals \(aN/((a+b)(a+c))\).
14. Leverage exactly equals \(a/N-((a+b)(a+c))/N^2\).
15. Population Jaccard exactly equals \(a/(a+b+c)\).
16. Natural-log PMI exactly equals \(\ln(lift)\) when defined.
17. Zero-joint PMI serializes as null with an explicit reason.
18. Undefined denominators never serialize as zero, NaN, or infinity.
19. Wilson intervals reproduce the approved hand-calculated fixtures.
20. Metric IDs and formula versions are persisted.
21. Directional and symmetric metrics obey their required invariants.
22. Weighted and unweighted metrics, if weighted metrics are authorized, remain visibly separate.
23. Weighted stability uses the approved effective-sample calculation.
24. Coverage exactly equals usable units divided by candidate units.
25. Low-sample gates reproduce the approved threshold fixtures.
26. Low-stability relationships do not appear in default rankings.
27. Card-to-tag association uses leave-one-out tag presence.
28. Direct card-tag ontology edges remain visible separately.
29. Tag-to-tag output distinguishes same-card bridges from cross-card presence.
30. Package-required and combo-required endpoint pairs are marked structural tautologies.
31. Structural tautologies are excluded from association rankings.
32. Exact commander signatures and exact partner pairs are handled correctly.
33. Partial partner matching requires explicit selection.
34. Commander cards do not enter mainboard presence unless the selected mode permits it.
35. Date-aware release and legality boundaries are enforced.
36. Regional comparisons use identical nonregional filters.
37. Placement-filtered populations display a selection-bias warning.
38. Repeated-pilot and repeated-deck concentration are disclosed when data permits.
39. The Simpson fixture produces the approved global and standardized results.
40. Theory claims do not alter any measured count or metric.
41. Theory claims remain attributed and scope-limited.
42. Relationship Intelligence produces no recommendation, replacement, or deck-health conclusion.
43. Evidence Fusion consumes measurement references without recalculating metrics.
44. Jin access is read-only.
45. Jin relationship packets distinguish directional confidence from evidence stability.
46. Jin does not convert correlation, lift, leverage, PMI, or dependence delta into causal claims.
47. Jin does not generate add, cut, or replacement recommendations directly from relationship evidence.
48. Pair-detail output includes the full 2×2 table.
49. Pair-detail output includes population, sample, coverage, formulas, versions, confounders, and provenance.
50. Structural, measured, and theory edges are distinguishable without relying solely on color.
51. Every displayed metric links to its formula and source population.
52. Every measurement links to canonical records and provider lineage.
53. Duplicate provider records produce one canonical observation.
54. Population manifests contain no duplicate canonical unit IDs.
55. Equivalent inputs produce equivalent counts, metrics, stability, and serialization.
56. Exports preserve filters, counts, formulas, versions, confidence handling, caveats, and provenance.
57. Private records do not leak into exports or Jin packets.
58. All required fixtures pass.
59. All unit, integration, negative-path, privacy, determinism, architecture, and adversarial tests pass.
60. No unresolved blocking validation finding remains.
61. No implementation work cites the V2 comparison draft as governing authority unless the relevant contract and constitutional status have been explicitly approved.
:::
> [!IMPORTANT]
> Repository intake note: This is a preserved pre-ratification design
> proposal. `docs/CODIE_V2_CONSTITUTION.md` is now ratified and is the
> governing authority. Statements below that call V2 a non-authoritative
> comparison draft are historical. This proposal does not authorize
> implementation.
