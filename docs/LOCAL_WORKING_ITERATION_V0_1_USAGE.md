# Codie Local Working Iteration v0.1

Codie runs as a local-only application on `http://127.0.0.1:8765/`. It stores
its workspace in a contained SQLite database. It performs no telemetry,
account login, paid-service work, background network work, or page-load fetch.

## First-time UI setup

From the repository root in Windows PowerShell:

```powershell
.\scripts\setup-codie-ui.ps1
```

This explicit setup step installs the already declared, locked UI development
dependencies and builds `ui/dist`. Normal Codie launch never installs packages
or downloads card data. Card data is downloaded only after you press
**Prepare Codie** or **Refresh card data**.

## Start Codie

```powershell
.\scripts\run-codie.ps1
```

The launcher opens the browser and remains attached to the local service. Press
`Ctrl+C` in that PowerShell window to stop Codie. The launcher reports the URL,
workspace, database path, process ID, and privacy boundary without printing
deck text or card payloads.

To use a different contained workspace or port:

```powershell
.\scripts\run-codie.ps1 -WorkspaceRoot "C:\CodieWorkspace" -Port 8765
```

Use `-NoBrowser` when you want the URL reported without automatically opening
it.

## Safe working sequence

1. Select **Prepare Codie**. This creates the private workspace and prepares
   locally cached card data. On later visits it safely reuses that cache.
2. Paste a public Moxfield deck link or decklist text, optionally give it a
   name, and select **Import and remember deck**.
3. Select the remembered deck.
4. Select a local evidence-candidate JSON packet.
5. Run and save the evidence-only comparison.
6. Inspect evidence type and provenance, then download JSON or Markdown.
7. Reload the page to confirm the same deck and analysis are read from SQLite.
8. Press `Ctrl+C` in the launcher window to stop the service.

## Accepted deck input

The normal deck field accepts either:

- a public `https://www.moxfield.com/decks/...` link; or
- pasted Commander deck text with section headings and quantity/name rows.

Moxfield access happens only after you select the import button. Private or
unavailable links, rate limits, network failures, and upstream changes fail
safely and ask you to paste the deck export instead. Codie does not require a
Moxfield account and does not ingest private notes or primer text.

## Accepted local evidence file

Evidence input may be either an array or an object with a `candidates` array.
Each candidate uses:

```json
{
  "oracle_id": "oracle-id",
  "card_name": "Card Name",
  "evidence_type": "tournament_evidence",
  "score": 0.75,
  "sample_size": 20,
  "source_record_id": "event:deck:card",
  "source_url": "https://source.example/record"
}
```

Evidence type and provenance remain visible. Presence or absence is descriptive
only; Codie v0.1 does not generate rankings, additions, cuts, or recommendations.

## Boundaries

- Prepared card data is identity truth, not tournament evidence or strategic
  advice.
- Remote access is user-initiated only; nothing is fetched on page load or in
  the background.
- Hareruya references are accepted only as tournament evidence.
- Theory, Rules, Corrections, Jin, simulations, and Goal Engine authority are
  unchanged and are not implemented by this slice.
- Stream Deck is absent and remains supplemental-only.
- Every API and UI request remains same-origin and loopback-only.
