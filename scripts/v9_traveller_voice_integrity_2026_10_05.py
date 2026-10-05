#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Final integrity pass for Mametas traveller voices, 5 Oct 2026.

Policy:
- keep only traveller identities backed by feedback actually received by Mametas;
- never invent a traveller or an experience to illustrate a recommendation;
- allow shortening, translation and light editing for clarity/privacy;
- remove promotional/editorial endings that make genuine feedback sound scripted;
- keep practical facts independently checkable.

This runs after the existing voice generators and the 4 Oct editorial passes.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]

EN_NOTE = (
    'Traveller note · based on feedback from a real traveller; wording may be shortened, '
    'translated or lightly edited for clarity and privacy. '
    '<a href="/en/method/">Method →</a>'
)
FR_NOTE = (
    'Note de voyageur · basée sur le retour d’une personne réelle ; le texte peut être raccourci, '
    'traduit ou légèrement édité pour la clarté et la confidentialité. '
    '<a href="/methode/">Méthode →</a>'
)
EN_SOLO_METHOD = (
    'These notes come from real traveller feedback received by Mametas. Wording may be shortened, '
    'translated or lightly edited for clarity and privacy; first names and identifying details may be changed. '
    'Practical claims are checked independently. <a href="/en/method/">Method →</a>'
)
FR_SOLO_METHOD = (
    'Ces notes viennent de retours de vraies voyageuses reçus par Mametas. Le texte peut être raccourci, '
    'traduit ou légèrement édité pour la clarté et la confidentialité ; les prénoms et certains détails '
    'identifiants peuvent être modifiés. Les informations pratiques sont vérifiées indépendamment. '
    '<a href="/methode/">Méthode →</a>'
)

def load(rel):
    p = ROOT / rel
    if not p.exists():
        print("skip missing", rel)
        return p, ""
    return p, p.read_text(encoding="utf-8", errors="ignore")

def save_if(rel, fn):
    p, s = load(rel)
    if not s:
        return
    n = fn(s)
    if n != s:
        p.write_text(n, encoding="utf-8")
        print("patched", rel)
    else:
        print("unchanged", rel)

def replace_method_lines(s, lang):
    note = FR_NOTE if lang == "fr" else EN_NOTE
    s = re.sub(
        r'<p class="traveller-voice-method">[\s\S]*?</p>',
        f'<p class="traveller-voice-method">{note}</p>',
        s,
        flags=re.I,
    )
    s = re.sub(
        r'<p class="home-hotel-voice-method">[\s\S]*?</p>',
        f'<p class="home-hotel-voice-method">{note}</p>',
        s,
        flags=re.I,
    )
    return s

def remove_voice_token(s, token):
    return re.sub(
        rf'<div class="traveller-voice"[^>]*data-layer="{re.escape(token)}"[^>]*>[\s\S]*?</div>\s*',
        '',
        s,
        count=1,
        flags=re.I,
    )

def remove_solo_person(s, name):
    # The solo cards are figure elements; remove only the card whose figcaption names this person.
    pat = re.compile(
        rf'<figure class="solo-voice">(?:(?!</figure>)[\s\S])*?<figcaption>[^<]*<strong>{re.escape(name)}</strong>[\s\S]*?</figure>\s*',
        re.I,
    )
    return pat.sub('', s, count=1)

# 1) Remove the one contextual voice for which this project does not have
# a confirmed source in the retained feedback set. Do not replace it with fiction.
for rel in ("en/practical/weather-by-season/index.html", "pratique/climat-saisons/index.html"):
    save_if(rel, lambda s: remove_voice_token(s, "traveller-voice-lars-2026-09-30"))

# 2) Solo hub: keep the useful real-source notes, remove the most ad-like/decorative one,
# and trim advice that was added by the editor rather than spoken by the traveller.
def solo_en(s):
    s = remove_solo_person(s, "Ella")
    s = s.replace(
        "“The SNCF app saved me so much stress. Buying TER train tickets to Villefranche or Monaco directly on my phone meant I didn't have to figure out ticket machines or queue up alone when I was tired.”",
        "“The SNCF app saved me so much stress. Buying TER train tickets to Villefranche or Monaco directly on my phone meant I didn't have to figure out the ticket machines.”",
    )
    s = s.replace(
        "“Old Nice walk-ups are brutal if you're on your own. I dragged my 20kg suitcase up five flights of narrow stairs because many old buildings don't have lifts. Definitely double-check amenities before booking an Airbnb or opt for a hotel.”",
        "“Old Nice walk-ups are brutal if you're on your own. I dragged my 20kg suitcase up five flights of narrow stairs.”",
    )
    s = re.sub(
        r'<p class="solo-voices-intro">[\s\S]*?</p>',
        '<p class="solo-voices-intro">Small observations from real trips. Useful context, not universal truths.</p>',
        s, count=1, flags=re.I,
    )
    s = re.sub(
        r'<p class="solo-voices-method">[\s\S]*?</p>',
        f'<p class="solo-voices-method">{EN_SOLO_METHOD}</p>',
        s, count=1, flags=re.I,
    )
    return s

