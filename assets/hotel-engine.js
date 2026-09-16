(function () {
  var root = document.querySelector('[data-hotel-engine]');
  if (!root) return;

  var fr = (document.documentElement.lang || '').toLowerCase().indexOf('fr') === 0;
  var state = { base: 'any', style: 'any', geography: 'any', mobility: 'any' };
  var output = root.querySelector('[data-engine-output]');
  var results = root.querySelector('[data-engine-results]');
  var summary = root.querySelector('[data-engine-summary]');
  var submit = root.querySelector('[data-engine-submit]');
  var cache = {};
  var unsafeAffiliateIds = { 'apollinaire-nice': true };

  var bases = fr ? [
    { id:'nice', label:'Nice', path:'/fr/dormir/nice/' },
    { id:'antibes', label:'Antibes & Juan-les-Pins', path:'/hotels/antibes/' },
    { id:'cannes', label:'Cannes', path:'/hotels/cannes/' },
    { id:'villefranche', label:'Villefranche & Cap-Ferrat', path:'/hotels/villefranche-sur-mer/' },
    { id:'monaco', label:'Monaco', path:'/hotels/monaco/' },
    { id:'menton', label:'Menton', path:'/hotels/menton/' },
    { id:'saint-paul', label:'Saint-Paul-de-Vence', path:'/hotels/saint-paul-de-vence/' },
    { id:'beaulieu', label:'Beaulieu-sur-Mer', path:'/hotels/beaulieu-sur-mer/' },
    { id:'mougins', label:'Mougins', path:'/hotels/mougins/' },
    { id:'saint-tropez', label:'Saint-Tropez', path:'/hotels/saint-tropez/' }
  ] : [
    { id:'nice', label:'Nice', path:'/stay/nice/' },
    { id:'antibes', label:'Antibes & Juan-les-Pins', path:'/en/hotels/antibes/' },
    { id:'cannes', label:'Cannes', path:'/en/hotels/cannes/' },
    { id:'villefranche', label:'Villefranche & Cap-Ferrat', path:'/en/hotels/villefranche-sur-mer/' },
    { id:'monaco', label:'Monaco', path:'/en/hotels/monaco/' },
    { id:'menton', label:'Menton', path:'/en/hotels/menton/' },
    { id:'saint-paul', label:'Saint-Paul-de-Vence', path:'/en/hotels/saint-paul-de-vence/' },
    { id:'beaulieu', label:'Beaulieu-sur-Mer', path:'/en/hotels/beaulieu-sur-mer/' },
    { id:'mougins', label:'Mougins', path:'/en/hotels/mougins/' },
    { id:'saint-tropez', label:'Saint-Tropez', path:'/en/hotels/saint-tropez/' }
  ];

  var labels = fr ? {
    loading:'On regarde la sélection Mametas…',
    choose:'Choisissez au moins un critère avant de lancer la recherche.',
    changed:'Vos choix ont changé. Relancez la sélection quand vous avez fini.',
    none:'Pas assez de correspondances nettes avec un lien tarifaire vérifiable. Élargissez un critère.',
    count:function(n){ return n + (n > 1 ? ' adresses ressortent' : ' adresse ressort') + ' de vos choix.'; },
    why:'Pourquoi elle ressort',
    catch:'Le compromis',
    rates:'Voir les tarifs',
    disclosure:'Transparence : les liens Expedia sont affiliés. Mametas peut percevoir une commission si vous réservez, sans que cela influence la sélection.'
  } : {
    loading:'Checking the Mametas selection…',
    choose:'Pick at least one criterion before running the finder.',
    changed:'Your choices changed. Run the shortlist again when you are done.',
    none:'Not enough clean matches with a verifiable rate link. Widen one criterion.',
    count:function(n){ return n + (n === 1 ? ' hotel matches' : ' hotels match') + ' your choices.'; },
    why:'Why it made the cut',
    catch:'The catch',
    rates:'Check rates',
    disclosure:'Transparency: Expedia links are affiliate links. Mametas may earn a commission if you book, without influencing the selection.'
  };

  function normalise(value) {
    return (value || '').toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').replace(/[^a-z0-9]+/g, ' ').trim();
  }

  function hasAny(text, words) {
    return words.some(function(word){ return text.indexOf(word) >= 0; });
  }

  function signals(hotel) {
    var text = normalise([hotel.section, hotel.sectionHeading, hotel.tag, hotel.copy, hotel.name].join(' '));
    var station = hasAny(text, ['gare','station','train','ter','sans voiture','no car','car free','day trip']);
    var sea = hasAny(text, ['mer','sea','beach','plage','seafront','promenade','bord de mer','harbour','port']);
    var oldtown = hasAny(text, ['vieux nice','old nice','old town','vieille ville','suquet','village','massena','centre','central']);
    var quiet = hasAny(text, ['calme','quiet','peaceful','retrait','retreat','garden','jardin','tranquille','slower','slow down']);
    var practical = station || hasAny(text, ['pratique','practical','budget','simple','straightforward','rationnel','rational','easy','value']);
    var active = oldtown || hasAny(text, ['vivant','lively','restaurants','bars','evening','soir','centre']);
    var chic = hasAny(text, ['chic','luxe','luxury','palace','riviera','resort','grand hotel','five star','5 star','spa','iconic','mythique']);
    return { station:station, sea:sea, oldtown:oldtown, quiet:quiet, practical:practical, active:active, chic:chic, text:text };
  }

  function classifyStyle(sig, style) {
    if (style === 'practical') return sig.practical;
    if (style === 'active') return sig.active;
    if (style === 'quiet') return sig.quiet;
    if (style === 'chic') return sig.chic;
    return true;
  }

  function classifyGeography(sig, geography) {
    if (geography === 'station') return sig.station;
    if (geography === 'sea') return sig.sea;
    if (geography === 'oldtown') return sig.oldtown;
    if (geography === 'quiet') return sig.quiet;
    return true;
  }

  function qualifies(hotel) {
    var sig = hotel.signals;
    if (state.style !== 'any' && !classifyStyle(sig, state.style)) return false;
    if (state.geography !== 'any' && !classifyGeography(sig, state.geography)) return false;
    if (state.mobility === 'nocar' && !sig.station && !sig.oldtown) return false;
    return true;
  }

  function score(hotel) {
    var sig = hotel.signals;
    var value = 0;
    if (state.style !== 'any' && classifyStyle(sig, state.style)) value += 12;
    if (state.geography !== 'any' && classifyGeography(sig, state.geography)) value += 12;
    if (state.mobility === 'nocar') {
      if (sig.station) value += 9;
      if (sig.oldtown) value += 4;
    }
    if (hotel.copy) value += 1;
    return value;
  }

  function slugFromHref(href) {
    if (!href || href.indexOf('/') !== 0) return '';
    var parts = href.split('/').filter(Boolean);
    return parts.length ? parts[parts.length - 1] : '';
  }

  function parseHotels(htmlText, base) {
    var doc = new DOMParser().parseFromString(htmlText, 'text/html');
    var hotels = [];
    doc.querySelectorAll('.hotel-choice-card').forEach(function(card){
      var heading = card.querySelector('h3');
      if (!heading) return;
      var name = heading.textContent.trim();
      if (!name) return;
      var headingLink = heading.querySelector('a');
      var headingHref = headingLink ? (headingLink.getAttribute('href') || '') : '';
      var internal = headingHref.indexOf('/') === 0 ? headingHref : '';
      if (!internal) {
        var internalLink = Array.prototype.find.call(card.querySelectorAll('a[href^="/"]'), function(a){
          var href = a.getAttribute('href') || '';
          return /\/hotels\//.test(href);
        });
        internal = internalLink ? internalLink.getAttribute('href') : '';
      }
      var directAffiliate = card.querySelector('a[href*="expedia.com/affiliates/"]');
      var section = card.closest('section');
      var sectionHeading = section ? section.querySelector('.hotel-style-heading') : null;
      var tag = card.querySelector('.hotel-choice-tags span');
      var copy = card.querySelector('.hotel-choice-copy > p') || card.querySelector('.hotel-choice-copy p');
      var id = card.getAttribute('data-hotel') || slugFromHref(internal) || normalise(name).replace(/ /g, '-');
      var hotel = {
        id:id,
        name:name,
        base:base.id,
        baseLabel:base.label,
        section:section ? (section.id || '') : '',
        sectionHeading:sectionHeading ? sectionHeading.textContent.trim() : '',
        tag:tag ? tag.textContent.trim() : '',
        copy:copy ? copy.textContent.trim() : '',
        detailPath:internal,
        affiliate:directAffiliate ? directAffiliate.getAttribute('href') : ''
      };
      hotel.signals = signals(hotel);
      hotels.push(hotel);
    });
    var seen = {};
    return hotels.filter(function(h){
      var key = h.base + '|' + h.id + '|' + normalise(h.name);
      if (seen[key]) return false;
      seen[key] = true;
      return true;
    });
  }

  function loadBase(base) {
    if (!cache[base.id]) {
      cache[base.id] = fetch(base.path, { credentials:'same-origin', cache:'no-store' })
        .then(function(response){ if (!response.ok) throw new Error(base.id); return response.text(); })
        .then(function(text){ return parseHotels(text, base); });
    }
    return cache[base.id];
  }

  function resolveAffiliate(hotel) {
    if (unsafeAffiliateIds[hotel.id]) return Promise.resolve(null);
    if (hotel.affiliate && hotel.affiliate.indexOf('expedia.com/affiliates/') >= 0) return Promise.resolve(hotel);
    if (!hotel.detailPath) return Promise.resolve(null);
    return fetch(hotel.detailPath, { credentials:'same-origin', cache:'no-store' })
      .then(function(response){ if (!response.ok) return null; return response.text(); })
      .then(function(text){
        if (!text) return null;
        var doc = new DOMParser().parseFromString(text, 'text/html');
        var link = doc.querySelector('a[href*="expedia.com/affiliates/"]');
        if (!link) return null;
        hotel.affiliate = link.getAttribute('href') || '';
        return hotel.affiliate ? hotel : null;
      })
      .catch(function(){ return null; });
  }

  function selectDiverse(ranked, limit) {
    if (state.base !== 'any') return ranked.slice(0, limit);
    var selected = [];
    var usedBases = {};
    ranked.forEach(function(h){
      if (selected.length >= limit) return;
      if (!usedBases[h.base]) {
        selected.push(h);
        usedBases[h.base] = 1;
      }
    });
    if (selected.length < limit) {
      ranked.forEach(function(h){
        if (selected.length >= limit) return;
        if (selected.indexOf(h) < 0) selected.push(h);
      });
    }
    return selected;
  }

  function catchText(hotel) {
    var sig = hotel.signals;
    if (sig.station && !sig.sea) return fr ? 'La logique est pratique avant d’être balnéaire.' : 'The logic is practical before it is seaside.';
    if (sig.sea && !sig.station) return fr ? 'La mer prime ; moins évident si vous enchaînez les départs en train.' : 'Sea comes first; less obvious for train-heavy days.';
    if (sig.quiet && !sig.active) return fr ? 'Le retrait prime ; moins pertinent si vous voulez toute la ville au pied de l’hôtel.' : 'Retreat comes first; less useful if you want the whole city at the door.';
    if (sig.active && !sig.quiet) return fr ? 'La vie autour fait partie du choix ; le retrait absolu, moins.' : 'The life around it is part of the choice; total retreat is not.';
    if (sig.chic) return fr ? 'L’hôtel compte dans l’expérience ; inutile de payer cette logique si la chambre ne sert qu’à dormir.' : 'The hotel is part of the experience; pointless if you only need somewhere to sleep.';
    return fr ? 'Bon compromis sur vos critères, sans prétendre cocher toutes les cases.' : 'A sound compromise on your criteria, without pretending to tick every box.';
  }

  function metaText(hotel) {
    var bits = [hotel.baseLabel];
    if (hotel.tag) bits.push(hotel.tag);
    else if (hotel.sectionHeading) bits.push(hotel.sectionHeading.split('\n')[0]);
    return bits.join(' · ');
  }

  function esc(value) {
    return String(value || '').replace(/[&<>"']/g, function(ch){
      return { '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;' }[ch];
    });
  }

  function render(shortlist) {
    summary.textContent = labels.count(shortlist.length);
    results.innerHTML = shortlist.map(function(hotel, index){
      var reason = hotel.copy || hotel.tag || (fr ? 'Une adresse retenue par Mametas pour cette logique de séjour.' : 'A Mametas pick for this trip logic.');
      return '<article class="hotel-engine-result">' +
        '<div class="hotel-engine-rank">0' + (index + 1) + '</div>' +
        '<div class="hotel-engine-copy">' +
          '<p class="eyebrow">' + esc(metaText(hotel)) + '</p>' +
          '<h3>' + esc(hotel.name) + '</h3>' +
          '<p class="engine-result-line"><strong>' + labels.why + '.</strong> ' + esc(reason) + '</p>' +
          '<p class="engine-result-line"><strong>' + labels.catch + '.</strong> ' + esc(catchText(hotel)) + '</p>' +
          '<div class="hotel-engine-actions"><a class="button" href="' + esc(hotel.affiliate) + '" rel="sponsored nofollow noopener" target="_blank" data-affiliate-network="expedia" data-affiliate-hotel="' + esc(hotel.id) + '">' + labels.rates + '</a></div>' +
        '</div>' +
      '</article>';
    }).join('');
    results.insertAdjacentHTML('afterend', '<p class="engine-disclosure" data-engine-disclosure>' + labels.disclosure + '</p>');
  }

  function clearDisclosure() {
    var old = root.querySelector('[data-engine-disclosure]');
    if (old) old.remove();
  }

  function chosenSomething() {
    return state.base !== 'any' || state.style !== 'any' || state.geography !== 'any' || state.mobility !== 'any';
  }

  function runFinder() {
    clearDisclosure();
    results.innerHTML = '';
    output.hidden = false;
    if (!chosenSomething()) {
      summary.textContent = labels.choose;
      return;
    }
    submit.disabled = true;
    summary.textContent = labels.loading;
    var wantedBases = state.base === 'any' ? bases : bases.filter(function(b){ return b.id === state.base; });
    Promise.allSettled(wantedBases.map(loadBase)).then(function(groups){
      var inventory = [];
      groups.forEach(function(group){ if (group.status === 'fulfilled') inventory = inventory.concat(group.value); });
      var ranked = inventory
        .filter(function(h){ return (state.base === 'any' || h.base === state.base) && qualifies(h); })
        .map(function(h){ h._score = score(h); return h; })
        .sort(function(a,b){ return b._score - a._score || a.name.localeCompare(b.name); });
      var candidates = selectDiverse(ranked, 12);
      return Promise.all(candidates.map(resolveAffiliate));
    }).then(function(resolved){
      var clean = resolved.filter(Boolean);
      var shortlist = selectDiverse(clean, 4);
      if (!shortlist.length) {
        summary.textContent = labels.none;
        results.innerHTML = '';
        return;
      }
      render(shortlist);
      output.scrollIntoView({ behavior:'smooth', block:'start' });
    }).catch(function(){
      summary.textContent = labels.none;
      results.innerHTML = '';
    }).finally(function(){
      submit.disabled = false;
    });
  }

  root.querySelectorAll('[data-engine-choice]').forEach(function(button){
    button.addEventListener('click', function(){
      var group = button.getAttribute('data-engine-group');
      var value = button.getAttribute('data-engine-choice');
      state[group] = value;
      root.querySelectorAll('[data-engine-group="' + group + '"]').forEach(function(other){
        var active = other === button;
        other.classList.toggle('is-active', active);
        other.setAttribute('aria-pressed', active ? 'true' : 'false');
      });
      if (!output.hidden) {
        clearDisclosure();
        results.innerHTML = '';
        summary.textContent = labels.changed;
        output.hidden = true;
      }
    });
  });

  submit.addEventListener('click', runFinder);
})();