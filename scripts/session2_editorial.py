#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def replace(path, old, new):
    p = ROOT / path
    text = p.read_text(encoding='utf-8')
    if old not in text:
        raise SystemExit(f'Missing expected text in {path}: {old[:80]}')
    p.write_text(text.replace(old, new, 1), encoding='utf-8')

# Homepage: one promise, no duplicate pitch.
replace('index.html',
'''<p class="hero-promise">Where to stay, what to book, how to move — and what really is not worth your time.</p><p class="hero-note">You’re very cute, coming all this way to see us on the Riviera. We won’t make you a local, pichoun. But listen carefully and we might save you a few cagades.</p>''',
'''<p class="hero-promise">We’ll tell you where to stay, what’s worth your time and how to get around. We won’t make you a local, pitchoun. But we might save you a few cagades.</p>''')
replace('fr/index.html',
'''<p class="hero-promise">Où dormir, quoi réserver, comment circuler — et ce qui ne mérite vraiment pas votre temps.</p><p class="hero-note">C’est très mignon de venir nous voir sur la Riviera. On ne fera pas de vous un enfant du pays, pichoun. Mais écoutez bien : on vous évitera peut-être quelques cagades.</p>''',
'''<p class="hero-promise">On vous dira où dormir, ce qui mérite vraiment votre temps et comment circuler. On ne fera pas de vous un enfant du pays, pitchoun. Mais on peut vous éviter quelques cagades.</p>''')

# Make the homepage practical path explicitly sequential.
replace('index.html',
'''<section class="v3-section practical"><div class="wrap"><p class="eyebrow">Practical essentials</p><div class="practical-grid"><div class="practical-title"><h2>Remove the friction.</h2></div>''',
'''<section class="v3-section practical"><div class="wrap"><p class="eyebrow">Your next decisions</p><div class="practical-grid"><div class="practical-title"><h2>Arrive. Sleep. Move. Then wander.</h2><p>Start with the boring decisions. They are what make the good bits feel easy.</p></div>''')
replace('fr/index.html',
'''<section class="v3-section practical"><div class="wrap"><p class="eyebrow">Essentiels pratiques</p><div class="practical-grid"><div class="practical-title"><h2>Enlever les frottements.</h2></div>''',
'''<section class="v3-section practical"><div class="wrap"><p class="eyebrow">Vos prochaines décisions</p><div class="practical-grid"><div class="practical-title"><h2>Arriver. Dormir. Circuler. Puis flâner.</h2><p>Réglez d’abord les décisions ennuyeuses. C’est précisément ce qui rend le reste facile.</p></div>''')

# Five-day plan: turn each day into a useful onward path.
repls_en = [
('''<p><strong>Do:</strong> leave one meal unplanned so the first day can absorb a late flight or an early collapse.</p></div>''', '''<p><strong>Do:</strong> leave one meal unplanned so the first day can absorb a late flight or an early collapse.</p><p><a class="inline-decision-link" href="/en/riviera-guide/nice/">Next decision: understand Nice before choosing what to skip →</a></p></div>'''),
('''<p><strong>The catch:</strong> gradients and walking time matter. Choose one main Cap-Ferrat objective rather than treating the peninsula as a checklist.</p></div>''', '''<p><strong>The catch:</strong> gradients and walking time matter. Choose one main Cap-Ferrat objective rather than treating the peninsula as a checklist.</p><p><a class="inline-decision-link" href="/en/riviera-guide/villefranche-cap-ferrat/">Choose your Villefranche / Cap-Ferrat version →</a></p></div>'''),
('''<p><strong>Do:</strong> check live rail information on the morning of travel. The route is frequent, but works and disruption do not consult your mood board.</p></div>''', '''<p><strong>Do:</strong> check live rail information on the morning of travel. The route is frequent, but works and disruption do not consult your mood board.</p><p><a class="inline-decision-link" href="/en/riviera-guide/monaco/">Decide how much Monaco you actually want →</a></p></div>'''),
('''<p><strong>The catch:</strong> Cap d’Antibes is not the same thing as central Antibes. Reaching coves around the cape changes the transport calculation.</p></div>''', '''<p><strong>The catch:</strong> Cap d’Antibes is not the same thing as central Antibes. Reaching coves around the cape changes the transport calculation.</p><p><a class="inline-decision-link" href="/en/riviera-guide/antibes/">See who Antibes suits — and who should keep going to Cannes →</a></p></div>'''),
('''<p>A multimodal SudAzur Explore Pass currently covers train, tram and bus travel in the Alpes-Maritimes and Monaco for 3, 7 or 14 days. Compare it with individual fares for your exact sequence; “pass” is not French for “automatically cheaper”.</p>''', '''<p>A multimodal SudAzur Explore Pass currently covers train, tram and bus travel in the Alpes-Maritimes and Monaco for 3, 7 or 14 days. Compare it with individual fares for your exact sequence; “pass” is not French for “automatically cheaper”.</p>\n          <div class="verdict-box"><span>Train, bus, taxi or car?</span><p><strong>Train:</strong> default for Antibes, Cannes, Monaco and Menton. <strong>Bus:</strong> use it when geography leaves the railway behind — Èze village and parts of Cap-Ferrat are the obvious examples. <strong>Taxi / ride-hail:</strong> buy back time for awkward first/last kilometres or late returns, not for routine coast-hopping. <strong>Car:</strong> earn the hassle only for inland villages, remote coves or a day whose value depends on several poorly connected stops.</p><p><a class="inline-decision-link" href="/en/hotels/without-a-car/">Then choose a base that works without a car →</a></p></div>''')]
for old,new in repls_en: replace('plan/five-days-nice-no-car/index.html', old, new)

