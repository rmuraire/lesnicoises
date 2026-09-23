(function(){
  var isFrench=(document.documentElement.lang||'').toLowerCase().indexOf('fr')===0;
  var path=window.location.pathname;
  var items=isFrench?[
    {label:'Planifier',href:'/riviera-chooser/'},
    {label:'Lieux',href:'/riviera-guide/'},
    {label:'Dormir',href:'/hotels/'},
    {label:'Explorer',href:'/explore/'},
    {label:'Maintenant',href:'/bons-plans/'}
  ]:[
    {label:'Plan',href:'/en/riviera-chooser/'},
    {label:'Places',href:'/en/riviera-guide/'},
    {label:'Stay',href:'/en/hotels/'},
    {label:'Explore',href:'/en/explore/'},
    {label:'Now',href:'/en/good-finds/'}
  ];

  function activeIndex(){
    if(isFrench){
      if(path.indexOf('/riviera-chooser/')===0 || path.indexOf('/fr/planifier/')===0) return 0;
      if(path.indexOf('/riviera-guide/')===0) return 1;
      if(path.indexOf('/fr/dormir/')===0 || path.indexOf('/hotels/')===0) return 2;
      if(path.indexOf('/explore/')===0 || path.indexOf('/culture/')===0 || path.indexOf('/restaurants/')===0 || path.indexOf('/plages/')===0 || path.indexOf('/escapades/')===0) return 3;
      if(path.indexOf('/bons-plans/')===0) return 4;
    }else{
      if(path.indexOf('/en/riviera-chooser/')===0 || path.indexOf('/plan/')===0) return 0;
      if(path.indexOf('/en/riviera-guide/')===0) return 1;
      if(path.indexOf('/stay/')===0 || path.indexOf('/en/hotels/')===0) return 2;
      if(path.indexOf('/en/explore/')===0 || path.indexOf('/en/culture/')===0 || path.indexOf('/en/restaurants/')===0 || path.indexOf('/en/beaches/')===0 || path.indexOf('/en/day-trips/')===0) return 3;
      if(path.indexOf('/en/good-finds/')===0) return 4;
    }
    return -1;
  }

  function navMarkup(){
    var current=activeIndex();
    return items.map(function(item,index){
      return '<li><a href="'+item.href+'"'+(index===current?' aria-current="page"':'')+'>'+item.label+'</a></li>';
    }).join('');
  }

  function alternate(lang){
    var link=document.querySelector('link[rel~="alternate"][hreflang="'+lang+'"]');
    if(link&&link.href) return link.href;
    if(lang==='fr') return isFrench?path:'/fr/';
    return isFrench?'/':path;
  }

  function languageMarkup(){
    return '<a class="'+(isFrench?'active':'muted')+'" href="'+alternate('fr')+'"'+(isFrench?' aria-current="page"':'')+'>FR</a><span>/</span><a class="'+(!isFrench?'active':'muted')+'" href="'+alternate('en')+'"'+(!isFrench?' aria-current="page"':'')+'>EN</a>';
  }

  var header=document.querySelector('.site-header');
  var inner=header&&header.querySelector('.header-inner');
  var desktopNav=inner&&inner.querySelector('.primary-nav');
  if(desktopNav){
    var list=desktopNav.querySelector('ul');
    if(!list){list=document.createElement('ul');desktopNav.appendChild(list);}
    list.innerHTML=navMarkup();
  }

  if(inner){
    var lang=inner.querySelector('.lang-switch');
    if(!lang){
      lang=document.createElement('div');
      lang.className='lang-switch';
      inner.appendChild(lang);
    }
    lang.setAttribute('aria-label',isFrench?'Langue':'Language');
    lang.innerHTML=languageMarkup();

    var buttons=inner.querySelectorAll('[data-menu-open]');
    var open=buttons[0];
    Array.prototype.slice.call(buttons,1).forEach(function(button){button.remove();});
    if(!open){
      open=document.createElement('button');
      open.className='menu-toggle';
      open.type='button';
      open.setAttribute('data-menu-open','');
      open.innerHTML='<span></span><span></span><span></span>';
      inner.appendChild(open);
    }
    open.setAttribute('aria-label',isFrench?'Ouvrir le menu':'Open menu');
    open.setAttribute('aria-expanded','false');
  }

  var mobile=document.querySelector('[data-mobile-nav]');
  if(!mobile&&header){
    mobile=document.createElement('div');
    mobile.className='mobile-nav';
    mobile.setAttribute('data-mobile-nav','');
    header.insertAdjacentElement('afterend',mobile);
  }
  if(mobile){
    mobile.innerHTML='<div class="mobile-nav-top"><span class="brand-name">Mametas</span><button type="button" aria-label="'+(isFrench?'Fermer':'Close')+'" class="mobile-nav-close" data-menu-close>×</button></div><ul>'+navMarkup()+'</ul><div class="lang-switch" aria-label="'+(isFrench?'Langue':'Language')+'">'+languageMarkup()+'</div>';
  }
})();

