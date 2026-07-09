/**
 * First Class Audit — Form Handler
 */

class AuditForm {
    constructor(config) {
        this.role = config.role;
        this.sections = config.sections;
        this.webhookUrl = config.webhookUrl || 'https://automation.landingpro.by/webhook/fc-audit';

        this.currentSection = 0;
        this.answers = {};

        this.init();
    }

    init() {
        this.renderSections();
        this.bindEvents();
        this.showSection(0);
        this.updateProgress();
    }

    renderSections() {
        const container = document.getElementById('form-container');

        this.sections.forEach((section, sIndex) => {
            const sectionEl = document.createElement('div');
            sectionEl.className = 'question-section';
            sectionEl.id = `section-${sIndex}`;

            let html = `<div class="section-badge">Раздел ${sIndex + 1} из ${this.sections.length}</div>`;
            html += `<h2 style="margin-bottom: 25px; font-size: 22px;">${section.title}</h2>`;

            section.questions.forEach((q, qIndex) => {
                const qId = `q_${sIndex}_${qIndex}`;
                html += this.renderQuestion(q, qId, sIndex, qIndex);
            });

            sectionEl.innerHTML = html;
            container.appendChild(sectionEl);
        });
    }

    renderQuestion(q, qId, sIndex, qIndex) {
        let html = `<div class="question" data-qid="${qId}">`;
        html += `<p class="question-text"><span class="question-number">${sIndex + 1}.${qIndex + 1}</span> ${q.text}</p>`;

        switch (q.type) {
            case 'radio':
                html += '<div class="options">';
                q.options.forEach((opt, i) => {
                    html += `
                        <label class="option" data-value="${opt}">
                            <input type="radio" name="${qId}" value="${opt}">
                            <div class="radio"></div>
                            <span class="option-text">${opt}</span>
                        </label>`;
                });
                html += '</div>';
                break;

            case 'checkbox':
                html += '<div class="options">';
                q.options.forEach((opt, i) => {
                    html += `
                        <label class="option" data-value="${opt}">
                            <input type="checkbox" name="${qId}" value="${opt}">
                            <div class="checkbox"></div>
                            <span class="option-text">${opt}</span>
                        </label>`;
                });
                html += '</div>';
                break;

            case 'text':
                html += `<input type="text" class="text-input" name="${qId}" placeholder="${q.placeholder || 'Ваш ответ...'}">`;
                break;

            case 'textarea':
                html += `<textarea class="text-input" name="${qId}" placeholder="${q.placeholder || 'Ваш ответ...'}"></textarea>`;
                break;

            case 'table':
                html += '<table class="table-input"><tbody>';
                q.rows.forEach((row, i) => {
                    html += `<tr>
                        <td style="width: 60%">${row}</td>
                        <td><input type="text" name="${qId}_${i}" placeholder="${q.placeholder || '___'}"></td>
                    </tr>`;
                });
                html += '</tbody></table>';
                break;
        }

        html += '</div>';
        return html;
    }

    bindEvents() {
        // Option selection
        document.addEventListener('click', (e) => {
            const option = e.target.closest('.option');
            if (!option) return;

            const input = option.querySelector('input');
            const isRadio = input.type === 'radio';

            if (isRadio) {
                // Deselect others in same group
                const name = input.name;
                document.querySelectorAll(`input[name="${name}"]`).forEach(inp => {
                    inp.closest('.option').classList.remove('selected');
                });
            }

            input.checked = !input.checked || isRadio;
            option.classList.toggle('selected', input.checked);

            this.collectAnswers();
        });

        // Text input changes
        document.addEventListener('input', (e) => {
            if (e.target.matches('.text-input, .table-input input')) {
                this.collectAnswers();
            }
        });

        // Navigation
        document.getElementById('btn-prev').addEventListener('click', () => this.prevSection());
        document.getElementById('btn-next').addEventListener('click', () => this.nextSection());
    }

