#!/usr/bin/env python3
from __future__ import annotations

import html
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPRITE = ROOT / "assets" / "hotels" / "batch-sprite-2026-09-13.jpg"
BATCH = "2026-09-13"
SPRITE_COLS = 5
SPRITE_ROWS = 9

BASES = {
    "nice": {
        "fr": "fr/dormir/nice/index.html",
        "en": "stay/nice/index.html",
        "count": 20,
        "fr_old": "Dix hôtels, quatre styles de séjour.",
        "fr_new": "Vingt hôtels, quatre styles de séjour.",
        "en_old": "Ten hotels, four trip styles.",
        "en_new": "Twenty hotels, four trip styles.",
    },
    "antibes": {
        "fr": "hotels/antibes/index.html",
        "en": "en/hotels/antibes/index.html",
        "count": 11,
        "fr_old": "Six adresses, trois logiques.",
        "fr_new": "Onze adresses, trois logiques.",
        "en_old": "Six addresses, three moods.",
        "en_new": "Eleven addresses, three moods.",
    },
    "cannes": {
        "fr": "hotels/cannes/index.html",
        "en": "en/hotels/cannes/index.html",
        "count": 15,
        "fr_old": "Sept hôtels, trois façons de faire Cannes.",
        "fr_new": "Quinze hôtels, trois façons de faire Cannes.",
        "en_old": "Seven hotels, three ways to do Cannes.",
        "en_new": "Fifteen hotels, three ways to do Cannes.",
    },
    "villefranche": {
        "fr": "hotels/villefranche-sur-mer/index.html",
        "en": "en/hotels/villefranche-sur-mer/index.html",
        "count": 6,
    },
    "monaco": {
        "fr": "hotels/monaco/index.html",
        "en": "en/hotels/monaco/index.html",
        "count": 7,
        "fr_old": "Trois hôtels, deux logiques : palace classique ou resort.",
        "fr_new": "Sept hôtels, deux logiques : grand luxe central ou séjour plus détendu.",
        "en_old": "Three hotels, two logics: classic palace or resort.",
        "en_new": "Seven hotels, two logics: central grand luxury or a more relaxed stay.",
    },
    "menton": {
        "fr": "hotels/menton/index.html",
        "en": "en/hotels/menton/index.html",
        "count": 9,
        "fr_old": "Cinq choix pour ralentir à l’est :",
        "fr_new": "Neuf choix pour ralentir à l’est :",
        "en_old": "Five choices for slowing down in the east:",
        "en_new": "Nine choices for slowing down in the east:",
    },
    "saint-paul": {
        "fr": "hotels/saint-paul-de-vence/index.html",
        "en": "en/hotels/saint-paul-de-vence/index.html",
        "count": 8,
        "fr_old": "Six adresses pour transformer la visite de Saint-Paul en séjour :",
        "fr_new": "Huit adresses pour transformer la visite de Saint-Paul en séjour :",
        "en_old": "Six addresses that turn a visit to Saint-Paul into a stay:",
        "en_new": "Eight addresses that turn a visit to Saint-Paul into a stay:",
    },
    "beaulieu": {
        "fr": "hotels/beaulieu-sur-mer/index.html",
        "en": "en/hotels/beaulieu-sur-mer/index.html",
        "count": 6,
        "fr_old": "Trois hôtels pour profiter d’une base plus calme",
        "fr_new": "Six hôtels pour profiter d’une base plus calme",
        "en_old": "Three hotels for a calmer base",
        "en_new": "Six hotels for a calmer base",
    },
    "mougins": {
        "fr": "hotels/mougins/index.html",
        "en": "en/hotels/mougins/index.html",
        "count": 6,
        "fr_old": "Deux choix, deux niveaux d’intensité :",
        "fr_new": "Six choix, deux niveaux d’intensité :",
        "en_old": "Two choices, two levels of intensity:",
        "en_new": "Six choices, two levels of intensity:",
    },
    "saint-tropez": {
        "fr": "hotels/saint-tropez/index.html",
        "en": "en/hotels/saint-tropez/index.html",
        "count": 12,
        "fr_old": "Sept adresses, quatre géographies.",
        "fr_new": "Douze adresses, quatre géographies.",
        "en_old": "Seven addresses, four geographies.",
        "en_new": "Twelve addresses, four geographies.",
    },
}