(function(){
  var isFrench=(document.documentElement.lang||'').toLowerCase().indexOf('fr')===0;
  var path=window.location.pathname;

  function makeNote(html){
    var block=document.createElement('div');
    block.className='note journey-next';
    block.innerHTML=html;
    return block;
  }

  if(!isFrench && path.indexOf('/en/hotels/nice/')===0 && path!=='/en/hotels/nice/'){
    document.querySelectorAll('a[href="/en/hotels/nice/"]').forEach(function(link){link.setAttribute('href','/stay/nice/');});
  }
  if(isFrench && path.indexOf('/hotels/nice/')===0 && path!=='/hotels/nice/'){
    document.querySelectorAll('a[href="/hotels/nice/"]').forEach(function(link){link.setAttribute('href','/fr/dormir/nice/');});
  }

  if(path==='/en/riviera-guide/nice/' || path==='/riviera-guide/nice/'){
    var article=document.querySelector('main .article');
    var sources=article&&article.querySelector('.sources');
    if(article && !article.querySelector('.journey-next')){
      var html=isFrench
        ? '<strong>Ensuite, pichoun.</strong><br><a href="/fr/dormir/nice/">Choisir votre hôtel à Nice →</a> · <a href="/restaurants/">Choisir où manger →</a> · <a href="/plages/">Choisir une plage →</a> · <a href="/fr/planifier/cinq-jours-nice-sans-voiture/">Ouvrir le parcours de 5 jours →</a>'
        : '<strong>Next, pichoun.</strong><br><a href="/stay/nice/">Choose your Nice hotel →</a> · <a href="/en/restaurants/">Choose where to eat →</a> · <a href="/en/beaches/">Choose a beach →</a> · <a href="/plan/five-days-nice-no-car/">Open the 5-day plan →</a>';
      var block=makeNote(html);
      if(sources) article.insertBefore(block,sources); else article.appendChild(block);
    }
  }

  if(path==='/en/hotels/without-a-car/' || path==='/hotels/sans-voiture/'){
    var carFreeArticle=document.querySelector('main .article');
    if(carFreeArticle && !carFreeArticle.querySelector('.journey-next')){
      carFreeArticle.appendChild(makeNote(isFrench
        ? '<strong>Faites maintenant le vrai choix.</strong><br><a href="/fr/dormir/nice/">Comparer les hôtels de Nice →</a> · <a href="/riviera-guide/villefranche-cap-ferrat/">Voir Villefranche comme base →</a> · <a href="/fr/planifier/cinq-jours-nice-sans-voiture/">Voir le séjour de 5 jours sans voiture →</a>'
        : '<strong>Now make the actual choice.</strong><br><a href="/stay/nice/">Compare Nice hotels →</a> · <a href="/en/riviera-guide/villefranche-cap-ferrat/">See Villefranche as a base →</a> · <a href="/plan/five-days-nice-no-car/">See the 5-day no-car trip →</a>'
      ));
    }
  }

  if(path==='/en/day-trips/'){
    document.querySelectorAll('a.card[href="/en/good-finds/"]').forEach(function(card){
      card.setAttribute('href','/en/good-finds/riviera-mistakes/');
      var more=card.querySelector('.more');
      if(more) more.textContent='Avoid the classic mistakes';
    });
  }
  if(path==='/escapades/'){
    document.querySelectorAll('a.card[href="/bons-plans/"]').forEach(function(card){
      card.setAttribute('href','/bons-plans/erreurs-riviera/');
      var more=card.querySelector('.more');
      if(more) more.textContent='Voir les erreurs à éviter';
    });
  }

  if(path==='/en/restaurants/' || path==='/restaurants/'){
    var main=document.querySelector('main');
    if(main && !main.querySelector('.journey-next-hub')){
      var section=document.createElement('section');
      section.className='section journey-next-hub';
      section.innerHTML=isFrench
        ? '<div class="wrap"><div class="note"><strong>Et après le dîner ?</strong><br><a href="/fr/planifier/cinq-jours-nice-sans-voiture/">Revenir au parcours →</a> · <a href="/explore/">Explorer plages, culture et excursions →</a> · <a href="/riviera-guide/">Comparer les bases →</a></div></div>'
        : '<div class="wrap"><div class="note"><strong>And after dinner?</strong><br><a href="/plan/five-days-nice-no-car/">Return to the trip plan →</a> · <a href="/en/explore/">Explore beaches, culture and day trips →</a> · <a href="/en/riviera-guide/">Compare bases →</a></div></div>';
      main.appendChild(section);
    }
  }
})();

