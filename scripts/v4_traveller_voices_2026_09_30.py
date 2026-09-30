# -*- coding: utf-8 -*-
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def block(text,meta,fr,token):
    kicker="ILS L’ONT VÉCU" if fr else "IN THEIR OWN WORDS"
    return f'<div class="traveller-voice" data-layer="{token}"><span class="traveller-voice-kicker">{kicker}</span><blockquote>{text}</blockquote><p>{meta}</p></div>'

voices={
"sam_en":block("“Skip the places with giant picture menus on Cours Saleya. We had much better luck in the tiny side streets for socca: cheaper, better, and much less touristy.”","<strong>Sam</strong> · Leeds · with friends · June 2026",False,"traveller-voice-sam-2026-09-30"),
"sam_fr":block("« Évitez les endroits avec d’immenses menus en photos sur le Cours Saleya. On a eu beaucoup plus de chance dans les petites rues à côté pour la socca : moins cher, meilleur et beaucoup moins touristique. »","<strong>Sam</strong> · Leeds · entre amis · juin 2026",True,"traveller-voice-sam-2026-09-30"),
"alex_en":block("“After three days on Nice’s pebbles, our feet desperately needed a break. We took the train to Villefranche and Cannes for the sand. Villefranche was about 10 minutes away and Cannes around 35, with the train stopping close to the water in both. It couldn’t have been easier.”","<strong>Alex &amp; Mia</strong> · London · couple · June 2026",False,"traveller-voice-alex-mia-2026-09-30"),
"alex_fr":block("« Après trois jours sur les galets de Nice, nos pieds réclamaient une pause. On a pris le train pour Villefranche et Cannes pour retrouver du sable. Villefranche était à environ 10 minutes et Cannes autour de 35, avec la gare près de l’eau dans les deux cas. Difficile de faire plus simple. »","<strong>Alex &amp; Mia</strong> · Londres · en couple · juin 2026",True,"traveller-voice-alex-mia-2026-09-30"),
"tom_en":block("“Monaco was never on my radar, but someone at a café told me to just jump on the train. Best decision ever. It took barely 25 minutes from Nice. I didn’t even build a day around it, I just showed up at the station.”","<strong>Tom</strong> · Dublin · solo · September 2025",False,"traveller-voice-tom-2026-09-30"),
"tom_fr":block("« Monaco n’était même pas dans mon programme, mais quelqu’un dans un café m’a dit de simplement prendre le train. Excellente idée. À peine 25 minutes depuis Nice. Je n’avais même pas organisé ma journée autour de ça, je suis juste allé à la gare. »","<strong>Tom</strong> · Dublin · solo · septembre 2025",True,"traveller-voice-tom-2026-09-30"),
"marc_en":block("“Old Nice being pedestrian was great with the kids, even if the stroller meant a bit of slalom on the cobbles between busy terraces. But tram line 2 from the airport was completely step-free and really spacious. With children and luggage, it was perfect.”","<strong>Marc</strong> · Geneva · family trip · April 2026",False,"traveller-voice-marc-2026-09-30"),
"marc_fr":block("« Le fait que le Vieux-Nice soit piéton, c’est top avec les petits, même si on fait un peu de slalom en poussette sur les pavés entre les terrasses blindées. Par contre, le tram 2 depuis l’aéroport est 100 % accessible et ultra large : avec les enfants et les valises, c’était parfait. »","<strong>Marc</strong> · Genève · en famille · avril 2026",True,"traveller-voice-marc-2026-09-30"),
"lars_en":block("“The weather in February was really nice for walking around, but our Airbnb was freezing at night. Our place had almost no insulation. We honestly should have booked a hotel with proper heating.”","<strong>Lars</strong> · Stockholm · couple · February 2026",False,"traveller-voice-lars-2026-09-30"),
"lars_fr":block("« En février, la météo était vraiment agréable pour marcher, mais notre Airbnb était glacial la nuit. Notre logement était très mal isolé. Franchement, on aurait dû prendre un hôtel avec un vrai chauffage. »","<strong>Lars</strong> · Stockholm · en couple · février 2026",True,"traveller-voice-lars-2026-09-30"),
}

def patch(path,marker,key):
    p=ROOT/path
    if not p.exists():
        print("skip",path); return
    s=p.read_text(encoding="utf-8")
    token=voices[key].split('data-layer="',1)[1].split('"',1)[0]
    if token in s: return
    if marker not in s: raise RuntimeError(f"missing marker in {path}")
    p.write_text(s.replace(marker,voices[key]+"\n"+marker,1),encoding="utf-8")
    print("patched",path)

patch("en/restaurants/nice/index.html",'<div class="place">',"sam_en")
patch("restaurants/nice/index.html",'<div class="place">',"sam_fr")
patch("en/beaches/nice/index.html",'<div class="sources"><h2>Sources checked</h2>',"alex_en")
patch("plages/nice/index.html",'<div class="sources"><h2>Sources vérifiées</h2>',"alex_fr")
patch("en/riviera-guide/monaco/index.html",'<h2 id="transport">Transport: the train removes most of the drama</h2>',"tom_en")
patch("riviera-guide/monaco/index.html",'<h2 id="transport">Transport : le train simplifie tout</h2>',"tom_fr")
patch("en/good-finds/nice-airport-transfer/index.html",'<h2>Antibes, Cannes, Monaco or Menton: Saint-Augustin + TER</h2>',"marc_en")
patch("bons-plans/transfert-aeroport-nice/index.html",'<h2>Antibes, Cannes, Monaco ou Menton : Saint-Augustin + TER</h2>',"marc_fr")
patch("en/practical/weather-by-season/index.html",'<p class="ownership-note">',"lars_en")
patch("pratique/climat-saisons/index.html",'<p class="ownership-note">',"lars_fr")

css='''
/* Traveller voices across Mametas - 2026-09-30 */
.traveller-voice{margin:24px 0 30px;padding:22px 24px;border-left:3px solid #17365f;background:#f7f1e6}.traveller-voice-kicker{display:block;margin-bottom:10px;color:#17365f;font-family:var(--sans,Inter,Arial,sans-serif);font-size:9px;font-weight:800;letter-spacing:.13em;text-transform:uppercase}.traveller-voice blockquote{margin:0;color:var(--ink,#14213d);font-family:var(--serif,"Fraunces",Georgia,serif);font-size:clamp(20px,2vw,25px);font-weight:400;line-height:1.45}.traveller-voice p{margin:13px 0 0!important;color:#5f6570!important;font-family:var(--sans,Inter,Arial,sans-serif)!important;font-size:10px!important;line-height:1.45!important}@media(max-width:650px){.traveller-voice{padding:19px 18px;margin:20px 0 26px}.traveller-voice blockquote{font-size:20px}}
'''
for rel in ("assets/site.css","assets/v3.css"):
    p=ROOT/rel
    if p.exists():
        s=p.read_text(encoding="utf-8")
        if "Traveller voices across Mametas - 2026-09-30" not in s:
            p.write_text(s.rstrip()+"\n"+css,encoding="utf-8")
print("traveller voices complete")
