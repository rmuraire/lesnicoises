#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
changed=[]

def save(path: Path, text: str, original: str):
    if text != original:
        path.write_text(text, encoding="utf-8")
        rel=path.relative_to(ROOT).as_posix()
        if rel not in changed: changed.append(rel)

def patch_monaco_fr():
    p=ROOT/"riviera-guide/monaco/index.html"
    text=p.read_text(encoding="utf-8"); original=text
    m=re.search(r'<div class="destination-practical">.*?</div></div></div>', text, flags=re.S)
    if m and m.start() < text.find('<header class="v3-header"'):
        block=m.group(0)
        text=text[:m.start()]+text[m.end():]
        hero=re.search(r'<header class="article-hero">.*?</header>', text, flags=re.S)
        if not hero: raise RuntimeError("Monaco FR article hero not found")
        hero_text=hero.group(0)
        pos=hero_text.rfind('</div></header>')
        if pos < 0: raise RuntimeError("Monaco FR hero close not found")
        hero_text=hero_text[:pos]+block+hero_text[pos:]
        text=text[:hero.start()]+hero_text+text[hero.end():]
    save(p,text,original)

HOTEL_SLUGS=("cannes","antibes","menton","villefranche-sur-mer","monaco","saint-paul-de-vence","beaulieu-sur-mer","mougins","saint-tropez")

def patch_hotel_lang_switches():
    for slug in HOTEL_SLUGS:
        for rel, lang in ((f"hotels/{slug}/index.html","fr"),(f"en/hotels/{slug}/index.html","en")):
            p=ROOT/rel
            if not p.exists(): continue
            text=p.read_text(encoding="utf-8"); original=text
            if lang=="fr":
                switch=(f'<div class="lang-switch"><a aria-current="page" class="active" href="/hotels/{slug}/">FR</a>'
                        f'<span>|</span><a class="muted" href="/en/hotels/{slug}/">EN</a></div>')
            else:
                switch=(f'<div class="lang-switch"><a class="muted" href="/hotels/{slug}/">FR</a>'
                        f'<span>|</span><a aria-current="page" class="active" href="/en/hotels/{slug}/">EN</a></div>')
            text,n=re.subn(r'<div class="lang-switch">.*?</div>',switch,text,count=1,flags=re.S)
            if n!=1: raise RuntimeError(f"{rel}: lang switch not found")
            save(p,text,original)

def patch_header_nav():
    replacements_en={
        'href="/#plan"':'href="/plan/"',
        'href="/plan/five-days-nice-no-car/"':'href="/plan/"',
        'href="/en/riviera-chooser/"':'href="/plan/"',
        'href="/stay/nice/"':'href="/en/hotels/"',
    }
    replacements_fr={
        'href="/fr/#planifier"':'href="/fr/planifier/"',
        'href="/fr/planifier/cinq-jours-nice-sans-voiture/"':'href="/fr/planifier/"',
        'href="/riviera-chooser/"':'href="/fr/planifier/"',
        'href="/fr/dormir/nice/"':'href="/hotels/"',
        'href="/fr/#maintenant"':'href="/bons-plans/"',
        'href="/fr/#lieux"':'href="/riviera-guide/"',
    }
    for p in ROOT.rglob("*.html"):
        rel=p.relative_to(ROOT).as_posix()
        text=p.read_text(encoding="utf-8"); original=text
        hm=re.search(r'<header class="(?:v3-header|site-header)">.*?</header>',text,flags=re.S)
        if not hm: continue
        h=hm.group(0)
        reps=replacements_en if rel.startswith("en/") or rel=="index.html" or rel.startswith("plan/") else replacements_fr
        for old,new in reps.items(): h=h.replace(old,new)
        # Restaurants legacy header: Explore must point to the Explore hub, not Restaurants.
        if rel=="en/restaurants/index.html":
            h=h.replace('aria-current="page" href="/en/restaurants/"','href="/en/explore/"')
        if rel=="restaurants/index.html":
            h=h.replace('aria-current="page" href="/restaurants/"','href="/explore/"')
        text=text[:hm.start()]+h+text[hm.end():]
        save(p,text,original)

