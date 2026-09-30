# -*- coding: utf-8 -*-
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def patch(path, func):
    p = ROOT / path
    if not p.exists():
        print("skip missing", path)
        return
    s = p.read_text(encoding="utf-8")
    ns = func(s)
    if ns != s:
        p.write_text(ns, encoding="utf-8")
        print("patched", path)
    else:
        print("unchanged", path)

def before_once(s, marker, block, token):
    if token in s or marker not in s:
        return s
    return s.replace(marker, block + marker, 1)

research_en = """<div class="verdict solo-research-context" data-layer="solo-research-context-2026-09-30"><span class="label">WHY THIS GUIDE EXISTS</span><p><strong>Solo travel is usually about autonomy, not isolation.</strong> In a 2024 peer-reviewed study of 250 solo travellers, independence and flexibility were the most-cited pre-pandemic motivation (54%), while safety was one of the leading constraints (38.8%). A separate peer-reviewed study of middle-aged and senior women travelling solo found that destination choice was shaped by perceived risk, with safety and health prioritised, alongside comfort, amenities and accessibility.</p><p class="research-note">Research context, not a claim about every traveller: <a href="https://doi.org/10.1108/CBTH-01-2024-0029" target="_blank" rel="nofollow noopener">Nirkow &amp; Abbasian, 2024</a> · <a href="https://doi.org/10.1007/s12062-024-09450-z" target="_blank" rel="nofollow noopener">Maiurro &amp; Brandão, 2025</a>.</p></div>"""
research_fr = """<div class="verdict solo-research-context" data-layer="solo-research-context-2026-09-30"><span class="label">POURQUOI CE GUIDE EXISTE</span><p><strong>Voyager seule relève d'abord de l'autonomie, pas de l'isolement.</strong> Dans une étude évaluée par les pairs publiée en 2024 auprès de 250 voyageurs solo, l'indépendance et la flexibilité étaient la motivation la plus citée avant la pandémie (54 %), tandis que la sécurité faisait partie des principales contraintes (38,8 %). Une autre étude, centrée sur des femmes d'âge mûr et seniors voyageant seules, montre que le choix de destination est influencé par le risque perçu, avec la sécurité et la santé en priorité, mais aussi le confort, les équipements et l'accessibilité.</p><p class="research-note">Contexte de recherche, sans généraliser à toutes les voyageuses : <a href="https://doi.org/10.1108/CBTH-01-2024-0029" target="_blank" rel="nofollow noopener">Nirkow &amp; Abbasian, 2024</a> · <a href="https://doi.org/10.1007/s12062-024-09450-z" target="_blank" rel="nofollow noopener">Maiurro &amp; Brandão, 2025</a>.</p></div>"""

friction_en = """<h2 data-layer="solo-friction-50plus-2026-09-30">If comfort matters more than proving a point</h2><p>For many experienced solo travellers - especially later in life - the useful filter is not “can I do it?” but “how much friction do I want?” Check whether the hotel has a lift, how steep the final approach is, how far it really is from the station with luggage, and whether a late dinner creates a long walk home. Build one lighter day into an ambitious itinerary. Comfort is not the opposite of independence; it often protects it.</p>"""
friction_fr = """<h2 data-layer="solo-friction-50plus-2026-09-30">Si le confort compte plus que de se prouver quelque chose</h2><p>Pour beaucoup de voyageuses solo expérimentées - notamment avec l'âge - la bonne question n'est pas « est-ce que je peux ? », mais « combien de friction est-ce que je veux ? ». Vérifiez l'ascenseur, la pente réelle vers l'hôtel, la distance gare-hôtel avec une valise et le trajet après un dîner tardif. Gardez une journée plus légère dans un programme ambitieux. Le confort n'est pas l'opposé de l'indépendance ; il la protège souvent.</p>"""

digital_en = """<h2 data-layer="solo-digital-safety-2026-09-30">One boring backup that earns its place</h2><p>Keep the hotel address, a copy of your ID, bank emergency numbers and one trusted contact somewhere other than the phone itself. Avoid sensitive transactions on public Wi-Fi where possible. And save the French emergency numbers before you need them. <a href="/en/practical/safety-emergencies/">Open the Riviera Safety &amp; Emergencies page →</a></p>"""
digital_fr = """<h2 data-layer="solo-digital-safety-2026-09-30">Le plan B ennuyeux qui mérite sa place</h2><p>Gardez l'adresse de l'hôtel, une copie de vos papiers, les numéros d'opposition bancaire et un contact de confiance ailleurs que dans le téléphone lui-même. Évitez les opérations sensibles sur les Wi-Fi publics quand c'est possible. Et enregistrez les numéros d'urgence français avant d'en avoir besoin. <a href="/pratique/securite-urgences/">Ouvrir la page Sécurité &amp; urgences →</a></p>"""

