# Règles pour toute IA travaillant sur ce dépôt (ChatGPT, Claude, autres)

Ces règles s'imposent à chaque modification. Les lire avant de commencer.

1. **Modifier les fichiers du site directement dans `site/`.** Le texte d'une
   page se change dans son `index.html`, un style dans sa feuille CSS. Ce qui
   est dans `site/` est publié tel quel.
2. **Ne jamais ajouter de script de transformation.** Aucun script qui
   réécrit, corrige, complète ou « normalise » des pages, ni au moment de la
   publication, ni dans un workflow. Une correction se fait une fois, dans
   les fichiers, puis le script éventuel est supprimé.
3. **Ne jamais ajouter ni modifier de workflow** sans accord explicite du
   propriétaire. Il en existe deux : `validation.yml` et `publication.yml`.
4. **Ne jamais télécharger de ressource extérieure pendant la publication.**
   Une image se dépose dans `site/assets/`.
5. **Toujours passer par une branche et une proposition de modification**
   (pull request) vers `mametas-v3`. Jamais d'envoi direct sur `mametas-v3`.
   Le propriétaire fusionne après avoir relu la liste des fichiers qui
   partiront sur OVH.
6. **Préserver** : URL publiques, redirections (`site/.htaccess`), balises
   canonical et hreflang, liens affiliés Booking via CJ, Riviera Fit et Hotel
   Fit, consentement, partage, suivi analytique.
7. **Garder les contrôles verts** : `python outils/controles.py` doit réussir
   avant toute proposition. Ne pas affaiblir un contrôle pour le faire passer.
8. **Ne rien mettre dans `site/` qui ne doive être public** : pas de notes,
   d'archives, de scripts ni de sauvegardes.
9. **Ne jamais toucher aux secrets OVH** ni aux réglages du dépôt.

Procédure complète : `MAINTENANCE.md`.
