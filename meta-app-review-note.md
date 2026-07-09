# Meta App Review — Submission Note

## Copy this text into the App Review submission note:

---

**This is a server-to-server application.** There is NO client-side login flow.

We use a **System User access token** (generated in Meta Business Manager) to authenticate all API calls from our backend server. The Meta Login dialog is NOT visible on the client side because our app operates entirely server-to-server.

### How we use each permission:

**instagram_business_basic**
- We call `GET /{user-id}` to retrieve the sender's Instagram profile (name, username) when a new DM arrives via webhook.
- This allows our human travel consultant to identify the customer before responding.

**instagram_business_manage_messages**
- We receive incoming Instagram DM webhooks (POST to our n8n server endpoint).
- We do NOT send any automated replies. No messages are ever sent back to the customer through the API.
- Each incoming DM is classified (destination, dates, budget) and forwarded as a lead card to our human travel consultant via Telegram bot.
- The consultant personally reviews each lead and responds manually through the Instagram app.

### Technical architecture:
1. Customer sends a DM to our Instagram Business account (@dasha_turaget_minsk)
2. Meta delivers the webhook payload to our n8n server (https://automation.landingpro.by)
3. n8n workflow "FC_Instagram_DM_Router" processes the DM:
   - Parses the message
   - Fetches sender profile via instagram_business_basic
   - Checks U-ON CRM for returning customers
   - Classifies the lead (destination, dates, budget, party size)
4. Classified lead card is sent to human consultant via Telegram bot (@fclassmsk_bot)
5. Human consultant reviews the lead and responds personally via Instagram DM

### Key points:
- **Human-in-the-loop**: Every lead is reviewed by a human before any response
- **No automated replies**: We never send messages to customers through the API
- **Server-to-server**: System User token authenticates all API calls
- **No client-side login**: There is no Meta Login flow in our application

App ID: 987255807812535
Business ID: 5010918918978380
Contact: coolemm@gmail.com

---
