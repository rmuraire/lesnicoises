# Mametas V3 — architecture de référence

## Rôle du produit

Mametas n'est pas un magazine généraliste supplémentaire sur la Côte d'Azur. C'est un guide de décision pour un premier séjour de 3 à 7 jours : où se baser, quoi réserver, comment circuler et quels compromis accepter.

Promesse fonctionnelle : **Where to stay, what to book, how to move — and what isn't worth your time.**

Signature de marque : **They know the Riviera.**

## Public prioritaire

- Voyageur international préparant son premier séjour sur la Riviera.
- Séjour de 3 à 7 jours.
- Budget confortable, sans présupposer l'ultraluxe.
- Besoin principal : réduire l'incertitude et le nombre d'onglets ouverts.

## Architecture visible

| Navigation | Travail rendu au visiteur | Contenus piliers |
|---|---|---|
| Plan | Organiser le séjour dans le bon ordre | 3/5/7 jours, choix de base, sans voiture, réservations |
| Places | Comprendre le caractère et la logistique de chaque lieu | Nice, Villefranche/Cap-Ferrat, Monaco/Menton, Antibes/Cannes, Saint-Paul, Saint-Tropez |
| Stay | Choisir un hôtel pour un usage, pas seulement pour sa photo | Hubs par base, sélections, fiches avec verdict et compromis |
| Eat & Do | Remplir intelligemment les journées | Restaurants, plages, culture et expériences reliés aux destinations |
| Now | Éviter les mauvaises surprises saisonnières | Événements, fermetures, réservations et conditions du moment |

## Langues et URL

- Anglais prioritaire à la racine : `/`, `/plan/`, `/places/`, `/stay/`.
- Français sous `/fr/`, avec contenus éditoriaux équivalents et non une traduction automatique pauvre.
- Pendant la préproduction : `noindex,nofollow` sur les pages V3.
- Au lancement : retrait du `noindex`, canonicals sur `mametas.com`, `hreflang` réciproques et redirections 301 page par page depuis `lesnicoises.com`.

## Ordre de construction

1. Accueil anglais et français.
2. Parcours étalon « Five days on the Riviera, based in Nice, without a car ».
3. Hubs Plan, Places et Stay.
4. Six destinations profondes avant d'élargir la couverture.
5. Quinze hôtels rééditorialisés avec `Best for`, `Mametas verdict`, `Why we picked it`, `The catch`, logistique et date de vérification.
6. Migration du contenu existant utile, puis redirections.

## Règles éditoriales

- Un choix doit expliciter son bénéfice et son coût réel.
- Les personnages Mametas sont fictifs ; les informations sont documentées et vérifiables.
- Les contenus pratiques importants affichent leur date de vérification et renvoient vers une source officielle.
- Une carte d'hôtel ne présente qu'un seul appel à l'action : `Check rates`.
- Les liens affiliés sont clairement signalés et ne modifient pas le verdict.
- La V3 privilégie les parcours à forte utilité plutôt que le volume de publications.

## Déploiement prévu

- Production actuelle maintenue sur `lesnicoises.com`.
- Développement isolé sur la branche `mametas-v3`.
- Préproduction privée sur `v3.mametas.com`, dossier OVH dédié, SSL et protection par mot de passe.
- Bascule publique uniquement après réception du rapport INPI, décision de dépôt et validation de la migration.
