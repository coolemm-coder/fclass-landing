# NEXT-STEPS — fclass.by SEO/конверсия (сессия 2026-06-01)

> ⚠️ Деплой шёл **прямым FTP** (live проверен), коммиты **локальные, НЕ запушены**. Канонический путь — `git push origin main` → GitHub Actions (curl FTP). **Запушить 6 коммитов**, чтобы CI и git синхронизировались (контент совпадает с live).

## ✅ Сделано (всё на live + git, 6 коммитов)
1. GSC: убраны 2 битых «sitemap», осталась чистая `sitemap.xml`.
2. **Формы захвата на 24 блог-страницы** → webhook `fc-lead`, цель `LEAD`. Было 21 без формы + 4 на легаси `fclass-blog-lead` (выпилен везде).
3. **Корректура русского: 18 ошибок / 13 страниц** (опечатки, падежи, пунктуация).
4. **Консолидация кластера «юрлиц»:** head-term анкоры → поз.9-победитель `aviabilety-dlya-yur-lic`; договор-анкоры на `korporativnye-aviabilety-minsk`.
5. **9 title билетных** обогащены коммерч. ключами.
6. **Mobile-фикс:** таблицы `.info-table/.route-table/.compare-table` → `@media(max-width:768px){display:block;overflow-x:auto}` на 35 страницах (устраняет Яндекс `NOT_MOBILE_FRIENDLY`; на 360px overflow было до 57px → стало 0, проверено эмуляцией).
7. **Яндекс-переобход 25 URL** через прямой Webmaster API (MCP не умеет; см. память `yandex-webmaster-recrawl-api`). Квота 150→125.
8. Google: `sitemap.xml` резабмит.

## ⏳ Наблюдать (время)
- [ ] **Mobile-флаг** Яндекса спадёт к ~2026-06-04 (после переобхода). Проверка: `get-diagnostics` host `https:fclass.by:443`.
- [ ] **Позиции коммерции** замер ~2026-06-22: `aviabilety-dlya-yur-lic` (9→топ-5?), `korporativnye-aviabilety-minsk` (поз.26 ожила? если нет → 301 на победителя), `/tickets/minsk-*` (8-10→?).
- [ ] **Лиды с форм** (`source=blog_*`, цель `LEAD` в Метрике 107237229). Удалить тестовый лид `_audit`.

## 🎯 Следующие рычаги (билеты + командировки)
1. Контент билетных `/tickets/minsk-*`: блоки «цены/расписание/прямые рейсы» в BODY (не только title) под «минск-X авиабилеты цена».
2. Усилить перелинковку из топ-инфо (komandirovka-v-rossiyu 52 клика, sutochnye, kalkulyator) → коммерческие.
3. Если korporativnye не ожила за 3 нед → 301 → aviabilety-dlya-yur-lic.

## 🔧 Тех-заметки
- **Деплой docroot:** FTP-root `/` (Bitrix), блог `/blog/`. **НЕ `/www/new.fclass.by/`** (Vercel-staging, вхолостую). Проверка: `ftp.size`==`curl|wc -c`. Память `fclass-deploy-docroot`.
- **Яндекс recrawl:** прямой API, токен в `~/.claude.json`, curl (не python-SSL), user_id `1666266757`, квота 150/день. Память `yandex-webmaster-recrawl-api`.
- Формы → `https://automation.landingpro.by/webhook/fc-lead` (живой). Билетные route-формы → `fc-ticket-request`.

---

# NEXT-STEPS — FC холодная рассылка (доделать)

> Создано 2026-05-23. Полный контекст: memory `fc-cold-email-system.md`.

## Статус
- ✅ Доставляемость проверена: mail-tester **7.9/10**, SPF+DKIM проходят (SMTP = Mail.ru подтверждён), DMARC p=none.
- ✅ Решение Эмиля: **медленный дрип с fclass.by** (~30-50/день + прогрев; не отдельный домен, не ESP).
- ✅ Парсер email готов: `scripts/email_parser.py` (прогон по 248 → +26 в `data/all_contacts.enriched.csv`).
- ✅ Список: `data/all_contacts.csv` — 3528/3789 с email.
- ✅ Воркфлоу есть: FC_ColdEmail_Campaign `RPVnm6DlyS1AK4JS` (webhook-триггер), FC_ManualSend `H8YOY2gf3rZANXFl`. SMTP cred `VpkGLKfbHK9X4zNb`.

## ДОДЕЛАТЬ — slow-drip двигатель
1. [ ] Залить контакты (3528+26) в источник, читаемый n8n ежедневно: Google Sheet «FC_Leads» или n8n DataTable. (n8n MCP лежит → строить через REST: POST `/api/v1/workflows` + `/activate`; `--resolve automation.landingpro.by:443:91.218.143.156`, ключ `$N8N_API_KEY`.)
2. [ ] Воркфлоу-планировщик: Schedule daily → читает источник → дедуп по sent-логу (static `sentEmails`) → берёт next N (warmup: нед.1 ~20/д → ~50/д) → Build+SMTP (реюз из FC_ColdEmail) → отметка sent + лог в Sheet.
3. [ ] Сегмент `category` → выбор v2-шаблона (`data/email_templates_v2_plaintext.md`: Экспортёры / IT-ПВТ / «киты»).
4. [ ] (опц.) Follow-up через 3-4 дня без ответа (шаблон готов).
5. [ ] (опц.) Парсер НОВЫХ лидов: каталоги РБ (b2b.by/tam.by/flagma) + ПВТ-реестр + rabota.by → компания+email (рост базы за 3789).
6. [ ] Дешёвые улучшения доставляемости: `List-Unsubscribe` заголовок в Build Email; DMARC → `p=quarantine`.

## Гочи
- Mail.ru лимит ~сотни/день, холодные режутся → НЕ превышать дневной cap, прогрев обязателен.
- 194 из «без email» = t.me-заглушки ПВТ (парсить нечего, нужен реальный домен через поиск).
- ⚠️ Есть параллельный `backlink-agent-autonomous` (Gmail API venv+OAuth) — это ДРУГАЯ система (беклинк-аутрич), не путать с FC-рассылкой.
