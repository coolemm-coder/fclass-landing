/*! fclass.by lead webhook guard.
 * Legacy inline handlers may only show success after the lead workflow
 * confirms delivery with a documented JSON success response.
 */
(function () {
  if (window.__fcLeadWebhookGuard) return;
  window.__fcLeadWebhookGuard = true;

  var nativeFetch = window.fetch.bind(window);
  var guardedUrls = {
    'https://automation.landingpro.by/webhook/fc-lead': true,
    'https://automation.landingpro.by/webhook/fc-ticket-request': true,
    'https://automation.landingpro.by/webhook/fclass-blog-lead': true,
    'https://automation.landingpro.by/webhook/fclass-pdf-lead': true
  };

  window.fetch = function (input, init) {
    var url = typeof input === 'string' ? input : input && input.url;
    if (!guardedUrls[url]) return nativeFetch(input, init);

    var controller = new AbortController();
    var timeoutId = window.setTimeout(function () { controller.abort(); }, 12000);
    var options = Object.assign({}, init || {}, {
      mode: 'cors',
      signal: controller.signal
    });

    return nativeFetch(input, options).then(function (response) {
      if (!response.ok) {
        throw new Error('Lead webhook HTTP ' + response.status);
      }
      return response.clone().json().then(function (result) {
        if (!result || (result.success !== true && result.ok !== true)) {
          throw new Error('Lead webhook rejected');
        }
        return response;
      }, function () {
        throw new Error('Lead webhook returned invalid JSON');
      });
    }).finally(function () {
      window.clearTimeout(timeoutId);
    });
  };
})();