HOTELS = [
    dict(slug="boscolo-nice-hotel-and-spa", display="Boscolo Nice Hôtel & Spa", url="https://expedia.com/affiliates/nice-hotels-boscolo-nice-hotel-spa.5HA4gsr", base="nice", fr_section="chic", en_section="chic", fr_tag="Luxe central & spa", en_tag="Central luxury & spa", fr_copy="Pour ceux qui veulent un cinq-étoiles central avec spa, sans faire de la Promenade l’unique sujet.", en_copy="For travellers who want central five-star comfort and a spa without making the Promenade the whole point."),
    dict(slug="hotel-64-nice", display="Hotel 64 Nice", url="https://expedia.com/affiliates/nice-hotels-hotel-64-nice.3ReHLsP", base="nice", fr_section="pratique", en_section="practical", fr_tag="Gare & pratique", en_tag="Station & practical", fr_copy="À deux pas de la gare : efficace pour rayonner en train sans sacrifier le centre.", en_copy="Close to the station: efficient for Riviera day trips without giving up central Nice."),
    dict(slug="hotel-amour-nice", display="Hotel Amour Nice", url="https://expedia.com/affiliates/nice-hotels-hotel-amour-nice.gMdQDW6", base="nice", fr_section="vivant", en_section="active", fr_tag="Vivant & stylé", en_tag="Lively & stylish", fr_copy="Le choix plus bohème quand les restaurants, les bars et une ambiance locale comptent autant que la chambre.", en_copy="The more bohemian pick when restaurants, bars and local atmosphere matter as much as the room."),
    dict(slug="hotel-beau-rivage", display="Hotel Beau Rivage", url="https://expedia.com/affiliates/nice-hotels-hotel-beau-rivage.auf2tdP", base="nice", fr_section="chic", en_section="chic", fr_tag="Mer & Vieux-Nice", en_tag="Sea & Old Nice", fr_copy="Entre Vieux-Nice et plage : la géographie fait une bonne partie du travail.", en_copy="Between Old Nice and the beach: the geography does a large part of the work."),
    dict(slug="hotel-byakko-nice", display="Hotel Byakko Nice", url="https://expedia.com/affiliates/nice-hotels-hotel-byakko-nice.Q5vULLq", base="nice", fr_section="pratique", en_section="practical", fr_tag="Gare & budget", en_tag="Station & value", fr_copy="Une base centrale et rationnelle pour ceux qui comptent davantage leurs trajets que les mètres carrés du lobby.", en_copy="A central, rational base for travellers counting journeys more carefully than lobby square metres."),
    dict(slug="hotel-florence-nice", display="Hotel Florence Nice", url="https://expedia.com/affiliates/nice-hotels-hotel-florence-nice.Hg6DWZD", base="nice", fr_section="pratique", en_section="practical", fr_tag="Centre & sans voiture", en_tag="Central & car-free", fr_copy="Très central pour un séjour à pied, avec la gare assez proche quand la Riviera vous appelle.", en_copy="Very central for a walking trip, with the station close enough when the Riviera calls."),
    dict(slug="hotel-west-end-nice-promenade", display="Hotel West End Nice Promenade", url="https://expedia.com/affiliates/nice-hotels-hotel-west-end-nice-promenade.vz6kpFQ", base="nice", fr_section="chic", en_section="chic", fr_tag="Promenade classique", en_tag="Classic Promenade", fr_copy="La Promenade en version classique, avec la mer devant et Nice derrière.", en_copy="A classic Promenade stay, with the sea in front and the city behind."),
    dict(slug="hotel-aston-la-scala", display="Hôtel Aston La Scala", url="https://expedia.com/affiliates/nice-hotels-hotel-aston-la-scala.6To0SKl", base="nice", fr_section="vivant", en_section="active", fr_tag="Masséna & vieille ville", en_tag="Masséna & Old Nice", fr_copy="Pour être au cœur de Nice, entre Masséna, coulée verte et Vieux-Nice.", en_copy="For being right in the middle of Nice, between Masséna, the green corridor and Old Nice."),
    dict(slug="hotel-khla-nice", display="Hôtel KHLA Nice", url="https://expedia.com/affiliates/nice-hotels-hotel-azurea.uoQzRgI", base="nice", fr_section="pratique", en_section="practical", fr_tag="Gare & simple", en_tag="Station & straightforward", fr_copy="Un choix simple près de la gare quand l’hôtel doit surtout faciliter le voyage.", en_copy="A straightforward station-side choice when the hotel mainly needs to make the trip easier."),
    dict(slug="hotel-le-grimaldi-by-happyculture", display="Hôtel Le Grimaldi by Happyculture", url="https://expedia.com/affiliates/nice-hotels-hotel-le-grimaldi-by-happyculture.WqyWIqH", base="nice", fr_section="calme", en_section="quiet", fr_tag="Central & plus posé", en_tag="Central & calmer", fr_copy="Une adresse centrale plus feutrée pour rester proche de tout sans dormir au milieu de tout.", en_copy="A calmer central address for staying close to everything without sleeping in the middle of everything."),

    dict(slug="ac-hotel-by-marriott-ambassadeur-antibes", display="AC Hotel by Marriott Ambassadeur Antibes", url="https://expedia.com/affiliates/cannes-hotels-ac-hotel-by-marriott-ambassadeur-antibes-juan-les-pins.0eATDLO", base="antibes", fr_section="riviera-bord-de-mer", en_section="riviera-seafront", fr_tag="Juan-les-Pins & services", en_tag="Juan-les-Pins & full-service", fr_copy="Pour Juan-les-Pins en version plus complète, avec piscine et services plutôt qu’une petite adresse.", en_copy="Juan-les-Pins in a fuller-service format, with pool and facilities rather than a small hotel."),
    dict(slug="hotel-josse", display="Hotel Josse", url="https://expedia.com/affiliates/cannes-hotels-hotel-josse.ADT4Ozw", base="antibes", fr_section="riviera-bord-de-mer", en_section="riviera-seafront", fr_tag="Salis & mer", en_tag="Salis & sea", fr_copy="Face à la mer côté Salis : une géographie plus balnéaire sans quitter Antibes.", en_copy="Facing the sea by Salis: a more beach-led geography without leaving Antibes."),
    dict(slug="hotel-mademoiselle", display="Hotel Mademoiselle", url="https://expedia.com/affiliates/cannes-hotels-hotel-mademoiselle.Yblmm7m", base="antibes", fr_section="vivant-facile", en_section="lively-easy", fr_tag="Juan-les-Pins central", en_tag="Central Juan-les-Pins", fr_copy="Au cœur de Juan-les-Pins pour sortir à pied et rentrer sans négocier avec la voiture.", en_copy="Right in Juan-les-Pins for evenings on foot and no late-night negotiation with the car."),
    dict(slug="hotel-le-pre-catelan", display="Hôtel Le Pré Catelan", url="https://expedia.com/affiliates/cannes-hotels-hotel-le-pre-catelan.amgwyHB", base="antibes", fr_section="vivant-facile", en_section="lively-easy", fr_tag="Jardin & Juan-les-Pins", en_tag="Garden & Juan-les-Pins", fr_copy="Une option plus douce à Juan-les-Pins, avec jardin et un peu de retrait.", en_copy="A gentler Juan-les-Pins option, with a garden and a little breathing room."),
    dict(slug="royal-antibes", display="Royal Antibes", url="https://expedia.com/affiliates/antibes-hotels-royal-antibes.MQf2YvF", base="antibes", fr_section="riviera-bord-de-mer", en_section="riviera-seafront", fr_tag="Antibes & front de mer", en_tag="Antibes & seafront", fr_copy="Pour mettre la mer dans le séjour sans renoncer à Antibes à pied.", en_copy="Put the sea into the stay without giving up walkable Antibes."),

    dict(slug="canopy-by-hilton-cannes", display="Canopy by Hilton Cannes", url="https://www.kqzyfj.com/click-101875476-15734754?url=https%3A%2F%2Fwww.booking.com%2FShare-q0isro", base="cannes", fr_section="luxe-central", en_section="central-luxury", fr_tag="Suquet & rooftop", en_tag="Suquet & rooftop", fr_copy="Un luxe contemporain côté Suquet, avec rooftop et moins de révérence pour la Croisette.", en_copy="Contemporary luxury by Le Suquet, with a rooftop and less reverence for Croisette ceremony."),
    dict(slug="hotel-barriere-le-gray-d-albion", display="Hôtel Barrière Le Gray d’Albion", url="https://www.kqzyfj.com/click-101875476-15734754?url=https%3A%2F%2Fwww.booking.com%2FShare-jIlHVPl", base="cannes", fr_section="luxe-central", en_section="central-luxury", fr_tag="Centre & plage", en_tag="Central & beach", fr_copy="Très central, très cannois, sans monter jusqu’au cérémonial des trois grands palaces.", en_copy="Very central and very Cannes, without going all the way into grand-palace ceremony."),
    dict(slug="jw-marriott-cannes", display="JW Marriott Cannes", url="https://expedia.com/affiliates/cannes-hotels-jw-marriott-cannes.y2ds8u3", base="cannes", fr_section="palaces-grand-spectacle", en_section="palaces-spectacle", fr_tag="Croisette & grand format", en_tag="Croisette & grand scale", fr_copy="La Croisette en grand format, pour ceux qui veulent être dans le spectacle plutôt qu’à côté.", en_copy="The Croisette at full scale, for travellers who want to be inside the spectacle rather than beside it."),
    dict(slug="mondrian-cannes", display="Mondrian Cannes", url="https://www.kqzyfj.com/click-101875476-15734754?url=https%3A%2F%2Fwww.booking.com%2FShare-Zlclqh", base="cannes", fr_section="luxe-central", en_section="central-luxury", fr_tag="Croisette contemporaine", en_tag="Contemporary Croisette", fr_copy="Une lecture plus contemporaine de la Croisette, avec la plage et le centre déjà dans l’équation.", en_copy="A more contemporary take on the Croisette, with beach and centre already built into the stay."),
    dict(slug="okko-hotels-cannes-centre-hotel-and-spa-belle-plage", display="OKKO Hotels Cannes Centre", url="https://expedia.com/affiliates/cannes-hotels-okko-hotels-cannes-centre.ol7POdv", base="cannes", fr_section="charme-plus-intime", en_section="character-more-intimate", fr_tag="Gare & ultra-pratique", en_tag="Station & ultra-practical", fr_copy="Le choix rationnel près de la gare quand Cannes sert aussi de base et pas seulement de scène.", en_copy="The rational station-side choice when Cannes is also a base, not only a stage."),
    dict(slug="hotel-and-spa-belle-plage", display="Hôtel & Spa Belle Plage", url="https://expedia.com/affiliates/cannes-hotels-residence-belle-plage.4sSSm0b", base="cannes", fr_section="luxe-central", en_section="central-luxury", fr_tag="Design & mer", en_tag="Design & sea", fr_copy="Une adresse design côté Suquet et mer, plus douce que la grammaire palace de la Croisette.", en_copy="A design-led Suquet-and-sea address, softer than the palace grammar of the Croisette."),
    dict(slug="hotel-splendid-cannes", display="Hôtel Splendid Cannes", url="https://www.kqzyfj.com/click-101875476-15734754?url=https%3A%2F%2Fwww.booking.com%2FShare-PcEg66K", base="cannes", fr_section="charme-plus-intime", en_section="character-more-intimate", fr_tag="Vieux Port & classique", en_tag="Old Port & classic", fr_copy="Face au Vieux Port, une adresse classique pour garder Cannes à pied sans passer par la grammaire palace.", en_copy="Facing the Old Port, a classic address for keeping Cannes walkable without buying into full palace ceremony.", image="/assets/hotels/v3/hotel-splendid-cannes/hero.jpg"),
    dict(slug="traverse-des-artistes", display="Hôtel Traverse des Artistes", url="https://www.kqzyfj.com/click-101875476-15734754?url=https%3A%2F%2Fwww.booking.com%2FShare-f75i69", base="cannes", fr_section="charme-plus-intime", en_section="character-more-intimate", fr_tag="Suquet & indépendant", en_tag="Le Suquet & independent", fr_copy="Côté Suquet pour ceux qui préfèrent un Cannes plus intime, avec le centre et le Vieux Port toujours proches.", en_copy="By Le Suquet for a more intimate Cannes, while keeping the centre and Old Port close.", image="/assets/hotels/v3/traverse-des-artistes/hero.jpg"),
    dict(slug="le-versailles", display="Le Versailles", url="https://www.kqzyfj.com/click-101875476-15734754?url=https%3A%2F%2Fwww.booking.com%2FShare-z55vIw", base="villefranche", fr_section="port-sans-voiture", en_section="harbour-car-free", fr_tag="Vue & hauteur", en_tag="View & hillside", fr_copy="Un peu en hauteur, avec piscine et vue : moins collé au port, toujours clairement à Villefranche.", en_copy="A little higher up, with pool and view: less glued to the harbour, still unmistakably Villefranche."),
    dict(slug="hotel-la-regence", display="Hôtel La Régence", url="https://www.kqzyfj.com/click-101875476-15734754?url=https%3A%2F%2Fwww.booking.com%2FShare-73XcZ2", base="villefranche", fr_section="port-sans-voiture", en_section="harbour-car-free", fr_tag="Village & simple", en_tag="Village & straightforward", fr_copy="Une petite base dans Villefranche pour privilégier le village, la baie et les déplacements sans voiture.", en_copy="A small Villefranche base for putting the village, bay and car-free movement first.", image="/assets/hotels/v3/hotel-la-regence/hero.jpg"),
    dict(slug="hotel-la-flore", display="Hôtel La Flore", url="https://www.kqzyfj.com/click-101875476-15734754?url=https%3A%2F%2Fwww.booking.com%2FShare-MUMOnO", base="villefranche", fr_section="port-sans-voiture", en_section="harbour-car-free", fr_tag="Vue & piscine", en_tag="View & pool", fr_copy="En hauteur avec piscine, pour profiter de la rade sans choisir le port comme unique centre de gravité.", en_copy="Higher up with a pool, for enjoying the bay without making the harbour your only centre of gravity.", image="/assets/hotels/v3/hotel-la-flore/hero.jpg"),
    dict(slug="brise-marine-cap-ferrat", display="Hôtel de Charme Brise Marine", url="https://www.kqzyfj.com/click-101875476-15734754?url=https%3A%2F%2Fwww.booking.com%2FShare-wE7vQSK", base="villefranche", fr_section="grand-luxe-retrait", en_section="grand-luxury-retreat", fr_tag="Cap-Ferrat & intime", en_tag="Cap-Ferrat & intimate", fr_copy="Une petite adresse sur le Cap pour mettre le port, les plages et le calme avant le grand cérémonial hôtelier.", en_copy="A small Cap-Ferrat address for putting harbour, beaches and calm ahead of grand-hotel ceremony.", image="/assets/hotels/v3/brise-marine/hero.jpg"),

    dict(slug="columbus-hotel-monte-carlo", display="Columbus Hotel Monte-Carlo", url="https://www.kqzyfj.com/click-101875476-15734754?url=https%3A%2F%2Fwww.booking.com%2FShare-aF6Pvj", base="monaco", fr_section="resort-plus-detendu", en_section="resort-more-relaxed", fr_tag="Fontvieille & détendu", en_tag="Fontvieille & relaxed", fr_copy="Fontvieille pour une version plus calme et moins cérémonielle de Monaco.", en_copy="Fontvieille for a calmer, less ceremonial version of Monaco."),
    dict(slug="fairmont-monte-carlo", display="Fairmont Monte Carlo", url="https://www.kqzyfj.com/click-101875476-15734754?url=https%3A%2F%2Fwww.booking.com%2FShare-GFAr0AP", base="monaco", fr_section="palace-classique", en_section="classic-palace", fr_tag="Grand luxe central", en_tag="Central grand luxury", fr_copy="Grand format, central et très Monaco : un choix évident si vous voulez que l’adresse fasse partie du séjour.", en_copy="Large-scale, central and unmistakably Monaco: an obvious pick when the address is part of the experience."),
    dict(slug="hotel-novotel-monte-carlo", display="Hotel Novotel Monte Carlo", url="https://expedia.com/affiliates/monaco-hotels-hotel-novotel-monte-carlo.82WL2E6", base="monaco", fr_section="resort-plus-detendu", en_section="resort-more-relaxed", fr_tag="Pratique & central", en_tag="Practical & central", fr_copy="La carte la plus rationnelle pour dormir à Monaco sans transformer chaque nuit en cérémonie.", en_copy="The rational card for sleeping in Monaco without turning every night into a ceremony."),
    dict(slug="hotel-port-palace", display="Hotel Port Palace", url="https://expedia.com/affiliates/monaco-hotels-hotel-port-palace.qFVFcsr", base="monaco", fr_section="palace-classique", en_section="classic-palace", fr_tag="Port & luxe boutique", en_tag="Harbour & boutique luxury", fr_copy="Face au port pour un Monaco plus compact, plus boutique et toujours très central.", en_copy="On the harbour for a more compact, boutique version of Monaco that remains very central."),

    dict(slug="best-western-hotel-mediterranee-menton", display="Best Western Hotel Mediterranee Menton", url="https://expedia.com/affiliates/monaco-hotels-best-western-hotel-mediterranee-menton.8OrA4io", base="menton", fr_section="pratique-budget", en_section="practical-budget", fr_tag="Centre & pratique", en_tag="Central & practical", fr_copy="Central et facile pour garder Menton au cœur du séjour sans surinvestir l’hôtel.", en_copy="Central and easy when Menton matters more than over-investing in the hotel."),
    dict(slug="hotel-riva-art-and-spa", display="Hotel Riva Art & Spa", url="https://www.kqzyfj.com/click-101875476-15734754?url=https%3A%2F%2Fwww.booking.com%2FShare-uZRCL6", base="menton", fr_section="mer-calme", en_section="sea-quiet", fr_tag="Mer & spa", en_tag="Sea & spa", fr_copy="Face à la mer avec spa : pour ralentir sans renoncer à marcher vers le centre.", en_copy="Sea-facing with a spa: slow down without giving up the walk into central Menton."),
    dict(slug="hotel-vacances-bleues-royal-westminster", display="Hôtel Vacances Bleues Royal Westminster", url="https://expedia.com/affiliates/monaco-hotels-hotel-vacances-bleues-royal-westminster.cFpOwlj", base="menton", fr_section="mer-calme", en_section="sea-quiet", fr_tag="Promenade & classique", en_tag="Promenade & classic", fr_copy="Un grand classique sur la promenade pour vivre Menton côté mer, sans complication inutile.", en_copy="A classic promenade address for a sea-side Menton stay without unnecessary complication."),
    dict(slug="princess-et-richmond", display="Princess et Richmond", url="https://www.kqzyfj.com/click-101875476-15734754?url=https%3A%2F%2Fwww.booking.com%2FShare-iomATB", base="menton", fr_section="riviera-plus-chic", en_section="riviera-more-polished", fr_tag="Mer & plus chic", en_tag="Sea & more polished", fr_copy="Une option plus soignée face à la mer, sans quitter le rythme lent qui fait l’intérêt de Menton.", en_copy="A more polished sea-facing option without losing the slower rhythm that makes Menton worthwhile."),

    dict(slug="hotel-le-hameau", display="Hotel Le Hameau", url="https://expedia.com/affiliates/nice-hotels-hotel-le-hameau.f7icHwW", base="saint-paul", fr_section="bon-equilibre", en_section="balanced-choice", fr_tag="Jardin & proche village", en_tag="Garden & near the village", fr_copy="À quelques minutes du village, avec jardin et piscine : proche sans être prisonnier des remparts.", en_copy="Minutes from the village, with garden and pool: close without being trapped inside the walls."),
    dict(slug="les-vergers-de-saint-paul", display="Les Vergers de Saint-Paul", url="https://expedia.com/affiliates/nice-hotels-les-vergers-de-saint-paul.BBu2gVV", base="saint-paul", fr_section="bon-equilibre", en_section="balanced-choice", fr_tag="Calme & proche", en_tag="Quiet & close", fr_copy="Une option calme juste à l’extérieur du village pour garder Saint-Paul au centre du séjour.", en_copy="A quiet option just outside the village that keeps Saint-Paul at the centre of the stay."),

    dict(slug="hotel-marcellin", display="Hotel Marcellin", url="https://expedia.com/affiliates/nice-hotels-hotel-marcellin.ul1g9Ie", base="beaulieu", fr_section="pratique-sans-spectacle", en_section="practical-low-key", fr_tag="Petit & pratique", en_tag="Small & practical", fr_copy="Une petite adresse simple pour profiter de Beaulieu sans payer un supplément de mise en scène.", en_copy="A small, straightforward address for enjoying Beaulieu without paying extra for theatre."),
    dict(slug="hotels-carlton-beaulieu", display="Hôtel Carlton", url="https://expedia.com/affiliates/nice-hotels-hotel-carlton.ZRVWsu2", base="beaulieu", fr_section="port-riviera", en_section="harbour-riviera", fr_tag="Piscine & Riviera", en_tag="Pool & Riviera", fr_copy="Un cran plus Riviera, avec piscine, tout en gardant l’échelle tranquille de Beaulieu.", en_copy="A little more Riviera, with a pool, while keeping Beaulieu’s quieter scale."),
    dict(slug="la-reserve-de-beaulieu", display="La Réserve de Beaulieu", url="https://www.kqzyfj.com/click-101875476-15734754?url=https%3A%2F%2Fwww.booking.com%2FShare-32AxGn", base="beaulieu", fr_section="port-riviera", en_section="harbour-riviera", fr_tag="Grand hôtel & mer", en_tag="Grand hotel & sea", fr_copy="Une adresse-destination au bord de l’eau quand Beaulieu doit être une parenthèse, pas seulement une base pratique.", en_copy="A waterfront destination hotel when Beaulieu should feel like a pause, not merely a practical base.", image="/assets/hotels/v3/la-reserve-de-beaulieu/hero.jpg"),

    dict(slug="hotel-royal-mougins", display="Hôtel Royal Mougins", url="https://expedia.com/affiliates/cannes-hotels-royal-mougins-golf-resort.bZx6BiE", base="mougins", fr_section="retraite-chic", en_section="chic-retreat", fr_tag="Golf & resort", en_tag="Golf & resort", fr_copy="Pour faire de Mougins une vraie retraite, avec golf et services de resort.", en_copy="Turn Mougins into a proper retreat, with golf and resort-level facilities."),
    dict(slug="hotel-les-liserons-de-mougins", display="Hôtel les Liserons de Mougins", url="https://expedia.com/affiliates/cannes-hotels-hotel-les-liserons-de-mougins.d8Mfn4w", base="mougins", fr_section="simple-calme", en_section="simple-quiet", fr_tag="Simple & budget", en_tag="Simple & value", fr_copy="Une base plus simple pour dormir dans l’arrière-pays sans payer l’hôtel-destination.", en_copy="A simpler hills base when you do not need to pay for a destination hotel."),
    dict(slug="la-bastide-de-mougins", display="La Bastide de Mougins", url="https://expedia.com/affiliates/mougins-hotels-hotel-de-mougins.DKE9QLc", base="mougins", fr_section="retraite-chic", en_section="chic-retreat", fr_tag="Bastide & calme", en_tag="Bastide & calm", fr_copy="Une bastide plus haut de gamme pour ceux qui veulent du calme sans quitter l’esprit Riviera.", en_copy="A more upmarket bastide for travellers who want calm without leaving Riviera polish behind."),
    dict(slug="la-lune-de-mougins", display="La Lune de Mougins", url="https://expedia.com/affiliates/cannes-hotels-la-lune-de-mougins.gFMAraI", base="mougins", fr_section="simple-calme", en_section="simple-quiet", fr_tag="Spa & tranquille", en_tag="Spa & quiet", fr_copy="Une option douce avec spa quand Mougins doit surtout servir à ralentir.", en_copy="A gentle spa option when Mougins is mainly about slowing down."),

    dict(slug="airelles-chateau-de-la-messardiere", display="Airelles Château de la Messardière", url="https://expedia.com/affiliates/saint-tropez-hotels-chateau-de-la-messardiere.o0Pu1w3", base="saint-tropez", fr_section="saint-tropez-meme", en_section="saint-tropez-itself", fr_tag="Hauteurs & grand resort", en_tag="Hills & grand resort", fr_copy="Un hôtel-destination sur les hauteurs : Saint-Tropez, mais clairement pas en mode tout-à-pied.", en_copy="A destination hotel in the hills: Saint-Tropez, but clearly not in walk-everywhere mode."),
    dict(slug="byblos-saint-tropez", display="Byblos Saint-Tropez", url="https://expedia.com/affiliates/sainte-maxime-saint-tropez-hotels-hotel-byblos-saint-tropez.zAumsZT", base="saint-tropez", fr_section="saint-tropez-meme", en_section="saint-tropez-itself", fr_tag="Centre & mythique", en_tag="Centre & iconic", fr_copy="Le mythe tropézien en plein centre. On ne le choisit pas pour rester discret.", en_copy="The Saint-Tropez myth in the centre. You do not choose it to stay discreet."),
    dict(slug="hotel-la-tartane-saint-tropez", display="Hôtel La Tartane Saint-Tropez", url="https://expedia.com/affiliates/saint-tropez-hotels-hotel-saint-amour-la-tartane.NQdXcP9", base="saint-tropez", fr_section="saint-tropez-meme", en_section="saint-tropez-itself", fr_tag="Salins & retrait", en_tag="Salins & retreat", fr_copy="Route des Salins pour davantage de retrait, avec Saint-Tropez toujours dans l’orbite.", en_copy="Out towards Les Salins for more retreat, with Saint-Tropez still firmly in orbit."),
    dict(slug="hotel-de-paris-saint-tropez", display="Hôtel de Paris Saint-Tropez", url="https://expedia.com/affiliates/saint-tropez-hotels-hotel-de-paris-saint-tropez.BEcwVfD", base="saint-tropez", fr_section="saint-tropez-meme", en_section="saint-tropez-itself", fr_tag="Centre & rooftop", en_tag="Centre & rooftop", fr_copy="En ville, avec rooftop : le choix logique si vous voulez Saint-Tropez sans transport à organiser le soir.", en_copy="In town with a rooftop: the logical choice if you want Saint-Tropez without evening transport logistics."),
    dict(slug="la-bastide-de-saint-tropez", display="La Bastide de Saint Tropez", url="https://expedia.com/affiliates/saint-tropez-hotels-la-bastide-de-saint-tropez.UDcJwNv", base="saint-tropez", fr_section="saint-tropez-meme", en_section="saint-tropez-itself", fr_tag="Calme & proche centre", en_tag="Quiet & near the centre", fr_copy="Une bastide plus calme à proximité du centre pour garder le village sans dormir dans son agitation.", en_copy="A calmer bastide near the centre, keeping the village close without sleeping inside its bustle."),
]


