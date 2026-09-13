#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def update(rel: str, pairs: list[tuple[str, str]]) -> None:
    path = ROOT / rel
    if not path.is_file():
        raise RuntimeError(f"Missing voice target: {rel}")
    text = path.read_text(encoding="utf-8")
    changed = 0
    for old, new in pairs:
        if old in text:
            text = text.replace(old, new)
            changed += 1
    path.write_text(text, encoding="utf-8")
    print(f"Mametas plan/places voice: {rel} ({changed}/{len(pairs)} replacements)")


def main() -> int:
    # HOME. Plan and Places need to sound like the Mametas before the visitor even clicks.
    update("fr/index.html", [
        (
            "Dites-nous combien de jours vous avez. On fera le tri. Cinq jours, c’est très bien si vous arrêtez d’essayer de collectionner toute la Côte d’Azur avant le déjeuner.",
            "Cinq jours ? Très bien. N’essayez pas d’en faire douze. On fera le tri. La Côte d’Azur sera encore là la prochaine fois, pitchoun.",
        ),
        (
            "Votre base décide du temps passé sur la plage, sur un quai ou à chercher un endroit vivant après dîner. Choisissez d’abord le lieu qui convient, ensuite l’hôtel.",
            "Choisissez la ville avant l’hôtel. Oui, on sait, les photos de piscine vous appellent. Résistez cinq minutes. Votre base décide si le séjour sera simple, vivant, calme ou une négociation quotidienne avec les horaires de train.",
        ),
    ])
    update("index.html", [
        (
            "Tell us how many days you have. We’ll do the editing. Five days is plenty if you stop trying to collect the whole Riviera before lunch.",
            "Five days? Good. Please do not turn them into twelve. We’ll do the editing. The Riviera will still be here next time, pichoun.",
        ),
        (
            "Your base decides how much time you spend on the beach, on a platform or trying to find somewhere lively after dinner. Pick the place that fits the trip, then the hotel.",
            "Choose the town before the hotel. Yes, we know, the pool photos are calling. Ignore them for five minutes. Your base decides whether the trip feels easy, lively, quiet or like a daily negotiation with a train timetable.",
        ),
    ])

    # PLACES HUB, FR. Always vous. Familiarity comes from tone, not tutoiement.
    update("riviera-guide/index.html", [
        (
            "Tu peux essayer de tout faire en trois jours. Tu peux aussi passer de bonnes vacances. Nous, pour un premier séjour, on choisirait Nice. Voilà, c’est dit. Après, on nuance.",
            "Vous pouvez essayer de tout faire en trois jours. Vous pouvez aussi passer de bonnes vacances. Nous, pour un premier séjour, on choisirait Nice. Voilà, c’est dit. Après, on nuance.",
        ),
        (
            "Tu peux essayer de tout faire en trois jours. Tu peux aussi passer de bonnes vacances. Choisis une base, comprends la côte, puis rayonne.",
            "Vous pouvez essayer de tout faire en trois jours. Vous pouvez aussi passer de bonnes vacances. Nous, pour un premier séjour, on choisirait Nice. Voilà, c’est dit. Après, on nuance.",
        ),
        (
            "Le plus bel endroit n’est pas forcément la meilleure base. Agaçant, on sait. Demande-toi plutôt où tu as envie de vivre pendant quelques jours.",
            "Le plus bel endroit n’est pas forcément la meilleure base. Agaçant, on sait. Demandez-vous plutôt où vous avez envie de vivre pendant quelques jours. Oui, vivre. Pas juste dormir.",
        ),
        (
            "Le bon séjour commence rarement par le nom d’un hôtel. Il commence par une question plus simple : où est-ce que tu veux vivre pendant quelques jours ?",
            "Le bon séjour ne commence pas par le nom d’un hôtel. Il commence par une question beaucoup plus simple : où avez-vous envie de vivre pendant quelques jours ? Oui, vivre. Pas juste dormir.",
        ),
        (
            "Une fois la base choisie, seulement là, tu peux commencer à regarder les chambres.",
            "Une fois la base choisie, là seulement vous regardez les chambres. Sinon vous comparez des piscines dans la mauvaise ville. Cagade classique.",
        ),
        ("CHOISIS TA RIVIERA", "CHOISISSEZ VOTRE RIVIERA"),
        (
            "On a nos préférées. Nice d’abord pour un premier séjour. Antibes juste derrière pour l’équilibre. Villefranche pour la beauté. Cannes, oui, on l’aime aussi. Choisis le caractère avant le palace.",
            "On a nos préférées. Nice d’abord pour un premier séjour. Antibes juste derrière pour l’équilibre. Villefranche pour la beauté. Cannes, oui, on l’aime aussi. Choisissez le caractère avant le palace.",
        ),
        (
            "Si tu hésites encore, commence par regarder les villes plutôt que les palaces. C’est moins glamour cinq minutes, mais beaucoup plus utile ensuite.",
            "Si vous hésitez encore, regardez les villes avant les palaces. C’est moins glamour pendant cinq minutes. C’est beaucoup plus intelligent pour les cinq jours suivants.",
        ),
        ('<span class="tiny">Riviera Guide</span><h3>Menton</h3>', '<span class="tiny">On aime quand ça ralentit</span><h3>Menton</h3>'),
        ('<span class="tiny">Riviera Guide</span><h3>Monaco</h3>', '<span class="tiny">Spectaculaire. Mèfi au budget.</span><h3>Monaco</h3>'),
        ('<span class="tiny">Riviera Guide</span><h3>Èze</h3>', '<span class="tiny">Très beau. Allez-y tôt.</span><h3>Èze</h3>'),
        ('<span class="tiny">Riviera Guide</span><h3>Nice</h3>', '<span class="tiny">Notre choix pour commencer</span><h3>Nice</h3>'),
        ('<span class="tiny">Riviera Guide</span><h3>Villefranche &amp; Cap-Ferrat</h3>', '<span class="tiny">La rade fait le travail. Laissez-la.</span><h3>Villefranche &amp; Cap-Ferrat</h3>'),
        ('<span class="tiny">Riviera Guide</span><h3>Antibes</h3>', '<span class="tiny">On l’aime beaucoup. Voilà.</span><h3>Antibes</h3>'),
        ('<span class="tiny">Riviera Guide</span><h3>Cannes</h3>', '<span class="tiny">On la taquine. On y retourne.</span><h3>Cannes</h3>'),
        ('<span class="tiny">Riviera Guide</span><h3>Saint-Tropez</h3>', '<span class="tiny">Magnifique. Pas pratique. Assumez.</span><h3>Saint-Tropez</h3>'),
        ("—", ","),
    ])

    # PLACES HUB, EN. Same information, more presence.
    update("en/riviera-guide/index.html", [
        (
            "We have a favourite first base. Nice. There, we said it. But sand, silence, palace life or a slower coast can change the answer. Choose the holiday first, then the town.",
            "We have a favourite first base. Nice. There, we said it. But sand, silence, palace life or a slower coast can change the answer. Choose the holiday first. Then the town. Then, finally, the pool photos.",
        ),
        (
            "The prettiest place is not automatically the best base. Annoying, we know. Pick the place that makes the days you actually want easier.",
            "The prettiest place is not automatically the best base. Annoying, we know. Pick the place that makes your actual holiday easier. Beauty can sulk for five minutes.",
        ),
        (
            "A good guide should reduce the number of tabs, not give you twelve new reasons to open them.",
            "Still hesitating? Fine. But do not open twelve more tabs. We have done enough of that for everybody.",
        ),
        (
            "The Riviera has already consumed enough browser tabs. Turn the decision into an actual trip.",
            "Good. Stop comparing towns now. The Riviera has already eaten enough of your browser. Pick the hotel, book the bits that matter and go have a life.",
        ),
        ("—", ","),
    ])

    # FIVE-DAY PLAN, FR. More speech, more judgement, still useful.
    update("fr/planifier/cinq-jours-nice-sans-voiture/index.html", [
        (
            "Un seul hôtel, une ligne ferroviaire utile et cinq journées qui ne ressemblent pas à une chasse au trésor chronométrée.",
            "Un seul hôtel. Pas de voiture. Cinq jours. Et non, vous n’avez pas besoin de caser Monaco, Cannes et Saint-Tropez avant mardi soir.",
        ),
        (
            "Nice ne gagne pas tous les concours de beauté. Elle gagne souvent dès qu’on ouvre la carte des trains. Vous pouvez arriver, manger, dormir et rejoindre plusieurs mondes très différents sans changer d’hôtel ni développer une expertise des parkings souterrains.",
            "On va vous éviter une première cagade : changer d’hôtel tous les deux jours. Nice n’est pas toujours la plus spectaculaire. On s’en fiche un peu. Regardez la carte des trains et elle devient soudain terriblement convaincante.",
        ),
        (
            "C’est le parcours que nous donnerions à une personne découvrant la région avec cinq nuits, de bonnes chaussures et aucune envie de passer ses vacances dans une voiture de location.",
            "C’est le parcours qu’on donnerait à nos propres amis : cinq nuits, de bonnes chaussures et aucune raison valable de passer les vacances dans une voiture de location.",
        ),
        (
            "Pour ce parcours, restez à distance facile d’un tram et à une marche raisonnable de Nice-Ville. Le Vieux-Nice offre l’atmosphère ; le quadrillage central autour de Jean-Médecin et Dubouchage simplifie souvent les départs. Le bon choix dépend de ce que vous privilégiez : la logistique matinale ou l’ambiance tardive.",
            "Pour ce parcours, restez près d’un tram et à distance raisonnable de Nice-Ville. Le Vieux-Nice a le charme. Jean-Médecin et Dubouchage ont la logistique. Vous ne pouvez pas tout avoir au même coin de rue, pitchoun. Choisissez votre priorité.",
        ),
        (
            "Le train côtier assure les grands déplacements est–ouest. Les bus et la marche couvrent ce que le rail ne dessert pas. La voiture redevient pertinente si vous ajoutez des villages de l’arrière-pays, des plages isolées ou Saint-Tropez avec des liaisons saisonnières peu commodes.",
            "Ne louez pas de voiture pour ces cinq jours. Vraiment. Le train fait le gros du travail, les bus et vos jambes font le reste. Prenez une voiture si vous partez dans l’arrière-pays, cherchez des criques isolées ou décidez que Saint-Tropez doit absolument entrer dans l’histoire.",
        ),
        (
            "Gardez l’arrivée locale. Parcourez le Vieux-Nice, le secteur du marché et le bord de mer, puis montez seulement si votre énergie et vos chaussures sont d’accord. L’objectif utile n’est pas de « finir Nice », mais de comprendre les distances entre l’hôtel, la vieille ville, la plage et la gare.",
            "Ne fuyez pas Nice à 9 h le premier matin. On vous voit venir. Faites le Vieux-Nice, le marché, la mer, puis montez si vos jambes sont d’accord. Vous n’avez pas à « finir Nice ». Vous devez juste commencer à la comprendre.",
        ),
        (
            "Commencez à Villefranche-sur-Mer, puis décidez si la journée souhaite une marche côtière, un jardin ou un long déjeuner. Cap-Ferrat est proche sur une carte mais ne constitue pas une attraction compacte ; collectionner toutes les criques produit généralement plus de transport que de plaisir.",
            "Commencez à Villefranche. Ensuite choisissez : une marche, un jardin ou un long déjeuner. Pas les trois plus six criques. Cap-Ferrat est magnifique, mais ce n’est pas une chasse au trésor.",
        ),
        (
            "Regroupez ces deux lieux parce que le train rend l’enchaînement logique. Accordez la première partie de journée à Monaco, puis continuez vers Menton pour une vieille ville plus douce et la soirée. Si un musée, un jardin ou un restaurant précis constitue le vrai but, inversez l’ordre selon ses horaires.",
            "Monaco d’abord, Menton ensuite. Oui, le contraste est un peu violent. C’est justement ce qu’on aime. Le train rend l’enchaînement simple, à condition de ne pas transformer Monaco en inventaire avant midi.",
        ),
        (
            "Antibes offre vieille ville, remparts et plage accessible sans exiger l’engagement esthétique de Cannes. Cela suffit largement à une journée détendue. N’ajoutez Cannes que si la Croisette et le théâtre des palaces vous intéressent réellement ; la proximité n’est pas une instruction.",
            "On aime beaucoup Antibes. Voilà, c’est dit. Vieille ville, remparts, plage, tout tient bien ensemble. N’ajoutez Cannes que si vous avez vraiment envie de Cannes. La proximité n’est toujours pas une obligation.",
        ),
        (
            "Èze village est le choix iconique, à rejoindre en bus plutôt qu’en prétendant que la gare côtière se trouve à côté du village perché. Consultez l’itinéraire du jour avant de partir. Si la météo, la foule ou vos jambes votent contre, restez à Nice : musée, marché, plage et un dîner correctement choisi.",
            "Èze est sublime. À 11 h en août, vous ne serez simplement pas les seuls à avoir eu l’idée. Prenez le bus pour le village perché. Et si la foule, la chaleur ou vos jambes disent non, restez à Nice. Personne ne vous retirera des points.",
        ),
        (
            "Utilisez le TER comme colonne vertébrale côtière pour Antibes, Monaco et Menton. Utilisez les bus locaux ou régionaux pour les lieux comme le village perché d’Èze et certaines parties de Cap-Ferrat. Vérifiez chaque déplacement dans les calculateurs officiels plutôt que de recopier le numéro de ligne d’un vieil article.",
            "Le TER est votre colonne vertébrale. Antibes, Monaco, Menton : train d’abord. Èze village et certains coins du Cap : bus. Et vérifiez les horaires du jour, pas le numéro de ligne recopié d’un article écrit quand tout le monde avait encore un BlackBerry.",
        ),
        ("—", ","),
    ])

    # FIVE-DAY PLAN, EN.
    update("plan/five-days-nice-no-car/index.html", [
        (
            "One hotel, a useful railway line and five days that do not resemble a competitive scavenger hunt.",
            "One hotel. No car. Five days. And no, you do not need to squeeze Monaco, Cannes and Saint-Tropez in before Tuesday night.",
        ),
        (
            "Nice may not win every beauty contest. It keeps winning once you look at the train map. You can arrive, eat, sleep and reach several very different places without changing hotels or acquiring strong opinions about underground car parks.",
            "Let us save you the first cagade: changing hotels every two days. Nice is not always the most spectacular base. We do not care. Look at the train map and it becomes horribly convincing.",
        ),
        (
            "This is the itinerary we would give a first-time visitor with five nights, sensible shoes and no desire to spend the holiday inside a rental car.",
            "This is the plan we would give our own friends: five nights, sensible shoes and absolutely no good reason to spend the holiday inside a rental car.",
        ),
        (
            "For this plan, stay within an easy walk of a tram stop and no more than a reasonable walk from Nice-Ville station. Old Nice is atmospheric; the central grid around Jean Médecin and Dubouchage is often simpler. The best choice depends on whether you value morning logistics or late-night atmosphere.",
            "Stay near a tram and within a sensible walk of Nice-Ville. Old Nice has the charm. Jean Médecin and Dubouchage have the logistics. You cannot have everything on the same corner, pichoun. Pick your priority.",
        ),
        (
            "The coastal railway handles the long east–west moves in this itinerary. Buses and walking cover the places the train does not. A car becomes useful when you add inland villages, remote beaches or a Saint-Tropez plan with awkward seasonal connections.",
            "Do not rent a car for these five days. Seriously. The train does the heavy lifting, buses and your legs do the rest. Rent one when you go inland, chase remote coves or decide Saint-Tropez absolutely has to enter the story.",
        ),
        (
            "Keep the arrival day local. Walk the Old Town, the market area and the seafront, then climb only if your energy and shoes agree. The useful objective is not to “finish Nice”; it is to understand the distances between your hotel, the old town, the beach and the station.",
            "Do not escape Nice at 9 am on your first morning. We can see you coming. Do Old Nice, the market and the sea. Climb if your legs agree. You do not need to finish Nice. You need to start understanding it.",
        ),
        (
            "Start with Villefranche-sur-Mer, then decide whether your day wants a coastal walk, a garden or a long lunch. Cap-Ferrat is close on a map but not one compact attraction; trying to collect every cove usually produces more transport than pleasure.",
            "Start in Villefranche. Then choose: a walk, a garden or a long lunch. Not all three plus six coves. Cap-Ferrat is gorgeous. It is not a scavenger hunt.",
        ),
        (
            "Group these two because the railway makes the sequence logical. Give Monaco the earlier part of the day, then continue east to Menton for a softer old town and evening. If museums, gardens or a specific restaurant are the real point, reverse the order around their opening hours.",
            "Monaco first, Menton after. Yes, the contrast is slightly violent. That is exactly why we like it. The train makes the pairing easy, provided you do not turn Monaco into an inventory before lunch.",
        ),
        (
            "Antibes gives you an old town, ramparts and an accessible beach without requiring a Cannes-level commitment to polish. It is enough for a full relaxed day. Add Cannes only if you genuinely want the Croisette and palace-hotel theatre; proximity is not an instruction.",
            "We really like Antibes. There, we said it. Old town, ramparts, beach. It all fits. Add Cannes only if you actually want Cannes. Proximity is still not an instruction.",
        ),
        (
            "Èze village is the iconic choice, reached by bus rather than by pretending the coastal railway station sits beside the hilltop village. Check the current journey planner before leaving. If the weather, crowds or your legs vote against it, keep the day in Nice: museum, market, beach and one properly chosen dinner.",
            "Èze is gorgeous. At 11 am in August, you will simply not be the only genius who had the idea. Take the bus to the hilltop village. If the crowds, heat or your legs say no, stay in Nice. Nobody is taking points away.",
        ),
        (
            "Use the regional train as the coastal spine for Antibes, Monaco and Menton. Use local or regional buses for places such as the hilltop village of Èze and parts of Cap-Ferrat. Check each trip in the official planners rather than copying a line number from an old article.",
            "The regional train is your spine. Antibes, Monaco, Menton: train first. Èze village and parts of the Cap: bus. Check the timetable for the actual day, not a line number copied from an article written when everybody still had a BlackBerry.",
        ),
        ("—", ","),
    ])

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