/* Hotel decision layer: one shared decision grammar across the Riviera.
   It deliberately describes relative positioning, not live nightly rates. */
(function(){
  var isFrench=(document.documentElement.lang||'').toLowerCase().indexOf('fr')===0;
  var path=window.location.pathname.replace(/^\/en/,'');
  var hotels={
    '/hotels/nice/anantara-plaza-nice/': ['Carré d’Or / Albert 1er','Seafront-central · strongest for doing Nice on foot','First stays that want centre, sea and polish','Luxury'],
    '/hotels/nice/apollinaire-nice/': ['Centre / Durandy','Central · between transport and Old Nice','Walkable city breaks without seafront pricing','Upscale'],
    '/hotels/nice/boutique-hotel-nice-cote-dazur/': ['Nice-Ville / Musiciens','Station-side central · easy departures','No-car trips and value-conscious city stays','Mid-range'],
    '/hotels/nice/hotel-66/': ['Nice-Ville / Jean Médecin','Station-side central · strongest for moving','No-car trips and train-heavy itineraries','Mid-range'],
    '/hotels/nice/hotel-du-couvent/': ['Vieux Nice','Historic-centre hideaway · strongest for atmosphere','A splurge built around the hotel as well as the city','Luxury'],
    '/hotels/nice/la-perouse/': ['Castle Hill / seafront','Old-Nice edge · strongest for sea and character','Romantic stays that want postcard Nice close by','Upscale'],
    '/hotels/nice/le-negresco/': ['Promenade / Carré d’Or','Seafront landmark · central enough, destination in itself','Iconic stays where the hotel is part of the trip','Luxury'],
    '/hotels/nice/maison-albar-le-victoria/': ['Jean Médecin / seafront','Hyper-central · sea, shopping and transport close together','Luxury city breaks with minimal logistics','Luxury'],
    '/hotels/nice/palais-de-la-mediterranee/': ['Promenade / Carré d’Or','Seafront-central · strongest for beach and city access','Classic Riviera stays with everything close','Luxury'],
    '/hotels/nice/villa-victoria/': ['Musiciens / Carré d’Or','Quiet-central · a calmer walkable base','City stays that want calm without exile','Upscale'],
    '/hotels/antibes/hotel-la-place/': ['Centre / Vieil Antibes','Central · old town and station both practical','Car-free Antibes and short stays','Mid-range'],
    '/hotels/antibes/la-villa-port-antibes/': ['Port Vauban / Vieil Antibes','Port-side central · strongest for walking','Antibes as a base without giving up atmosphere','Upscale'],
    '/hotels/cap-d-antibes/cap-d-antibes-beach-hotel/': ['Cap d’Antibes / waterfront','Resort location · deliberately away from the centre','Beach-first stays where the hotel is the destination','Luxury'],
    '/hotels/cap-d-antibes/la-villa-cap-d-antibes/': ['Juan-les-Pins / Cap edge','Residential-resort · calmer than central Antibes','Pool-and-beach stays with town within reach','Upscale'],
    '/hotels/cannes/carlton-cannes/': ['Croisette','Prime seafront · Cannes happening outside the door','Iconic Cannes and event-led stays','Luxury'],
    '/hotels/cannes/hotel-martinez/': ['Croisette','Prime seafront · polished and highly walkable','Beach, glamour and festival-season Cannes','Luxury'],
    '/hotels/cannes/le-cavendish/': ['Centre / Carnot','Central edge · practical rather than beachfront','Walkable Cannes with more discretion','Upscale'],
    '/hotels/cannes/majestic-cannes/': ['Palais / Croisette','Hyper-central · strongest for events and old-town access','First-time Cannes with zero appetite for commuting','Luxury'],
    '/hotels/eze/la-chevre-d-or/': ['Èze Village','Hilltop village · spectacular, intentionally isolated','A destination stay rather than a transport base','Luxury'],
    '/hotels/menton/villa-genesis/': ['Borrigo / seafront','Seafront-residential · calm with centre accessible','Slow Menton stays with beach priority','Luxury'],
    '/hotels/monaco/hotel-de-paris-monte-carlo/': ['Carré d’Or / Casino','Hyper-central Monaco · the address is the point','A Monaco splurge with everything ceremonial close','Luxury'],
    '/hotels/roquebrune-cap-martin/the-maybourne-riviera/': ['Roquebrune cliffs','Panoramic retreat · deliberately removed from town life','Hotel-first stays with views over convenience','Luxury'],
    '/hotels/saint-jean-cap-ferrat/royal-riviera/': ['Baie des Fourmis / Cap Ferrat','Waterfront-resort · between Beaulieu and the peninsula','Beach-led stays with Riviera day trips possible','Luxury'],
    '/hotels/saint-tropez/lou-pinet/': ['Residential Saint-Tropez','Quiet edge of town · privacy over doorstep action','Pool-and-hotel time with Saint-Tropez nearby','Luxury'],
    '/hotels/antibes/royal-antibes/': ['Seafront / old-town edge','Seafront-central · beach and old town both easy','Antibes stays balancing beach and town','Upscale'],
    '/hotels/antibes/best-western-hotel-journel-antibes/': ['Residential Antibes / centre edge','Near-centre · calmer, less postcard-pretty','Value-conscious stays that still want Antibes walkable','Mid-range'],
    '/hotels/monaco/port-palace/': ['Port Hercule','Port-central · strong for walking Monaco','First stays wanting views without Casino-square formality','Luxury'],
    '/hotels/monaco/columbus-hotel-monte-carlo/': ['Fontvieille','Quieter Monaco · removed from the Casino core','Calmer stays and Fontvieille-focused trips','Upscale'],
    '/hotels/beaulieu-sur-mer/hotel-carlton-beaulieu-sur-mer/': ['Beaulieu centre / Baie des Fourmis','Quiet-central · beach and station both useful','Car-free Riviera stays based east of Nice','Upscale'],
    '/hotels/beaulieu-sur-mer/hotel-marcellin/': ['Beaulieu centre','Small-town central · practical for train and waterfront','Simple car-free stays with Beaulieu as base','Mid-range'],
    '/hotels/saint-tropez/pastis-hotel-saint-tropez/': ['Saint-Tropez / centre edge','Near-centre retreat · calmer than the port','Boutique stays wanting town nearby, not underneath','Upscale'],
    '/hotels/saint-tropez/hotel-de-paris-saint-tropez/': ['Centre / port edge','Hyper-central · strongest for Saint-Tropez on foot','Short glamorous stays with no appetite for driving','Luxury'],
    '/hotels/cannes/hotel-le-canberra/': ['Rue d’Antibes / Croisette edge','Central · shopping, beach and station all workable','Walkable Cannes without palace-hotel scale','Upscale'],
    '/hotels/menton/ibis-styles-menton-centre/': ['Menton centre','Central · strongest for station, old town and value','Car-free stays and practical Riviera itineraries','Mid-range']
  };
  var data=hotels[path];
  if(!data) return;
  var article=document.querySelector('.hotel-detail');
  if(!article || article.querySelector('.hotel-facts')) return;
  var copies=article.querySelectorAll('.hotel-copy');
  var copy=copies.length>1?copies[1]:copies[0];
  if(!copy) return;
  var values=data.slice();
  if(isFrench){
    var budget={'Mid-range':'Milieu de gamme','Upscale':'Haut de gamme','Luxury':'Luxe'};
    values[3]=budget[values[3]]||values[3];
  }
  var labels=isFrench?['Quartier','Logique de localisation','Idéal pour','Budget']:['Area','Location logic','Best for','Budget'];
  var facts=document.createElement('div');
  facts.className='hotel-facts';
  facts.innerHTML=values.map(function(value,i){return '<div><span>'+labels[i]+'</span><b>'+value+'</b></div>';}).join('');
  var note=document.createElement('p');
  note.className='disclosure';
  note.textContent=isFrench?'Positionnement relatif sur la Riviera. Les tarifs varient fortement selon la saison et les grands événements.':'Relative Riviera positioning. Rates move sharply with season and major events.';
  var verdict=copy.querySelector('.verdict');
  var firstHeading=copy.querySelector('h2');
  var anchor=verdict||firstHeading;
  if(anchor){copy.insertBefore(facts,anchor);copy.insertBefore(note,anchor);}else{copy.appendChild(facts);copy.appendChild(note);}
})();

