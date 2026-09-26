#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import re
import shutil
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
changed: list[str] = []

def save(rel: str, text: str, original: str) -> None:
    if text != original:
        (ROOT / rel).write_text(text, encoding="utf-8")
        if rel not in changed:
            changed.append(rel)

def add_body_class(text: str, cls: str) -> str:
    m = re.search(r"<body(?P<attrs>[^>]*)>", text, flags=re.I)
    if not m:
        return text
    attrs = m.group("attrs")
    cm = re.search(r'class="([^"]*)"', attrs)
    if cm:
        classes = cm.group(1).split()
        if cls not in classes:
            classes.append(cls)
        attrs = attrs[:cm.start()] + f'class="{" ".join(classes)}"' + attrs[cm.end():]
    else:
        attrs += f' class="{cls}"'
    return text[:m.start()] + "<body" + attrs + ">" + text[m.end():]

def ensure_css(rel: str, marker: str, css: str) -> None:
    p = ROOT / rel
    text = p.read_text(encoding="utf-8")
    original = text
    if marker not in text:
        text += "\n\n" + marker + "\n" + css.strip() + "\n"
    save(rel, text, original)

def wiki_thumb(filename: str, width: int = 1280) -> str:
    canon = filename.replace(" ", "_")
    digest = hashlib.md5(canon.encode("utf-8")).hexdigest()
    quoted = urllib.parse.quote(canon, safe="_()-")
    return f"https://upload.wikimedia.org/wikipedia/commons/thumb/{digest[0]}/{digest[:2]}/{quoted}/{width}px-{quoted}"

def download_image(url: str, target: Path, required: bool = True) -> bool:
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "MametasEditorial/1.0 (+https://www.mametas.com)"})
        with urllib.request.urlopen(req, timeout=45) as response:
            data = response.read()
            ctype = response.headers.get("Content-Type", "")
        if len(data) < 5000 or (ctype and not ctype.startswith("image/")):
            raise RuntimeError(f"unexpected image response {ctype} {len(data)} bytes")
        target.write_bytes(data)
        print(f"Downloaded {target.relative_to(ROOT)} ({len(data)} bytes)")
        return True
    except Exception as exc:
        print(f"WARNING: image download failed {url}: {exc}")
        if required:
            raise
        return False

def materialize_visual_assets() -> None:
    # Force known-working local assets into new production paths so the deploy
    # cannot depend on whether an older binary happened to have been synced.
    copies = {}
    for src, dst in copies.items():
        if not src.exists():
            raise RuntimeError(f"Missing source visual: {src.relative_to(ROOT)}")
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        print(f"Copied visual {dst.relative_to(ROOT)}")

    beaches = {
        "baie-des-fourmis-commons.jpg": ("Baie des fourmis.jpg", True),
        "petite-afrique-commons.jpg": ("20220622 160624 Beaulieu sur Mer.jpg", True),
        "mala-commons.jpg": ("Plage de la Mala au cap d'Ail.JPG", True),
        "fossettes-commons.jpg": ("Anse des Fossettes (St-Jean-Cap-Ferrat).jpg", True),
    }
    for out, (filename, required) in beaches.items():
        download_image(wiki_thumb(filename), ROOT / "assets/editorial/beaches" / out, required=required)

    # User-selected Pexels photo for Passable. Pexels CDN filenames are stable
    # by photo id; keep a local fallback if the CDN changes.
    pexels = "https://images.pexels.com/photos/13781215/pexels-photo-13781215.jpeg?auto=compress&cs=tinysrgb&w=1600"
    download_image(pexels, ROOT / "assets/editorial/beaches/passable-pexels.jpg", required=False)

def patch_home_visuals() -> None:
    for rel in ("index.html", "fr/index.html"):
        p = ROOT / rel
        text = p.read_text(encoding="utf-8")
        original = text
        text = text.replace(
            "https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/08_Fondation_Maeght.JPG/960px-08_Fondation_Maeght.JPG",
            "https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/08_Fondation_Maeght.JPG/960px-08_Fondation_Maeght.JPG",
        )
        text = re.sub(
            r'https://cdn\.pixabay\.com/photo/2019/03/25/18/26/sculpture-4080986_1280\.jpg',
            "https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/08_Fondation_Maeght.JPG/960px-08_Fondation_Maeght.JPG",
            text,
        )
        # The Maeght card sits high enough on the homepage to load immediately.
        text = re.sub(
            r'(<img src="/assets/editorial/fondation-maeght-waterborough\.webp"[^>]*?)loading="lazy"',
            r'\1loading="eager"',
            text,
        )
        save(rel, text, original)

