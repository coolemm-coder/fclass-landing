#!/bin/bash
# Запись скринкастов через твой Chrome (уже залогинен) + macOS screencapture
# Запуск: bash scripts/record-screencast.sh

APP_ID="987255807812535"
SUBMISSION="987270334477749"
WORKFLOW_ID="s9Ywcb4QkN1jRfyb"
WEBHOOK_URL="https://emikss.host/webhook/fc-instagram-dm"
N8N_URL="https://emikss.host"
OUT="/Users/admin/Desktop/FirstClass_Automation/data/screencasts"

mkdir -p "$OUT"
CHROME="open -a 'Comet'"

open_tab() {
  osascript -e "tell application \"Comet\" to open location \"$1\""
}

echo "================================================"
echo "  Meta App Review — Запись скринкастов"
echo "================================================"
echo ""
echo "Убедись что Chrome открыт и залогинен в:"
echo "  ✓ Meta Developer Portal"
echo "  ✓ n8n (emikss.host)"
echo "  ✓ Telegram Web"
echo ""
read -p "Готов? Нажми Enter..."

# ══════════════════════════════════════════════════
# ВИДЕО 1: instagram_business_basic (~70 сек)
# ══════════════════════════════════════════════════
echo ""
echo "▶ Видео 1: instagram_business_basic (70 сек)"
echo "  Запускаю запись..."

screencapture -v -V 72 -k "$OUT/instagram_business_basic.mov" &
REC_PID=$!
sleep 2

echo "  → Meta App Settings..."
open_tab "https://developers.facebook.com/apps/$APP_ID/settings/basic/"
sleep 12

echo "  → Instagram Business раздел..."
open_tab "https://developers.facebook.com/apps/$APP_ID/instagram-business/"
sleep 12

echo "  → Webhooks..."
open_tab "https://developers.facebook.com/apps/$APP_ID/webhooks/"
sleep 12

echo "  → App Review форма..."
open_tab "https://developers.facebook.com/apps/$APP_ID/app-review/submissions/?submission_id=$SUBMISSION&business_id=5010918918978380"
sleep 18

echo "  Ожидаю конца записи..."
wait $REC_PID

# Конвертация
ffmpeg -i "$OUT/instagram_business_basic.mov" -c:v libx264 -preset fast -crf 20 \
  "$OUT/instagram_business_basic.mp4" -y -loglevel error
rm "$OUT/instagram_business_basic.mov"
SIZE=$(du -sh "$OUT/instagram_business_basic.mp4" | cut -f1)
echo "  ✅ instagram_business_basic.mp4 ($SIZE)"

sleep 3

# ══════════════════════════════════════════════════
# ВИДЕО 2: instagram_business_manage_messages (~100 сек)
# ══════════════════════════════════════════════════
echo ""
echo "▶ Видео 2: instagram_business_manage_messages (100 сек)"
echo "  Запускаю запись..."

screencapture -v -V 130 -k "$OUT/instagram_business_manage_messages.mov" &
REC_PID=$!
sleep 2

echo "  → Instagram Direct (Даша)..."
open_tab "https://www.instagram.com/direct/inbox/"
sleep 15

echo "  → n8n workflow..."
open_tab "$N8N_URL/workflow/$WORKFLOW_ID"
sleep 10

echo "  → Отправка тестового DM..."
curl -s -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d "{
    \"object\": \"instagram\",
    \"entry\": [{
      \"id\": \"17841443163477494\",
      \"time\": $(date +%s),
      \"messaging\": [{
        \"sender\": {\"id\": \"6823941070982134\"},
        \"recipient\": {\"id\": \"17841443163477494\"},
        \"timestamp\": $(date +%s000),
        \"message\": {
          \"mid\": \"test_$(date +%s)\",
          \"text\": \"Привет! Хочу тур в Египет на 2 взрослых в июле, бюджет ~2000 долларов\"
        }
      }]
    }]
  }" && echo "  ✅ Вебхук отправлен!"

sleep 5

echo "  → n8n история выполнений..."
open_tab "$N8N_URL/workflow/$WORKFLOW_ID/executions"
sleep 18

echo "  → Telegram Web..."
open_tab "https://web.telegram.org/k/"
sleep 25

echo "  → Возврат в n8n..."
open_tab "$N8N_URL/workflow/$WORKFLOW_ID/executions"
sleep 12

echo "  Ожидаю конца записи..."
wait $REC_PID

# Конвертация
ffmpeg -i "$OUT/instagram_business_manage_messages.mov" -c:v libx264 -preset fast -crf 20 \
  "$OUT/instagram_business_manage_messages.mp4" -y -loglevel error
rm "$OUT/instagram_business_manage_messages.mov"
SIZE=$(du -sh "$OUT/instagram_business_manage_messages.mp4" | cut -f1)
echo "  ✅ instagram_business_manage_messages.mp4 ($SIZE)"

# ══════════════════════════════════════════════════
echo ""
echo "================================================"
echo "  ГОТОВО! Видео в папке:"
echo "  $OUT"
echo "================================================"
ls -lh "$OUT"/*.mp4
echo ""
echo "Следующий шаг — загрузи в Meta App Review:"
echo "  https://developers.facebook.com/apps/$APP_ID/app-review/submissions/?submission_id=$SUBMISSION"
