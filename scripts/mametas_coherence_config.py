#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Single source of truth for Mametas coherence cleanup.

This file deliberately stores only cross-page system data: canonical destination
names, grouping, tags and Reality Check copy. Editorial body copy stays owned by
its individual page.
"""

DESTINATIONS = {
    "nice": {
        "name": {"en": "Nice", "fr": "Nice"},
        "paths": {"en": "en/riviera-guide/nice/index.html", "fr": "riviera-guide/nice/index.html"},
        "group": "base",
        "tag": {"en": "Best first base", "fr": "Meilleure première base"},
        "reality": {
            "en": (
                "No car needed for a first trip",
                "€€ to €€€€",
                "Strong year-round",
                "Low",
            ),
            "fr": (
                "Voiture inutile pour un premier séjour",
                "€€ à €€€€",
                "Très solide toute l’année",
                "Faible",
            ),
        },
    },
    "villefranche-cap-ferrat": {
        "name": {"en": "Villefranche & Cap-Ferrat", "fr": "Villefranche & Cap-Ferrat"},
        "paths": {"en": "en/riviera-guide/villefranche-cap-ferrat/index.html", "fr": "riviera-guide/villefranche-cap-ferrat/index.html"},
        "group": "base",
        "tag": {"en": "Best for beauty", "fr": "Pour la beauté"},
        "reality": {
            "en": (
                "Car-free works, less seamlessly than Nice",
                "€€ to €€€€",
                "Spring and autumn are particularly easy",
                "Medium: hills and transfers",
            ),
            "fr": (
                "Possible sans voiture, moins fluide que Nice",
                "€€ à €€€€",
                "Printemps et automne sont particulièrement agréables",
                "Moyenne : relief et correspondances",
            ),
        },
    },
    "antibes": {
        "name": {"en": "Antibes", "fr": "Antibes"},
        "paths": {"en": "en/riviera-guide/antibes/index.html", "fr": "riviera-guide/antibes/index.html"},
        "group": "base",
        "tag": {"en": "Best balance", "fr": "Meilleur équilibre"},
        "reality": {
            "en": (
                "Yes without a car in town. The Cap asks for more.",
                "€€ to €€€€",
                "May to September for beach time",
                "Low in town, medium on the Cap",
            ),
            "fr": (
                "Oui sans voiture en ville. Le Cap demande plus.",
                "€€ à €€€€",
                "Mai à septembre pour la plage",
                "Faible en ville, moyenne sur le Cap",
            ),
        },
    },
    "cannes": {
        "name": {"en": "Cannes", "fr": "Cannes"},
        "paths": {"en": "en/riviera-guide/cannes/index.html", "fr": "riviera-guide/cannes/index.html"},
        "group": "base",
        "tag": {"en": "Best for polish", "fr": "Pour le vernis"},
        "reality": {
            "en": (
                "Very easy without a car",
                "€€ to €€€€",
                "Spring to early autumn",
                "Low, except during major events",
            ),
            "fr": (
                "Très simple sans voiture",
                "€€ à €€€€",
                "Printemps à début automne",
                "Faible, sauf grands événements",
            ),
        },
    },
    "monaco": {
        "name": {"en": "Monaco", "fr": "Monaco"},
        "paths": {"en": "en/riviera-guide/monaco/index.html", "fr": "riviera-guide/monaco/index.html"},
        "group": "base",
        "tag": {"en": "Best for spectacle", "fr": "Pour le spectacle"},
        "reality": {
            "en": (
                "No car recommended",
                "€€€ to €€€€",
                "Year-round, with event-driven spikes",
                "Medium: hills and spend",
            ),
            "fr": (
                "Sans voiture recommandé",
                "€€€ à €€€€",
                "Toute l’année, avec pics lors des grands événements",
                "Moyenne : relief et budget",
            ),
        },
    },
    "menton": {
        "name": {"en": "Menton", "fr": "Menton"},
        "paths": {"en": "en/riviera-guide/menton/index.html", "fr": "riviera-guide/menton/index.html"},
        "group": "base",
        "tag": {"en": "Best for a slower east", "fr": "Pour l’est plus calme"},
        "reality": {
            "en": (
                "Very good without a car",
                "€ to €€€",
                "Particularly good outside peak summer",
                "Low to medium: you are far east",
            ),
            "fr": (
                "Très bon sans voiture",
                "€ à €€€",
                "Très agréable hors plein été",
                "Faible à moyenne : vous êtes très à l’est",
            ),
        },
    },
    "eze": {
        "name": {"en": "Èze", "fr": "Èze"},
        "paths": {"en": "en/riviera-guide/eze/index.html", "fr": "riviera-guide/eze/index.html"},
        "group": "detour",
        "tag": {"en": "Best for the panorama", "fr": "Pour le panorama"},
        "reality": {
            "en": (
                "No car needed. Bus reaches the village; the train stops at Èze-sur-Mer.",
                "€ to €€€€ depending on whether you stay overnight",
                "Year-round; go early or late in peak season",
                "High: village and station are not in the same place",
            ),
            "fr": (
                "Pas besoin de voiture. Le bus monte au village ; le train s’arrête à Èze-sur-Mer.",
                "€ à €€€€ selon que vous y dormez ou non",
                "Toute l’année ; tôt ou tard en haute saison",
                "Élevée : le village et la gare ne sont pas au même endroit",
            ),
        },
    },
    "saint-paul-de-vence": {
        "name": {"en": "Saint-Paul-de-Vence", "fr": "Saint-Paul-de-Vence"},
        "paths": {"en": "en/riviera-guide/saint-paul-de-vence/index.html", "fr": "riviera-guide/saint-paul-de-vence/index.html"},
        "group": "detour",
        "tag": {"en": "Best for art inland", "fr": "Pour l’art dans les terres"},
        "reality": {
            "en": (
                "A car is very useful. Bus is possible.",
                "€€ to €€€€",
                "Spring and autumn are the easiest",
                "Medium to high: inland stop",
            ),
            "fr": (
                "Voiture très utile. Bus possible.",
                "€€ à €€€€",
                "Printemps et automne sont les plus souples",
                "Moyenne à élevée : détour dans les terres",
            ),
        },
    },
    "saint-tropez": {
        "name": {"en": "Saint-Tropez", "fr": "Saint-Tropez"},
        "paths": {"en": "en/riviera-guide/saint-tropez/index.html", "fr": "riviera-guide/saint-tropez/index.html"},
        "group": "detour",
        "tag": {"en": "Only if you really want it", "fr": "Quand vous le voulez vraiment"},
        "reality": {
            "en": (
                "Car, boat or transfers need planning",
                "€€€ to €€€€",
                "May to September, with heavy summer pressure",
                "High",
            ),
            "fr": (
                "Voiture, bateau ou transferts à organiser",
                "€€€ à €€€€",
                "Mai à septembre, avec forte pression en été",
                "Élevée",
            ),
        },
    },
}

REALITY_LABELS = {
    "en": ("Getting around", "Budget", "Season", "Logistics"),
    "fr": ("Déplacements", "Budget", "Saison", "Logistique"),
}

DESTINATION_BACK = {
    "en": ('/en/riviera-guide/', '← Back to Places'),
    "fr": ('/riviera-guide/', '← Retour aux destinations'),
}

RIVIERA_FIT = {
    "en": ('/en/riviera-fit/', 'Run my profile through Riviera Fit →'),
    "fr": ('/riviera-fit/', 'Tester mon profil dans Riviera Fit →'),
}
