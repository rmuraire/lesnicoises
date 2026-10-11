# Mise à l'écart des anciens fichiers du serveur OVH

Branche ponctuelle. Les 292 fichiers présents sur le serveur mais absents du
site (relevés par la sauvegarde du 11 octobre 2026) sont listés dans
`a-ecarter.tsv`, avec leur empreinte.

- `MODE` = `apercu` : liste ce qui serait déplacé, ne modifie rien.
- `MODE` = `deplacer` : déplace chaque fichier inchangé depuis la sauvegarde
  vers `~/mametas-hors-ligne/2026-10-11/`, hors du dossier web. Rien n'est
  supprimé ; un fichier modifié depuis la sauvegarde est laissé en place.

Pour revenir en arrière : redéplacer le contenu de
`~/mametas-hors-ligne/2026-10-11/` dans le dossier web.
