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
      if(path.indexOf('/explore/')===0 || path.indexOf('/culture/')===0 || path.indexOf('/restaurants/')===0 || path.indexOf('/plages/')===0 || path.indexOf('/excursions/')===0) return 3;
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