def fmt_position(index: int) -> tuple[str, str]:
    col = index % SPRITE_COLS
    row = index // SPRITE_COLS
    x = col * 100 / (SPRITE_COLS - 1)
    y = row * 100 / (SPRITE_ROWS - 1)
    def fmt(v: float) -> str:
        return f"{v:.1f}".rstrip("0").rstrip(".")
    return fmt(x), fmt(y)


def card_markup(hotel: dict[str, str], lang: str, index: int) -> str:
    x, y = fmt_position(index)
    display = html.escape(hotel["display"], quote=True)
    raw_url = hotel["url"]
    url = html.escape(raw_url, quote=True)
    tag = html.escape(hotel[f"{lang}_tag"], quote=True)
    copy = html.escape(hotel[f"{lang}_copy"], quote=False)
    is_booking = "booking.com" in raw_url or "kqzyfj.com" in raw_url or "jdoqocy.com" in raw_url
    cta = ("Voir les tarifs sur Booking.com" if lang == "fr" else "Check rates on Booking.com") if is_booking else ("Voir les tarifs sur Expedia" if lang == "fr" else "Check rates on Expedia")
    slug = hotel["slug"]
    image = hotel.get("image")
    if image:
        media = f'<img src="{html.escape(image, quote=True)}" alt="{display}" loading="lazy"/>'
    else:
        media = (f'<span class="batch-thumb batch-thumb-13" role="img" aria-label="{display}" '
                 f'style="background-position:{x}% {y}%"></span>')
    return (
        f'<article class="hotel-choice-card" data-batch="{BATCH}" data-hotel="{slug}">'
        f'<a aria-label="{display}" class="hotel-choice-media" href="{url}" rel="sponsored nofollow noopener">'
        f'{media}</a>'
        f'<div class="hotel-choice-copy"><div class="hotel-choice-tags"><span>{tag}</span></div>'
        f'<h3><a href="{url}" rel="sponsored nofollow noopener">{display}</a></h3>'
        f'<p>{copy}</p><a class="rate-link" href="{url}" rel="sponsored nofollow noopener">{cta}</a>'
        f'</div></article>'
    )


