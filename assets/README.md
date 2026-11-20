# Book styling and assets

The HTML stylesheet and PDF templates are adapted from the MISP Project and contributors' [MISP User Guide](https://github.com/MISP/misp-book/tree/68e2dfc4893db0143bd91a8fb6ff2d6a52f65f18). The adapted styling files are licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), one of the upstream book's two licenses. The adaptation uses the shared HTML styles and PDF layout with the CVD book's metadata, chapter labels, and Vulnerability-Lookup branding.

- The HTML theme comes from [misp.scss](https://github.com/MISP/misp-book/blob/68e2dfc4893db0143bd91a8fb6ff2d6a52f65f18/assets/misp.scss).
- The Typst layout, template, and chapter link filter come from [the MISP Book PDF assets](https://github.com/MISP/misp-book/tree/68e2dfc4893db0143bd91a8fb6ff2d6a52f65f18/assets/pdf).
- Source Sans 3 and Source Code Pro are distributed under the SIL Open Font License 1.1. Their licenses, upstream locations, and checksums are in [pdf/fonts](pdf/fonts/).
- The [Vulnerability-Lookup logo](https://www.vulnerability-lookup.org/images/VL-hori-coul.jpg) and [favicon](https://www.vulnerability-lookup.org/favicon.svg) come from the project's website.

## Mermaid diagrams

The shared theme and renderer adapt the MISP Book's diagram palette and frame under CC BY-SA 4.0. They add the Vulnerability-Lookup wordmark above the graph at the top left. The renderer embeds the project's PNG wordmark in the SVG for both HTML and PDF. [MISP Book diagram assets](https://github.com/MISP/misp-book/tree/68e2dfc4893db0143bd91a8fb6ff2d6a52f65f18/assets/diagrams) · [Vulnerability-Lookup wordmark](https://github.com/vulnerability-lookup/vulnerability-lookup/blob/b4c82c13e40a3e2ee91436ff1c52c9bc7021b50d/website/web/static/img/VL-hori-coul.png)

Put editable sources in each chapter's `diagrams/` directory. Include `accTitle` and `accDescr`, and use the semantic classes in [theme.json](diagrams/theme.json) for flowchart accents. Generate the SVGs with Python Playwright, Chromium, DejaVu Sans and the Mermaid bundle from Quarto 1.11.9.

```sh
python assets/diagrams/render.py \
  --mermaid-js /path/to/quarto/share/formats/html/mermaid/mermaid.min.js \
  --chromium /usr/bin/chromium
```

Commit the Mermaid sources and generated SVGs together. Quarto renders the committed SVGs directly.

## MISP Book copyright notices

- Copyright © 2012 Christophe Vandeplas
- Copyright © 2012 Belgian Defence
- Copyright © 2012 NATO / NCIRC
- Copyright © 2013–2026 Andras Iklody
- Copyright © 2015–2026 Alexandre Dulaunoy
- Copyright © 2014–2026 CIRCL – Computer Incident Response Center Luxembourg
- Copyright © 2018 Camille Schneider
- Copyright © 2018–2026 Steve Clement
- Copyright © 2021 Jeroen Pinoy
