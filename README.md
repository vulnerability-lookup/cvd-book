# Coordinated Vulnerability Disclosure

*A Practical Guide for CNAs, GNAs, CSIRTs, and Publishers* is an operational book about using Vulnerability-Lookup to handle and publish coordinated vulnerability disclosures. Its lifecycle follows [GCVE BCP-02](https://gcve.eu/bcp/gcve-bcp-02/). Its Quarto layout follows the [MISP Book](https://github.com/MISP/misp-book/), with chapters in their own directories and grouped into parts in `_quarto.yml`.

## Build and preview

Install the [Quarto CLI](https://quarto.org/docs/get-started/). The HTML book builds from the repository root with Quarto alone. Validation used Quarto 1.11.9.

```sh
quarto render --to html
quarto preview --no-browser
```

The render writes `_book/index.html`. The preview server prints its local address and rebuilds pages as you edit. A Vulnerability-Lookup instance is useful for trying the workflows in the guide. The book itself renders without one.

## Add a chapter

1. Create a `topic-name/index.qmd` file and give it a level-one heading.
2. Add the file under the relevant part in `_quarto.yml` and use relative `.qmd` links between chapters.
3. Cite the relevant BCP section and Vulnerability-Lookup documentation. Use fictional case data and note the Vulnerability-Lookup release and configuration when documenting version-specific behavior.
4. Render the book and check the chapter in the sidebar along with its links and headings.
