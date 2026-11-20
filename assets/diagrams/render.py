#!/usr/bin/env python3
# SPDX-License-Identifier: CC-BY-SA-4.0
"""Render the book's Mermaid sources as self-contained SVGs."""

import argparse
import base64
import json
import re
from pathlib import Path
from xml.etree import ElementTree

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[2]
ASSETS = ROOT / "assets" / "diagrams"
SVG_NS = "http://www.w3.org/2000/svg"

# The frame follows the MISP Book diagram renderer. See assets/README.md.
RENDER = r"""
async ({source, id, theme, logo}) => {
  mermaid.initialize({...theme.mermaid, deterministicIDSeed: id});
  const {svg} = await mermaid.render(id, source);
  document.body.innerHTML = svg;
  const graph = document.querySelector("svg");
  const frame = theme.frame;

  for (const node of graph.querySelectorAll(".node rect")) {
    node.setAttribute("rx", frame.nodeRadius);
    node.setAttribute("ry", frame.nodeRadius);
  }

  const [x, y, width, height] = graph.getAttribute("viewBox").split(/\s+/).map(Number);
  const logoImage = new Image();
  logoImage.src = logo;
  await logoImage.decode();
  const logoHeight = frame.logoWidth * logoImage.naturalHeight / logoImage.naturalWidth;
  const totalWidth = Math.max(width, frame.logoWidth) + 2 * frame.padding;
  const graphTop = frame.headerHeight + frame.graphGap;
  const totalHeight = graphTop + height + frame.padding;

  function element(name, attributes) {
    const node = document.createElementNS("http://www.w3.org/2000/svg", name);
    for (const [key, value] of Object.entries(attributes)) node.setAttribute(key, value);
    return node;
  }

  const contents = element("g", {
    transform: `translate(${(totalWidth - width) / 2 - x}, ${graphTop - y})`,
  });
  for (const child of [...graph.children]) {
    if (!["title", "desc", "style", "defs"].includes(child.localName)) contents.append(child);
  }
  graph.append(
    element("rect", {
      x: 0.5, y: 0.5, width: totalWidth - 1, height: totalHeight - 1, rx: 10,
      fill: frame.background, stroke: frame.border, "aria-hidden": "true",
    }),
    element("image", {
      x: frame.padding, y: frame.logoTop, width: frame.logoWidth, height: logoHeight,
      href: logo, "aria-hidden": "true",
    }),
    element("line", {
      x1: frame.padding, x2: totalWidth - frame.padding,
      y1: frame.headerHeight, y2: frame.headerHeight,
      stroke: frame.border, "aria-hidden": "true",
    }),
    contents,
  );
  graph.setAttribute("viewBox", `0 0 ${totalWidth} ${totalHeight}`);
  graph.setAttribute("width", totalWidth);
  graph.setAttribute("height", totalHeight);
  return graph.outerHTML;
}
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mermaid-js", type=Path, required=True)
    parser.add_argument("--chromium", default="/usr/bin/chromium")
    args = parser.parse_args()

    theme = json.loads((ASSETS / "theme.json").read_text())
    logo_bytes = (ASSETS / "vulnerability-lookup-logo.png").read_bytes()
    logo = "data:image/png;base64," + base64.b64encode(logo_bytes).decode("ascii")
    classes = "\n".join(
        f"  classDef {name} {style}" for name, style in theme["classes"].items()
    )

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=args.chromium)
        page = browser.new_page()
        page.set_content("<!doctype html><html><body></body></html>")
        page.add_script_tag(path=str(args.mermaid_js.resolve()))

        for source in sorted(ROOT.glob("*/diagrams/*.mmd")):
            definition = source.read_text()
            if re.search(r"^\s*(flowchart|graph)\b", definition, re.MULTILINE):
                definition += "\n" + classes
            svg = page.evaluate(RENDER, {
                "source": definition,
                "id": f"cvd-{source.parent.parent.name}-{source.stem}",
                "theme": theme,
                "logo": logo,
            })
            root = ElementTree.fromstring(svg)
            if any(root.find(f"{{{SVG_NS}}}{tag}") is None for tag in ("title", "desc")):
                raise ValueError(f"{source}: add accTitle and accDescr to the Mermaid source")
            if root.find(f".//{{{SVG_NS}}}foreignObject") is not None:
                raise ValueError(f"{source}: use SVG labels for Typst compatibility")
            target = source.with_suffix(".svg")
            target.write_text(svg + "\n")
            print(target.relative_to(ROOT))
        browser.close()


if __name__ == "__main__":
    main()