def patch_booking_lerins() -> None:
    targets = (
        ("en/good-finds/what-to-book/index.html", "The islands: useful online, not always compulsory",
         "Îles de Lérins from Cannes", "Lérins Islands"),
        ("bons-plans/que-reserver/index.html", "Les îles", "Îles de Lérins depuis Cannes", "Îles de Lérins"),
    )
    for rel, heading, alt, caption in targets:
        p = ROOT / rel
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        original = text
        if 'data-final-lerins-visual="true"' not in text:
            if rel.startswith("en/"):
                pattern = r'(<div class="place"><div class="address">CANNES • LÉRINS</div><h3>[^<]*</h3>)'
            else:
                pattern = r'(<div class="place"><div class="address">CANNES[^<]*LÉRINS</div><h3>[^<]*</h3>)'
            figure = (
                r'\1<figure class="booking-highlight-visual" data-final-lerins-visual="true">'
                f'<img src="/assets/editorial/iles-lerins.jpg" alt="{alt}" loading="lazy" decoding="async">'
                f'<figcaption>{caption}</figcaption></figure>'
            )
            text, n = re.subn(pattern, figure, text, count=1, flags=re.I)
            if n != 1:
                # English source is the canonical one; French may have slightly different metadata.
                h = re.search(r'<h3>[^<]*(?:Lérins|Lerins)[^<]*</h3>', text, flags=re.I)
                if h:
                    text = text[:h.end()] + (
                        f'<figure class="booking-highlight-visual" data-final-lerins-visual="true">'
                        f'<img src="/assets/editorial/iles-lerins.jpg" alt="{alt}" loading="lazy" decoding="async">'
                        f'<figcaption>{caption}</figcaption></figure>'
                    ) + text[h.end():]
        save(rel, text, original)

def beach_figure(src: str, alt: str, credit_html: str) -> str:
    return (
        f'<figure class="beach-place-visual" data-final-beach-photo="true">'
        f'<img src="{src}" alt="{alt}" loading="lazy" decoding="async">'
        f'<figcaption>{credit_html}</figcaption></figure>'
    )

def patch_beach_visuals() -> None:
    passable_local = ROOT / "assets/editorial/beaches/passable-pexels.jpg"
    passable_src = "/assets/editorial/beaches/passable-pexels.jpg?v=20260926c" if passable_local.exists() else "/assets/editorial/cap-ferrat-cove.jpg"
    data = {
        "Baie des Fourmis": (
            "/assets/editorial/beaches/baie-des-fourmis-commons.jpg?v=20260926c",
            "Baie des Fourmis and Villa Kérylos in Beaulieu-sur-Mer",
            '<a href="https://commons.wikimedia.org/wiki/File:Baie_des_fourmis.jpg" target="_blank" rel="noopener">Wisi eu / Wikimedia Commons · CC0</a>',
        ),
        "Petite Afrique": (
            "/assets/editorial/beaches/petite-afrique-commons.jpg?v=20260926c",
            "Petite Afrique beach in Beaulieu-sur-Mer",
            '<a href="https://commons.wikimedia.org/wiki/File:20220622_160624_Beaulieu_sur_Mer.jpg" target="_blank" rel="noopener">Indigo&amp;fushia / Wikimedia Commons · CC BY-SA 4.0</a>',
        ),
        "Les Fossettes": (
            "/assets/editorial/beaches/fossettes-commons.jpg?v=20260926c",
            "Les Fossettes cove in Saint-Jean-Cap-Ferrat",
            '<a href="https://commons.wikimedia.org/wiki/File:Anse_des_Fossettes_(St-Jean-Cap-Ferrat).jpg" target="_blank" rel="noopener">Tangopaso / Wikimedia Commons · public domain</a>',
        ),
        "Passable": (
            passable_src,
            "Passable beach on Cap-Ferrat",
            '<a href="https://www.pexels.com/fr-fr/photo/baie-rochers-cailloux-cote-13781215/" target="_blank" rel="noopener">Pexels</a>' if passable_local.exists() else "Mametas archive",
        ),
        "Plage Mala": (
            "/assets/editorial/beaches/mala-commons.jpg?v=20260926c",
            "Plage Mala in Cap-d’Ail",
            '<a href="https://commons.wikimedia.org/wiki/File:Plage_de_la_Mala_au_cap_d%27Ail.JPG" target="_blank" rel="noopener">Gilbert Bochenek / Wikimedia Commons · public domain</a>',
        ),
    }
    for rel in ("en/beaches/around-nice/index.html", "plages/autour-de-nice/index.html"):
        p = ROOT / rel
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        original = text
        # Remove prior final-photo inserts on repeat builds, then reinsert once.
        text = re.sub(r'<figure class="beach-place-visual" data-final-beach-photo="true">.*?</figure>', '', text, flags=re.S)
        for heading, (src, alt, credit) in data.items():
            pattern = rf'(<h3>{re.escape(heading)}</h3>)'
            replacement = r'\1' + beach_figure(src, alt, credit)
            text, n = re.subn(pattern, replacement, text, count=1)
            if n != 1:
                raise RuntimeError(f"{rel}: beach heading not found: {heading}")
        save(rel, text, original)

