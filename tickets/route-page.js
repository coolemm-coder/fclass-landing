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
        form.addEventListener('submit', async function (event) {
            event.preventDefault();

            var button = form.querySelector('.route-submit');
            var status = form.parentElement.querySelector('.form-status');
            var originalText = button ? button.textContent : '';
            var data = new FormData(form);
            data.set('page', window.location.pathname + window.location.search);
            data.set('timestamp', new Date().toISOString());

            if (status) {
                status.style.display = 'none';
                status.removeAttribute('role');
            }
            if (button) {
                button.disabled = true;
                button.textContent = 'Отправляем...';
            }

            try {
                var response = await fetch('https://automation.landingpro.by/webhook/fc-ticket-request', {
                    method: 'POST',
                    body: data
                });
                var result = await response.json();
                if (!response.ok || !result || result.success !== true) {
                    throw new Error('Lead webhook rejected');
                }

                form.reset();
                if (status) {
                    status.textContent = 'Заявка отправлена. Менеджер ответит в рабочее время.';
                    status.setAttribute('role', 'status');
                    status.style.display = 'block';
                }
                if (button) button.textContent = 'Заявка отправлена';
                try {
                    if (window.ym) {
                        ym(107237229, 'reachGoal', 'route_form_submit');
                    }
                    if (window.gtag) {
                        gtag('event', 'generate_lead', { event_category: 'lead', event_label: form.dataset.route || 'route_page' });
                    }
                } catch (err) {}
            } catch (error) {
                if (status) {
                    status.textContent = 'Не удалось отправить заявку. Попробуйте ещё раз или напишите нам в Telegram.';
                    status.setAttribute('role', 'alert');
                    status.style.display = 'block';
                }
                if (button) button.textContent = 'Попробовать снова';
            } finally {
                if (button) {
                    window.setTimeout(function () {
                        button.disabled = false;
                        button.textContent = originalText;
                    }, 4500);
                }
            }
        });
    });
});