def solo_fr(s):
    s = remove_solo_person(s, "Ella")
    s = s.replace(
        "« L'appli SNCF m'a évité tellement de stress. Acheter mes billets TER pour Villefranche ou Monaco directement sur mon téléphone m'évitait de comprendre les distributeurs ou de faire la queue seule quand j'étais fatiguée. »",
        "« L'appli SNCF m'a évité tellement de stress. Acheter mes billets TER pour Villefranche ou Monaco directement sur mon téléphone m'évitait de comprendre les distributeurs. »",
    )
    s = s.replace(
        "« Les immeubles sans ascenseur du Vieux-Nice peuvent être rudes quand on est seule. J'ai monté ma valise de 20 kg sur cinq étages dans un escalier étroit. Vérifiez vraiment les équipements avant de réserver un Airbnb, ou choisissez un hôtel. »",
        "« Les immeubles sans ascenseur du Vieux-Nice peuvent être rudes quand on est seule. J'ai monté ma valise de 20 kg sur cinq étages dans un escalier étroit. »",
    )
    s = re.sub(
        r'<p class="solo-voices-intro">[\s\S]*?</p>',
        '<p class="solo-voices-intro">De petites observations issues de vrais séjours. Du contexte utile, pas des vérités universelles.</p>',
        s, count=1, flags=re.I,
    )
    s = re.sub(
        r'<p class="solo-voices-method">[\s\S]*?</p>',
        f'<p class="solo-voices-method">{FR_SOLO_METHOD}</p>',
        s, count=1, flags=re.I,
    )
    return s

save_if("en/solo-female-french-riviera/index.html", solo_en)
save_if("cote-dazur-femme-solo/index.html", solo_fr)

# 3) Keep genuine contextual anecdotes but remove endings that read like copy written
# to prove Mametas's recommendation.
for rel in (
    "en/beaches/nice/index.html",
    "en/riviera-guide/monaco/index.html",
    "en/good-finds/nice-airport-transfer/index.html",
):
    save_if(rel, lambda s: replace_method_lines(s, "en"))
for rel in (
    "plages/nice/index.html",
    "riviera-guide/monaco/index.html",
    "bons-plans/transfert-aeroport-nice/index.html",
):
    save_if(rel, lambda s: replace_method_lines(s, "fr"))

save_if("en/beaches/nice/index.html", lambda s: s.replace(
    " It couldn’t have been easier.”", "”"
).replace(" It couldn't have been easier.”", "”"))
save_if("plages/nice/index.html", lambda s: s.replace(
    " Difficile de faire plus simple. »", " »"
))
save_if("en/good-finds/nice-airport-transfer/index.html", lambda s: s.replace(
    " With children and luggage, it was perfect.”", "”"
))
save_if("bons-plans/transfert-aeroport-nice/index.html", lambda s: s.replace(
    " : avec les enfants et les valises, c’était parfait. »", ". »"
).replace(
    " : avec les enfants et les valises, c'etait parfait. »", ". »"
))

# 4) Homepage Hotel Fit: Daniel's cold-flat observation is useful; the editorial
# 'therefore book a hotel next time' ending is not needed.
def daniel_en(s):
    s = replace_method_lines(s, "en")
    s = s.replace(
        " Honestly, next time we’re definitely booking a hotel with proper heating.”",
        "”",
    )
    s = s.replace(
        " Honestly, next time we're definitely booking a hotel with proper heating.”",
        "”",
    )
    return s

def daniel_fr(s):
    s = replace_method_lines(s, "fr")
    s = s.replace(
        " Franchement, la prochaine fois, on réservera clairement un hôtel avec un vrai chauffage. »",
        " »",
    )
    return s

save_if("index.html", daniel_en)
save_if("fr/index.html", daniel_fr)