def insert_into_section(text: str, section_id: str, cards: list[str], path: str) -> str:
    if not cards:
        return text
    marker = f'id="{section_id}"'
    marker_pos = text.find(marker)
    if marker_pos < 0:
        raise RuntimeError(f"{path}: section {section_id!r} not found")
    section_start = text.rfind("<section", 0, marker_pos)
    section_end = text.find("</section>", marker_pos)
    if section_start < 0 or section_end < 0:
        raise RuntimeError(f"{path}: malformed section {section_id!r}")
    grid_start = text.find('<div class="hotel-choice-grid">', marker_pos, section_end)
    if grid_start < 0:
        raise RuntimeError(f"{path}: hotel grid not found in section {section_id!r}")
    segment = text[grid_start:section_end]
    closes = [m.start() for m in re.finditer(r"</div>", segment)]
    if len(closes) < 2:
        raise RuntimeError(f"{path}: could not locate grid closing tag in section {section_id!r}")
    insert_at = grid_start + closes[-2]
    return text[:insert_at] + "".join(cards) + text[insert_at:]


def update_page_copy(text: str, base: str, lang: str) -> str:
    cfg = BASES[base]
    count = cfg["count"]
    if lang == "fr":
        text = re.sub(r"\b\d+ hôtels sélectionnés\b", f"{count} hôtels sélectionnés", text)
        old, new = cfg.get("fr_old"), cfg.get("fr_new")
        if old:
            text = text.replace(old, new)
        text = text.replace("12 septembre 2026", "13 septembre 2026")
        text = text.replace("2 septembre 2026", "13 septembre 2026")
    else:
        text = re.sub(r"\b\d+ selected hotels\b", f"{count} selected hotels", text)
        old, new = cfg.get("en_old"), cfg.get("en_new")
        if old:
            text = text.replace(old, new)
        text = text.replace("12 September 2026", "13 September 2026")
        text = text.replace("2 September 2026", "13 September 2026")
    return text