/* Affiliate CTA cleanup: provider-aware conversion copy plus one transparency line. */
(function(){
  var isFrench=(document.documentElement.lang||'').toLowerCase().indexOf('fr')===0;
  document.querySelectorAll('.affiliate-cta').forEach(function(cta){
    var button=cta.querySelector('a[href]');
    var href=button?(button.getAttribute('href')||''):'';
    var provider=/expedia\.com\/affiliates\//i.test(href)?'Expedia':(/kqzyfj\.com|jdoqocy\.com|anrdoezrs\.net|tkqlhce\.com|dpbolvw\.net|booking\.com\//i.test(href)?'Booking':'le partenaire');
    var copy=cta.querySelector('p');
    if(copy){
      copy.textContent=isFrench
        ? 'Consultez les disponibilités et les tarifs sur '+provider+'.'
        : 'Check current availability and rates on '+provider+'.';
    }
    if(button&&provider!=='le partenaire'){
      button.textContent=isFrench?'Voir les tarifs sur '+provider:'Check rates on '+provider;
    }
    var parent=cta.parentElement;
    var disclosure=parent&&parent.querySelector('.disclosure');
    if(disclosure){
      disclosure.textContent=isFrench
        ? 'Transparence : ce lien est affilié. Mametas peut percevoir une commission si vous réservez, sans que cela influence notre sélection.'
        : 'Transparency: this is an affiliate link. Mametas may earn a commission if you book, without influencing our selection.';
    }
  });
})();

