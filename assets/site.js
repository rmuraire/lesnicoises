(function(){
  var isFrench=(document.documentElement.lang||'').toLowerCase().indexOf('fr')===0;
  var path=window.location.pathname;
  var items=isFrench?[
    {label:'Planifier',href:'/fr/#planifier'},
    {label:'Lieux',href:'/riviera-guide/'},
    {label:'Dormir',href:'/fr/dormir/nice/'},
    {label:'Explorer',href:'/explore/'},
    {label:'Maintenant',href:'/bons-plans/'}
  ]:[
    {label:'Plan',href:'/#plan'},
    {label:'Places',href:'/en/riviera-guide/'},
    {label:'Stay',href:'/stay/nice/'},
    {label:'Explore',href:'/en/explore/'},
    {label:'Now',href:'/en/good-finds/'}
  ];

  function activeIndex(){
    if(isFrench){
      if(path.indexOf('/fr/planifier/')===0) return 0;
      if(path.indexOf('/riviera-guide/')===0) return 1;
      if(path.indexOf('/fr/dormir/')===0 || path.indexOf('/hotels/')===0) return 2;
      if(path.indexOf('/explore/')===0 || path.indexOf('/culture/')===0 || path.indexOf('/restaurants/')===0 || path.indexOf('/plages/')===0 || path.indexOf('/escapades/')===0) return 3;
      if(path.indexOf('/bons-plans/')===0) return 4;
    }else{
      if(path.indexOf('/plan/')===0) return 0;
      if(path.indexOf('/en/riviera-guide/')===0) return 1;
      if(path.indexOf('/stay/')===0 || path.indexOf('/en/hotels/')===0) return 2;
      if(path.indexOf('/en/explore/')===0 || path.indexOf('/en/culture/')===0 || path.indexOf('/en/restaurants/')===0 || path.indexOf('/en/beaches/')===0 || path.indexOf('/en/day-trips/')===0) return 3;
      if(path.indexOf('/en/good-finds/')===0) return 4;
    }
    return -1;
  }

  var current=activeIndex();
  document.querySelectorAll('.primary-nav ul, .mobile-nav > ul').forEach(function(list){
    var links=list.querySelectorAll(':scope > li > a');
    if(links.length<5) return;
    items.forEach(function(item,index){
      var link=links[index];
      link.textContent=item.label;
      link.setAttribute('href',item.href);
      if(index===current) link.setAttribute('aria-current','page');
      else link.removeAttribute('aria-current');
    });
  });
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

  // Hotel detail pages should return to the complete decision page, not the old partial list.
  if(!isFrench && path.indexOf('/en/hotels/nice/')===0 && path!=='/en/hotels/nice/'){
    document.querySelectorAll('a[href="/en/hotels/nice/"]').forEach(function(link){link.setAttribute('href','/stay/nice/');});
  }
  if(isFrench && path.indexOf('/hotels/nice/')===0 && path!=='/hotels/nice/'){
    document.querySelectorAll('a[href="/hotels/nice/"]').forEach(function(link){link.setAttribute('href','/fr/dormir/nice/');});
  }

  // Nice is the main base: it needs explicit exits into the rest of the trip.
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

  // The car-free guide must lead to the concrete base/hotel decisions it describes.
  if(path==='/en/hotels/without-a-car/' || path==='/hotels/sans-voiture/'){
    var carFreeArticle=document.querySelector('main .article');
    if(carFreeArticle && !carFreeArticle.querySelector('.journey-next')){
      carFreeArticle.appendChild(makeNote(isFrench
        ? '<strong>Faites maintenant le vrai choix.</strong><br><a href="/fr/dormir/nice/">Comparer les hôtels de Nice →</a> · <a href="/riviera-guide/villefranche-cap-ferrat/">Voir Villefranche comme base →</a> · <a href="/fr/planifier/cinq-jours-nice-sans-voiture/">Voir le séjour de 5 jours sans voiture →</a>'
        : '<strong>Now make the actual choice.</strong><br><a href="/stay/nice/">Compare Nice hotels →</a> · <a href="/en/riviera-guide/villefranche-cap-ferrat/">See Villefranche as a base →</a> · <a href="/plan/five-days-nice-no-car/">See the 5-day no-car trip →</a>'
      ));
    }
  }

  // “Do less” is timeless advice, so send it to the timeless mistakes guide rather than seasonal Now content.
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

  // Restaurant hubs should not end after the city list.
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

(function(){
  var nav=document.querySelector('[data-mobile-nav]');
  var open=document.querySelector('[data-menu-open]');
  var close=document.querySelector('[data-menu-close]');
  if(!nav||!open||!close)return;
  function show(){nav.classList.add('open');document.body.style.overflow='hidden';}
  function hide(){nav.classList.remove('open');document.body.style.overflow='';}
  open.addEventListener('click',show);close.addEventListener('click',hide);
  nav.querySelectorAll('a').forEach(function(a){a.addEventListener('click',hide);});
  document.addEventListener('keydown',function(e){if(e.key==='Escape')hide();});
})();