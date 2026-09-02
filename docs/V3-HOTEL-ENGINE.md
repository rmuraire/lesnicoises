# Mametas V3 — moteur hôtel et affiliation

## Décision produit

Mametas ne commence pas par une liste d'hôtels. Le visiteur choisit d'abord le type de séjour qu'il veut : **pratique**, **animé**, **paisible** ou **chic face à la mer**. Chaque hôtel peut répondre à plusieurs intentions.

La source de référence de Nice est `data/hotels/nice.json`. Les pages restent rendues en HTML statique pour le référencement ; le fichier de données sert à garder les catégories, les compromis et les liens partenaires cohérents lors de chaque mise à jour.

## Inventaire de Nice au 2 septembre 2026

| Intention | Couverture actuelle | Diagnostic |
|---|---:|---|
| Pratique | 3 | Une seule option hors très haut de gamme |
| Animé | 4 | Bonne couverture centrale, mais chère |
| Paisible | 2 | Deux bonnes options, toutes deux chères |
| Chic / mer | 6 | Couverture déjà abondante |

Objectif avant montée en puissance : **12 à 14 hôtels à Nice**, sans ajouter un sixième palace interchangeable.

## Prochaines fiches à produire

1. Deux hôtels centraux milieu de gamme, faciles sans voiture.
2. Deux adresses paisibles, dont au moins une hors luxe.
3. Un hôtel proche de Nice-Ville réellement adapté aux excursions en train.
4. Une petite adresse de caractère à budget plus contenu.

Chaque nouvelle fiche doit comporter : quartier, gamme de prix qualitative, usages, durées adaptées, voiture ou non, `Best for`, verdict, compromis réel, date de vérification, source officielle et liens partenaires disponibles.

## Expedia

- Renommer immédiatement le profil professionnel **Mametas**.
- Conserver `lesnicoises.com` et l'Instagram actuel dans le profil jusqu'à la bascule publique.
- Ne pas régénérer les liens existants : les conserver et tester les destinations.
- Contrôle prioritaire : le lien Apollinaire contient encore l'ancien nom Ellington dans son URL et doit être testé manuellement.
- À la bascule : remplacer le site par `https://mametas.com/`, puis les liens sociaux lors de leur renommage.

## Booking.com

- La candidature n'est pas un prérequis à la V3.
- Déposer la candidature Mametas via le réseau officiel CJ lorsque `mametas.com` est public et que le parcours hôtel est cohérent.
- Après validation, renseigner les URL Booking dans la même source de données.
- Sur une carte, conserver un seul bouton principal `Check rates`; sur la fiche détaillée, proposer Expedia et Booking sans transformer la page en comparateur.

## Mesure

Les liens partenaires portent `data-affiliate-network` et `data-affiliate-hotel`. `assets/v3.js` envoie un événement `affiliate_click` à Google Analytics lorsqu'il est disponible. Les dimensions à suivre sont : hôtel, partenaire, langue et page source.
