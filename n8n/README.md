# n8n Workflows — FirstClass_Automation

## Server

- **URL:** https://emikss.host
- **Auth:** Login через браузер или N8N_API_KEY

## Workflows

### fc_lead_webhook.json
- **Trigger:** `POST https://emikss.host/webhook/fc-lead`
- **Input:** `{ name, phone, email, company, message, comment, source, page, route, date, pax, payment, timestamp }`
- **Output:** Telegram message → группа лидов First Class
- **Chat ID:** `FCLASS_LEADS_CHAT_ID` в env n8n или ручная замена `-100REPLACE_WITH_GROUP_ID`
- **Used by:** fclass.by contact forms, /komandirovki/, /tickets/aviabilety-dlya-yurlic/, web-panel

### fc_ticket_request_webhook.json
- **Trigger:** `POST https://emikss.host/webhook/fc-ticket-request`
- **Input:** `{ name, phone, email, route, date, pax, comment, source, page, timestamp }`
- **Output:** Telegram message → группа лидов First Class
- **Chat ID:** `FCLASS_LEADS_CHAT_ID` в env n8n или ручная замена `-100REPLACE_WITH_GROUP_ID`
- **Used by:** route pages under `/tickets/` and direct flights forms

### fc_audit_webhook.json
- **Trigger:** `POST https://emikss.host/webhook/fc-audit`
- **Input:** `{ role, answers: [...], timestamp }`
- **Output:** Telegram message → Chat ID 543428212
- **Used by:** Audit questionnaire forms

### ai_manager_assistant.json
- **Trigger:** Manual / API call
- **Function:** legacy AI assistant workflow; do not use it for public fclass.by positioning without removing tour logic
- **Output:** legacy formatted recommendations

## How to Import

1. Login: https://emikss.host
2. Workflows → Import from File → select JSON
3. Update credentials:
   - Telegram: set Bot Token in n8n Credentials
   - Leads group: add `@travelangelby_bot` to the Telegram group and set env `FCLASS_LEADS_CHAT_ID` to the group id, usually `-100...`
   - Claude: set API key via n8n Credentials
4. Test webhook: `curl -X POST https://emikss.host/webhook/fc-lead -H "Content-Type: application/json" -d '{"name":"test","phone":"test"}'`
5. Activate workflow

## Known Issues

- The real Telegram group id still must be supplied in n8n as `FCLASS_LEADS_CHAT_ID` or pasted into each Telegram node.
- No fallback channel if Telegram send fails.
- No Google Sheets/CRM logging yet.

## Missing Workflows (planned)

- [ ] FC_ColdEmail_Scheduler — автоматическая email-рассылка
- [ ] FC_EmailTracker — трекинг открытий и кликов
- [ ] FC_FollowUp — автоматический follow-up через 4 дня
- [ ] FC_LeadScoring — квалификация лидов через AI

---

*Обновлено: 2026-05-15*