def patch_footers():
    targets={
        "en/explore/index.html":(
            ('href="/plan/five-days-nice-no-car/"','href="/plan/"'),
            ('>Five days, no car<','>Plan your trip<'),
            ('href="/stay/nice/"','href="/en/hotels/"'),
            ('>Where to stay<','>Choose a hotel<'),
        ),
        "explore/index.html":(
            ('href="/fr/planifier/cinq-jours-nice-sans-voiture/"','href="/fr/planifier/"'),
            ('>Cinq jours sans voiture<','>Planifier le séjour<'),
            ('href="/fr/dormir/nice/"','href="/hotels/"'),
            ('>Où dormir<','>Choisir un hôtel<'),
        ),
    }
    for rel,reps in targets.items():
        p=ROOT/rel
        text=p.read_text(encoding="utf-8"); original=text
        fm=re.search(r'<footer class="v3-footer">.*?</footer>',text,flags=re.S)
        if fm:
            f=fm.group(0)
            for old,new in reps: f=f.replace(old,new)
            text=text[:fm.start()]+f+text[fm.end():]
        save(p,text,original)

def patch_fr_copy():
    for p in ROOT.rglob("*.html"):
        rel=p.relative_to(ROOT).as_posix()
        if rel.startswith("en/") or rel=="index.html": continue
        text=p.read_text(encoding="utf-8"); original=text
        text=text.replace("The Catch :", "Le compromis :")
        text=text.replace("The Catch:", "Le compromis :")
        text=text.replace("The Catch", "Le compromis")
        text=text.replace("Pichoun, ouvrir 100 onglets d’hôtels, ce n’est pas une stratégie !",
                          "Pichoun, 100 onglets d’hôtels, ce n’est pas une stratégie&nbsp;!")
        text=text.replace("La sélection Mametas permet désormais de faire un vrai choix plutôt que d’exposer notre liste de choses à produire. Choisissez d’abord l’ambiance.",
                          "La sélection Mametas permet de faire un vrai choix sans dérouler un annuaire. Choisissez d’abord l’ambiance.")
        save(p,text,original)

def patch_riviera_logic():
    p=ROOT/"assets/riviera-chooser.js"
    text=p.read_text(encoding="utf-8"); original=text
    old="""    var order = (profile.mobility === 'car' ? data.carOrder : data.defaultOrder)[profile.mood] || data.defaultOrder.decide;
    var exclude = REGIONAL_EXCLUDES[baseId] || [];
    var count = regionalCount(profile, baseId);"""
    new="""    var order = (profile.mobility === 'car' ? data.carOrder : data.defaultOrder)[profile.mood] || data.defaultOrder.decide;
    var exclude = (REGIONAL_EXCLUDES[baseId] || []).slice();
    // If Cannes wins a balanced, car-free glamour trip, the editorial rule explicitly
    // says not to turn the stay into an automatic Monaco/Menton day. Keep the
    // "go further" suggestions on the western/central Riviera so the verdict
    // and the follow-up recommendations tell the same story.
    if (baseId === 'cannes' && profile.mobility === 'nocar' &&
        profile.mood === 'glamour' && profile.pace === 'balanced') {
      ['monaco','menton'].forEach(function (id) {
        if (exclude.indexOf(id) < 0) exclude.push(id);
      });
    }
    var count = regionalCount(profile, baseId);"""
    if old not in text: raise RuntimeError("Riviera regional logic anchor not found")
    text=text.replace(old,new,1)
    save(p,text,original)

def patch_hotel_budget_logic():
    p=ROOT/"assets/hotel-engine.js"
    text=p.read_text(encoding="utf-8"); original=text
    # Add an explicit budget-empty message.
    text=text.replace(
        "none:'No Mametas hotel is currently available for this base.',",
        "none:'No Mametas hotel is currently available for this base.',\n    noneBudget:'No Mametas hotel in this base sits within that budget ceiling yet. Raise the ceiling to see the closest fits.',"
    )
    text=text.replace(
        "none:'Aucune adresse Mametas disponible pour cette base.',",
        "none:'Aucune adresse Mametas disponible pour cette base.',\n    noneBudget:'Aucune adresse Mametas de cette base ne respecte encore ce plafond. Relevez le plafond pour voir les compromis les plus proches.',"
    )
    old="""      if (!rankedSource.length) {
        relaxed = true;
        rankedSource = inventory.filter(function(h){ return state.base === 'any' || h.base === state.base; });
      }

      var ranked = rankedSource"""
    new="""      var budgetBlocked = false;
      if (!rankedSource.length) {
        relaxed = true;
        rankedSource = inventory.filter(function(h){
          if (!(state.base === 'any' || h.base === state.base)) return false;
          // Budget is a ceiling, not a preference. Relax style/geography/mobility
          // if needed, but never return a hotel above the user's stated ceiling.
          if (state.budget !== 'any') {
            var ceiling = priceLevel[state.budget] || 4;
            var hotelPrice = priceLevel[h.priceBand] || 0;
            return hotelPrice > 0 && hotelPrice <= ceiling;
          }
          return true;
        });
        if (!rankedSource.length && state.budget !== 'any') budgetBlocked = true;
      }

      var ranked = rankedSource"""
    if old not in text: raise RuntimeError("Hotel Fit fallback source anchor not found")
    text=text.replace(old,new,1)
    old2="""        return { hotels:resolved.filter(Boolean), wholeBase:false, relaxed:relaxed };
      });
    }).then(function(payload){
      var clean = payload.hotels;
      var shortlist = payload.wholeBase ? clean : selectDiverse(clean, 4);
      if (!shortlist.length) {
        summary.textContent = labels.none;"""
    new2="""        return { hotels:resolved.filter(Boolean), wholeBase:false, relaxed:relaxed, budgetBlocked:budgetBlocked };
      });
    }).then(function(payload){
      var clean = payload.hotels;
      var shortlist = payload.wholeBase ? clean : selectDiverse(clean, 4);
      if (!shortlist.length) {
        summary.textContent = payload.budgetBlocked ? labels.noneBudget : labels.none;"""
    if old2 not in text: raise RuntimeError("Hotel Fit payload anchor not found")
    text=text.replace(old2,new2,1)
    save(p,text,original)

