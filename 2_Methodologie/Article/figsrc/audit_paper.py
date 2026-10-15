# -*- coding: utf-8 -*-
"""Audit of main.tex: every number traces to faits_sources.csv, and the style rules hold.

Run from article/:  py -I figsrc/audit_paper.py
Exit code 0 when everything passes.
"""
import csv
import io
import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
RACINE = os.path.dirname(ICI)
TEX = os.path.join(RACINE, "main.tex")
FAITS = os.path.join(ICI, "faits_sources.csv")

src = io.open(TEX, encoding="utf-8").read()
corps = src.split("\\begin{document}", 1)[1]
# commentaires
corps = re.sub(r"(?<!\\)%.*", "", corps)
# le resume francais est verifie a part (meme contenu que l'abstract, sans chiffre)
texte = corps

problemes = []

# 1. tirets longs
for motif, nom in [("---", "tiret cadratin LaTeX"), ("—", "tiret cadratin"), ("–", "tiret demi-cadratin"),
                   (r"(?<![-\w])--(?![-\w])", "tiret demi-cadratin LaTeX")]:
    for m in re.finditer(motif, texte):
        problemes.append("%s : ...%s..." % (nom, texte[max(0, m.start()-30):m.end()+30].replace("\n", " ")))

# 2. point median
if "·" in texte:
    problemes.append("point median present")

# 3. chiffres
nettoye = texte
for cmd in ["cite", "ref", "eqref", "label", "includegraphics", "bibliography", "bibliographystyle",
            "url", "href", "hypersetup", "captionsetup", "sisetup"]:
    nettoye = re.sub(r"\\%s(\[[^\]]*\])?\{[^}]*\}" % cmd, " ", nettoye)
nettoye = re.sub(r"\\(begin|end)\{[^}]*\}(\{[^}]*\})?", " ", nettoye)
nettoye = re.sub(r"\{@\{\}[^}]*\}", " ", nettoye)
nettoye = re.sub(r"[LYp]\{\d+(\.\d+)?cm\}", " ", nettoye)
nettoye = re.sub(r"\d+(\.\d+)?\s*(pt|cm|mm|em|ex)\b(?![a-z])", " ", nettoye)
nettoye = re.sub(r"\\linewidth", " ", nettoye)
nettoye = re.sub(r"\\section\*?|\\subsection\*?", " ", nettoye)
nettoye = re.sub(r"\$\^\{\d\}\$|\$\^\{\d,\d\}\$", " ", nettoye)          # indices d'affiliation
nettoye = re.sub(r"\\num\{([^}]*)\}", r" \1 ", nettoye)
nettoye = re.sub(r"\\SI\{([^}]*)\}\{[^}]*\}", r" \1 ", nettoye)
nettoye = re.sub(r"(\d)\\,", r"\1 ", nettoye)
nettoye = re.sub(r"\\\w+", " ", nettoye)

autorises = {}
for ligne in csv.DictReader(io.open(FAITS, encoding="utf-8"), delimiter=";"):
    autorises[ligne["valeur"]] = ligne["source"]

inconnus = {}
for m in re.finditer(r"(?<![\w.])(\d+(?:\.\d+)?)(?![\w.])", nettoye):
    v = m.group(1)
    if v not in autorises:
        inconnus.setdefault(v, nettoye[max(0, m.start()-40):m.end()+40].replace("\n", " "))
for v, ctx in sorted(inconnus.items()):
    problemes.append("chiffre sans source %s : ...%s..." % (v, ctx))

# 4. questions rhetoriques (un ? hors citation entre guillemets)
for m in re.finditer(r"\?", texte):
    avant = texte[max(0, m.start()-60):m.start()]
    if "``" in avant and "''" not in avant.split("``")[-1]:
        continue
    problemes.append("point d'interrogation : ...%s?..." % avant.replace("\n", " ")[-50:])

# 5. signalisation enumerative et tournures interdites
interdits = [r"\bThe (first|second|third) is\b", r"\b(two|three|four|five) (things|readings|mechanisms|contributions)\b",
             r"\bearns its place\b", r"\bper cent\b", r"\bFinally,\s+(?=[a-z])", r"\bTODO\b", r"lorem"]
for p in interdits:
    for m in re.finditer(p, texte, flags=re.I):
        problemes.append("tournure interdite '%s' : ...%s..." % (p, texte[max(0, m.start()-30):m.end()+30].replace("\n", " ")))

# 6. deux-points suivis d'une enumeration dans la prose (hors maths et tableaux)
prose = re.sub(r"\$[^$]*\$", " ", texte)
prose = re.sub(r"\\begin\{(tabularx|equation)\}.*?\\end\{\1\}", " ", prose, flags=re.S)
for m in re.finditer(r"[a-z]\s*:\s+[^.\n]{0,80},[^.\n]{0,80}\band\b", prose):
    problemes.append("deux-points + enumeration : ...%s..." % prose[m.start():m.end()].replace("\n", " "))

if problemes:
    print("AUDIT : %d probleme(s)" % len(problemes))
    for p in problemes:
        print(" -", p)
    sys.exit(1)
print("AUDIT OK : chiffres traces (%d valeurs sources), aucun tiret long, aucun point median, "
      "aucune question rhetorique, aucune tournure interdite." % len(autorises))
