// Finder V3.1: city-only selections show the full city inventory; filtered searches remain shortlists.
(function () {
  var root = document.querySelector('[data-hotel-engine]');
  if (!root) return;

  var fr = (document.documentElement.lang || '').toLowerCase().indexOf('fr') === 0;
  var state = { base: 'any', style: 'any', geography: 'any', mobility: 'any', budget: 'any' };
  var output = root.querySelector('[data-engine-output]');
  var results = root.querySelector('[data-engine-results]');
  var summary = root.querySelector('[data-engine-summary]');
  var submit = root.querySelector('[data-engine-submit]');
  var cache = {};
  var unsafeAffiliateIds = { 'apollinaire-nice': true };

  var bases = fr ? [
    { id:'nice', label:'Nice', path:'/fr/dormir/nice/', dataPath:'/assets/hotel-finder-nice.json?v=2', stationFriendly:true, noCarFriendly:true },
    { id:'antibes', label:'Antibes & Juan-les-Pins', path:'/hotels/antibes/', stationFriendly:true, noCarFriendly:true },
    { id:'cannes', label:'Cannes', path:'/hotels/cannes/', stationFriendly:true, noCarFriendly:true },
    { id:'villefranche', label:'Villefranche & Cap-Ferrat', path:'/hotels/villefranche-sur-mer/', stationFriendly:true, noCarFriendly:true },
    { id:'monaco', label:'Monaco', path:'/hotels/monaco/', stationFriendly:true, noCarFriendly:true },
    { id:'menton', label:'Menton', path:'/hotels/menton/', stationFriendly:true, noCarFriendly:true },
    { id:'saint-paul', label:'Saint-Paul-de-Vence', path:'/hotels/saint-paul-de-vence/', stationFriendly:false, noCarFriendly:false },
    { id:'beaulieu', label:'Beaulieu-sur-Mer', path:'/hotels/beaulieu-sur-mer/', stationFriendly:true, noCarFriendly:true },
    { id:'mougins', label:'Mougins', path:'/hotels/mougins/', stationFriendly:false, noCarFriendly:false },
    { id:'saint-tropez', label:'Saint-Tropez', path:'/hotels/saint-tropez/', stationFriendly:false, noCarFriendly:false }
  ] : [
    { id:'nice', label:'Nice', path:'/stay/nice/', dataPath:'/assets/hotel-finder-nice.json?v=2', stationFriendly:true, noCarFriendly:true },
    { id:'antibes', label:'Antibes & Juan-les-Pins', path:'/en/hotels/antibes/', stationFriendly:true, noCarFriendly:true },
    { id:'cannes', label:'Cannes', path:'/en/hotels/cannes/', stationFriendly:true, noCarFriendly:true },
    { id:'villefranche', label:'Villefranche & Cap-Ferrat', path:'/en/hotels/villefranche-sur-mer/', stationFriendly:true, noCarFriendly:true },
    { id:'monaco', label:'Monaco', path:'/en/hotels/monaco/', stationFriendly:true, noCarFriendly:true },
    { id:'menton', label:'Menton', path:'/en/hotels/menton/', stationFriendly:true, noCarFriendly:true },
    { id:'saint-paul', label:'Saint-Paul-de-Vence', path:'/en/hotels/saint-paul-de-vence/', stationFriendly:false, noCarFriendly:false },
    { id:'beaulieu', label:'Beaulieu-sur-Mer', path:'/en/hotels/beaulieu-sur-mer/', stationFriendly:true, noCarFriendly:true },
    { id:'mougins', label:'Mougins', path:'/en/hotels/mougins/', stationFriendly:false, noCarFriendly:false },
    { id:'saint-tropez', label:'Saint-Tropez', path:'/en/hotels/saint-tropez/', stationFriendly:false, noCarFriendly:false }
  ];

  var labels = fr ? {
    loading:'On passe la sélection Mametas au crible…',
    choose:'Choisissez au moins un critère avant de lancer la recherche.',
    changed:'Vous avez changé un critère. Relancez quand c’est bon.',
    none:'Rien de suffisamment net. Élargissez un critère.',
    count:function(n){ return n + (n > 1 ? ' adresses correspondent' : ' adresse correspond') + ' vraiment à vos choix.'; },
    bestFor:'Idéal pour',
    why:'Pourquoi elle ressort',
    notFor:'Moins adapté à',
    catch:'Le compromis',
    rates:'Voir les tarifs',
    details:'Voir la fiche Mametas',
    disclosure:'Transparence : certains liens de réservation sont affiliés. Mametas peut percevoir une commission si vous réservez, sans que cela influence la sélection.'
  } : {
    loading:'Checking the Mametas selection…',
    choose:'Pick at least one criterion before running the finder.',
    changed:'Your choices changed. Run the shortlist again when you are done.',
    none:'Not enough clean matches. Widen one criterion.',
    count:function(n){ return n + (n === 1 ? ' hotel matches' : ' hotels match') + ' your choices.'; },
    bestFor:'Best for',
    why:'Why it made the cut',
    notFor:'Not for',
    catch:'The catch',
    rates:'Check rates',
    details:'See the Mametas review',
    disclosure:'Transparency: some booking links are affiliate links. Mametas may earn a commission if you book, without influencing the selection.'
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
    return { station:station, noCar:false, sea:sea, oldtown:oldtown, quiet:quiet, practical:practical, active:active, chic:chic, text:text };
  }

  function structuredSignals(item) {
    var styles = item.styles || [];
    var fit = item.fit || {};
    var best = fit.bestFor || [];
    return {
      station: !!item.stationFriendly || best.indexOf('excursions') >= 0,
      noCar: item.carFree === true || item.noCarFriendly === true || best.indexOf('car-free') >= 0,
      sea: !!item.seaAccess || best.indexOf('beach-first') >= 0,
      oldtown: !!item.oldTownAccess || best.indexOf('old-town') >= 0,
      quiet: !!item.quiet || best.indexOf('quiet') >= 0,
      practical: styles.indexOf('practical') >= 0 || best.indexOf('excursions') >= 0 || best.indexOf('car-free') >= 0 || best.indexOf('value') >= 0,
      active: styles.indexOf('active') >= 0 || best.indexOf('city-life') >= 0,
      chic: styles.indexOf('chic') >= 0 || best.indexOf('hotel-as-trip') >= 0,
      text: normalise([item.name, item.neighborhood, styles.join(' '), best.join(' ')].join(' '))
    };
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

  var priceLevel = { low:1, mid:2, 'upper-mid':3, high:4, 'very-high':4 };
  var priceSymbol = { low:'€', mid:'€€', 'upper-mid':'€€€', high:'€€€€', 'very-high':'€€€€' };

  function qualifies(hotel) {
    var sig = hotel.signals;
    if (state.style !== 'any' && !classifyStyle(sig, state.style)) return false;
    if (state.geography !== 'any' && !classifyGeography(sig, state.geography)) return false;
    if (state.mobility === 'nocar' && !sig.noCar) return false;
    if (state.budget !== 'any') {
      var ceiling = priceLevel[state.budget] || 4;
      var hotelPrice = priceLevel[hotel.priceBand] || 0;
      if (!hotelPrice || hotelPrice > ceiling) return false;
    }
    return true;
  }

  function score(hotel) {
    var sig = hotel.signals;
    var value = 0;
    if (state.style !== 'any' && classifyStyle(sig, state.style)) value += 12;
    if (state.geography !== 'any' && classifyGeography(sig, state.geography)) value += 12;
    if (state.mobility === 'nocar') {
      if (sig.noCar) value += 9;
      if (sig.station) value += 4;
    }
    if (state.budget !== 'any' && hotel.priceBand) {
      var ceiling = priceLevel[state.budget] || 4;
      var hotelPrice = priceLevel[hotel.priceBand] || 0;
      if (hotelPrice === ceiling) value += 7;
      else if (hotelPrice && hotelPrice < ceiling) value += 4;
    }
    if (hotel.copy) value += 1;
    return value;
  }

  function slugFromHref(href) {
    if (!href || href.indexOf('/') !== 0) return '';
    var parts = href.split('/').filter(Boolean);
    return parts.length ? parts[parts.length - 1] : '';
  }

  function affiliateAnchor(scope) {
    if (!scope) return null;
    var sponsored = Array.prototype.find.call(scope.querySelectorAll('a[rel~="sponsored"]'), function(a){
      var href = a.getAttribute('href') || '';
      return /^https?:\/\//i.test(href);
    });
    if (sponsored) return sponsored;
    return scope.querySelector(
      'a[href*="expedia.com/affiliates/"],' +
      'a[href*="kqzyfj.com/"],a[href*="jdoqocy.com/"],a[href*="anrdoezrs.net/"],' +
      'a[href*="tkqlhce.com/"],a[href*="dpbolvw.net/"],a[href*="booking.com/"]'
    );
  }

  function parseHotels(htmlText, base) {
    var doc = new DOMParser().parseFromString(htmlText, 'text/html');
    var hotels = [];
    doc.querySelectorAll('.hotel-choice-card').forEach(function(card, index){
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
      var directAffiliate = affiliateAnchor(card);
      var section = card.closest('section');
      var sectionHeading = section ? section.querySelector('.hotel-style-heading') : null;
      var tag = card.querySelector('.hotel-choice-tags span');
      var copy = card.querySelector('.hotel-choice-copy > p') || card.querySelector('.hotel-choice-copy p');
      var id = card.getAttribute('data-hotel') || slugFromHref(internal) || normalise(name).replace(/ /g, '-');
      var media = null;
      var mediaImg = card.querySelector('.hotel-choice-media img[src]');
      var mediaSprite = card.querySelector('.hotel-choice-media .batch-thumb');
      if (mediaImg) {
        media = { type:'img', src:mediaImg.getAttribute('src') || '', alt:mediaImg.getAttribute('alt') || name };
      } else if (mediaSprite) {
        var spriteClass = 'batch-thumb' + (mediaSprite.classList.contains('batch-thumb-13') ? ' batch-thumb-13' : '');
        var spriteStyle = mediaSprite.getAttribute('style') || '';
        var spritePos = (spriteStyle.match(/background-position\s*:\s*[^;]+/i) || [''])[0];
        media = { type:'sprite', className:spriteClass, style:spritePos };
      }
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
        affiliate:directAffiliate ? (directAffiliate.getAttribute('href') || '') : '',
        priceBand:(card.getAttribute('data-price-band') || '').trim(),
        media:media,
        _order:index
      };
      hotel.signals = signals(hotel);
      /* Transport is explicit: never infer rail/no-car suitability from marketing copy. */
      hotel.signals.station = !!base.stationFriendly;
      hotel.signals.noCar = !!base.noCarFriendly;
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

  function parseStructuredHotels(payload, base) {
    var items = payload && Array.isArray(payload.hotels) ? payload.hotels : [];
    return items.map(function(item, index){
      var paths = item.paths || {};
      var affiliate = item.affiliate || {};
      var affiliateUrl = affiliate.url || (affiliate.expedia && affiliate.expedia.url) || (affiliate.booking && affiliate.booking.url) || '';
      var styleText = (item.styles || []).join(' · ');
      var hotel = {
        id:item.id || normalise(item.name).replace(/ /g, '-'),
        name:item.name || '',
        base:base.id,
        baseLabel:base.label,
        section:styleText,
        sectionHeading:styleText,
        tag:item.neighborhood || '',
        copy:item.neighborhood ? ((fr ? 'Quartier : ' : 'Area: ') + item.neighborhood) : '',
        detailPath:fr ? (paths.fr || '') : (paths.en || ''),
        affiliate:affiliateUrl,
        priceBand:item.priceBand || '',
        fit:item.fit || {},
        media:(item.image && item.image.indexOf('batch-sprite') < 0) ? { type:'img', src:item.image, alt:item.name || '' } : null,
        _order:index
      };
      hotel.signals = structuredSignals(item);
      return hotel;
    }).filter(function(h){ return !!h.name; });
  }

  function loadBase(base) {
    if (!cache[base.id]) {
      if (base.dataPath) {
        cache[base.id] = fetch(base.dataPath, { credentials:'same-origin', cache:'no-store' })
          .then(function(response){ if (!response.ok) throw new Error(base.id); return response.json(); })
          .then(function(payload){ return parseStructuredHotels(payload, base); });
      } else {
        cache[base.id] = fetch(base.path, { credentials:'same-origin', cache:'no-store' })
          .then(function(response){ if (!response.ok) throw new Error(base.id); return response.text(); })
          .then(function(text){ return parseHotels(text, base); });
      }
    }
    return cache[base.id];
  }

  function resolveAffiliate(hotel) {
    if (unsafeAffiliateIds[hotel.id]) {
      hotel.affiliate = '';
      return Promise.resolve(hotel);
    }
    if (hotel.affiliate) return Promise.resolve(hotel);
    if (!hotel.detailPath) return Promise.resolve(hotel);
    return fetch(hotel.detailPath, { credentials:'same-origin', cache:'no-store' })
      .then(function(response){ if (!response.ok) return hotel; return response.text(); })
      .then(function(text){
        if (!text) return hotel;
        var doc = new DOMParser().parseFromString(text, 'text/html');
        var link = affiliateAnchor(doc);
        if (link) hotel.affiliate = link.getAttribute('href') || '';
        return hotel;
      })
      .catch(function(){ return hotel; });
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

  var fitTagLabels = fr ? {
    'car-free':'Sans voiture',
    'excursions':'Excursions',
    'beach-first':'Plage d’abord',
    'city-life':'Vie de ville',
    'quiet':'Calme',
    'hotel-as-trip':'L’hôtel fait partie du voyage',
    'old-town':'Vieille ville',
    'value':'Budget maîtrisé',
    'romantic':'Couple'
  } : {
    'car-free':'Car-free',
    'excursions':'Day trips',
    'beach-first':'Beach-first',
    'city-life':'City life',
    'quiet':'Quiet',
    'hotel-as-trip':'Hotel as the trip',
    'old-town':'Old town',
    'value':'Value',
    'romantic':'Couples'
  };

  function fitText(hotel, field) {
    var fit = hotel.fit || {};
    var value = fit[field];
    if (!value) return '';
    if (typeof value === 'string') return value;
    return value[fr ? 'fr' : 'en'] || value.en || value.fr || '';
  }

  function bestForText(hotel) {
    var tags = (hotel.fit && hotel.fit.bestFor) || [];
    return tags.map(function(tag){ return fitTagLabels[tag] || tag; }).join(' · ');
  }

  function esc(value) {
    return String(value || '').replace(/[&<>"']/g, function(ch){
      return { '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;' }[ch];
    });
  }

  function affiliateNetwork(href) {
    href = href || '';
    if (href.indexOf('expedia.com/affiliates/') >= 0) return 'expedia';
    if (/kqzyfj\.com|jdoqocy\.com|anrdoezrs\.net|tkqlhce\.com|dpbolvw\.net/i.test(href)) return 'booking-cj';
    if (href.indexOf('booking.com/') >= 0) return 'booking';
    return 'affiliate';
  }

  function renderHotelMedia(hotel) {
    if (!hotel.media) return '';
    if (hotel.media.type === 'img' && hotel.media.src) {
      return '<div class="hotel-engine-media"><img src="' + esc(hotel.media.src) + '" alt="' + esc(hotel.media.alt || hotel.name) + '" loading="lazy"></div>';
    }
    if (hotel.media.type === 'sprite') {
      var cls = hotel.media.className === 'batch-thumb batch-thumb-13' ? 'batch-thumb batch-thumb-13' : 'batch-thumb';
      var style = /^background-position\s*:\s*[-0-9.% ]+$/i.test(hotel.media.style || '') ? hotel.media.style : '';
      return '<div class="hotel-engine-media"><span class="' + cls + '"' + (style ? ' style="' + esc(style) + '"' : '') + ' aria-hidden="true"></span></div>';
    }
    return '';
  }

  function render(shortlist) {
    summary.textContent = labels.count(shortlist.length);
    results.innerHTML = shortlist.map(function(hotel, index){
      var reason = fitText(hotel, 'why') || hotel.copy || hotel.tag || (fr ? 'Une adresse retenue par Mametas pour cette logique de séjour.' : 'A Mametas pick for this trip logic.');
      var bestFor = bestForText(hotel);
      var notFor = fitText(hotel, 'notForText');
      var tradeOff = fitText(hotel, 'tradeOff') || catchText(hotel);
      var action = '';
      if (hotel.affiliate) {
        action = '<a class="button" href="' + esc(hotel.affiliate) + '" rel="sponsored nofollow noopener" target="_blank" data-affiliate-network="' + affiliateNetwork(hotel.affiliate) + '" data-affiliate-hotel="' + esc(hotel.id) + '">' + labels.rates + '</a>';
      } else if (hotel.detailPath) {
        action = '<a class="button" href="' + esc(hotel.detailPath) + '">' + labels.details + '</a>';
      }
      return '<article class="hotel-engine-result' + (hotel.media ? ' has-media' : '') + '">' +
        '<div class="hotel-engine-rank">' + String(index + 1).padStart(2, '0') + '</div>' +
        renderHotelMedia(hotel) +
        '<div class="hotel-engine-copy">' +
          '<p class="eyebrow">' + esc(metaText(hotel)) + '</p>' +
          '<h3>' + esc(hotel.name) + '</h3>' +
          (hotel.priceBand ? '<p class="engine-price-band" title="' + (fr ? 'Positionnement prix relatif, pas un tarif en temps réel' : 'Relative price positioning, not a live rate') + '">' + esc(priceSymbol[hotel.priceBand] || '') + '<span>' + (fr ? 'repère budget' : 'budget guide') + '</span></p>' : '') +
          (bestFor ? '<p class="engine-result-line engine-fit-line"><strong>' + labels.bestFor + '.</strong> ' + esc(bestFor) + '</p>' : '') +
          '<p class="engine-result-line"><strong>' + labels.why + '.</strong> ' + esc(reason) + '</p>' +
          (notFor ? '<p class="engine-result-line"><strong>' + labels.notFor + '.</strong> ' + esc(notFor) + '</p>' : '') +
          '<p class="engine-result-line"><strong>' + labels.catch + '.</strong> ' + esc(tradeOff) + '</p>' +
          (action ? '<div class="hotel-engine-actions">' + action + '</div>' : '') +
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
    return state.base !== 'any' || state.style !== 'any' || state.geography !== 'any' || state.mobility !== 'any' || state.budget !== 'any';
  }

  function baseOnly() {
    return state.base !== 'any' && state.style === 'any' && state.geography === 'any' && state.mobility === 'any' && state.budget === 'any';
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
    var showWholeBase = baseOnly();

    Promise.allSettled(wantedBases.map(loadBase)).then(function(groups){
      var inventory = [];
      groups.forEach(function(group){ if (group.status === 'fulfilled') inventory = inventory.concat(group.value); });

      var matching = inventory.filter(function(h){
        return (state.base === 'any' || h.base === state.base) && qualifies(h);
      });

      if (showWholeBase) {
        matching.sort(function(a,b){ return (a._order || 0) - (b._order || 0); });
        return Promise.all(matching.map(resolveAffiliate)).then(function(resolved){
          return { hotels:resolved.filter(Boolean), wholeBase:true };
        });
      }

      var ranked = matching
        .map(function(h){ h._score = score(h); return h; })
        .sort(function(a,b){ return b._score - a._score || (a._order || 0) - (b._order || 0) || a.name.localeCompare(b.name); });
      var candidates = selectDiverse(ranked, 12);
      return Promise.all(candidates.map(resolveAffiliate)).then(function(resolved){
        return { hotels:resolved.filter(Boolean), wholeBase:false };
      });
    }).then(function(payload){
      var clean = payload.hotels;
      var shortlist = payload.wholeBase ? clean : selectDiverse(clean, 4);
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
