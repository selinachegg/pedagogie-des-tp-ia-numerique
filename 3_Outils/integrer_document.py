# -*- coding: utf-8 -*-
# (c) 2026 Selina Cheggour. Tous droits reserves. Reproduction, adaptation ou reutilisation
# interdites sans autorisation ecrite de l auteure. Presente au conseil de perfectionnement
# de l Icam Toulouse, 14-15 octobre 2026. Partie de « Pedagogie des TP IA numerique ».
"""
Integre un PDF directement DANS Atelier_IA.html, en base64.

Le PDF s'affiche dans la page comme un PDF normal, dans une visionneuse, et
un bouton permet de le telecharger pour l'importer dans NotebookLM.
Le HTML reste un livrable unique : plus rien a deposer a cote, plus de lien
qui casse quand on met la page sur Moodle.

Usage :
    py integrer_document.py "..\\etudiant_IA\\document_atelier.pdf"
    py integrer_document.py "..." --titre "Note interne NI-2027-04"

Le script est idempotent : on peut le relancer avec un autre PDF, il remplace
le precedent.

Pourquoi un Blob et pas un simple lien data: ?
    Chrome bloque la navigation de premier niveau vers une URL data:, et
    refuse egalement d'afficher un PDF servi en data: dans une iframe. On
    stocke donc le base64 dans une variable JS, on reconstruit un Blob, et on
    fabrique une URL temporaire. Cela fonctionne pour l'affichage dans la
    page, pour le telechargement et pour l'ouverture dans un onglet.
"""
import argparse
import base64
import io
import os
import re
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.normpath(os.path.join(ICI, "..", "etudiant_IA", "Atelier_IA.html"))

DEBUT = "/* ==== DOCUMENT INTEGRE, genere par integrer_document.py ==== */"
FIN = "/* ==== fin du document integre ==== */"

BLOC_HTML = """    <p>
      Tout le monde travaille sur <strong>le m&#234;me document</strong> : <b>{titre}</b>.
      Il est int&#233;gr&#233; &#224; cette page, vous n'avez rien &#224; aller chercher ailleurs.
      Feuilletez-le ci-dessous, puis t&#233;l&#233;chargez-le pour l'importer dans NotebookLM.
    </p>

    <div style="border:1px solid var(--rule2);background:var(--paper2);margin:18px 0 0">
      <iframe id="doc-cadre" title="{titre}"
              style="display:block;width:100%;height:640px;border:0;background:#fff"></iframe>
    </div>
    <div class="barre" style="margin:12px 0 28px">
      <button class="btn" id="doc-tel">T&#233;l&#233;charger le PDF</button>
      <button class="btn sec" id="doc-voir">Ouvrir dans un onglet</button>
      <span class="rappel" id="doc-poids"></span>
    </div>
"""

BLOC_JS = """
{debut}
var DOC_NOM = "{nom}";
var DOC_POIDS = "{poids}";
var DOC_B64 = "{b64}";

(function(){{
  var info = document.getElementById('doc-poids');
  if(info) info.textContent = 'PDF \\u00b7 ' + DOC_POIDS + ' \\u00b7 \\u00e0 importer dans NotebookLM';

  var cache = null;
  function urlDoc(){{
    if(cache) return cache;
    var bin = atob(DOC_B64), n = bin.length, oct = new Uint8Array(n);
    for(var i = 0; i < n; i++) oct[i] = bin.charCodeAt(i);
    cache = URL.createObjectURL(new Blob([oct], {{type: 'application/pdf'}}));
    return cache;
  }}

  // la visionneuse : le PDF s'affiche dans la page comme un PDF normal
  var cadre = document.getElementById('doc-cadre');
  if(cadre) cadre.src = urlDoc();

  var tel = document.getElementById('doc-tel');
  if(tel) tel.addEventListener('click', function(){{
    var a = document.createElement('a');
    a.href = urlDoc(); a.download = DOC_NOM; a.click();
  }});

  var voir = document.getElementById('doc-voir');
  if(voir) voir.addEventListener('click', function(){{
    window.open(urlDoc(), '_blank');
  }});
}})();
{fin}
"""


def lisible(o):
    if o < 1024:
        return "%d o" % o
    if o < 1024 * 1024:
        return "%.0f Ko" % (o / 1024.0)
    return "%.1f Mo" % (o / 1048576.0)


def main():
    ap = argparse.ArgumentParser(description="Integre un PDF dans Atelier_IA.html")
    ap.add_argument("pdf", help="chemin du PDF a integrer")
    ap.add_argument("--nom", help="nom du fichier propose au telechargement")
    ap.add_argument("--titre", default="le document de r&#233;f&#233;rence",
                    help="libelle affiche dans la page")
    a = ap.parse_args()

    if not os.path.isfile(a.pdf):
        sys.exit("PDF introuvable : " + a.pdf)
    if not os.path.isfile(HTML):
        sys.exit("Atelier_IA.html introuvable : " + HTML)

    brut = open(a.pdf, "rb").read()
    if brut[:5] != b"%PDF-":
        sys.exit("Ce fichier ne commence pas par %PDF-, ce n'est pas un PDF valide.")

    nom = a.nom or os.path.basename(a.pdf)
    b64 = base64.b64encode(brut).decode("ascii")
    poids = lisible(len(brut))

    s = io.open(HTML, encoding="utf-8").read()

    # 1. retirer une integration precedente
    s = re.sub(re.escape(DEBUT) + r".*?" + re.escape(FIN), "", s, flags=re.S)
    s = re.sub(r"    <p>\s*Tout le monde travaille sur <strong>.*?</p>\n"
               r"(\s*<div style=\"border:1px solid var\(--rule2\).*?</div>\n)?"
               r"(\s*<div class=\"barre\" style=\"margin:12px 0 28px\">.*?</div>\n)?",
               "@@ANCRE@@\n", s, count=1, flags=re.S)
    if "@@ANCRE@@" not in s:
        sys.exit("Paragraphe de la manche 02 introuvable. Le HTML a-t-il ete modifie a la main ?")

    # 2. poser le nouveau bloc
    s = s.replace("@@ANCRE@@\n", BLOC_HTML.format(titre=a.titre), 1)

    # 3. injecter la charge et le code juste avant la fin du script
    ancre = "\n</script>\n</body>"
    if ancre not in s:
        sys.exit("Fin de script introuvable dans le HTML.")
    s = s.replace(ancre, BLOC_JS.format(debut=DEBUT, fin=FIN, nom=nom,
                                        poids=poids, b64=b64) + ancre, 1)

    io.open(HTML, "w", encoding="utf-8").write(s)

    print("Document integre  :", nom)
    print("Poids du PDF      :", poids)
    print("Poids du HTML     :", lisible(len(s.encode("utf-8"))))
    print()
    print("La manche 02 affiche desormais le PDF dans une visionneuse,")
    print("avec un bouton de telechargement pour NotebookLM.")


if __name__ == "__main__":
    main()