    collectAnswers() {
        const section = this.sections[this.currentSection];

        section.questions.forEach((q, qIndex) => {
            const qId = `q_${this.currentSection}_${qIndex}`;

            if (q.type === 'radio') {
                const selected = document.querySelector(`input[name="${qId}"]:checked`);
                this.answers[qId] = selected ? selected.value : null;
            }
            else if (q.type === 'checkbox') {
                const selected = document.querySelectorAll(`input[name="${qId}"]:checked`);
                this.answers[qId] = Array.from(selected).map(el => el.value);
            }
            else if (q.type === 'text' || q.type === 'textarea') {
                const input = document.querySelector(`[name="${qId}"]`);
                this.answers[qId] = input ? input.value : '';
            }
            else if (q.type === 'table') {
                const values = {};
                q.rows.forEach((row, i) => {
                    const input = document.querySelector(`[name="${qId}_${i}"]`);
                    values[row] = input ? input.value : '';
                });
                this.answers[qId] = values;
            }
        });
    }

    showSection(index) {
        document.querySelectorAll('.question-section').forEach((el, i) => {
            el.classList.toggle('active', i === index);
        });

        this.currentSection = index;
        this.updateProgress();
        this.updateButtons();

        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    updateProgress() {
        const progress = ((this.currentSection + 1) / this.sections.length) * 100;
        document.getElementById('progress-fill').style.width = `${progress}%`;
        document.getElementById('progress-text').textContent =
            `Раздел ${this.currentSection + 1} из ${this.sections.length}`;
    }

    updateButtons() {
        const prevBtn = document.getElementById('btn-prev');
        const nextBtn = document.getElementById('btn-next');

        prevBtn.style.display = this.currentSection === 0 ? 'none' : 'block';

        if (this.currentSection === this.sections.length - 1) {
            nextBtn.textContent = 'Отправить ✓';
            nextBtn.onclick = () => this.submit();
        } else {
            nextBtn.textContent = 'Далее →';
            nextBtn.onclick = () => this.nextSection();
        }
    }

    prevSection() {
        if (this.currentSection > 0) {
            this.showSection(this.currentSection - 1);
        }
    }

    nextSection() {
        this.collectAnswers();

        if (this.currentSection < this.sections.length - 1) {
            this.showSection(this.currentSection + 1);
        }
    }

    async submit() {
        this.collectAnswers();

        const btn = document.getElementById('btn-next');
        btn.disabled = true;
        btn.textContent = 'Отправка...';

        // Build answers with question texts
        const answersWithQuestions = {};
        this.sections.forEach((section, sIndex) => {
            section.questions.forEach((q, qIndex) => {
                const qId = `q_${sIndex}_${qIndex}`;
                const answer = this.answers[qId];
                // Only include non-empty answers
                if (answer && (Array.isArray(answer) ? answer.length > 0 : (typeof answer === 'object' ? Object.values(answer).some(v => v) : answer))) {
                    answersWithQuestions[q.text] = answer;
                }
            });
        });

        const payload = {
            role: this.role,
            answers: answersWithQuestions,
            sections: this.sections.map(s => s.title),
            timestamp: new Date().toISOString(),
            userAgent: navigator.userAgent
        };

        try {
            const response = await fetch(this.webhookUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            // Save locally as backup
            this.saveLocal(payload);

            // Redirect to thank you page
            window.location.href = 'thank-you.html';

        } catch (error) {
            console.error('Submit error:', error);

            // Save locally anyway
            this.saveLocal(payload);

            // Still redirect - data is saved locally
            window.location.href = 'thank-you.html';
        }
    }

    saveLocal(payload) {
        const key = `fc_audit_${this.role}_${Date.now()}`;
        localStorage.setItem(key, JSON.stringify(payload));

        // Also save to a combined key for admin panel
        const allResponses = JSON.parse(localStorage.getItem('fc_audit_responses') || '[]');
        allResponses.push(payload);
        localStorage.setItem('fc_audit_responses', JSON.stringify(allResponses));
    }
}

// Export for use in pages
window.AuditForm = AuditForm;
