# Supporting references

These fourteen owner-selected sources provide benchmark, methodology and credit-risk
context for reading the TFM literature. They are **not** part of the mirrored
`Tabular Foundation Models` Zotero collection or the core `papers/` corpus.

`pdfs/<year>/` holds byte-for-byte copies of the owner's linked Zotero PDFs;
`text/<year>/` holds their generated UTF-8 full-text extracts. The year is the
Zotero publication year, not necessarily the revision date of a preprint PDF.
`manifest.json` records each title, Zotero item and attachment keys, citation key,
DOI where present, exact PDF and text paths, PDF and text SHA-256 hashes, and
any visible arXiv version banner.

To regenerate the extracts after a deliberate source update, update the PDF hash
in the manifest and run, from the TFM Library root:

```bash
python scripts/papers/extract_supporting_text.py --all
```

Use `python scripts/papers/extract_supporting_text.py --check` to verify the
files and recorded hashes without writing. Do not edit generated text by hand.
Consumer projects receive repository changes only after a separately authorized
publication and submodule pin update.

## Added method references (3 November 2026)

- **TabM: Advancing Tabular Deep Learning with Parameter-Efficient Ensembling** — `2025.GORISHNIY.tabmadvancingtabulardeeplearningparameterefficientensembling`. Published conference or journal PDF
- **Catastrophic Interference in Connectionist Networks: The Sequential Learning Problem** — `1989.MCCLOSKEY.catastrophicinterferenceconnectionistnetworkssequentiallearningproblem`. Published chapter
- **Catastrophic forgetting in connectionist networks** — `1999.FRENCH.catastrophicforgettingconnectionistnetworks`. Published conference or journal PDF
- **Overcoming catastrophic forgetting in neural networks** — `2017.KIRKPATRICK.overcomingcatastrophicforgettingneuralnetworks`. Author-accepted manuscript from Imperial College London; journal metadata retained.
- **Explicit Inductive Bias for Transfer Learning with Convolutional Networks** — `2018.LI.explicitinductivebiastransferlearningconvolutionalnetworks`. Published conference or journal PDF
