(function(){
var P=location.pathname.replace(/\/$/,'');
function get(k){try{return JSON.parse(localStorage.getItem(k)||'[]')}catch(e){return[]}}
function set(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}
var steps=document.querySelectorAll('.step input');
if(steps.length){
  var key='ka:'+P,d=get(key),bar=document.getElementById('bar'),lab=document.getElementById('lab');
  function upd(){var n=0;steps.forEach(function(c,i){c.checked=!!d[i];c.parentNode.classList.toggle('done',!!d[i]);if(d[i])n++});
    var p=Math.round(n*100/steps.length);bar.style.width=p+'%';lab.textContent='%'+p+' tamamlandı'}
  steps.forEach(function(c,i){c.onchange=function(){d[i]=c.checked;set(key,d);upd()}});upd();
}
document.querySelectorAll('[data-g]').forEach(function(a){
  var d=get('ka:'+a.getAttribute('data-g')),t=+a.getAttribute('data-n'),n=0;
  for(var i=0;i<t;i++)if(d[i])n++;
  var p=Math.round(n*100/t),e=a.querySelector('i'),l=a.querySelector('.pl');
  if(e)e.style.width=p+'%';if(l)l.textContent='%'+p+' tamamlandı';
});
var arama = document.getElementById('arama');

if (arama) {
  var kartlar = document.querySelectorAll('.grid .card');

  arama.addEventListener('input', function() {
    var kelime = this.value.toLocaleLowerCase('tr-TR').trim();

    kartlar.forEach(function(kart) {
      var metin = kart.textContent.toLocaleLowerCase('tr-TR');

      if (metin.includes(kelime)) {
        kart.style.display = '';
      } else {
        kart.style.display = 'none';
      }
    });
  });
}
})();