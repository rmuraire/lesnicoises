#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mametas final audit, lot 4B: high-value EN/FR content parity.

This pass is intentionally explicit rather than generic. It closes the parity
gaps Claude found on the Gay Riviera family and the generated Solo Female hub.
The French additions are translations of content already present in the
English version or vice versa; no new practical facts are invented.
"""
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]

def rw(rel,fn):
    p=ROOT/rel
    if not p.exists():
        print("skip missing",rel); return False
    s=p.read_text(encoding="utf-8",errors="ignore")
    n=fn(s)
    if n!=s:
        p.write_text(n,encoding="utf-8"); print("patched",rel); return True
    print("unchanged",rel); return False

def insert_before(s,marker,block,guard):
    if guard in s: return s
    if marker not in s: raise RuntimeError("insert marker missing: "+marker[:80])
    return s.replace(marker,block+marker,1)

def patch_gay_root_fr():
    rel="cote-dazur-gay/index.html"
    def fn(s):
        hotel_block='''<h2>Trois façons utiles de dormir</h2>
<p>Nice reste la base par défaut, mais le choix devient plus simple si vous commencez par le profil du séjour.</p>
<div class="hotel-grid">
<div class="hotel-card"><div class="hotel-card-media"><img src="/assets/hotels/refonte-2026/hotel-windsor.webp" alt="Le Windsor à Nice" loading="lazy"/></div><div class="hotel-card-body"><span class="kicker">NICE RAINBOW · CENTRE</span><h3>Le Windsor</h3><p>Du caractère, un jardin et une base centrale qui fonctionne sans voiture.</p><a class="more" href="https://www.kqzyfj.com/click-101875476-15734754?url=https%3A%2F%2Fwww.booking.com%2Fhotel%2Ffr%2Fhotel-windsor-nice1.html" target="_blank" rel="sponsored nofollow noopener">Voir les tarifs sur Booking.com ↗</a></div></div>
<div class="hotel-card"><div class="hotel-card-media"><img src="/assets/hotels/gay-v4/hotel-ozz-happyculture.webp" alt="Hotel Ozz by HappyCulture à Nice" loading="lazy"/></div><div class="hotel-card-body"><span class="kicker">BUDGET · NICE-VILLE</span><h3>Hotel Ozz</h3><p>Le choix pratique à budget plus serré, surtout si le train fait partie du séjour.</p><a class="more" href="https://www.kqzyfj.com/click-101875476-15734754?url=https%3A%2F%2Fwww.booking.com%2Fhotel%2Ffr%2Fnormandie.html" target="_blank" rel="sponsored nofollow noopener">Voir les tarifs sur Booking.com ↗</a></div></div>
<div class="hotel-card"><div class="hotel-card-media"><img src="/assets/hotels/gay-v4/la-connexion-gay-men-only.webp" alt="La Connexion Gay Men Only à Peymeinade" loading="lazy"/></div><div class="hotel-card-body"><span class="kicker">GAY MEN ONLY · ARRIÈRE-PAYS</span><h3>La Connexion</h3><p>À choisir quand une retraite explicitement gay compte davantage que la logistique urbaine.</p><a class="more" href="https://www.kqzyfj.com/click-101875476-15734754?url=https%3A%2F%2Fwww.booking.com%2Fhotel%2Ffr%2Fla-connexion-gay-men-only-peymeinade.html" target="_blank" rel="sponsored nofollow noopener">Voir les tarifs sur Booking.com ↗</a></div></div>
</div>
<p><a href="/cote-dazur-gay/ou-dormir/"><strong>Voir la décision complète pour choisir où dormir →</strong></a></p>
<h2>Le reste de la côte, en un coup d’œil</h2>
<div class="fact-grid"><div class="fact"><b>Cannes</b><span>À utiliser comme base lorsque l’ouest de la Riviera est vraiment le voyage. La couche LGBTQ+ est moins profonde qu’à Nice.</span></div><div class="fact"><b>Saint-Tropez</b><span>Un détour volontaire pour le village, Pampelonne et l’ambiance, pas l’ossature d’un premier séjour sans voiture.</span></div><div class="fact"><b>Monaco + Menton</b><span>Deux journées faciles en train vers l’est depuis Nice.</span></div><div class="fact"><b>Villefranche + Cap-Ferrat</b><span>Les journées de respiration : baie, sentiers, eau et rythme plus lent.</span></div><div class="fact"><b>Antibes</b><span>Une journée simple vers l’ouest depuis Nice et une association naturelle avec Cannes.</span></div></div>
<h2>FAQ</h2>
<div class="place"><h3>La Côte d’Azur est-elle gay-friendly ?</h3><p class="why">Nice possède l’infrastructure LGBTQ+ la plus explicite de cette partie de la côte. Ailleurs, la question utile est surtout de savoir où vous voulez passer la journée.</p></div>
<div class="place"><h3>Nice ou Cannes pour un séjour gay ?</h3><p class="why">Nice pour la couche communautaire la plus forte et la meilleure base sans voiture. Cannes lorsque l’ouest de la Riviera est le cœur du séjour.</p></div>
<div class="place"><h3>Monaco est-il gay-friendly ?</h3><p class="why">Pour la plupart des visiteurs, Monaco fonctionne comme une excursion plutôt que comme une destination LGBTQ+. Utilisez Nice pour la scène et Monaco pour Monaco.</p></div>
<div class="place"><h3>Quand a lieu la Pride de Nice ?</h3><p class="why">Les dates peuvent bouger. Vérifiez l’agenda LGBTQIA+ officiel avant de réserver autour d’un événement précis.</p></div>
<div class="place"><h3>Faut-il une voiture ?</h3><p class="why">Pas pour un premier séjour basé à Nice. Train, tram et marche couvrent efficacement le cœur de la côte.</p></div>
'''
        return insert_before(s,'<h2>Quatre portes utiles</h2>',hotel_block,'Trois façons utiles de dormir')
    rw(rel,fn)

def patch_gay_itinerary_fr():
    rel="cote-dazur-gay/itineraire-5-jours/index.html"
    def fn(s):
        block='''<h2>Où dormir pour cet itinéraire</h2>
<p>Nice sert ici de base de transport : l’accès à la gare compte davantage que sur une page consacrée à la vie nocturne. <a href="/cote-dazur-gay/ou-dormir/"><strong>Voir le guide complet où dormir →</strong></a></p>
<div class="hotel-grid">
<div class="hotel-card"><div class="hotel-card-media"><img src="/assets/hotels/gay-v4/hotel-ozz-happyculture.webp" alt="Hotel Ozz by HappyCulture à Nice" loading="lazy"/></div><div class="hotel-card-body"><span class="kicker">NICE-VILLE · BUDGET</span><h3>Hotel Ozz</h3><p>La base la plus simple à budget serré lorsque vous utiliserez souvent le train.</p><a class="more" href="https://www.kqzyfj.com/click-101875476-15734754?url=https%3A%2F%2Fwww.booking.com%2Fhotel%2Ffr%2Fnormandie.html" target="_blank" rel="sponsored nofollow noopener">Voir les tarifs sur Booking.com ↗</a></div></div>
<div class="hotel-card"><div class="hotel-card-media"><img src="/assets/hotels/refonte-2026/hotel-windsor.webp" alt="Le Windsor à Nice" loading="lazy"/></div><div class="hotel-card-body"><span class="kicker">NICE RAINBOW · 4★ · CENTRE</span><h3>Le Windsor, Jungle Art Hotel</h3><p>Artistique, central et plus personnel qu’un hôtel de chaîne. Environ 800 mètres de Nice-Ville et 500 mètres de la Promenade.</p><a class="more" href="https://www.kqzyfj.com/click-101875476-15734754?url=https%3A%2F%2Fwww.booking.com%2Fhotel%2Ffr%2Fhotel-windsor-nice1.html" target="_blank" rel="sponsored nofollow noopener">Voir les tarifs sur Booking.com ↗</a></div></div>
</div>
'''
        return insert_before(s,'<h2>Jour 1',block,'Où dormir pour cet itinéraire')
    rw(rel,fn)

def patch_gay_nice_fr_faq():
    rel="guide-gay-nice/index.html"
    def fn(s):
        block='''<h2>FAQ</h2>
<div class="place"><h3>Quels sont les meilleurs bars gay à Nice ?</h3><p class="why">Ramdam fonctionne bien comme point de départ social ; Le Glam et Le 6 sont les options les plus évidentes pour finir plus tard. Vérifiez la programmation avant de traverser la ville pour une soirée précise.</p></div>
<div class="place"><h3>Y a-t-il un quartier gay à Nice ?</h3><p class="why">Pas sous la forme d’un quartier fermé sur lui-même. Le regroupement utile passe par le Vieux-Nice, Garibaldi et le côté Port, avec d’autres adresses dans le centre.</p></div>
<div class="place"><h3>À quelle heure ferment les clubs ?</h3><p class="why">Certaines fiches actuelles vont jusqu’à environ 5 h, mais les nuits d’ouverture et les horaires changent. Utilisez l’agenda officiel et les pages des établissements pour la date de votre sortie.</p></div>
'''
        return insert_before(s,'<h2>Une version simple sur 48 heures</h2>',block,'Quels sont les meilleurs bars gay à Nice ?')
    rw(rel,fn)

def patch_where_to_stay_en_markup():
    rel="en/gay-french-riviera/where-to-stay/index.html"
    def fn(s):
        blue='''<div class="place"><h3>Blue Angels Bed &amp; Breakfast: Nice</h3><div class="address">8 rue Assalit · central Nice</div><p class="why">Two rooms, four guests maximum, and an official description as a 100% gay B&amp;B. This is much closer to a community stay than a conventional labelled hotel.</p><p class="practical">Men only · Nice Rainbow · very small capacity · direct booking.</p></div>
'''
        gardens='''<div class="place"><h3>Les Jardins de Baquis: Nice</h3><div class="address">3 avenue Baquis · central Nice</div><p class="why">A quiet gay-friendly guest room with a private shower room and balcony, central enough to reach the sea and centre on foot.</p><p class="practical">Nice Rainbow · one room · direct booking.</p></div>
'''
        # Replace the two malformed place stubs independently. Upstream language
        # cleanup may change dash punctuation, so anchor on names/addresses only.
        p1=re.compile(r'<div class="place"><h3>Blue Angels Bed &amp; Breakfast[^<]*</h3><div class="address">8 rue Assalit · central Nice</div>[\s\S]*?(?=<div class="place"><h3>Les Jardins de Baquis)',re.I)
        p2=re.compile(r'<div class="place"><h3>Les Jardins de Baquis[^<]*</h3><div class="address">3 avenue Baquis · central Nice</div>[\s\S]*?(?=<h2>Labelled and lower budget</h2>)',re.I)
        if p1.search(s): s=p1.sub(blue,s,count=1)
        if p2.search(s): s=p2.sub(gardens,s,count=1)
        return s
    rw(rel,fn)

def patch_where_to_stay_fr_faq_and_hotels():
    rel="cote-dazur-gay/ou-dormir/index.html"
    def fn(s):
        hotel_block='''<h2>Deux compléments utiles à Nice</h2>
<div class="hotel-grid">
<div class="hotel-card"><div class="hotel-card-media"><img src="/assets/hotels/refonte-2026/hotel-windsor.webp" alt="Le Windsor à Nice" loading="lazy"/></div><div class="hotel-card-body"><span class="kicker">NICE RAINBOW · 4★ · CENTRE</span><h3>Le Windsor, Jungle Art Hotel</h3><p>Le plus de personnalité dans la catégorie 4 étoiles centrale : jardin, art et bonne logistique sans voiture.</p><a class="btn btn--primary" href="/hotels/nice/hotel-windsor/">Lire notre avis</a><a class="btn btn--affiliate" href="https://www.kqzyfj.com/click-101875476-15734754?url=https%3A%2F%2Fwww.booking.com%2Fhotel%2Ffr%2Fhotel-windsor-nice1.html" target="_blank" rel="sponsored nofollow noopener">Voir les tarifs ↗</a></div></div>
<div class="hotel-card"><div class="hotel-card-media"><img src="/assets/hotels/la-perouse/hero.jpg" alt="Hôtel La Pérouse à Nice" loading="lazy"/></div><div class="hotel-card-body"><span class="kicker">CHOIX MAMETAS · VIEUX-NICE · MER</span><h3>Hôtel La Pérouse</h3><p>Pas labellisé Nice Rainbow, mais l’un des meilleurs emplacements pour le Vieux-Nice, la Colline du Château et le côté Port.</p><a class="btn btn--primary" href="/hotels/nice/la-perouse/">Lire notre avis</a><a class="btn btn--affiliate" href="https://expedia.com/affiliates/nice-hotels-hotel-la-perouse-nice.iaOhaln" target="_blank" rel="sponsored nofollow noopener">Voir les tarifs ↗</a></div></div>
</div>
'''
        if 'Deux compléments utiles à Nice' not in s:
            m=re.search(r'<h2[^>]*>\s*2\.\s*Vous voulez une vraie maison d[’\']hôtes gay à Nice\s*[\u202f\u00a0 ]*\?\s*</h2>',s,re.I)
            if not m: raise RuntimeError("FR gay stay section marker missing")
            s=s[:m.start()]+hotel_block+s[m.start():]
        faq='''<h2>FAQ</h2>
<div class="place"><h3>Qu’est-ce que le label Nice Rainbow ?</h3><p class="why">Un programme officiel d’accueil de Nice Côte d’Azur. C’est un signal utile d’accueil LGBTQ+ explicite ; cela ne signifie ni hôtel réservé aux gays ni clientèle majoritairement LGBTQ+.</p></div>
<div class="place"><h3>Existe-t-il des hôtels gay-only près de Nice ?</h3><p class="why">L’option dédiée la plus claire de ce guide est La Connexion, dans l’arrière-pays cannois. À Nice, Blue Angels est un très petit B&amp;B réservé aux hommes plutôt qu’un hôtel classique.</p></div>
<div class="place"><h3>Quel quartier de Nice choisir pour la vie nocturne gay ?</h3><p class="why">Vieux-Nice, Garibaldi et le côté Port gardent les adresses du soir les plus proches. Si la nuit compte, privilégiez la possibilité de rentrer à pied plutôt qu’un code postal en bord de mer.</p></div>
'''
        if 'Qu’est-ce que le label Nice Rainbow ?' not in s:
            m=re.search(r'<div class="verdict"><span class="label">DÉCISION SUIVANTE</span>',s,re.I)
            if not m: raise RuntimeError("FR gay stay next-decision marker missing")
            s=s[:m.start()]+faq+s[m.start():]
        return s
    rw(rel,fn)

def patch_gay_beaches_fr():
    rel="cote-dazur-gay/plages-sans-voiture/index.html"
    def fn(s):
        block='''<h2>Pour la plus belle journée de baignade, quittez le centre de Nice</h2>
<p><strong>Villefranche-sur-Mer et Saint-Jean-Cap-Ferrat sont de meilleurs choix lorsque le but est simplement une belle eau et une journée plus lente.</strong> Ce ne sont pas des « plages gay », et elles n’ont pas besoin de l’être. Cette distinction permet de séparer les signaux liés à l’identité du meilleur choix de baignade.</p>
<div class="fact-grid"><div class="fact"><b>Villefranche</b><span>Facile en train ou en bus, baie calme et simple sans voiture.</span></div><div class="fact"><b>Cap-Ferrat</b><span>Plus intéressant pour les criques, le sentier côtier et une vraie journée lente.</span></div><div class="fact"><b>Rester à Nice</b><span>Castel ou Coco Beach si vous ne voulez aucune logistique supplémentaire.</span></div></div>
'''
        if 'Pour la plus belle journée de baignade' not in s:
            m=re.search(r'<h2[^>]*>\s*Laquelle choisir\s*[\u202f\u00a0 ]*\?\s*</h2>',s,re.I)
            if not m: raise RuntimeError("FR gay beaches choice marker missing")
            s=s[:m.start()]+block+s[m.start():]
        faq='''<h2>FAQ</h2>
<div class="place"><h3>Y a-t-il une plage gay à Nice ?</h3><p class="why">Castel est l’option centrale la plus claire avec un signal Nice Rainbow explicite. Coco Beach est un lieu de baignade public plus informel, sans label gay.</p></div>
<div class="place"><h3>Saint-Laurent-d’Èze est-elle naturiste ?</h3><p class="why">C’est l’option la plus orientée naturisme de ce guide, mais l’accès demande davantage de préparation que les plages niçoises.</p></div>
<div class="place"><h3>Peut-on y aller sans voiture ?</h3><p class="why">Oui pour les plages couvertes ici, mais « possible » ne veut pas dire « sans effort ». Castel est la plus simple ; Saint-Laurent-d’Èze demande le plus d’organisation.</p></div>
'''
        if 'Y a-t-il une plage gay à Nice' not in s:
            marker='<div class="sources">'
            pos=s.find(marker)
            if pos < 0: raise RuntimeError("FR gay beaches sources container missing")
            s=s[:pos]+faq+s[pos:]
        return s
    rw(rel,fn)

def patch_solo_fr_if_generated():
    rel="cote-dazur-femme-solo/index.html"
    p=ROOT/rel
    if not p.exists():
        print("solo FR not materialised at this stage; skip"); return
    s=p.read_text(encoding="utf-8",errors="ignore"); old=s
    if "Trois hôtels faciles" not in s:
        block='''<h2>Trois hôtels faciles pour un premier séjour solo</h2>
<div class="hotel-grid">
<div class="hotel-card"><div class="hotel-card-media"><img src="/assets/hotels/villa-victoria/hero.jpg" alt="Villa Victoria à Nice" loading="lazy"/></div><div class="hotel-card-body"><h3>Villa Victoria</h3><p>Central, avec jardin, pour rester à pied du centre sans dormir dans le Vieux-Nice.</p><a class="btn btn--primary" href="/hotels/nice/villa-victoria/">Lire notre avis</a></div></div>
<div class="hotel-card"><div class="hotel-card-body"><h3>Hotel 66</h3><p>Pratique près de Nice-Ville lorsque les excursions en train comptent beaucoup.</p><a class="btn btn--primary" href="/hotels/nice/hotel-66/">Lire notre avis</a></div></div>
<div class="hotel-card"><div class="hotel-card-media"><img src="/assets/hotels/la-perouse/hero.jpg" alt="Hôtel La Pérouse à Nice" loading="lazy"/></div><div class="hotel-card-body"><h3>Hôtel La Pérouse</h3><p>Le choix plus cher si le Vieux-Nice, la mer et un retour à pied après dîner sont prioritaires.</p><a class="btn btn--primary" href="/hotels/nice/la-perouse/">Lire notre avis</a></div></div>
</div>
'''
        marker='<h2>FAQ</h2>'
        if marker in s: s=s.replace(marker,block+marker,1)
    if s!=old:
        p.write_text(s,encoding="utf-8"); print("patched",rel)

def validate():
    checks={
      "cote-dazur-gay/index.html":("Trois façons utiles de dormir","La Côte d’Azur est-elle gay-friendly ?"),
      "cote-dazur-gay/itineraire-5-jours/index.html":("Où dormir pour cet itinéraire","Le Windsor, Jungle Art Hotel"),
      "guide-gay-nice/index.html":("Quels sont les meilleurs bars gay à Nice ?","À quelle heure ferment les clubs ?"),
      "cote-dazur-gay/ou-dormir/index.html":("Deux compléments utiles à Nice","Qu’est-ce que le label Nice Rainbow ?"),
      "cote-dazur-gay/plages-sans-voiture/index.html":("Pour la plus belle journée de baignade","Y a-t-il une plage gay à Nice ?"),
    }
    for rel,tokens in checks.items():
        s=(ROOT/rel).read_text(encoding="utf-8",errors="ignore")
        missing=[x for x in tokens if x not in s]
        if missing: raise RuntimeError(f"{rel}: missing lot4B tokens {missing}")
    en=(ROOT/"en/gay-french-riviera/where-to-stay/index.html").read_text(encoding="utf-8",errors="ignore")
    for token in ("Two rooms, four guests maximum","A quiet gay-friendly guest room"):
        if token not in en:
            raise RuntimeError("EN gay stay description repair missing: "+token)
    print("Claude final audit lot 4B parity validation passed.")

def main():
    patch_gay_root_fr()
    patch_gay_itinerary_fr()
    patch_gay_nice_fr_faq()
    patch_where_to_stay_en_markup()
    patch_where_to_stay_fr_faq_and_hotels()
    patch_gay_beaches_fr()
    patch_solo_fr_if_generated()
    validate()

if __name__=="__main__":
    main()
