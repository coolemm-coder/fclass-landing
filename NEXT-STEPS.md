# NEXT-STEPS — FC холодная рассылка (доделать)

> Создано 2026-05-23. Полный контекст: memory `fc-cold-email-system.md`.

## Статус
- ✅ Доставляемость проверена: mail-tester **7.9/10**, SPF+DKIM проходят (SMTP = Mail.ru подтверждён), DMARC p=none.
- ✅ Решение Эмиля: **медленный дрип с fclass.by** (~30-50/день + прогрев; не отдельный домен, не ESP).
- ✅ Парсер email готов: `scripts/email_parser.py` (прогон по 248 → +26 в `data/all_contacts.enriched.csv`).
- ✅ Список: `data/all_contacts.csv` — 3528/3789 с email.
- ✅ Воркфлоу есть: FC_ColdEmail_Campaign `RPVnm6DlyS1AK4JS` (webhook-триггер), FC_ManualSend `H8YOY2gf3rZANXFl`. SMTP cred `VpkGLKfbHK9X4zNb`.

## ДОДЕЛАТЬ — slow-drip двигатель
1. [ ] Залить контакты (3528+26) в источник, читаемый n8n ежедневно: Google Sheet «FC_Leads» или n8n DataTable. (n8n MCP лежит → строить через REST: POST `/api/v1/workflows` + `/activate`; `--resolve emikss.host:443:91.218.143.156`, ключ `$N8N_API_KEY`.)
2. [ ] Воркфлоу-планировщик: Schedule daily → читает источник → дедуп по sent-логу (static `sentEmails`) → берёт next N (warmup: нед.1 ~20/д → ~50/д) → Build+SMTP (реюз из FC_ColdEmail) → отметка sent + лог в Sheet.
3. [ ] Сегмент `category` → выбор v2-шаблона (`data/email_templates_v2_plaintext.md`: Экспортёры / IT-ПВТ / «киты»).
4. [ ] (опц.) Follow-up через 3-4 дня без ответа (шаблон готов).
5. [ ] (опц.) Парсер НОВЫХ лидов: каталоги РБ (b2b.by/tam.by/flagma) + ПВТ-реестр + rabota.by → компания+email (рост базы за 3789).
6. [ ] Дешёвые улучшения доставляемости: `List-Unsubscribe` заголовок в Build Email; DMARC → `p=quarantine`.

## Гочи
- Mail.ru лимит ~сотни/день, холодные режутся → НЕ превышать дневной cap, прогрев обязателен.
- 194 из «без email» = t.me-заглушки ПВТ (парсить нечего, нужен реальный домен через поиск).
- ⚠️ Есть параллельный `backlink-agent-autonomous` (Gmail API venv+OAuth) — это ДРУГАЯ система (беклинк-аутрич), не путать с FC-рассылкой.