def update_editorial_labels(text: str, base: str, lang: str) -> str:
    if base == "nice" and lang == "fr":
        text = text.replace("<strong>Chic & mer</strong>", "<strong>Chic & expérience</strong>")
        text = text.replace("<span>04 · Chic & mer</span>", "<span>04 · Chic & expérience</span>")
        text = text.replace("L’hôtel comme expérience", "L’hôtel fait partie du voyage")
        text = text.replace(
            '<div><p class="eyebrow">La sélection est plus large</p><h2>Le milieu qui manquait devient enfin utile.</h2></div><p>Hotel 66 et Boutique Hôtel Nice Côte d’Azur ajoutent des options pratiques près de la gare. Villa Victoria apporte l’adresse centrale plus calme qui manquait au catalogue.</p>',
            '<div><p class="eyebrow">Décider avant de réserver</p><h2>Vingt adresses. Quatre logiques. Vous pouvez enfin arrêter de comparer Nice entière à la fois.</h2></div><p>Gare et escapades, ville vivante, calme central ou hôtel qui compte vraiment dans le voyage : choisissez d’abord le rôle, puis le tarif.</p>'
        )
        text = text.replace(
            '<div><span>04 · Chic & expérience</span><h2>L’hôtel fait partie de la raison du voyage.</h2></div><p>Le catalogue était déjà fort ici. Inutile d’inventer un problème.</p>',
            '<div><span>04 · Chic & expérience</span><h2>L’hôtel fait partie de la raison du voyage.</h2></div><p>Mer, spa, histoire ou grand confort : ici, on paie aussi pour l’hôtel lui-même. Autant le faire consciemment.</p>'
        )
    elif base == "nice" and lang == "en":
        text = text.replace("<strong>Chic & sea</strong>", "<strong>Chic & experience</strong>")
        text = text.replace("<span>04 · Chic & sea</span>", "<span>04 · Chic & experience</span>")
        text = text.replace("Hotel as experience", "Hotel as part of the trip")
        text = text.replace(
            '<div><p class="eyebrow">The shortlist is broader now</p><h2>The missing middle is finally useful.</h2></div><p>Hotel 66 and Boutique Hôtel Nice Côte d’Azur add practical station-friendly choices. Villa Victoria adds the calmer central option the catalogue was missing.</p>',
            '<div><p class="eyebrow">Decide before booking</p><h2>Twenty addresses. Four clear logics. You can finally stop comparing all of Nice at once.</h2></div><p>Station-and-day-trip logic, lively city, calmer central stays or hotels that are part of the experience: choose the role first, then the rate.</p>'
        )
        text = text.replace(
            '<div><span>04 · Chic & experience</span><h2>The hotel is part of the reason.</h2></div><p>The catalogue was already strong here. No need to manufacture a problem.</p>',
            '<div><span>04 · Chic & experience</span><h2>The hotel is part of the reason.</h2></div><p>Sea, spa, history or serious comfort: here you are paying for the hotel itself too. Better to do it deliberately.</p>'
        )
    elif base == "monaco" and lang == "fr":
        text = text.replace("<strong>Palace classique</strong><small>Pour vivre Monaco de l’intérieur, avec le cérémonial qui va avec.</small>",
                            "<strong>Grand luxe central</strong><small>Palaces, port et grandes adresses au cœur de Monaco.</small>")
        text = text.replace("<span>01 · Palace classique</span><h2>Pour vivre Monaco de l’intérieur, avec le cérémonial qui va avec.</h2>",
                            "<span>01 · Grand luxe central</span><h2>Quand l’adresse doit faire partie de l’expérience monégasque.</h2>")
        text = text.replace("<strong>Resort & plus détendu</strong><small>Pour garder Monaco, mais changer le rythme.</small>",
                            "<strong>Plus détendu & pratique</strong><small>Pour garder Monaco tout en réduisant le cérémonial.</small>")
        text = text.replace("<span>02 · Resort & plus détendu</span><h2>Pour garder Monaco, mais changer le rythme.</h2>",
                            "<span>02 · Plus détendu & pratique</span><h2>Pour garder Monaco tout en changeant le rythme.</h2>")
    elif base == "monaco" and lang == "en":
        text = text.replace("<strong>Classic palace</strong><small>Live Monaco from the inside, ceremony included.</small>",
                            "<strong>Central grand luxury</strong><small>Palaces, harbour and major addresses in the heart of Monaco.</small>")
        text = text.replace("<span>01 · Classic palace</span><h2>Live Monaco from the inside, ceremony included.</h2>",
                            "<span>01 · Central grand luxury</span><h2>When the address should be part of the Monaco experience.</h2>")
        text = text.replace("<strong>Resort & more relaxed</strong><small>Keep Monaco, change the rhythm.</small>",
                            "<strong>More relaxed & practical</strong><small>Keep Monaco while reducing the ceremony.</small>")
        text = text.replace("<span>02 · Resort & more relaxed</span><h2>Keep Monaco, change the rhythm.</h2>",
                            "<span>02 · More relaxed & practical</span><h2>Keep Monaco while changing the rhythm.</h2>")
    elif base == "saint-tropez" and lang == "fr":
        text = text.replace("<strong>Saint-Tropez même</strong><small>Pour rester au plus près de la ville et réduire les arbitrages de transport.</small>",
                            "<strong>Saint-Tropez · dans la commune</strong><small>Centre, hauteurs ou route des Salins : bien à Saint-Tropez, pas forcément à pied du port.</small>")
        text = text.replace("<span>01 · Saint-Tropez même</span><h2>Pour rester au plus près de la ville et réduire les arbitrages de transport.</h2>",
                            "<span>01 · Saint-Tropez · dans la commune</span><h2>Centre, hauteurs ou route des Salins : choisissez la bonne version de Saint-Tropez.</h2>")
    elif base == "saint-tropez" and lang == "en":
        text = text.replace("<strong>Saint-Tropez itself</strong><small>Stay as close to town as possible and reduce transport decisions.</small>",
                            "<strong>Saint-Tropez proper</strong><small>Centre, hills or Route des Salins: still Saint-Tropez, not always walkable.</small>")
        text = text.replace("<span>01 · Saint-Tropez itself</span><h2>Stay as close to town as possible and reduce transport decisions.</h2>",
                            "<span>01 · Saint-Tropez proper</span><h2>Centre, hills or Route des Salins: choose the right version of Saint-Tropez.</h2>")
    return text


