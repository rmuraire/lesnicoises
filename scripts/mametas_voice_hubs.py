#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def update(rel: str, pairs: list[tuple[str, str]]) -> None:
    path = ROOT / rel
    if not path.is_file():
        raise RuntimeError(f"Missing entry page: {rel}")
    text = path.read_text(encoding="utf-8")
    changed = 0
    for old, new in pairs:
        if old in text:
            text = text.replace(old, new)
            changed += 1
    path.write_text(text, encoding="utf-8")
    print(f"Mametas hub voice: {rel} ({changed} replacements)")


def main() -> int:
    # Clean title punctuation after the global no-em-dash pass.
    update("index.html", [
        ("<title>Mametas, The opinionated French Riviera guide</title>", "<title>Mametas | The opinionated French Riviera guide</title>"),
        ('<meta property="og:title" content="Mametas, They know the Riviera.">', '<meta property="og:title" content="Mametas | They know the Riviera.">'),
    ])
    update("fr/index.html", [
        ("<title>Mametas, Le guide très décidé de la Côte d’Azur</title>", "<title>Mametas | Le guide très décidé de la Côte d’Azur</title>"),
        ('<meta property="og:title" content="Mametas, They know the Riviera.">', '<meta property="og:title" content="Mametas | They know the Riviera.">'),
    ])

    update("en/restaurants/index.html", [
        ("Seventy-nine addresses. Enough to choose by budget, cuisine and atmosphere; not enough to abandon you with 147 results and a “relevance” filter.",
         "Seventy-nine addresses. Some we love. Some we love for one very specific reason. None are here just to make the list look impressive."),
        ("A brilliant restaurant 45 minutes away from your day is still a bad recommendation. Choose the town, then the table.",
         "Tell us where you’ll be. We’ll tell you where we’d eat. A brilliant table 45 minutes away is still the wrong table."),
        ("Nice, Cannes and Antibes keep the greatest depth. Monaco, Villefranche-Cap-Ferrat and Saint-Tropez now cover several price and ceremony levels; Menton reaches six genuinely different choices. Secondary destinations stay deliberately tighter: four or five useful decisions beat ten filler addresses.",
         "Nice, Cannes and Antibes get the longer lists because they earn them. Smaller places stay tighter. We’d rather give you four tables we can defend than ten names for decoration."),
        ("From socca counter to the big night: the broadest choice.", "Our home turf. From hot socca to the big night, we have opinions."),
        ("Old town, Juan-les-Pins and the Cap according to the mood.", "One of our favourite food stops. Old town, Juan-les-Pins or the Cap, depending on the mood."),
        ("Bistro, market, seafood, polished dinner or full occasion.", "Yes, we like Cannes. Bistro, market, seafood, polished dinner or the full occasion."),
    ])
    update("restaurants/index.html", [
        ("Soixante-dix-neuf adresses. Assez pour choisir selon le budget, la cuisine et l’ambiance ; pas assez pour vous abandonner avec 147 résultats et un filtre « pertinence ».",
         "Soixante-dix-neuf adresses. Il y en a qu’on adore. D’autres qu’on aime pour une seule très bonne raison. Aucune n’est là pour faire joli dans une liste."),
        ("Une excellente table à 45 minutes de votre journée reste une mauvaise recommandation. Choisissez la ville, puis le restaurant.",
         "Dites-nous où vous serez. On vous dira où nous, on mangerait. Une excellente table à 45 minutes de votre journée reste la mauvaise table."),
        ("Nice, Cannes et Antibes gardent la plus grande profondeur. Monaco, Villefranche-Cap-Ferrat et Saint-Tropez couvrent désormais plusieurs niveaux de prix et de cérémonie ; Menton atteint six choix réellement différents. Les destinations secondaires restent volontairement plus courtes : quatre à cinq bonnes décisions valent mieux que dix adresses de remplissage.",
         "Nice, Cannes et Antibes ont les listes longues parce qu’elles les méritent. Les plus petites destinations restent serrées. On préfère quatre tables qu’on peut défendre à dix noms mis là pour remplir."),
        ("Du comptoir à socca au grand soir : le choix le plus large.", "Notre terrain. De la socca brûlante au grand soir, on a des avis."),
        ("Vieille ville, Juan-les-Pins et Cap selon le moment.", "Une de nos étapes préférées pour manger. Vieille ville, Juan-les-Pins ou le Cap selon l’envie."),
        ("Bistrot, marché, mer, soirée chic ou grand soir.", "Oui, on aime Cannes. Bistrot, marché, mer, soirée chic ou grand soir."),
    ])

    update("en/explore/index.html", [
        ("Mametas can tell you where to base yourself and what to book. It can also get out of the way. This is the part for restaurants, swims, walks, islands, museums and good detours.",
         "Sometimes we have a plan. Sometimes we want lunch, a swim and absolutely no ambition. This is that part of Mametas."),
        ("Four doors in. We start with the question that returns every day, usually around noon: where are we eating?",
         "Four doors. Pick one. If it’s noon, obviously start with food."),
        ("Choices by town, budget, cuisine and mood. Enough addresses to decide; not enough to hand the problem back to you.",
         "We have opinions. Plenty of them. Choose by town, price and mood, then go eat."),
        ("Pebbles, sand, coves and the useful difference between a famous beach and a pleasant one.",
         "Famous is not the same as pleasant. Pebbles, sand, coves. We’ll tell you which is which."),
        ("Matisse, Picasso, Maeght, Cocteau, villas and places where the Riviera becomes more than a view.",
         "We love Matisse. We love Picasso. We also love air conditioning in August. Culture can do all three."),
        ("Some places deserve to be discovered because they fit the day, not because an itinerary assigned them a slot.",
         "See something you fancy? Go. Not every good idea needs a colour-coded itinerary."),
    ])
    update("explore/index.html", [
        ("Mametas peut vous dire où dormir et quoi réserver. Elle peut aussi vous laisser tranquille. Ici : restaurants, baignades, balades, îles, musées et détours qui méritent qu’on change le programme.",
         "Parfois on a un plan. Parfois on veut déjeuner, se baigner et n’avoir absolument aucune ambition. Cette partie de Mametas est faite pour ça."),
        ("Quatre portes d’entrée. On commence par la question qui revient tous les jours, généralement vers midi : où est-ce qu’on mange ?",
         "Quatre portes. Choisissez-en une. S’il est midi, commencez évidemment par manger."),
        ("Des choix par ville, budget, cuisine et ambiance. Assez d’adresses pour décider ; pas assez pour vous rendre le problème.",
         "On a des avis. Beaucoup. Choisissez la ville, le prix et l’envie, puis allez manger."),
        ("Galets, sable, criques et la différence utile entre une plage célèbre et une plage agréable.",
         "Célèbre ne veut pas dire agréable. Galets, sable, criques. On vous dira la différence."),
        ("Matisse, Picasso, Maeght, Cocteau, villas et lieux qui donnent un peu plus d’épaisseur au décor.",
         "On adore Matisse. On adore Picasso. On adore aussi la climatisation en août. La culture sait faire les trois."),
        ("Certains lieux méritent simplement d’être découverts parce qu’ils collent à la journée, pas parce qu’un itinéraire leur a réservé un créneau.",
         "Quelque chose vous fait envie ? Allez-y. Toutes les bonnes idées n’ont pas besoin d’un itinéraire avec des couleurs."),
    ])

    update("en/riviera-guide/index.html", [
        ("Nice, Villefranche, Antibes, Cannes, Monaco and Menton share a railway line and very little personality. Choose what you want the holiday to feel like before opening the booking tabs.",
         "We have a favourite first base. Nice. There, we said it. But sand, silence, palace life or a slower coast can change the answer. Choose the holiday first, then the town."),
        ("The best base is not the most beautiful place in isolation. It is the place that makes the days you actually want easier.",
         "The prettiest place is not automatically the best base. Annoying, we know. Pick the place that makes the days you actually want easier."),
        ("<strong>Best first base.</strong> Transport, restaurants, culture and a city that remains alive after dinner.",
         "<strong>Our default first base.</strong> Not sacred. Just annoyingly useful, with trains, restaurants, culture and a real city after dinner."),
        ("<strong>Best for beauty and a slower pace.</strong> Fewer choices, considerably better excuses to do nothing.",
         "<strong>We adore it.</strong> Beauty wins. Logistics sulk a little. That can be a very good trade."),
        ("<strong>Best balance.</strong> Old town, sandy beach and useful rail links without Cannes-level performance.",
         "<strong>One of our favourites.</strong> Old town, sand and useful trains. Very little need to perform."),
        ("<strong>Best for polish and beach.</strong> Compact, sandy and unusually serious about the hotel being part of the holiday.",
         "<strong>We like Cannes.</strong> Another confession. Compact, sandy and very serious about the hotel being part of the holiday."),
        ("<strong>Best when you have a reason to stay.</strong> Easy day trip; expensive base; very good at spectacle.",
         "<strong>Amazing at spectacle.</strong> Easy day trip, expensive base. We would not make it the default unless Monaco itself is the point."),
        ("<strong>Best for the quiet eastern edge.</strong> Softer, slower and a natural counterpoint to Monaco.",
         "<strong>We breathe better here.</strong> Softer, slower and the perfect counterpoint to Monaco."),
    ])
    update("riviera-guide/index.html", [
        ("Tu peux essayer de tout faire en trois jours. Tu peux aussi passer de bonnes vacances. Choisis une base, comprends la côte, puis rayonne.",
         "Tu peux essayer de tout faire en trois jours. Tu peux aussi passer de bonnes vacances. Nous, pour un premier séjour, on choisirait Nice. Voilà, c’est dit. Après, on nuance."),
        ("Le bon séjour commence rarement par le nom d’un hôtel. Il commence par une question plus simple : où est-ce que tu veux vivre pendant quelques jours ?",
         "Le plus bel endroit n’est pas forcément la meilleure base. Agaçant, on sait. Demande-toi plutôt où tu as envie de vivre pendant quelques jours."),
        ("Si tu hésites encore, commence par regarder les villes plutôt que les palaces. C’est moins glamour cinq minutes, mais beaucoup plus utile ensuite.",
         "On a nos préférées. Nice d’abord pour un premier séjour. Antibes juste derrière pour l’équilibre. Villefranche pour la beauté. Cannes, oui, on l’aime aussi. Choisis le caractère avant le palace."),
    ])

    update("en/hotels/index.html", [
        ("A beautiful hotel in the wrong place is still in the wrong place. Start with the town that fits your trip, then choose the address inside it.",
         "We love hotels. Really love them. Which is exactly why we refuse to let a gorgeous lobby put you in the wrong town. Choose the base first."),
        ("Nice is still our best all-round first base. It is not a compulsory religion.",
         "Nice is still our favourite all-round first base. There, we said it again. It is not a compulsory religion."),
        ("Good addresses, for different reasons.", "Hotels we’d actually consider. For very different reasons."),
        ("We are not building a census. We are building enough choice to make a decision without spending the evening comparing 143 beige rooms.",
         "We do not need every hotel on the Riviera. Dégun needs that. We need enough good ones to make a decision without comparing 143 beige rooms."),
    ])
    update("hotels/index.html", [
        ("Un très bel hôtel au mauvais endroit reste au mauvais endroit. Mametas commence par la géographie et le style de séjour, puis seulement par l’adresse.",
         "On adore les hôtels. Vraiment. C’est justement pour ça qu’on ne laissera pas un très beau lobby vous mettre dans la mauvaise ville. Choisissez d’abord la base."),
        ("Nice reste notre meilleure base polyvalente pour un premier séjour. Mais ce n’est plus la seule page où l’on vous aide vraiment à décider.",
         "Nice reste notre base préférée pour un premier séjour. Voilà, on l’a encore dit. Ce n’est pas une religion obligatoire."),
        ("Une sélection courte vaut mieux qu’un faux choix infini.", "Des hôtels qu’on envisagerait vraiment. Pour des raisons très différentes."),
        ("Chaque destination est désormais rangée par attente : pratique, calme, vivant, Riviera, palace, retrait… Vous devriez pouvoir éliminer une moitié des hôtels avant même de regarder le prix.",
         "On n’a pas besoin de tous les hôtels de la Côte d’Azur. Dégun n’a besoin de ça. Il en faut assez de bons pour éliminer la moitié des options avant même de regarder le prix."),
        ("<b>Riviera &amp; bord de mer.</b> Juan-les-Pins en version Riviera assumée.",
         "<b>Riviera &amp; bord de mer.</b> On aime beaucoup celle-ci. Juan-les-Pins en version Riviera assumée."),
        ("<b>Grand luxe &amp; retrait.</b> Ici, l’hôtel n’accompagne pas le séjour : il en devient une bonne partie.",
         "<b>Grand luxe &amp; retrait.</b> Oui, c’est sublime. Ici, l’hôtel n’accompagne pas le séjour. Il en devient une bonne partie."),
    ])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
