#!/bin/bash
# ============================================================
# Meta App Review — Автозапись скринкастов
# Записывает 2 видео:
#   1. instagram_business_basic (показывает IG-интеграцию в Meta Dev Portal)
#   2. instagram_business_manage_messages (полный флоу DM → n8n → Telegram)
# ============================================================

set -e

OUTPUT_DIR="$HOME/Desktop/FirstClass_Automation/data/screencasts"
mkdir -p "$OUTPUT_DIR"

APP_ID="987255807812535"
WEBHOOK_URL="https://automation.landingpro.by/webhook/fc-instagram-dm"
N8N_URL="https://automation.landingpro.by"
N8N_WORKFLOW_ID="s9Ywcb4QkN1jRfyb"
TELEGRAM_URL="https://web.telegram.org"

echo "==================================================="
echo "  Meta App Review — Запись скринкастов"
echo "==================================================="
echo ""
echo "Будет записано 2 видео:"
echo "  1. instagram_business_basic.mov (60 сек)"
echo "  2. instagram_business_manage_messages.mov (90 сек)"
echo ""
echo "ВАЖНО: перед запуском:"
echo "  - войди в Meta Developer Portal в браузере"
echo "  - войди в n8n (automation.landingpro.by)"
echo "  - войди в Telegram Web"
echo ""
read -p "Готов? Нажми Enter для старта..."

# ============================================================
# ВИДЕО 1: instagram_business_basic (60 сек)
# ============================================================
echo ""
echo "▶  Запись видео 1: instagram_business_basic (60 сек)..."
echo "   Скрипт автоматически откроет нужные страницы."
echo ""

VIDEO1="$OUTPUT_DIR/instagram_business_basic.mov"

# Запускаем запись в фоне
screencapture -v -V 65 -k "$VIDEO1" &
SCREEN_PID=$!
sleep 2  # Даём время начать запись

# Автоматически открываем страницы в браузере
open "https://developers.facebook.com/apps/$APP_ID/settings/basic/"
sleep 5
open "https://developers.facebook.com/apps/$APP_ID/instagram-business/"
sleep 8
# Показываем раздел разрешений
open "https://developers.facebook.com/apps/$APP_ID/app-review/submissions/?submission_id=987270334477749"
sleep 8
# Возвращаемся к настройкам IG
open "https://developers.facebook.com/apps/$APP_ID/instagram-business/"
sleep 10

echo "   Видео 1 записывается... ожидание завершения..."
wait $SCREEN_PID 2>/dev/null || true
sleep 1

# Конвертируем в MP4 (Meta принимает MOV но MP4 надёжнее)
echo "   Конвертация в MP4..."
ffmpeg -i "$VIDEO1" -c:v libx264 -preset fast -crf 23 \
  "$OUTPUT_DIR/instagram_business_basic.mp4" -y -loglevel error
echo "   ✅ Видео 1 готово: instagram_business_basic.mp4"

# ============================================================
# ВИДЕО 2: instagram_business_manage_messages (90 сек)
# ============================================================
echo ""
echo "▶  Запись видео 2: instagram_business_manage_messages (90 сек)..."
echo ""

VIDEO2="$OUTPUT_DIR/instagram_business_manage_messages.mov"

screencapture -v -V 95 -k "$VIDEO2" &
SCREEN_PID=$!
sleep 2

# Открываем n8n — показываем workflow
open "$N8N_URL/workflow/$N8N_WORKFLOW_ID"
sleep 10

# Отправляем тестовый вебхук (имитируем входящий IG DM)
echo "   Отправка тестового вебхука..."
curl -s -X POST "$WEBHOOK_URL" \
  -H "Content-Type: application/json" \
  -d '{
    "object": "instagram",
    "entry": [{
      "id": "17841443163477494",
      "time": '"$(date +%s)"',
      "messaging": [{
        "sender": {"id": "TEST_SENDER_123"},
        "recipient": {"id": "17841443163477494"},
        "timestamp": '"$(date +%s000)"',
        "message": {
          "mid": "test_screencast_'"$(date +%s)"'",
          "text": "Привет! Хочу тур в Египет на 2 взрослых в июле. Какие есть варианты?"
        }
      }]
    }]
  }' > /dev/null
echo "   Вебхук отправлен! Смотри n8n..."
sleep 8

# Открываем историю выполнений workflow
open "$N8N_URL/workflow/$N8N_WORKFLOW_ID/executions"
sleep 10

# Открываем Telegram Web
open "$TELEGRAM_URL"
sleep 10

echo "   Видео 2 записывается... ожидание завершения..."
wait $SCREEN_PID 2>/dev/null || true
sleep 1

echo "   Конвертация в MP4..."
ffmpeg -i "$VIDEO2" -c:v libx264 -preset fast -crf 23 \
  "$OUTPUT_DIR/instagram_business_manage_messages.mp4" -y -loglevel error
echo "   ✅ Видео 2 готово: instagram_business_manage_messages.mp4"

# ============================================================
# ГОТОВО
# ============================================================
echo ""
echo "==================================================="
echo "  ВСЕ СКРИНКАСТЫ ГОТОВЫ!"
echo "==================================================="
echo ""
echo "Файлы сохранены в:"
echo "  $OUTPUT_DIR/"
ls -lh "$OUTPUT_DIR"/*.mp4 2>/dev/null
echo ""
echo "Следующий шаг:"
echo "  1. Открой Meta App Review: Секция 3 → Допустимое использование"
echo "  2. Нажми 'Начать' для instagram_business_basic"
echo "  3. Загрузи instagram_business_basic.mp4"
echo "  4. Нажми 'Начать' для instagram_business_manage_messages"
echo "  5. Загрузи instagram_business_manage_messages.mp4"
echo "  6. Нажми 'Отправить на проверку'"
echo ""
echo "URL формы:"
echo "  https://developers.facebook.com/apps/$APP_ID/app-review/submissions/?submission_id=987270334477749"