def augment_page(base: str, lang: str) -> None:
    path = ROOT / BASES[base][lang]
    if not path.is_file():
        raise RuntimeError(f"Missing page: {path.relative_to(ROOT)}")
    text = path.read_text(encoding="utf-8")
    text = update_page_copy(text, base, lang)
    text = update_editorial_labels(text, base, lang)

    grouped: dict[str, list[str]] = {}
    for index, hotel in enumerate(HOTELS):
        if hotel["base"] != base:
            continue
        if f'data-hotel="{hotel["slug"]}"' in text:
            continue
        section = hotel[f"{lang}_section"]
        grouped.setdefault(section, []).append(card_markup(hotel, lang, index))

    for section, cards in grouped.items():
        text = insert_into_section(text, section, cards, str(path.relative_to(ROOT)))

    path.write_text(text, encoding="utf-8")
    print(f"Augmented {path.relative_to(ROOT)}")


def update_hubs() -> None:
    replacements = {
        "hotels/index.html": [
            ("40+ adresses éditorialisées", "90+ adresses éditorialisées"),
            ("Mis à jour le 12 septembre 2026", "Mis à jour le 13 septembre 2026"),
        ],
        "en/hotels/index.html": [
            ("40+ editorially selected addresses", "90+ editorially selected addresses"),
            ("Updated 12 September 2026", "Updated 13 September 2026"),
        ],
    }
    for rel, pairs in replacements.items():
        path = ROOT / rel
        if not path.is_file():
            raise RuntimeError(f"Missing hotel hub: {rel}")
        text = path.read_text(encoding="utf-8")
        for old, new in pairs:
            text = text.replace(old, new)
        path.write_text(text, encoding="utf-8")
        print(f"Updated {rel}")


