/*! fclass.by mobile nav — single source of truth.
 * Builds a burger + full-screen overlay menu on any page that has .nav/.nav-links.
 * Overlay is appended directly to <body> (NOT inside .nav), so a transform/
 * backdrop-filter on the fixed .nav can never shrink it to the navbar box
 * (the containing-block bug that collapsed the menu). Idempotent & dependency-free.
 */
(function () {
  if (window.__fcMobnav) return;
  window.__fcMobnav = true;

  var BP = 1024; // show burger at <= 1024px, consistent with the homepage
  var CANON = [
    ['/#services', 'Услуги'],
    ['/tickets/', 'Билеты'],
    ['/tarify/', 'Тарифы'],
    ['/visa-support/', 'Визы'],
    ['/#expertise', 'О нас'],
    ['/blog/', 'Блог'],
    ['/#contact', 'Контакты']
  ];

  var css =
    '.fc-burger{display:none}' +
    '@media(max-width:' + BP + 'px){' +
      '.nav .nav-links{display:none!important}' +
      '.nav .nav-cta{display:none!important}' +
      '.nav .nav-mobile{display:none!important}' +
      '.fc-burger{display:flex;flex-direction:column;justify-content:center;align-items:center;' +
        'gap:5px;width:46px;height:46px;padding:0;margin:0;border:none;border-radius:10px;' +
        'background:rgba(12,24,37,0.55);cursor:pointer;position:relative;z-index:1002;' +
        '-webkit-tap-highlight-color:transparent}' +
      '.fc-burger span{display:block;width:22px;height:2.5px;border-radius:2px;background:#fff}' +
    '}' +
    '#fc-overlay{display:none}' +
    '#fc-overlay.open{display:flex;position:fixed;top:0;right:0;bottom:0;left:0;z-index:3000;' +
      'flex-direction:column;align-items:center;justify-content:center;gap:6px;' +
      'background:#0c1825;padding:72px 24px 32px;overflow-y:auto;-webkit-overflow-scrolling:touch}' +
    '#fc-overlay a{color:#fff;text-decoration:none;font-size:20px;line-height:1.2;' +
      'padding:14px 0;display:block;font-family:inherit;text-align:center}' +
    '#fc-overlay .fc-close{position:absolute;top:14px;right:16px;width:46px;height:46px;' +
      'display:flex;align-items:center;justify-content:center;font-size:34px;line-height:1;' +
      'color:#fff;background:none;border:none;cursor:pointer;padding:0}' +
    'body.fc-lock{overflow:hidden}';

  function inject() {
    var st = document.createElement('style');
    st.id = 'fc-mobnav-css';
    st.textContent = css;
    document.head.appendChild(st);
  }

  function build() {
    var nav = document.querySelector('.nav');
    if (!nav) return;

    // collect menu items from the existing desktop links, fallback to canonical
    var items = [];
    var links = nav.querySelector('.nav-links');
    if (links) {
      var anchors = links.querySelectorAll('a');
      for (var i = 0; i < anchors.length; i++) {
        var a = anchors[i];
        if (a.className.indexOf('nav-close') !== -1) continue;
        var href = a.getAttribute('href');
        var text = (a.textContent || '').replace(/\s+/g, ' ').trim();
        if (href && text) items.push([href, text]);
      }
    }
    if (items.length < 2) items = CANON;

    // overlay (direct child of body)
    var overlay = document.createElement('div');
    overlay.id = 'fc-overlay';
    var html = '<button class="fc-close" type="button" aria-label="Закрыть меню">&#10005;</button>';
    for (var j = 0; j < items.length; j++) {
      html += '<a href="' + items[j][0] + '">' + items[j][1] + '</a>';
    }
    overlay.innerHTML = html;
    document.body.appendChild(overlay);

    // burger button
    var burger = document.createElement('button');
    burger.className = 'fc-burger';
    burger.type = 'button';
    burger.setAttribute('aria-label', 'Открыть меню');
    burger.innerHTML = '<span></span><span></span><span></span>';
    nav.appendChild(burger);

    function open() { overlay.classList.add('open'); document.body.classList.add('fc-lock'); }
    function close() { overlay.classList.remove('open'); document.body.classList.remove('fc-lock'); }

    burger.addEventListener('click', open);
    overlay.querySelector('.fc-close').addEventListener('click', close);
    var oa = overlay.querySelectorAll('a');
    for (var k = 0; k < oa.length; k++) oa[k].addEventListener('click', close);

    // close on resize back to desktop and on bfcache restore (fixes "back = криво")
    window.addEventListener('resize', function () { if (window.innerWidth > BP) close(); });
    window.addEventListener('pageshow', close);
  }

  inject();
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', build);
  } else {
    build();
  }
})();