repls_fr = [
('''<p><strong>À faire :</strong> laissez un repas sans réservation afin que la première journée absorbe un vol tardif ou une fatigue précoce.</p></div>''', '''<p><strong>À faire :</strong> laissez un repas sans réservation afin que la première journée absorbe un vol tardif ou une fatigue précoce.</p><p><a class="inline-decision-link" href="/riviera-guide/nice/">Décision suivante : comprendre Nice avant de choisir ce qu’on peut ignorer →</a></p></div>'''),
('''<p><strong>Le compromis :</strong> le dénivelé et les temps de marche comptent. Choisissez un objectif principal sur la presqu’île.</p></div>''', '''<p><strong>Le compromis :</strong> le dénivelé et les temps de marche comptent. Choisissez un objectif principal sur la presqu’île.</p><p><a class="inline-decision-link" href="/riviera-guide/villefranche-cap-ferrat/">Choisir sa version Villefranche / Cap-Ferrat →</a></p></div>'''),
('''<p><strong>À faire :</strong> vérifiez le trafic ferroviaire le matin même. La ligne est fréquente ; les travaux et perturbations ne consultent pas votre tableau Pinterest.</p></div>''', '''<p><strong>À faire :</strong> vérifiez le trafic ferroviaire le matin même. La ligne est fréquente ; les travaux et perturbations ne consultent pas votre tableau Pinterest.</p><p><a class="inline-decision-link" href="/riviera-guide/monaco/">Décider de la dose de Monaco qui vous convient →</a></p></div>'''),
('''<p><strong>Le compromis :</strong> le cap d’Antibes n’est pas le centre d’Antibes. Rejoindre les criques du cap modifie le calcul des transports.</p></div>''', '''<p><strong>Le compromis :</strong> le cap d’Antibes n’est pas le centre d’Antibes. Rejoindre les criques du cap modifie le calcul des transports.</p><p><a class="inline-decision-link" href="/riviera-guide/antibes/">Voir à qui Antibes convient — et qui devrait continuer vers Cannes →</a></p></div>'''),
('''<p>Le pass multimodal SudAzur Explore couvre actuellement train, tram et bus dans les Alpes-Maritimes et à Monaco pendant 3, 7 ou 14 jours. Comparez son prix avec des billets individuels pour votre parcours exact ; « pass » ne signifie pas automatiquement « moins cher ».</p>''', '''<p>Le pass multimodal SudAzur Explore couvre actuellement train, tram et bus dans les Alpes-Maritimes et à Monaco pendant 3, 7 ou 14 jours. Comparez son prix avec des billets individuels pour votre parcours exact ; « pass » ne signifie pas automatiquement « moins cher ».</p>\n        <div class="verdict-box"><span>Train, bus, taxi ou voiture ?</span><p><strong>Train :</strong> choix par défaut pour Antibes, Cannes, Monaco et Menton. <strong>Bus :</strong> dès que la géographie abandonne le rail — Èze village et certaines parties de Cap-Ferrat sont les exemples évidents. <strong>Taxi / VTC :</strong> pour racheter du temps sur un premier ou dernier kilomètre pénible ou un retour tardif, pas pour longer la côte par habitude. <strong>Voiture :</strong> acceptez les contraintes seulement pour l’arrière-pays, les criques isolées ou une journée composée de plusieurs étapes mal reliées.</p><p><a class="inline-decision-link" href="/hotels/sans-voiture/">Puis choisir une base qui fonctionne vraiment sans voiture →</a></p></div>''')]
for old,new in repls_fr: replace('fr/planifier/cinq-jours-nice-sans-voiture/index.html', old, new)

print('Session 2 editorial transformations applied.')
