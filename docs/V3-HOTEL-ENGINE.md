# Mametas V3 — moteur hôtel et affiliation

## Décision produit

Mametas ne commence pas par une liste d'hôtels. Le visiteur choisit d'abord ce que l'hôtel doit faire pour son séjour, puis le niveau de dépense qu'il accepte. Le moteur doit réduire vingt hôtels à une courte sélection argumentée, jamais afficher un catalogue brut.

La source de référence de Nice est `data/hotels/nice.json`. Les pages restent rendues en HTML statique pour le référencement ; le fichier de données sert au moteur, aux catégories, aux compromis et aux liens partenaires.

## Inventaire de Nice au 15 septembre 2026

**20 hôtels publiés et structurés.** Le trou milieu / milieu-haut de gamme est considéré comme fermé pour la V1.

| Intention | Couverture | Rôle dans le moteur |
|---|---:|---|
| Pratique / excursions | 7 | Prioriser gare, marche et séjour sans voiture |
| Paisible | 3 | Prioriser calme relatif et centralité |
| Animé | 4 | Prioriser restaurants, centre et Vieux-Nice |
| Chic / expérience | 9, avec recoupements | Prioriser mer, caractère et hôtel comme partie du voyage |

Les catégories se recoupent volontairement : un hôtel peut répondre à plusieurs intentions.

## Critères V1 du moteur

Le moteur du prochain lot doit s'appuyer sur les champs structurés, dans cet ordre :

1. **Usage principal** : practical / active / quiet / chic.
2. **Sans voiture** : filtre fort pour un premier séjour.
3. **Gare** : utile pour les voyageurs qui rayonnent en TER.
4. **Mer / Vieux-Nice** : préférence de géographie, pas promesse de vue depuis la chambre.
5. **Calme relatif** : aide à départager les options centrales.
6. **Niveau de gamme** : `mid`, `upper-mid`, `high`, `very-high`. Positionnement relatif à Nice, jamais tarif live.
7. **Durée** : 3 / 5 / 7 jours quand elle aide réellement le classement.

### Sortie attendue

- 3 à 5 recommandations maximum.
- Pour chaque résultat : **Best for**, **The catch**, logique de quartier, niveau de gamme relatif et CTA principal.
- Le CTA mène vers la fiche Mametas ou directement vers Expedia quand la fiche n'ajoute pas de décision supplémentaire.
- Ne jamais classer uniquement par commission ou par prix supposé.

## Règles de données

- `data/hotels/nice.json` est la source canonique du moteur Nice.
- Les nouveaux hôtels doivent être ajoutés à cette source avant d'être proposés par le moteur.
- `priceBand` est qualitatif et relatif au marché niçois ; aucune valeur en euros ne doit être déduite de ce champ.
- `stationFriendly`, `seaAccess`, `oldTownAccess`, `quiet` décrivent la logique de localisation, pas une garantie de chambre ou de service.
- Les liens Expedia sont conservés tels qu'ils ont été fournis et doivent être contrôlés avant toute modification.

## Expedia

- Conserver les liens existants ; ne pas les régénérer sans nécessité.
- Le lien Apollinaire contient encore l'ancien nom Ellington dans son URL : statut `active-needs-link-check`, à contrôler sans le remplacer arbitrairement.
- Sur une carte : un seul CTA principal `Check rates` / `Voir les tarifs`.
- Sur une fiche détaillée : Expedia peut rester le CTA transactionnel principal sans transformer Mametas en comparateur.

## Mesure

Les liens partenaires doivent porter `data-affiliate-network` et `data-affiliate-hotel` lorsque le composant les rend. `assets/v3.js` envoie un événement `affiliate_click` à Google Analytics lorsqu'il est disponible. Dimensions à suivre : hôtel, partenaire, langue et page source.

## Hors périmètre du lot de consolidation

La logique interactive / scoring du moteur est le lot suivant. La consolidation du 15 septembre prépare les données et ferme le sourcing ; elle ne doit pas déclencher une refonte visuelle ou une migration d'URL.
