(function () {
  var root = document.querySelector('[data-hotel-engine]');
  if (!root) return;
  var fr = (document.documentElement.lang || '').toLowerCase().indexOf('fr') === 0;
  var state = { style: 'practical', geography: 'any', band: 'any', trip: 5 };
  var labels = fr ? {
    mid:'Milieu', 'upper-mid':'Milieu-haut', high:'Haut de gamme', 'very-high':'Très haut de gamme',
    practical:'Pratique', active:'Vivant', quiet:'Calme', chic:'Chic',
    best:'Idéal pour', catch:'Le compromis', area:'Logique de quartier', rates:'Voir les tarifs', full:'Voir la fiche Mametas', none:'Aucune option nette. Élargissez un critère.'
  } : {
    mid:'Mid-range', 'upper-mid':'Upper-mid', high:'High-end', 'very-high':'Very high-end',
    practical:'Practical', active:'Lively', quiet:'Peaceful', chic:'Chic',
    best:'Best for', catch:'The catch', area:'Location logic', rates:'Check rates', full:'Read the Mametas take', none:'No clean match. Widen one criterion.'
  };
  var priceRank = {mid:1,'upper-mid':2,high:3,'very-high':4};
  var results = root.querySelector('[data-engine-results]');
  var summary = root.querySelector('[data-engine-summary]');

  function score(h) {
    var s = 0;
    if ((h.styles || []).indexOf(state.style) >= 0) s += 9; else s -= 4;
    if (h.carFree) s += 2;
    if ((h.tripLengths || []).indexOf(state.trip) >= 0) s += 2;
    if (state.style === 'practical' && h.stationFriendly) s += 5;
    if (state.style === 'quiet' && h.quiet) s += 5;
    if (state.style === 'active' && h.oldTownAccess) s += 4;
    if (state.style === 'chic' && h.seaAccess) s += 4;
    if (state.geography === 'station') s += h.stationFriendly ? 6 : -3;
    if (state.geography === 'sea') s += h.seaAccess ? 6 : -3;
    if (state.geography === 'oldtown') s += h.oldTownAccess ? 6 : -3;
    if (state.geography === 'quiet') s += h.quiet ? 6 : -3;
    if (state.band !== 'any') {
      var d = Math.abs(priceRank[h.priceBand] - priceRank[state.band]);
      s += d === 0 ? 5 : d === 1 ? 1 : -3;
    }
    return s;
  }
  function bestFor(h) {
    if (state.style === 'practical') return fr ? (h.stationFriendly ? 'rayonner en train sans voiture' : 'un séjour simple et central sans voiture') : (h.stationFriendly ? 'train day trips without a car' : 'an easy central no-car stay');
    if (state.style === 'quiet') return fr ? 'dormir plus au calme sans quitter Nice' : 'more peace without leaving Nice';
    if (state.style === 'active') return fr ? 'sortir à pied et garder la ville près de vous' : 'walking out to dinner and keeping the city close';
    return fr ? 'faire de l’hôtel une partie du voyage' : 'making the hotel part of the trip';
  }
  function catchText(h) {
    if (h.stationFriendly && !h.seaAccess) return fr ? 'pratique avant d’être balnéaire' : 'practical before it is seaside';
    if (h.seaAccess && !h.oldTownAccess) return fr ? 'la mer d’abord, le Vieux-Nice un peu moins immédiat' : 'sea first; Old Nice is less immediate';
    if (h.oldTownAccess && !h.quiet) return fr ? 'central signifie aussi plus vivant' : 'central also means livelier';
    if (h.quiet && !h.stationFriendly) return fr ? 'plus paisible, moins optimisé pour les départs TER' : 'calmer, less optimised for TER departures';
    if (h.priceBand === 'very-high') return fr ? 'un vrai choix de dépense, pas un simple upgrade' : 'a real spending decision, not a casual upgrade';
    return fr ? 'bon équilibre, sans cocher toutes les cases à la fois' : 'a good balance, without pretending to tick every box';
  }
  function render(data) {
    var hotels = data.hotels.slice().sort(function(a,b){ return score(b)-score(a); }).slice(0,4);
    summary.textContent = fr ? '4 choix maximum, classés selon vos décisions — pas selon une commission.' : 'Up to four picks, ranked by your decisions — never by commission.';
    results.innerHTML = hotels.map(function(h, i){
      var exp = h.affiliate && h.affiliate.expedia;
      var safeExpedia = exp && exp.status === 'active';
      var path = h.paths[fr ? 'fr' : 'en'];
      var cta = safeExpedia
        ? '<a class="button" href="'+exp.url+'" rel="sponsored nofollow noopener" data-affiliate-network="expedia" data-affiliate-hotel="'+h.id+'">'+labels.rates+'</a>'
        : '<a class="button" href="'+path+'">'+labels.full+'</a>';
      return '<article class="hotel-engine-result"><div class="hotel-engine-rank">0'+(i+1)+'</div><div><p class="eyebrow">'+labels[h.priceBand]+' · '+h.neighborhood+'</p><h3><a href="'+path+'">'+h.name+'</a></h3><dl><div><dt>'+labels.best+'</dt><dd>'+bestFor(h)+'</dd></div><div><dt>'+labels.catch+'</dt><dd>'+catchText(h)+'</dd></div><div><dt>'+labels.area+'</dt><dd>'+h.neighborhood+(h.stationFriendly ? (fr ? ' · gare pratique' : ' · station-friendly') : '')+(h.seaAccess ? (fr ? ' · mer proche' : ' · sea access') : '')+(h.oldTownAccess ? (fr ? ' · Vieux-Nice proche' : ' · Old Nice access') : '')+'</dd></div></dl><div class="hotel-engine-actions">'+cta+'<a class="text-link" href="'+path+'">'+labels.full+' →</a></div></div></article>';
    }).join('');
  }
  function bind(data) {
    root.querySelectorAll('[data-engine-choice]').forEach(function(btn){
      btn.addEventListener('click', function(){
        var group = btn.getAttribute('data-engine-group');
        var value = btn.getAttribute('data-engine-choice');
        state[group] = group === 'trip' ? parseInt(value,10) : value;
        root.querySelectorAll('[data-engine-group="'+group+'"]').forEach(function(x){ x.classList.toggle('is-active', x === btn); x.setAttribute('aria-pressed', x === btn ? 'true':'false'); });
        render(data);
      });
    });
    render(data);
  }
  fetch('/data/hotels/nice.json').then(function(r){ if(!r.ok) throw new Error('data'); return r.json(); }).then(bind).catch(function(){
    summary.textContent = fr ? 'Le moteur est momentanément indisponible. La sélection éditoriale reste juste en dessous.' : 'The finder is temporarily unavailable. The editorial shortlist remains below.';
  });
})();