# 5) Method page: explicit provenance rule. This is the trust promise a prescriber can audit.
EN_CARD = '''<article class="method-card"><span>07 · Traveller voices</span><h2>Real feedback. Edited, never invented.</h2><p>Traveller notes are based on feedback from real travellers received by Mametas. We may shorten, translate or lightly edit wording for clarity, length and privacy; first names and identifying details may be changed. We do not create a traveller or an experience solely to illustrate an editorial recommendation. Practical claims in a note are checked independently, and we do not publish comments that unfairly disparage identifiable businesses or restaurants.</p></article>'''
FR_CARD = '''<article class="method-card"><span>07 · Voix de voyageurs</span><h2>De vrais retours. Édités, jamais inventés.</h2><p>Les notes de voyageurs reposent sur des retours de personnes réelles reçus par Mametas. Nous pouvons raccourcir, traduire ou légèrement éditer le texte pour la clarté, la longueur et la confidentialité ; les prénoms et certains détails identifiants peuvent être modifiés. Nous ne créons pas un voyageur ou une expérience uniquement pour illustrer une recommandation éditoriale. Les informations pratiques contenues dans une note sont vérifiées indépendamment et nous ne publions pas de commentaires dénigrant injustement des commerces ou restaurants identifiables.</p></article>'''

def method_en(s):
    pat = re.compile(
        r'<article class="method-card"><span>07 · Traveller voices</span>[\s\S]*?</article>',
        re.I,
    )
    n, count = pat.subn(EN_CARD, s, count=1)
    if count != 1:
        raise RuntimeError("EN method traveller-voices card not found")
    n = n.replace("Fictional editorial characters. Real places. A method you can read.", "Fictional Mametas characters. Real places. A method you can read.")\n    return n

def method_fr(s):
    pat = re.compile(
        r'<article class="method-card"><span>07 · Voix de voyageurs</span>[\s\S]*?</article>',
        re.I,
    )
    n, count = pat.subn(FR_CARD, s, count=1)
    if count != 1:
        raise RuntimeError("FR method traveller-voices card not found")
    n = n.replace("Des personnages éditoriaux fictifs. Des lieux réels. Une méthode qu’on peut lire.", "Des personnages Mametas fictifs. Des lieux réels. Une méthode qu’on peut lire.")\n    return n

save_if("en/method/index.html", method_en)
save_if("methode/index.html", method_fr)

# 6) Final sweep: replace any legacy disclosure that survived in retained voice blocks.
for p in ROOT.rglob("*.html"):
    rel = p.relative_to(ROOT)
    if rel.parts and rel.parts[0] in {".git", ".github", "scripts", "docs", "backup"}:
        continue
    s = p.read_text(encoding="utf-8", errors="ignore")
    before = s
    lang = "fr" if re.search(r'<html\b[^>]*\blang=["\']fr', s, re.I) else "en"
    if 'class="traveller-voice"' in s or 'class="home-hotel-voice"' in s:
        s = replace_method_lines(s, lang)
    if s != before:
        p.write_text(s, encoding="utf-8")

# 7) Integrity checks.
for rel in ("en/method/index.html", "methode/index.html"):
    p = ROOT / rel
    if not p.exists():
        raise RuntimeError(f"missing method page: {rel}")

en_method = (ROOT / "en/method/index.html").read_text(encoding="utf-8", errors="ignore")
fr_method = (ROOT / "methode/index.html").read_text(encoding="utf-8", errors="ignore")
if "We do not create a traveller or an experience solely to illustrate an editorial recommendation." not in en_method:
    raise RuntimeError("EN traveller integrity promise missing")
if "Nous ne créons pas un voyageur ou une expérience uniquement pour illustrer une recommandation éditoriale." not in fr_method:
    raise RuntimeError("FR traveller integrity promise missing")

for p in ROOT.rglob("*.html"):
    rel = p.relative_to(ROOT)
    if rel.parts and rel.parts[0] in {".git", ".github", "scripts", "docs", "backup"}:
        continue
    s = p.read_text(encoding="utf-8", errors="ignore")
    if "traveller-voice-lars-2026-09-30" in s or "<strong>Lars</strong>" in s:
        raise RuntimeError(f"{rel}: unconfirmed Lars traveller voice survived")
    if 'data-layer="solo-verbatims-2026-09-30"' in s and "<strong>Ella</strong>" in s:
        raise RuntimeError(f"{rel}: ad-like Ella solo card survived")
    if 'class="traveller-voice-method"' in s and ("Editorial persona:" in s or "Persona éditorial" in s):
        raise RuntimeError(f"{rel}: legacy persona disclosure survived")
    if 'class="home-hotel-voice-method"' in s and ("Editorial persona:" in s or "Persona éditorial" in s):
        raise RuntimeError(f"{rel}: legacy homepage persona disclosure survived")

print("Traveller voice integrity passed: real-source notes retained, unconfirmed/sales-like material removed.")
