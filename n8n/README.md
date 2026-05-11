# n8n Workflows — FirstClass_Automation

## Server

- **URL:** https://emikss.host
- **Auth:** Login через браузер или N8N_API_KEY

## Workflows

### fc_lead_webhook.json
- **Trigger:** `POST https://emikss.host/webhook/fc-lead`
- **Input:** `{ name, phone, email, company, message, source, timestamp }`
- **Output:** Telegram message → Chat ID 543428212
- **Used by:** fclass.by contact form, web-panel

### fc_audit_webhook.json
- **Trigger:** `POST https://emikss.host/webhook/fc-audit`
- **Input:** `{ role, answers: [...], timestamp }`
- **Output:** Telegram message → Chat ID 543428212
- **Used by:** Audit questionnaire forms

### ai_manager_assistant.json
- **Trigger:** Manual / API call
- **Function:** AI-assisted tour search using Claude API
- **Output:** Formatted tour recommendations

## How to Import

1. Login: https://emikss.host
2. Workflows → Import from File → select JSON
3. Update credentials:
   - Telegram: set Bot Token + Chat ID via n8n Credentials
   - Claude: set API key via n8n Credentials
4. Test webhook: `curl -X POST https://emikss.host/webhook/fc-lead -H "Content-Type: application/json" -d '{"name":"test","phone":"test"}'`
5. Activate workflow

## Known Issues

- ⚠️ Telegram Chat ID hardcoded (should be in n8n credentials)
- ⚠️ No error handling for failed Telegram sends
- ⚠️ No Google Sheets logging (TODO)

## Missing Workflows (planned)

- [ ] FC_ColdEmail_Scheduler — автоматическая email-рассылка
- [ ] FC_EmailTracker — трекинг открытий и кликов
- [ ] FC_FollowUp — автоматический follow-up через 4 дня
- [ ] FC_LeadScoring — квалификация лидов через AI

---

*Обновлено: 2026-03-27*
