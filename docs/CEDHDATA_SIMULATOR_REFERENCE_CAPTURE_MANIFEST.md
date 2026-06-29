# cEDHData Simulator Reference Capture Manifest

Date: 2026-06-29

## Purpose

Record the public cEDHData simulator assets inspected for Codie's simulator
design without copying third-party source code or full card data into Codie.

## Capture Boundary

Allowed:

- public URL metadata
- local reference file hashes
- derived architecture notes
- derived data-shape notes
- future fixture checklist

Forbidden:

- copying `bundle.js` into Codie
- copying `cards.json` into Codie
- porting cEDHData JavaScript line-by-line
- treating simulator outputs as tournament evidence

## Public Page Metadata

Inspected URL:

```text
https://www.cedhdata.com/simulator
```

Observed:

```text
PAGE_STATUS 200
PAGE_BYTES 5584
```

Script URLs observed:

```text
/bundle.js
https://cdn.tailwindcss.com?plugins=typography
```

Relevant public asset HEAD checks:

```text
https://www.cedhdata.com/bundle.js
STATUS=200
LENGTH=3018857
TYPE=application/javascript; charset=utf-8

https://www.cedhdata.com/data/cards.json
STATUS=200
LENGTH=12371959
TYPE=application/json; charset=utf-8
```

## User-Supplied Local Reference Files

These files remain outside the Codie repository:

```text
C:\Users\Main\Downloads\cedhdata_cards.json
C:\Users\Main\Downloads\cedhdata_simulator_main_bundle.js
C:\Users\Main\Downloads\cedhdata_simulator_scripts_list.txt
```

SHA256 hashes:

```text
cedhdata_cards.json
F05E42EE65B4ADAB22EE23251E964207AEB29AFCF4241D046AC49102A845E925

cedhdata_simulator_main_bundle.js
AC9D6EFEB40130992F27BCA0F7B49709F6DBE2EE91AFAE3783669E5CF34EC523

cedhdata_simulator_scripts_list.txt
D198FB143F0DA87B0A01FEC4877AA45FE9043D26733C838775275BFB2F07FA16
```

## Derived Findings Already Recorded

See:

```text
docs/PHASE13A_CEDHDATA_REFERENCE_EXTRACTION_AND_CORE_MODEL_DESIGN.md
docs/PHASE13A_CEDHDATA_REFERENCE_EXTRACTION_AND_CORE_MODEL_DESIGN_REPORT.md
docs/ROADMAP_PATCH_SIMULATOR_CARD_DEFINITION_MANAGER.md
```

Those documents record only architecture and model-shape lessons.

## Still Needed

The static assets are enough for architecture and card model design, but not
enough for behavior parity tests.

Still useful to capture manually from the simulator UI:

```text
one complete input deck + target config
one successful output summary
one successful action trace
one failed output summary
one failed action trace
one unsupported-card warning/output
screenshots of simulator settings and results
```

Preferred future filenames outside the repo:

```text
cedhdata_example_input_rhystic_t2.json
cedhdata_example_output_rhystic_t2.json
cedhdata_success_trace_rhystic_t2.json
cedhdata_failed_trace_rhystic_t2.json
cedhdata_unsupported_cards_example.json
cedhdata_simulator_settings_screenshots.zip
```

## Implementation Reminder

Codie should implement a clean Python-native simulator. The cEDHData files are
reference inputs only.
