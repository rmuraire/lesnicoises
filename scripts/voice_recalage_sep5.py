#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

repls = {
    "en/riviera-guide/nice/index.html": [
        ('<li><a href="/en/restaurants/">Eat &amp; Do</a></li>', '<li><a href="/en/explore/">Explore</a></li>'),
        ('Every summer, the same niocou tries to do Old Nice, Èze, Monaco and Menton before aperitivo. Calm down. Nice is a real city, with working neighbourhoods, early markets and locals who have no desire to become extras in your stories. You are welcome. Mèfi: welcome is not ownership.', 'Every summer, somebody tries to do Old Nice, Èze, Monaco and Menton before aperitivo. Ambitious. Nice is a real city, with working neighbourhoods, early markets and locals who have no desire to become extras in your stories. You are welcome; just leave enough time to notice where you are.'),
        ('At noon in August you are not discovering Cours Saleya, pichoun, you are attending a convention. Do not play the paillassou afterwards and complain that nobody knows the good places anymore. You all arrived together.', 'At noon in August you are not discovering Cours Saleya; you are attending a convention. Do not complain afterwards that nobody knows the good places anymore. You all arrived together.'),
        ('Mèfi: a six-page menu in five languages and a waiter waving at you from the pavement are not signs of local authenticity.', 'A six-page menu in five languages and a waiter waving at you from the pavement are not, despite appearances, signs of local authenticity.'),
        ('<div class="verdict"><span class="label">MÈFI, PICHOUN</span><p>', '<div class="verdict"><span class="label">THE MAMETAS VERDICT</span><p>'),
        ('Arrive at Cours Saleya at noon in August and complain that Nice is touristy. Hu. You and half of Europe had exactly the same idea. Dégun set a trap for you. You are the trap.', 'Arrive at Cours Saleya at noon in August and complain that Nice is touristy. You and half of Europe had exactly the same idea. Nobody set a trap for you. You are the traffic.'),
    ],
    "riviera-guide/nice/index.html": [
        ('<li><a href="/restaurants/">Manger &amp; faire</a></li>', '<li><a href="/fr/explorer/">Explorer</a></li>'),
        ('Chaque été, on voit le même niocou vouloir faire le Vieux-Nice, Èze, Monaco et Menton avant l’apéro. Calmez-vous. Nice est une vraie ville, avec des quartiers qui travaillent, un marché qui se lève tôt et des Niçois qui n’ont aucune envie de devenir figurants dans vos stories. Vous êtes les bienvenus. Mais mèfi : accueil ne veut pas dire propriété.', 'Chaque été, quelqu’un veut faire le Vieux-Nice, Èze, Monaco et Menton avant l’apéro. Ambitieux. Nice est une vraie ville, avec des quartiers qui travaillent, un marché qui se lève tôt et des Niçois qui n’ont aucune envie de devenir figurants dans vos stories. Vous êtes les bienvenus ; laissez-vous simplement assez de temps pour regarder où vous êtes.'),
        ('À midi en août, vous ne découvrez plus le Cours Saleya, pichoun, vous assistez à un congrès. Ne faites pas le paillassou ensuite en expliquant que « personne ne connaît plus les bons coins ». Vous êtes arrivés tous ensemble.', 'À midi en août, vous ne découvrez plus le Cours Saleya : vous assistez à un congrès. N’expliquez pas ensuite que « personne ne connaît plus les bons coins ». Vous êtes arrivés tous ensemble.'),
        ('Mèfi : six pages de menu en cinq langues et un serveur qui vous fait signe depuis le trottoir ne prouvent pas l’authenticité.', 'Six pages de menu en cinq langues et un serveur qui vous fait signe depuis le trottoir ne sont pas, malgré les apparences, des preuves d’authenticité.'),
        ('<div class="verdict"><span class="label">MÈFI, PICHOUN</span><p>', '<div class="verdict"><span class="label">LE VERDICT MAMETAS</span><p>'),
        ('Arriver au Cours Saleya à midi en août puis expliquer que Nice est trop touristique. Hu. Vous et la moitié de l’Europe avez eu exactement la même idée. Dégun ne vous a tendu un piège : vous êtes le piège.', 'Arriver au Cours Saleya à midi en août puis expliquer que Nice est trop touristique. Vous et la moitié de l’Europe avez eu exactement la même idée. Personne ne vous a tendu un piège : vous êtes l’embouteillage.'),
    ],
    "en/riviera-guide/nice-or-cannes/index.html": [
        ('<li><a href="/en/restaurants/">Eat &amp; Do</a></li>', '<li><a href="/en/explore/">Explore</a></li>'),
        ('Both can work beautifully. They simply optimise different things.', 'Both can work beautifully. They simply optimise different things, and pretending otherwise is how people end up paying palace rates for the wrong holiday.'),
        ('A rooftop pool is delightful. It remains surprisingly poor at getting you to Menton before lunch.', 'A rooftop pool is delightful. It remains surprisingly poor at getting you to Menton before lunch. Geography is terribly resistant to branding.'),
    ],
    "riviera-guide/nice-ou-cannes/index.html": [
        ('<li><a href="/restaurants/">Manger &amp; faire</a></li>', '<li><a href="/fr/explorer/">Explorer</a></li>'),
        ('Les deux peuvent être excellentes. Elles n’optimisent simplement pas la même chose.', 'Les deux peuvent être excellentes. Elles n’optimisent simplement pas la même chose, et faire semblant du contraire est une excellente façon de payer un palace pour les mauvaises vacances.'),
        ('Une piscine sur le toit est charmante. Elle reste étonnamment mauvaise pour vous déposer à Menton avant déjeuner.', 'Une piscine sur le toit est charmante. Elle reste étonnamment mauvaise pour vous déposer à Menton avant déjeuner. La géographie résiste assez bien au marketing.'),
    ],
}

changed = []
for rel, pairs in repls.items():
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    original = text
    for old, new in pairs:
        if old not in text:
            raise SystemExit(f"Expected text not found in {rel}: {old[:80]}")
        text = text.replace(old, new)
    if text != original:
        p.write_text(text, encoding="utf-8")
        changed.append(rel)

print("Voice recalibration updated:")
for rel in changed:
    print(rel)