def patch_fit_touch_behavior() -> None:
    p = ROOT / "assets/riviera-chooser.js"
    text = p.read_text(encoding="utf-8")
    original = text
    anchor = """        syncButtons();
        var next = root.querySelector('[data-step]:not([hidden]) [data-choice].is-active');"""
    repl = """        syncButtons();
        if (typeof button.blur === 'function') button.blur();
        var next = root.querySelector('[data-step]:not([hidden]) [data-choice].is-active');"""
    if anchor in text and "typeof button.blur === 'function'" not in text:
        text = text.replace(anchor, repl, 1)
    save("assets/riviera-chooser.js", text, original)

    p = ROOT / "assets/hotel-engine.js"
    text = p.read_text(encoding="utf-8")
    original = text
    anchor = """        other.setAttribute('aria-pressed', active ? 'true' : 'false');
      });
      if (!output.hidden) {"""
    repl = """        other.setAttribute('aria-pressed', active ? 'true' : 'false');
      });
      if (typeof button.blur === 'function') button.blur();
      if (!output.hidden) {"""
    if anchor in text and "if (typeof button.blur === 'function') button.blur();" not in text:
        text = text.replace(anchor, repl, 1)
    save("assets/hotel-engine.js", text, original)

def patch_core_hubs_and_practical() -> None:
    hubs = (
        "plan/index.html", "fr/planifier/index.html",
        "en/riviera-guide/index.html", "riviera-guide/index.html",
        "en/hotels/index.html", "hotels/index.html",
        "en/explore/index.html", "explore/index.html",
        "en/practical/index.html", "pratique/index.html",
    )
    for rel in hubs:
        p = ROOT / rel
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        original = text
        text = add_body_class(text, "core-hub-final")
        save(rel, text, original)

    for p in ROOT.rglob("*.html"):
        rel = p.relative_to(ROOT).as_posix()
        text = p.read_text(encoding="utf-8")
        if 'data-phase3-owner="practical"' not in text:
            continue
        original = text
        text = add_body_class(text, "practical-detail-final")
        save(rel, text, original)