(function(){
  var nav=document.querySelector('[data-mobile-nav]');
  var open=document.querySelector('[data-menu-open]');
  var close=document.querySelector('[data-menu-close]');
  if(!nav||!open||!close||open.getAttribute('data-menu-bound')==='true')return;
  open.setAttribute('data-menu-bound','true');

  function show(){
    nav.classList.add('open');
    nav.setAttribute('aria-hidden','false');
    open.setAttribute('aria-expanded','true');
    document.body.classList.add('menu-open');
    close.focus();
  }
  function hide(returnFocus){
    nav.classList.remove('open');
    nav.setAttribute('aria-hidden','true');
    open.setAttribute('aria-expanded','false');
    document.body.classList.remove('menu-open');
    if(returnFocus!==false)open.focus();
  }
  nav.setAttribute('aria-hidden','true');
  open.addEventListener('click',show);
  close.addEventListener('click',function(){hide(true);});
  nav.querySelectorAll('a').forEach(function(a){a.addEventListener('click',function(){hide(false);});});
  document.addEventListener('keydown',function(e){if(e.key==='Escape'&&nav.classList.contains('open'))hide(true);});
  window.addEventListener('resize',function(){if(window.innerWidth>1080&&nav.classList.contains('open'))hide(false);});
})();

/* Audit guard: canonical internal anchors. */
(function(){
  var fixes={
    '/fr/dormir/nice/#anime':'/fr/dormir/nice/#vivant',
    '/fr/dormir/nice/#paisible':'/fr/dormir/nice/#calme',
    '/fr/planifier/cinq-jours-nice-sans-voiture/#day-three':'/fr/planifier/cinq-jours-nice-sans-voiture/#jour-trois'
  };
  document.querySelectorAll('a[href]').forEach(function(link){
    var href=link.getAttribute('href');
    if(fixes[href]) link.setAttribute('href',fixes[href]);
  });
})();


