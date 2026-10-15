# Pédagogie des TP IA numérique

[![DOI méthodologie](https://zenodo.org/badge/DOI/10.5281/zenodo.23390567.svg)](https://doi.org/10.5281/zenodo.23390567) [![DOI supports](https://zenodo.org/badge/DOI/10.5281/zenodo.23390565.svg)](https://doi.org/10.5281/zenodo.23390565)

**Étalonner l'instrument : de l'atelier guidé au mini-projet**

Selina Cheggour, University of Strasbourg (ICube UMR 7357) et Icam, Institut Catholique d'Arts
et Métiers, Strasbourg. Méthode pédagogique, version 1.1 du 15 octobre 2026.

> **Présentée au conseil de perfectionnement de l'Icam Toulouse, les 14 et 15 octobre 2026.**

> © 2026 Selina Cheggour. **Tous droits réservés.** Voir [LICENCE.md](LICENCE.md).
> Ce dépôt est consultable publiquement, mais **aucune** licence de réutilisation n'est accordée :
> reproduction, adaptation ou réutilisation interdites sans autorisation écrite de l'auteure.

## La méthode en bref

Une séance de TP sur l'IA est transformée en une séquence en deux phases :

1. **Un atelier guidé, « Étalonner l'instrument ».** L'étudiant passe cinq outils d'IA au banc,
   comme un instrument de mesure : *soumettre une entrée connue, relever la sortie, la confronter
   à une référence, noter l'écart.* Des pièges d'injection indirecte sont cachés dans les supports.
2. **Un mémo de transition**, remis après l'atelier, qui révèle les pièges et fixe la méthode.
3. **Un mini-projet décisionnel**, « Dossier LC-4 » : une décision d'ingénieur à signer, sur un
   dossier contenant ses propres pièges, évaluée sur la traçabilité de chaque affirmation.

L'atelier tient dans **un seul fichier HTML centralisé** ; chaque format de fichier (HTML, PDF,
PNG, CSV) est choisi pour ce qu'il enseigne ; l'ensemble est **scénarisé**, **challengeant** et
pensé comme une initiation à la **cybersécurité de l'IA**.

## Contenu

| Dossier | Fichier | Contenu |
|---|---|---|
| `1_Documents/` | `TP5-IA.html` | Atelier guidé (page web autonome et centralisée) |
| | `Mini_Projet.pdf` | Énoncé du mini-projet |
| | `Dossier_LC-4.pdf` | Dossier remis aux étudiants (contient des pièges volontaires) |
| `2_Methodologie/` | `Pedagogie_des_TP_IA_numerique.pdf` / `.tex` | Note de méthode : phases et contenu |
| | `Annexe_A_Choix_de_conception.pdf` / `.tex` | Annexe A : support HTML centralisé, formats de fichiers, scénarisation, défi, cybersécurité de l'IA |
| `2_Methodologie/Article/` | `Cheggour_2026_Calibrating_generative_AI_with_indirect_prompt_injection.pdf` | Article de recherche (anglais), avec ses sources LaTeX, figures et audit des chiffres |
| | `Cheggour_2026_Resume_francais.pdf` | Résumé de l'article en français |
| `3_Outils/` | `integrer_document.py` | Script qui intègre le PDF de référence dans la page HTML de l'atelier |
| racine | `EMPREINTES_SHA256.txt` | Empreintes des fichiers déposés |

⚠️ Les documents de `1_Documents/` contiennent **volontairement** du texte caché et des
métadonnées trompeuses : ce sont les pièges pédagogiques décrits dans la méthode. Ne pas les
confier à une IA en croyant leur contenu.

## Citer ce travail

Cheggour, S. (2026). *Pédagogie des TP IA numérique : étalonner l'instrument, de l'atelier guidé au mini-projet*. Méthode pédagogique. Présentée au conseil de perfectionnement de l'Icam
Toulouse, 14-15 octobre 2026. https://doi.org/10.5281/zenodo.23390567

Article : Cheggour, S. (2026). *Teaching first-year engineering students to calibrate generative AI with indirect prompt injections hidden in course materials*. https://doi.org/10.5281/zenodo.23390567

Supports du TP (dépôt séparé) : https://doi.org/10.5281/zenodo.23390565

Les DOI ci-dessus désignent toutes les versions. Version 1.0 : méthodologie
10.5281/zenodo.23390568, supports 10.5281/zenodo.23390566. Version 1.1 : méthodologie
10.5281/zenodo.23390946, supports 10.5281/zenodo.23390945.

Un fichier [`CITATION.cff`](CITATION.cff) est fourni (bouton « Cite this repository » de GitHub).

## Contact

Selina Cheggour, selina.cheggour@icam.fr
