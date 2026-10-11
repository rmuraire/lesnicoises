# Sauvegarde OVH du 11 octobre 2026

Branche ponctuelle, sans lien avec le site publié. Son seul envoi déclenche
le workflow « Sauvegarde OVH (lecture seule) », qui :

1. copie par SFTP, en lecture seule, l'intégralité du dossier web OVH ;
2. conserve cette copie en archive GitHub Actions pendant 90 jours
   (`sauvegarde-ovh-2026-10-11`, téléchargeable depuis la page de
   l'exécution) ;
3. vérifie dans un second temps que l'archive se restaure à l'identique ;
4. verse dans cette branche l'inventaire des fichiers du serveur
   (`inventaire.tsv`) et les 23 images que l'ancienne chaîne
   retéléchargeait à chaque déploiement (`figees/`).

Aucune écriture, suppression ni modification n'est faite sur le serveur.

Restaurer : télécharger l'archive, la décompresser, renvoyer le dossier
`www/` par SFTP à la racine du site.