def solo_en(s):
    s = before_once(s, '<h2>Six useful doors</h2>', research_en + friction_en, 'solo-research-context-2026-09-30')
    s = before_once(s, '<div class="sources"><h2>Sources checked</h2>', digital_en, 'solo-digital-safety-2026-09-30')
    return s

def solo_fr(s):
    s = before_once(s, '<h2>Six portes utiles</h2>', research_fr + friction_fr, 'solo-research-context-2026-09-30')
    s = before_once(s, '<div class="sources"><h2>Sources vérifiées</h2>', digital_fr, 'solo-digital-safety-2026-09-30')
    return s

practical_en = """<section class="v3-section practical-safety-entry" data-layer="safety-practical-entry-2026-09-30"><div class="wrap"><a class="practical-feature-card practical-feature-card--safety" href="/en/practical/safety-emergencies/"><span class="practical-feature-copy"><small>IF SOMETHING GOES WRONG</small><strong>Emergency numbers, theft, fire, sea rescue and the next useful step.</strong><p>Save the numbers once. Then forget this page unless you need it.</p><b>Open Safety &amp; Emergencies →</b></span></a></div></section>
"""
practical_fr = """<section class="v3-section practical-safety-entry" data-layer="safety-practical-entry-2026-09-30"><div class="wrap"><a class="practical-feature-card practical-feature-card--safety" href="/pratique/securite-urgences/"><span class="practical-feature-copy"><small>SI QUELQUE CHOSE TOURNE MAL</small><strong>Urgences, vol, incendie, secours en mer et la prochaine étape utile.</strong><p>Enregistrez les numéros une fois. Puis oubliez cette page sauf si vous en avez besoin.</p><b>Ouvrir Sécurité &amp; urgences →</b></span></a></div></section>
"""

def practical_patch_en(s):
    marker = '<section class="v3-section"><div class="wrap">\n<div class="section-heading"><div><p class="eyebrow">SOURCES &amp; STUDIES</p>'
    return before_once(s, marker, practical_en, 'safety-practical-entry-2026-09-30')

def practical_patch_fr(s):
    marker = '<section class="v3-section"><div class="wrap">\n<div class="section-heading"><div><p class="eyebrow">SOURCES &amp; ÉTUDES</p>'
    return before_once(s, marker, practical_fr, 'safety-practical-entry-2026-09-30')

def safety_sub_en(s):
    block = '<p class="mini-rule" data-layer="safety-general-link-2026-09-30">For medical, fire, sea rescue, theft and victim-support contacts beyond the solo-female context, <a href="/en/practical/safety-emergencies/">open the general Riviera Safety &amp; Emergencies page →</a></p>\n'
    return before_once(s, '<h2>Three things we would actually do</h2>', block, 'safety-general-link-2026-09-30')

def safety_sub_fr(s):
    block = '<p class="mini-rule" data-layer="safety-general-link-2026-09-30">Pour les contacts médicaux, incendie, secours en mer, vol et aide aux victimes au-delà du seul contexte femme solo, <a href="/pratique/securite-urgences/">ouvrez la page générale Sécurité &amp; urgences →</a></p>\n'
    return before_once(s, '<h2>Trois choses que nous ferions vraiment</h2>', block, 'safety-general-link-2026-09-30')

patch('en/solo-female-french-riviera/index.html', solo_en)
patch('cote-dazur-femme-solo/index.html', solo_fr)
patch('en/practical/index.html', practical_patch_en)
patch('pratique/index.html', practical_patch_fr)
patch('en/solo-female-french-riviera/safety/index.html', safety_sub_en)
patch('cote-dazur-femme-solo/securite/index.html', safety_sub_fr)

sp = ROOT / 'sitemap.xml'
if sp.exists():
    s = sp.read_text(encoding='utf-8')
    additions = []
    for url in ['https://www.mametas.com/en/practical/safety-emergencies/','https://www.mametas.com/pratique/securite-urgences/']:
        if url not in s:
            additions.append('<url><loc>'+url+'</loc></url>')
    if additions and '</urlset>' in s:
        s = s.replace('</urlset>', ''.join(additions) + '</urlset>')
        sp.write_text(s, encoding='utf-8')
        print('patched sitemap.xml')

print('safety / solo authority layer complete')