def validate() -> None:
    if not SPRITE.is_file():
        raise RuntimeError(f"New hotel sprite missing: {SPRITE.relative_to(ROOT)}")
    if len(HOTELS) != 44:
        raise RuntimeError(f"Expected 44 new hotels, found {len(HOTELS)}")
    slugs = [h["slug"] for h in HOTELS]
    urls = [h["url"] for h in HOTELS]
    if len(set(slugs)) != 44:
        raise RuntimeError("New hotel slugs are not unique")
    if len(set(urls)) != 44:
        raise RuntimeError("New Expedia links are not unique")

    css = (ROOT / "assets" / "hotel-batch.css").read_text(encoding="utf-8")
    if "/assets/hotels/batch-sprite-2026-09-13.jpg" not in css:
        raise RuntimeError("New batch cards exist but CSS sprite rule is missing")

    all_text = ""
    for cfg in BASES.values():
        for lang in ("fr", "en"):
            path = ROOT / cfg[lang]
            text = path.read_text(encoding="utf-8")
            all_text += text
            expected = cfg["count"]
            needle = f"{expected} hôtels sélectionnés" if lang == "fr" else f"{expected} selected hotels"
            if needle not in text:
                raise RuntimeError(f"{path.relative_to(ROOT)}: expected count marker {needle!r}")

    counts = Counter(re.findall(r'data-hotel="([^"]+)"', all_text))
    bad = {slug: counts[slug] for slug in slugs if counts[slug] != 2}
    if bad:
        raise RuntimeError(f"Each new hotel must appear once in FR and once in EN; bad counts: {bad}")
    print("Validated 44 new hotels across FR and EN pages")


def main() -> int:
    if not SPRITE.is_file():
        raise RuntimeError("September 13 hotel sprite is missing")
    for base in BASES:
        augment_page(base, "fr")
        augment_page(base, "en")
    update_hubs()
    validate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
