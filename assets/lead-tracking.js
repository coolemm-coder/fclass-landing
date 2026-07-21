(function() {
  'use strict';

  var YM_COUNTER_ID = 107237229;
  var DEDUPE_MS = 1500;

  function cleanParams(params) {
    var out = {};
    Object.keys(params || {}).forEach(function(key) {
      if (params[key] !== undefined && params[key] !== null && params[key] !== '') {
        out[key] = params[key];
      }
    });
    return out;
  }

  function isDuplicate(eventName, label) {
    var key = 'fc_track_' + eventName + '_' + String(label || '').slice(0, 80);
    var now = Date.now();
    try {
      var last = Number(sessionStorage.getItem(key) || 0);
      sessionStorage.setItem(key, String(now));
      return last && now - last < DEDUPE_MS;
    } catch (err) {
      return false;
    }
  }

  function sendYm(goal, params) {
    if (typeof window.ym === 'function') {
      window.ym(YM_COUNTER_ID, 'reachGoal', goal, params || {});
    }
  }

  function sendGtag(eventName, params) {
    if (typeof window.gtag === 'function') {
      window.gtag('event', eventName, params || {});
    }
  }

  function track(eventName, options) {
    var opts = options || {};
    var label = opts.label || opts.event_label || opts.method || location.pathname;
    if (isDuplicate(eventName, label)) return;

    var params = cleanParams({
      event_category: opts.category || 'lead',
      event_label: label,
      method: opts.method,
      link_url: opts.linkUrl,
      page_path: location.pathname,
      source: opts.source || location.pathname
    });

    sendGtag(eventName, params);
    if (opts.gaLead) sendGtag('generate_lead', params);
    if (opts.ymGoal) sendYm(opts.ymGoal, params);
    if (opts.ymLead) sendYm('LEAD', params);
  }

  function textLabel(link, fallback) {
    var text = (link.getAttribute('aria-label') || link.textContent || '').replace(/\s+/g, ' ').trim();
    return (link.dataset.trackLabel || text || fallback || 'link').slice(0, 100);
  }

  function pathnameFromHref(href) {
    try {
      return new URL(href, location.origin).pathname;
    } catch (err) {
      return '';
    }
  }

  function isMessengerHref(href) {
    return /(^|\/\/)(t\.me|telegram\.me|wa\.me|api\.whatsapp\.com|web\.whatsapp\.com)\b/i.test(href);
  }

  function isCommercialPath(pathname) {
    return pathname === '/komandirovki/' ||
      pathname === '/tickets/' ||
      pathname === '/tickets/aviabilety-dlya-yurlic/' ||
      pathname === '/visa-support/';
  }

  document.addEventListener('click', function(event) {
    if (!event.target || !event.target.closest) return;
    var link = event.target.closest('a[href]');
    if (!link) return;

    var href = link.getAttribute('href') || '';
    var absoluteHref = link.href || href;
    var label = textLabel(link, href);
    var source = link.dataset.trackSource || location.pathname;

    if (/^tel:/i.test(href)) {
      track('lead_phone_click', {
        label: label,
        method: 'phone',
        linkUrl: href,
        source: source,
        ymGoal: 'PHONE_CLICK',
        ymLead: true,
        gaLead: true
      });
      return;
    }

    if (/^mailto:/i.test(href)) {
      track('lead_email_click', {
        label: label,
        method: 'email',
        linkUrl: href,
        source: source,
        ymGoal: 'EMAIL_CLICK',
        ymLead: true,
        gaLead: true
      });
      return;
    }

    if (isMessengerHref(absoluteHref)) {
      track('lead_messenger_click', {
        label: label,
        method: /wa\.me|whatsapp/i.test(absoluteHref) ? 'whatsapp' : 'telegram',
        linkUrl: absoluteHref,
        source: source,
        ymGoal: 'MESSENGER_CLICK',
        ymLead: true,
        gaLead: true
      });
      return;
    }

    var path = pathnameFromHref(absoluteHref);
    if (path === '/tarify/') {
      track('pricing_intent', {
        category: 'navigation',
        label: label,
        method: 'pricing',
        linkUrl: absoluteHref,
        source: source,
        ymGoal: 'TARIFF_CLICK'
      });
      return;
    }

    if (isCommercialPath(path)) {
      track('commercial_intent', {
        category: 'navigation',
        label: label,
        method: 'commercial_page',
        linkUrl: absoluteHref,
        source: source,
        ymGoal: 'COMMERCIAL_INTENT'
      });
    }
  }, true);

  document.addEventListener('submit', function(event) {
    var form = event.target;
    if (!form || !form.querySelector) return;
    var sourceInput = form.querySelector('input[name="source"]');
    var label = form.dataset.trackLabel || form.id || (sourceInput && sourceInput.value) || location.pathname;
    track('lead_form_submit_intent', {
      label: label,
      method: 'form',
      source: location.pathname,
      ymGoal: 'FORM_SUBMIT_INTENT'
    });
  }, true);

  window.fcTrackEvent = track;
  window.fcTrackLead = function(method, label, extra) {
    var opts = extra || {};
    opts.method = method || opts.method || 'manual';
    opts.label = label || opts.label || opts.method;
    opts.ymGoal = opts.ymGoal || 'LEAD';
    opts.ymLead = false;
    opts.gaLead = true;
    track('generate_lead', opts);
  };
})();