/* Mametas dialect: link one first-use term per page to the mini-lexicon. */
(function(){
  function addDialectLink(){
    if(!document.body || document.documentElement.dataset.mametasDialectLink === '1') return;
    var lang=(document.documentElement.lang || 'en').toLowerCase().indexOf('fr') === 0 ? 'fr' : 'en';
    if(location.pathname.indexOf('/lexique/') >= 0 || location.pathname.indexOf('/en/lexicon/') >= 0) return;
    var base=lang === 'fr' ? '/lexique/' : '/en/lexicon/';
    var terms=[
      {re:/(mèfi)/i,id:'mefi'},
      {re:/(pichoun|pitchoun)/i,id:'pichoun'},
      {re:/(cagade)/i,id:'cagade'},
      {re:/(dégun)/i,id:'degun'},
      {re:/(niocou)/i,id:'niocou'},
      {re:/(paillassou)/i,id:'paillassou'},
      {re:/(empégué)/i,id:'empegue'},
      {re:/(ficanas)/i,id:'ficanas'}
    ];
    var walker=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);
    var nodes=[],node;
    while((node=walker.nextNode())) nodes.push(node);
    for(var i=0;i<nodes.length;i++){
      node=nodes[i];
      var parent=node.parentElement;
      if(!parent || parent.closest('a,script,style,button,code,pre,noscript,textarea')) continue;
      for(var j=0;j<terms.length;j++){
        var match=node.nodeValue.match(terms[j].re);
        if(!match) continue;
        var at=match.index, before=node.nodeValue.slice(0,at), after=node.nodeValue.slice(at+match[0].length);
        var frag=document.createDocumentFragment();
        if(before) frag.appendChild(document.createTextNode(before));
        var link=document.createElement('a');
        link.className='dialect-inline';
        link.href=base+'#'+terms[j].id;
        link.title=lang === 'fr' ? 'Voir le petit lexique niçois' : 'See the Niçois mini-lexicon';
        link.textContent=match[0];
        frag.appendChild(link);
        if(after) frag.appendChild(document.createTextNode(after));
        parent.replaceChild(frag,node);
        document.documentElement.dataset.mametasDialectLink='1';
        return;
      }
    }
  }
  if(document.readyState === 'loading') document.addEventListener('DOMContentLoaded',addDialectLink);
  else addDialectLink();
})();