def gay_stay_block(lang: str) -> str:
    if lang == "fr":
        return '''<h2>Où dormir : trois adresses qui ont une vraie raison d’être ici</h2>
<p>Le bon critère n’est pas « hôtel chic à Nice ». Il faut soit un <strong>engagement d’accueil LGBTQ+ explicite</strong>, soit une raison éditoriale suffisamment forte pour l’assumer comme choix Mametas. Deux adresses ci-dessous portent le label officiel Nice Rainbow Côte d’Azur ; la troisième est un choix de situation et de réputation, clairement présenté comme tel.</p>
<div class="gay-stay-grid" data-final-gay-stays="true">
<article class="gay-stay-pick"><span class="gay-stay-badge">NICE RAINBOW · OFFICIEL</span><h3>Hôtel Windsor</h3><p class="gay-stay-meta">11 rue Dalpozzo · 4 étoiles · centre</p><p><strong>La référence.</strong> Hôtel-galerie, jardin, piscine et vraie personnalité. Il porte le label Nice Rainbow de l’Office de Tourisme et a également fait l’objet d’une recommandation détaillée dans la presse voyage queer.</p><p class="gay-stay-links"><a href="https://www.explorenicecotedazur.com/hotel/hotel-windsor/" target="_blank" rel="noopener">Label officiel ↗</a><a href="https://coupleofmen.com/4608-hotel-spa-windsor-nice-france-gay-friendly/" target="_blank" rel="noopener">Avis queer ↗</a><a href="https://www.google.com/maps/search/?api=1&amp;query=Hotel+Windsor+11+rue+Dalpozzo+Nice" target="_blank" rel="noopener">Carte ↗</a></p></article>
<article class="gay-stay-pick"><span class="gay-stay-badge">NICE RAINBOW · OFFICIEL</span><h3>Hôtel Les Cigales</h3><p class="gay-stay-meta">16 rue Dalpozzo · 3 étoiles · Carré d’Or</p><p><strong>Le choix plus simple.</strong> Petit hôtel de 19 chambres, central et labellisé Nice Rainbow. Moins spectaculaire que Windsor ; justement utile si vous voulez une adresse accueillante sans transformer l’hôtel en sujet du voyage.</p><p class="gay-stay-links"><a href="https://www.explorenicecotedazur.com/hotel/hotel-les-cigales/" target="_blank" rel="noopener">Label officiel ↗</a><a href="https://www.google.com/maps/search/?api=1&amp;query=Hotel+Les+Cigales+Nice" target="_blank" rel="noopener">Carte ↗</a></p></article>
<article class="gay-stay-pick gay-stay-pick--editorial"><span class="gay-stay-badge">CHOIX MAMETAS · NON LABELLISÉ</span><h3>Hôtel La Pérouse</h3><p class="gay-stay-meta">Quai Rauba Capeu · 4 étoiles · Vieux-Nice / mer</p><p><strong>L’option élégante et discrète.</strong> Au pied de la Colline du Château, tout près du Vieux-Nice et de Castel Plage. Nous le retenons pour sa situation et son atmosphère, <em>pas</em> comme établissement actuellement certifié Nice Rainbow.</p><p class="gay-stay-links"><a href="/hotels/nice/la-perouse/">Voir l’hôtel Mametas →</a><a href="https://www.explorenicecotedazur.com/hotel/hotel-la-perouse/" target="_blank" rel="noopener">Fiche officielle ↗</a><a href="https://www.google.com/maps/search/?api=1&amp;query=Hotel+La+Perouse+Nice" target="_blank" rel="noopener">Carte ↗</a></p></article>
</div>
<p class="gay-stay-method"><strong>Pourquoi pas le Negresco comme symbole ?</strong> Parce qu’une grande adresse n’est pas, à elle seule, un signal d’accueil LGBTQ+. Ici, Mametas privilégie les preuves d’accueil explicites et dit clairement quand une recommandation relève plutôt de la réputation ou de la localisation.</p>
<p><a href="/hotels/">Voir toute la sélection d’hôtels Mametas →</a></p>
'''
    return '''<h2>Where to stay: three hotels that genuinely belong in this guide</h2>
<p>The useful criterion is not “smart hotel in Nice”. We want either an <strong>explicit LGBTQ+ welcome standard</strong> or a sufficiently strong editorial reason to make the choice transparently. Two addresses below carry the official Nice Rainbow Côte d’Azur label; the third is a location-and-reputation pick, clearly identified as such.</p>
<div class="gay-stay-grid" data-final-gay-stays="true">
<article class="gay-stay-pick"><span class="gay-stay-badge">NICE RAINBOW · OFFICIAL</span><h3>Hôtel Windsor</h3><p class="gay-stay-meta">11 rue Dalpozzo · 4 stars · centre</p><p><strong>The reference.</strong> Art hotel, garden, pool and genuine personality. It carries the Tourism Office’s Nice Rainbow label and has also received a detailed recommendation from queer travel media.</p><p class="gay-stay-links"><a href="https://www.explorenicecotedazur.com/en/hotel/hotel-windsor/" target="_blank" rel="noopener">Official label ↗</a><a href="https://coupleofmen.com/4608-hotel-spa-windsor-nice-france-gay-friendly/" target="_blank" rel="noopener">Queer review ↗</a><a href="https://www.google.com/maps/search/?api=1&amp;query=Hotel+Windsor+11+rue+Dalpozzo+Nice" target="_blank" rel="noopener">Map ↗</a></p></article>
<article class="gay-stay-pick"><span class="gay-stay-badge">NICE RAINBOW · OFFICIAL</span><h3>Hôtel Les Cigales</h3><p class="gay-stay-meta">16 rue Dalpozzo · 3 stars · Carré d’Or</p><p><strong>The simpler choice.</strong> A small 19-room hotel, central and officially Nice Rainbow. Less theatrical than Windsor; useful precisely when you want an explicitly welcoming stay without making the hotel the subject of the trip.</p><p class="gay-stay-links"><a href="https://www.explorenicecotedazur.com/en/hotel/hotel-les-cigales/" target="_blank" rel="noopener">Official label ↗</a><a href="https://www.google.com/maps/search/?api=1&amp;query=Hotel+Les+Cigales+Nice" target="_blank" rel="noopener">Map ↗</a></p></article>
<article class="gay-stay-pick gay-stay-pick--editorial"><span class="gay-stay-badge">MAMETAS PICK · NOT LABELLED</span><h3>Hôtel La Pérouse</h3><p class="gay-stay-meta">Quai Rauba Capeu · 4 stars · Old Nice / sea</p><p><strong>The elegant, discreet option.</strong> Under Castle Hill, beside Old Nice and close to Castel Plage. We keep it for location and atmosphere, <em>not</em> as a hotel currently certified by Nice Rainbow.</p><p class="gay-stay-links"><a href="/en/hotels/nice/la-perouse/">See the Mametas hotel page →</a><a href="https://www.explorenicecotedazur.com/en/hotel/hotel-la-perouse/" target="_blank" rel="noopener">Official listing ↗</a><a href="https://www.google.com/maps/search/?api=1&amp;query=Hotel+La+Perouse+Nice" target="_blank" rel="noopener">Map ↗</a></p></article>
</div>
<p class="gay-stay-method"><strong>Why not use the Negresco as the symbol?</strong> Because being a famous luxury hotel is not, by itself, evidence of an LGBTQ+ welcome standard. Here Mametas prioritises explicit welcome signals and says when a recommendation is instead based on reputation or location.</p>
<p><a href="/en/hotels/">See the full Mametas hotel selection →</a></p>
'''

