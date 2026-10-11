# Mametas : procédure de maintenance

Ce dépôt contient le site www.mametas.com tel qu'il est publié, et rien
d'autre que les outils pour le contrôler et le publier.

## La règle

**Le dossier `site/` est exactement le dossier web OVH.** Chaque fichier de
`site/` est publié tel quel ; aucun autre fichier ne l'est. Il n'existe plus
d'étape qui réécrit les pages avant publication : ce que l'on voit dans
`site/` est ce que voient les visiteurs.

## Organisation du dépôt

| Emplacement | Rôle |
| --- | --- |
| `site/` | Le site publié : pages HTML, CSS, JavaScript, images, sitemaps, `.htaccess` |
| `outils/controles.py` | Lance les contrôles bloquants |
| `outils/controles/` | Les trois contrôles : site général, affiliation Booking, hubs d'hôtels |
| `outils/publier_ovh.py` | Compare `site/` à la production, envoie les différences, vérifie |
| `.github/workflows/validation.yml` | Circuit de validation, sur chaque proposition de modification |
| `.github/workflows/publication.yml` | Circuit de publication, seul chemin vers OVH |
| `AGENTS.md` | Règles imposées à toute IA qui modifie le dépôt |

La branche de production est `mametas-v3`.

## Modifier le site

1. Créer une branche à partir de `mametas-v3`.
2. Modifier directement les fichiers concernés dans `site/` : le texte d'une
   page dans son `index.html`, un style dans la feuille CSS, une image en la
   remplaçant.
3. Ouvrir une proposition de modification (pull request) vers `mametas-v3`.
   Le circuit de validation lance les contrôles et indique, dans le résumé
   de l'exécution, la liste exacte des fichiers qui partiraient sur OVH.
4. Relire la liste. Si elle correspond à la modification voulue, fusionner.
5. La fusion déclenche le circuit de publication : contrôles, envoi des
   seuls fichiers différents, vérification de la production.

Une page modifiée en français a souvent son équivalent anglais sous `site/en/`.

## Ce que font les contrôles

- `site/` ne contient que des fichiers publiables (pas de script, d'archive
  ni de configuration).
- Chaque JavaScript est syntaxiquement valide.
- Chaque page a sa langue, un titre, un h1, une canonical unique vers
  www.mametas.com et le bandeau de consentement ; chaque lien, image ou
  script interne existe ; les blocs JSON-LD sont valides.
- `sitemap.xml` est un XML valide ; `robots.txt` le déclare.
- Chaque lien de réservation Booking passe par CJ (les citations de source
  en nofollow sont autorisées).
- Les 18 hubs d'hôtels FR/EN sont bien formés.
- Le moteur de Riviera Fit passe son autotest (648 profils).

Si un contrôle échoue, rien n'est envoyé sur OVH.

## Ce que fait la publication

1. Contrôles bloquants.
2. Comparaison de chaque fichier de `site/` avec ce que la production sert
   réellement (empreinte SHA-256, lue en HTTPS ou par SFTP).
3. Sauvegarde des versions qui vont être remplacées (archive GitHub
   `avant-publication-<commit>`, 90 jours).
4. Envoi des seuls fichiers différents ou absents, dans cet ordre : images,
   CSS et JavaScript, puis pages, puis sitemaps et robots, `.htaccess` en
   dernier.
5. Vérification : chaque fichier de `site/` doit être servi à l'identique.

Rien n'est jamais supprimé sur le serveur par la publication. Une seule
publication tourne à la fois ; une publication interrompue est simplement
complétée par la suivante.

## Revenir en arrière

- **Une modification publiée pose problème** : sur GitHub, ouvrir la
  proposition fusionnée et cliquer sur « Revert », puis fusionner la
  proposition de retour. La publication renvoie les anciennes versions.
- **Retrouver un fichier remplacé** : l'archive `avant-publication-<commit>`
  de l'exécution concernée contient la version d'avant.
- **Restaurer tout le serveur** : la sauvegarde complète du 11 octobre 2026
  est sur la branche `sauvegarde/ovh-2026-10-11` (archive de l'exécution
  « Sauvegarde OVH »). La décompresser et renvoyer le dossier `www/` par SFTP.
- **Revenir à l'ancienne architecture** : la branche
  `reference/avant-migration-2026-10-11` contient la version d'avant la
  migration, avec ses 159 étapes et ses workflows.

## Ce qu'il ne faut plus faire

- Ajouter un script qui modifie des pages au moment de la publication.
- Ajouter un workflow qui envoie des fichiers sur OVH.
- Télécharger des images depuis un site extérieur pendant la publication :
  une image se dépose directement dans `site/assets/`.
- Envoyer des fichiers sur OVH à la main : la production s'écarterait du
  dépôt (la vérification le signalerait).

## Accès et secrets

Les accès OVH sont des secrets GitHub (`OVH_FTP_SERVER`, `OVH_FTP_USERNAME`,
`OVH_FTP_PASSWORD`, `OVH_FTP_ROOT`). Ils ne figurent dans aucun fichier.
