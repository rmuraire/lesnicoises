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