def patch_asset_versions():
    for p in ROOT.rglob("*.html"):
        text=p.read_text(encoding="utf-8"); original=text
        text=re.sub(r'/assets/hotel-engine\.js\?v=\d+', '/assets/hotel-engine.js?v=12', text)
        text=re.sub(r'/assets/riviera-chooser\.js\?v=\d+', '/assets/riviera-chooser.js?v=10', text)
        save(p,text,original)

def patch_logo_css():
    css=r"""
/* Final header logo parity 2026-09-25 */
.brand-name,.v3-brand-name{
  font-family:"Fraunces",Georgia,serif!important;
  font-size:clamp(28px,3vw,40px)!important;
  font-weight:600!important;
  letter-spacing:-.05em!important;
  line-height:.9!important;
}
.brand-sub,.v3-brand-line{
  margin-top:8px!important;
  color:#176f83!important;
  font-family:"Fraunces",Georgia,serif!important;
  font-size:10px!important;
  font-style:italic!important;
  font-weight:400!important;
  letter-spacing:.04em!important;
  line-height:normal!important;
}
.hotel-fit-launch-punch{ text-wrap:balance; }
"""
    for rel in ("assets/site.css","assets/v3.css"):
        p=ROOT/rel
        text=p.read_text(encoding="utf-8"); original=text
        marker="/* Final header logo parity 2026-09-25 */"
        if marker not in text: text+="\n"+css
        save(p,text,original)

def validate():
    errors=[]
    monaco=(ROOT/"riviera-guide/monaco/index.html").read_text(encoding="utf-8")
    if monaco.find("destination-practical") < monaco.find('<header class="v3-header"'):
        errors.append("Monaco FR practical block still precedes header")
    if "liste de choses à produire" in (ROOT/"riviera-guide/menton/index.html").read_text(encoding="utf-8"):
        errors.append("Menton FR internal production wording remains")
    for slug in HOTEL_SLUGS:
        fr=(ROOT/f"hotels/{slug}/index.html").read_text(encoding="utf-8")
        if f'href="/en/hotels/{slug}/"' not in fr:
            errors.append(f"{slug}: FR->EN destination switch missing")
    if "profile.mobility === 'nocar'" not in (ROOT/"assets/riviera-chooser.js").read_text(encoding="utf-8"):
        errors.append("Riviera Fit consistency rule missing")
    hoteljs=(ROOT/"assets/hotel-engine.js").read_text(encoding="utf-8")
    if "Budget is a ceiling" not in hoteljs or "noneBudget" not in hoteljs:
        errors.append("Hotel Fit hard budget ceiling fix missing")
    if "/assets/hotel-engine.js?v=12" not in (ROOT/"en/hotels/finder/index.html").read_text(encoding="utf-8"):
        errors.append("Hotel Fit v12 cache bust missing")
    if errors: raise SystemExit("Closure QA failed:\n- "+"\n- ".join(errors))

def main():
    patch_monaco_fr()
    patch_hotel_lang_switches()
    patch_header_nav()
    patch_footers()
    patch_fr_copy()
    patch_riviera_logic()
    patch_hotel_budget_logic()
    patch_asset_versions()
    patch_logo_css()
    validate()
    print(f"Closure QA passed; changed {len(changed)} files.")
    for rel in sorted(changed): print(rel)

if __name__=="__main__":
    main()
