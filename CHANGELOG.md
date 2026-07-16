# Changelog

Human-readable log of library updates, newest first. Consuming projects pin
a commit of this repo — read this to decide whether to bump your pin.
One line per change; date every entry.

## 2026-07-11

- Restructured for multi-project use: `LITERATURE.md` → `SUMMARIES.md`,
  `SUMMARY.md` → `SYNTHESIS.md`; human `README.md` + agent contract
  `AGENTS.md`; added `CHANGELOG.md` and `scripts/extract_paper_text.py`.
- Policy: papers are added only on the owner's explicit request (no
  proactive collecting; the earlier WATCHLIST.md was removed for this
  reason).
- Initial import from CreditPFN: 30 papers (PDF + text), 15 repository
  dumps, per-paper summaries, field synthesis, repository guide,
  standalone dump-refresh script.
