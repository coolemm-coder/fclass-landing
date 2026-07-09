function toggleRouteMenu() {
    var links = document.querySelector('.nav-links');
    if (links) {
        links.classList.toggle('mobile-open');
    }
}

document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('.page-field').forEach(function (field) {
        field.value = window.location.pathname + window.location.search;
    });

    document.querySelectorAll('.route-form').forEach(function (form) {
        form.addEventListener('submit', function (event) {
            event.preventDefault();

            var button = form.querySelector('.route-submit');
            var status = form.parentElement.querySelector('.form-status');
            var originalText = button ? button.textContent : '';
            var data = new FormData(form);
            data.set('page', window.location.pathname + window.location.search);
            data.set('timestamp', new Date().toISOString());

            if (button) {
                button.disabled = true;
                button.textContent = 'Отправляем...';
            }

            fetch('https://automation.landingpro.by/webhook/fc-ticket-request', {
                method: 'POST',
                body: data,
                mode: 'no-cors'
            }).finally(function () {
                form.reset();
                if (status) {
                    status.style.display = 'block';
                }
                if (button) {
                    button.textContent = 'Заявка отправлена';
                    setTimeout(function () {
                        button.disabled = false;
                        button.textContent = originalText;
                    }, 4500);
                }
                try {
                    if (window.ym) {
                        ym(107237229, 'reachGoal', 'route_form_submit');
                    }
                    if (window.gtag) {
                        gtag('event', 'generate_lead', { event_category: 'lead', event_label: form.dataset.route || 'route_page' });
                    }
                } catch (err) {}
            });
        });
    });
});
