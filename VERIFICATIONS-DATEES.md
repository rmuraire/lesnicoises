# Vérifications datées — contrôle mensuel

Liste suivie par le contrôle planifié du début de chaque mois. Chaque point
se vérifie sur une source officielle ou, à défaut, une presse locale datée.
Les pages concernées existent en français et en anglais : corriger les deux.

**Règle** : le contrôle ne publie jamais. Il ouvre une proposition de
modification (PR) vers `mametas-v3` avec les corrections sourcées, et le
propriétaire décide de la fusion. Une information non confirmée est signalée,
pas inventée ni supprimée d'office.

## Agenda

| Point | Pages | Ce qu'il faut vérifier |
|---|---|---|
| Page du mois en cours et du mois suivant | `bons-plans/<mois>-2026/`, `en/good-finds/<month>-2026/` | Dates d'événements, fermetures, travaux. Signaler si la page du mois suivant n'existe pas encore (ne pas la créer sans accord). |
| Hub agenda | `bons-plans/`, `en/good-finds/` | Liens vers des événements passés, ordre des cartes. |
| Grand Prix de Monaco 2027 | `bons-plans/grand-prix-monaco/` | Programme ACM, billetterie, E-Prix et Grand Prix Historique, tarifs du train. |
| Festival de Cannes 2027 | `bons-plans/festival-de-cannes/` | Dates officielles, Cinéma de la Plage, 3 jours à Cannes, Cannes Cinéphiles. |
| Carnaval de Nice, MIPIM, Ironman | `bons-plans/carnaval-nice/`, `bons-plans/mipim-cannes/`, `bons-plans/ironman-nice/` | Dates, programme, billetterie. |

## Transports

| Point | Pages | Ce qu'il faut vérifier |
|---|---|---|
| Fermetures de ligne SNCF annoncées | `bons-plans/train-ou-bus/`, page du mois | Nouvelles coupures, travaux, substitutions par car. |
| Tarifs enfants TER, ZOU! Mini-Groupe, Pass SudAzur Explore | `explore/cote-d-azur-en-famille/` | Tarifs et conditions. |
| Stationnement Monaco (tarif fin 2024) | `pratique/taxis-vtc-stationnement/`, `fr/planifier/voiture-ou-pas/` | Tarif en vigueur. |

## Lieux et horaires

| Point | Pages | Ce qu'il faut vérifier |
|---|---|---|
| Musée Bonnard (réaccrochage, réouverture 21 novembre) | `culture/musee-bonnard/`, page du mois | Dates. |
| Bastion Cocteau (fermé 14–24 novembre) | `culture/musee-cocteau-bastion/` | Dates. |
| Chapelle du Rosaire (ouverte jusqu'au 14 novembre) | `culture/chapelle-du-rosaire-matisse/` | Saison, horaires. |
| Musée Matisse (exposition Katz, 12 €) | `culture/musee-matisse/`, accueil, agenda | Dates, tarif. |
| Horaires d'hiver (Léger, Picasso, Ephrussi…) | `culture/*`, `pratique/fermetures-horaires/` | Horaires à partir du 1er novembre. |
| Sorties famille (Aquasplash 2027, surveillance des plages, bateaux de Lérins) | `explore/cote-d-azur-en-famille/` | Dates de saison et tarifs publiés. |

## Après chaque vérification

- Mettre à jour la date « Vérifié le … » des pages corrigées.
- `python outils/controles.py` doit rester vert.
- Résumer dans la PR : vérifié, corrigé, non confirmé (avec la source).
