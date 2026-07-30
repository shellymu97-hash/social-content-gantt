#!/usr/bin/env python3
"""Builds the three shipped variants of the planner from template.html.

  planner.html   body-only, full fonts, sync off   -> published as a Claude artifact
  index.html     standalone, subset fonts, sync on -> served by GitHub Pages (root)
  local copy     standalone, full fonts, sync on   -> the file she keeps on disk
"""
import base64, os, sys

ROOT = "/Users/guyk/Downloads/claude/projects/גאנט תוכן סושיאל"
SCR  = os.path.dirname(os.path.abspath(__file__))
OUT  = ROOT
os.makedirs(OUT, exist_ok=True)

def b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

FULL = (b64(os.path.join(ROOT, "Talent_FS-Regular_Web-sk4vjg/Talent_FS-Regular.woff2")),
        b64(os.path.join(ROOT, "Talent_FS-Bold_Web-wie17a/Talent_FS-Bold.woff2")))
SUB  = (b64(os.path.join(SCR, "reg.sub.woff2")),
        b64(os.path.join(SCR, "bold.sub.woff2")))

tpl = open(os.path.join(SCR, "template.html"), encoding="utf-8").read()

def build(fonts, sync):
    out = tpl.replace("__FONT_R__", fonts[0]).replace("__FONT_B__", fonts[1])
    out = out.replace("__SYNC__", "true" if sync else "false")
    assert "__FONT_" not in out and "__SYNC__" not in out
    return out

def standalone(body):
    head = ('<!doctype html>\n<html lang="he" dir="rtl">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
            '<meta name="color-scheme" content="light">\n'
            '<meta name="theme-color" content="#FAFCFC">\n')
    doc = head + body + "\n</body>\n</html>\n"
    doc = doc.replace('</style>\n\n<div class="app">', '</style>\n</head>\n<body>\n<div class="app">', 1)
    assert "</head>" in doc
    return doc

targets = {
    os.path.join(SCR, "planner.html"): build(FULL, False),                 # artifact body
    os.path.join(OUT, "index.html"):   standalone(build(SUB,  True)),      # hosted
    os.path.join(ROOT, "תכנון-תוכן-סושיאל.html"): standalone(build(FULL, True)),   # local copy
}
for path, content in targets.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("%7d KB  %s" % (len(content.encode()) / 1024, os.path.basename(path)))