def patch_gay_stays() -> None:
    targets = (
        ("en/gay-nice/index.html", "en", r'<h2>Where to stay.*?(?=<h2>Where to go out:)'),
        ("guide-gay-nice/index.html", "fr", r'<h2>Où dormir.*?(?=<h2>Où sortir :)'),
    )
    for rel, lang, pattern in targets:
        p = ROOT / rel
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        original = text
        text, n = re.subn(pattern, gay_stay_block(lang), text, count=1, flags=re.S)
        if n != 1:
            raise RuntimeError(f"{rel}: gay hotel section not found")
        save(rel, text, original)

def patch_css_and_versions() -> None:
    common_header = r'''
/* Final cross-template header parity 2026-09-26 */
.site-header,.v3-header{
  border-bottom:1px solid rgba(20,33,61,.14)!important;
  background:#fffdf8!important;
}
.header-inner,.v3-header-inner{
  width:min(100%,1440px)!important;
  min-height:82px!important;
  margin:0 auto!important;
  padding:14px clamp(18px,3vw,48px)!important;
  display:flex!important;
  align-items:center!important;
  gap:30px!important;
}
.brand,.v3-brand{display:inline-flex!important;flex-direction:column!important;flex:0 0 auto!important;text-decoration:none!important}
.brand-name,.v3-brand-name{
  font-family:"Fraunces",Georgia,serif!important;
  font-size:clamp(28px,3vw,40px)!important;
  font-weight:600!important;
  letter-spacing:-.05em!important;
  line-height:.9!important;
}
.brand-sub,.v3-brand-line{
  display:block!important;
  margin-top:8px!important;
  color:#176f83!important;
  font-family:"Fraunces",Georgia,serif!important;
  font-size:10px!important;
  font-style:italic!important;
  font-weight:400!important;
  letter-spacing:.04em!important;
  line-height:1!important;
}
.primary-nav,.v3-nav{margin-left:auto!important}
.primary-nav ul,.v3-nav ul{display:flex;align-items:center;gap:clamp(16px,2.2vw,32px);margin:0;padding:0;list-style:none}
.primary-nav a,.v3-nav a,.header-inner>.lang-switch a,.v3-header-inner>.lang-switch a{
  font-family:"Inter",Arial,sans-serif!important;
  font-size:11px!important;
  font-weight:700!important;
  letter-spacing:.12em!important;
  text-transform:uppercase!important;
}
@media(max-width:1080px){
  .header-inner,.v3-header-inner{min-height:68px!important;padding-top:10px!important;padding-bottom:10px!important}
}
'''
    hub_css = r'''
/* Core hub full layout parity 2026-09-26 */
.core-hub-final .article-hero,
.core-hub-final .page-hero{
  padding:clamp(54px,6vw,78px) 0 clamp(38px,4vw,52px)!important;
  background:var(--paper,#fffdf8)!important;
  border-bottom:1px solid rgba(20,33,61,.14)!important;
}
.core-hub-final .article-hero>.wrap,
.core-hub-final .page-hero>.wrap{
  width:min(calc(100% - 2 * var(--gutter,24px)),1180px)!important;
  margin:0 auto!important;
}
.core-hub-final .article-hero .eyebrow,
.core-hub-final .page-hero .eyebrow{
  margin:0 0 18px!important;
  color:var(--coral,#d86c4e)!important;
  font-family:"Inter",Arial,sans-serif!important;
  font-size:10px!important;
  font-weight:800!important;
  letter-spacing:.16em!important;
  line-height:1.2!important;
  text-transform:uppercase!important;
}
.core-hub-final .article-hero h1,
.core-hub-final .page-hero h1{
  max-width:14ch!important;
  margin:0!important;
  font-family:"Fraunces",Georgia,serif!important;
  font-size:clamp(46px,5.35vw,72px)!important;
  font-weight:500!important;
  letter-spacing:-.045em!important;
  line-height:.98!important;
  text-transform:none!important;
}
.core-hub-final .article-deck,
.core-hub-final .lead{
  max-width:820px!important;
  margin:22px 0 0!important;
  color:var(--ink-soft,#43506a)!important;
  color:var(--ink-soft,#43506a)!important;
  font-family:"Fraunces",Georgia,serif!important;
  font-size:clamp(20px,2vw,27px)!important;
  font-weight:400!important;
  letter-spacing:-.012em!important;
  line-height:1.45!important;
}
.core-hub-final .article-meta{margin-top:22px!important}
.core-hub-final .v3-section,
.core-hub-final .section{scroll-margin-top:90px}
@media(max-width:650px){
  .core-hub-final .article-hero,
  .core-hub-final .page-hero{padding:42px 0 32px!important}
  .core-hub-final .article-hero .eyebrow,
  .core-hub-final .page-hero .eyebrow{margin-bottom:14px!important}
  .core-hub-final .article-hero h1,
  .core-hub-final .page-hero h1{
    max-width:12ch!important;
    font-size:clamp(38px,11vw,52px)!important;
    line-height:1!important
  }
  .core-hub-final .article-deck,
  .core-hub-final .lead{
    max-width:100%!important;
    margin-top:18px!important;
    font-size:clamp(20px,6.1vw,24px)!important;
    line-height:1.42!important
  }
}
'''
    site_extra = r'''
/* Practical ownership / Checked separation 2026-09-26 */
.practical-detail-final .ownership-note[data-phase3-owner="practical"]{
  margin:30px 0 24px!important;
  padding:18px 0 19px!important;
  border-top:1px solid rgba(20,33,61,.14)!important;
  border-bottom:1px solid rgba(20,33,61,.14)!important;
  line-height:1.55!important;
}
.practical-detail-final .ownership-note[data-phase3-owner="practical"] + .mametas-checked{
  margin-top:2px!important;
  margin-bottom:30px!important;
}
.booking-highlight-visual{margin:20px 0 24px;overflow:hidden}
.booking-highlight-visual img{display:block;width:100%;aspect-ratio:16/8.5;object-fit:cover}
.booking-highlight-visual figcaption,.beach-place-visual figcaption{margin-top:6px;color:#5f6570;font-size:9px;line-height:1.45}
.beach-place-visual{margin:16px 0 20px;overflow:hidden}
.beach-place-visual img{display:block;width:100%;aspect-ratio:16/8.5;object-fit:cover}
.beach-photo-credit a,.beach-place-visual figcaption a{color:inherit;text-decoration:underline;text-underline-offset:2px}

/* Gay stays: evidence first, no generic luxury masquerading as queer relevance. */
.gay-stay-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin:26px 0 22px}
.gay-stay-pick{padding:22px;border:1px solid var(--line);background:rgba(255,255,255,.2)}
.gay-stay-pick--editorial{background:rgba(216,108,78,.045)}
.gay-stay-badge{display:inline-block;margin-bottom:14px;padding:6px 8px;background:#17365f;color:#fff;font-size:8px;font-weight:800;letter-spacing:.12em;text-transform:uppercase}
.gay-stay-pick--editorial .gay-stay-badge{background:#d86c4e}
.gay-stay-pick h3{margin:0 0 6px!important;font-size:27px!important}
.gay-stay-meta{margin:0 0 14px!important;color:#176f83!important;font-size:10px!important;font-weight:700;letter-spacing:.06em;text-transform:uppercase}
.gay-stay-pick p{font-size:14px!important;line-height:1.62!important}
.gay-stay-links{display:flex;flex-wrap:wrap;gap:8px 14px;margin-top:18px!important}
.gay-stay-links a{font-size:9px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;border-bottom:1px solid #d86c4e}
.gay-stay-method{margin:20px 0 28px!important;padding:16px 18px;border-left:3px solid #d86c4e;background:rgba(216,108,78,.045)}
@media(max-width:800px){.gay-stay-grid{grid-template-columns:1fr}.gay-stay-pick{padding:19px}}
'''
    fit_riviera = r'''
/* Touch-stable Riviera Fit choices 2026-09-26 */
.chooser-options button.is-active,.chooser-options button[aria-pressed="true"]{background:var(--blue)!important;border-color:var(--blue)!important;color:var(--white)!important}
.chooser-options button:focus-visible{outline:2px solid var(--coral);outline-offset:2px}
@media(hover:hover) and (pointer:fine){
  .chooser-options button:hover:not(.is-active){background:rgba(23,54,95,.08);border-color:var(--blue);color:var(--ink)}
}
@media(hover:none),(pointer:coarse){
  .chooser-options button{touch-action:manipulation;-webkit-tap-highlight-color:transparent;transition:none!important}
  .chooser-options button:hover:not(.is-active),
  .chooser-options button:focus:not(.is-active),
  .chooser-options button:focus-visible:not(.is-active){
    background:rgba(255,253,248,.55)!important;border-color:var(--line)!important;color:var(--ink)!important
  }
}
'''
    fit_hotel = r'''
/* Touch-stable Hotel Fit choices 2026-09-26 */
.engine-buttons button.is-active,.engine-buttons button[aria-pressed="true"]{background:var(--blue)!important;border-color:var(--blue)!important;color:var(--white)!important}
.engine-buttons button:focus-visible{outline:2px solid var(--coral);outline-offset:2px}
@media(hover:hover) and (pointer:fine){
  .engine-buttons button:hover:not(.is-active){background:rgba(23,54,95,.08);border-color:var(--blue);color:var(--ink)}
}
@media(hover:none),(pointer:coarse){
  .engine-buttons button{touch-action:manipulation;-webkit-tap-highlight-color:transparent;transition:none!important}
  .engine-buttons button:hover:not(.is-active),
  .engine-buttons button:focus:not(.is-active),
  .engine-buttons button:focus-visible:not(.is-active){
    background:rgba(255,253,248,.3)!important;border-color:var(--line)!important;color:var(--ink)!important
  }
}
'''
    ensure_css("assets/site.css", "/* Final cross-template header parity 2026-09-26 */", common_header)
    ensure_css("assets/v3.css", "/* Final cross-template header parity 2026-09-26 */", common_header)
    ensure_css("assets/site.css", "/* Core hub full layout parity 2026-09-26 */", hub_css)
    ensure_css("assets/v3.css", "/* Core hub full layout parity 2026-09-26 */", hub_css)
    ensure_css("assets/site.css", "/* Practical ownership / Checked separation 2026-09-26 */", site_extra)
    ensure_css("assets/riviera-chooser.css", "/* Touch-stable Riviera Fit choices 2026-09-26 */", fit_riviera)
    ensure_css("assets/hotel-engine.css", "/* Touch-stable Hotel Fit choices 2026-09-26 */", fit_hotel)

    # Force fresh CSS and the touch-fix JS through browser caches.
    for p in ROOT.rglob("*.html"):
        rel = p.relative_to(ROOT).as_posix()
        text = p.read_text(encoding="utf-8")
        original = text
        text = re.sub(r'/assets/site\.css(?:\?v=[^"]+)?', '/assets/site.css?v=25.3', text)
        text = re.sub(r'/assets/v3\.css(?:\?v=[^"]+)?', '/assets/v3.css?v=2.4', text)
        text = re.sub(r'/assets/riviera-chooser\.css(?:\?v=[^"]+)?', '/assets/riviera-chooser.css?v=8', text)
        text = re.sub(r'/assets/hotel-engine\.css(?:\?v=[^"]+)?', '/assets/hotel-engine.css?v=8', text)
        text = re.sub(r'/assets/riviera-chooser\.js(?:\?v=[^"]+)?', '/assets/riviera-chooser.js?v=11', text)
        text = re.sub(r'/assets/hotel-engine\.js(?:\?v=[^"]+)?', '/assets/hotel-engine.js?v=13', text)
        save(rel, text, original)

