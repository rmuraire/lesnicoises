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

## PRIORITÉ — prochaine mise à jour du finder

**Ajouter la notion de prix / budget au finder est la priorité du prochain lot. Ne pas la perdre dans les optimisations secondaires.** Les données `priceBand` sont déjà présentes et doivent servir de base. L'interface et les libellés exacts (bandes relatives et/ou repères en euros) seront décidés dans ce lot ; ne pas inventer de tarif live.

### Sortie attendue

- Si l'utilisateur choisit uniquement une ville : afficher toutes les adresses Mametas disponibles pour cette ville.
- Dès qu'un critère supplémentaire est choisi : revenir à une shortlist de 3 à 5 recommandations maximum.
- Pour chaque résultat : **Best for**, **The catch**, logique de quartier, niveau de gamme relatif et CTA principal.
- Le CTA mène vers la fiche Mametas ou directement vers le partenaire de réservation quand la fiche n'ajoute pas de décision supplémentaire.
- Ne jamais classer uniquement par commission ou par prix supposé.

## Règles de données

- `data/hotels/nice.json` est la source canonique du moteur Nice.
- Les nouveaux hôtels doivent être ajoutés à cette source avant d'être proposés par le moteur.
- `priceBand` est qualitatif et relatif au marché niçois ; aucune valeur en euros ne doit être déduite de ce champ sans décision éditoriale explicite.
- `stationFriendly`, `seaAccess`, `oldTownAccess`, `quiet` décrivent la logique de localisation, pas une garantie de chambre ou de service.
- Les liens partenaires sont conservés tels qu'ils ont été fournis et doivent être contrôlés avant toute modification.

## Affiliation hôtels

- Booking.com via CJ est désormais le canal principal quand un lien Booking validé a été fourni.
- Les liens Expedia existants peuvent rester en secours pour les hôtels sans lien Booking validé.
- Sur une carte : un seul CTA principal `Check rates` / `Voir les tarifs`.
- Sur une fiche détaillée : le partenaire transactionnel peut rester le CTA principal sans transformer Mametas en comparateur.
- Un hôtel sans lien affilié valide ne doit jamais disparaître d'une recommandation éditoriale : le CTA revient alors vers la fiche Mametas.

## Mesure

Les liens partenaires doivent porter `data-affiliate-network` et `data-affiliate-hotel` lorsque le composant les rend. `assets/v3.js` envoie un événement `affiliate_click` à Google Analytics lorsqu'il est disponible. Dimensions à suivre : hôtel, partenaire, langue et page source.

## Hors périmètre du lot de consolidation

La consolidation du 15 septembre prépare les données et ferme le sourcing ; elle ne doit pas déclencher une refonte visuelle ou une migration d'URL. Le prochain changement fonctionnel prioritaire est le filtre prix / budget du finder.