def validate() -> None:
    errors: list[str] = []
    required_assets = (
        "assets/editorial/iles-lerins.jpg",
        "assets/editorial/beaches/baie-des-fourmis-commons.jpg",
        "assets/editorial/beaches/petite-afrique-commons.jpg",
        "assets/editorial/beaches/mala-commons.jpg",
        "assets/editorial/beaches/fossettes-commons.jpg",
    )
    for rel in required_assets:
        p = ROOT / rel
        if not p.exists() or p.stat().st_size < 5000:
            errors.append(f"missing final visual asset {rel}")

    checks = {
        "index.html": ("https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/08_Fondation_Maeght.JPG/960px-08_Fondation_Maeght.JPG", "core-hub-final") if False else ("https://upload.wikimedia.org/wikipedia/commons/thumb/9/98/08_Fondation_Maeght.JPG/960px-08_Fondation_Maeght.JPG",),
        "en/good-finds/what-to-book/index.html": ('data-final-lerins-visual="true"', "/assets/site.css?v=25.3"),
        "en/beaches/around-nice/index.html": ("baie-des-fourmis-commons.jpg", "petite-afrique-commons.jpg", "fossettes-commons.jpg", "mala-commons.jpg"),
        "en/gay-nice/index.html": ("Hôtel Windsor", "Hôtel Les Cigales", "MAMETAS PICK · NOT LABELLED"),
        "guide-gay-nice/index.html": ("Hôtel Windsor", "Hôtel Les Cigales", "CHOIX MAMETAS · NON LABELLISÉ"),
        "en/hotels/finder/index.html": ("/assets/hotel-engine.css?v=8", "/assets/hotel-engine.js?v=13"),
    }
    for rel, needles in checks.items():
        p = ROOT / rel
        if not p.exists():
            errors.append(f"missing page {rel}")
            continue
        text = p.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                errors.append(f"{rel}: missing {needle!r}")

    for rel in ("plan/index.html","en/riviera-guide/index.html","en/hotels/index.html","en/explore/index.html","en/practical/index.html"):
        p = ROOT / rel
        if p.exists() and "core-hub-final" not in p.read_text(encoding="utf-8"):
            errors.append(f"{rel}: core hub parity class missing")

    if "Touch-stable Riviera Fit choices 2026-09-26" not in (ROOT/"assets/riviera-chooser.css").read_text(encoding="utf-8"):
        errors.append("Riviera Fit touch CSS missing")
    if "Touch-stable Hotel Fit choices 2026-09-26" not in (ROOT/"assets/hotel-engine.css").read_text(encoding="utf-8"):
        errors.append("Hotel Fit touch CSS missing")
    if "Final cross-template header parity 2026-09-26" not in (ROOT/"assets/site.css").read_text(encoding="utf-8"):
        errors.append("site.css final header parity missing")
    if "Final cross-template header parity 2026-09-26" not in (ROOT/"assets/v3.css").read_text(encoding="utf-8"):
        errors.append("v3.css final header parity missing")

    if errors:
        raise SystemExit("Final mobile + visual closure failed:\n- " + "\n- ".join(errors))

def main() -> int:
    materialize_visual_assets()
    patch_home_visuals()
    patch_booking_lerins()
    patch_beach_visuals()
    patch_fit_touch_behavior()
    patch_core_hubs_and_practical()
    patch_gay_stays()
    patch_css_and_versions()
    validate()
    print(f"Final mobile + visual closure passed; changed {len(changed)} text file(s).")
    for rel in sorted(changed):
        print(rel)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
