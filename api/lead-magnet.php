<?php
/**
 * Lead Magnet endpoint for fclass.by/komandirovochnye-kalkulyator/
 *
 * POST { email, company, source, ts } -> JSON { ok: true }
 *
 * - Saves to /api/leads.csv (private dir, .htaccess deny all)
 * - Sends notification to marketing@fclass.by
 * - Sends Excel template to user (attachment)
 * - CORS open for fclass.by
 */

header('Content-Type: application/json; charset=utf-8');
header('Access-Control-Allow-Origin: https://fclass.by');
header('Access-Control-Allow-Methods: POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') { http_response_code(204); exit; }

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    http_response_code(405);
    echo json_encode(['ok' => false, 'error' => 'method_not_allowed']);
    exit;
}

// Parse JSON body
$raw = file_get_contents('php://input');
$data = json_decode($raw, true);

if (!$data || empty($data['email'])) {
    http_response_code(400);
    echo json_encode(['ok' => false, 'error' => 'missing_email']);
    exit;
}

$email = filter_var(trim($data['email']), FILTER_VALIDATE_EMAIL);
$company = htmlspecialchars(substr(trim($data['company'] ?? ''), 0, 200), ENT_QUOTES, 'UTF-8');
$source = htmlspecialchars(substr(trim($data['source'] ?? 'unknown'), 0, 100), ENT_QUOTES, 'UTF-8');
$ts = date('Y-m-d H:i:s');
$ip = $_SERVER['REMOTE_ADDR'] ?? '';
$ua = substr($_SERVER['HTTP_USER_AGENT'] ?? '', 0, 200);

if (!$email) {
    http_response_code(400);
    echo json_encode(['ok' => false, 'error' => 'invalid_email']);
    exit;
}

// Anti-spam: simple honeypot if 'website' field exists
if (!empty($data['website'])) {
    echo json_encode(['ok' => true]); // Pretend success
    exit;
}

// 1. Save to CSV (private)
$leadsFile = __DIR__ . '/leads.csv';
$isNew = !file_exists($leadsFile);
$fp = fopen($leadsFile, 'a');
if ($fp) {
    if ($isNew) fputcsv($fp, ['ts', 'email', 'company', 'source', 'ip', 'ua']);
    fputcsv($fp, [$ts, $email, $company, $source, $ip, $ua]);
    fclose($fp);
}

// 2. Notify team
$mailTo = 'marketing@fclass.by';
$mailSubject = '[Lead] ' . $source . ' — ' . $email;
$mailBody = "Новая заявка с лид-магнита:\n\n";
$mailBody .= "Email: $email\n";
$mailBody .= "Компания: " . ($company ?: '—') . "\n";
$mailBody .= "Источник: $source\n";
$mailBody .= "Время: $ts\n";
$mailBody .= "IP: $ip\n\n";
$mailBody .= "Открыть лиды: https://fclass.by/api/leads.csv (требует Basic Auth)\n";

$headers = "From: lead-magnet@fclass.by\r\n" .
           "Reply-To: $email\r\n" .
           "MIME-Version: 1.0\r\n" .
           "Content-Type: text/plain; charset=utf-8\r\n" .
           "X-Mailer: PHP/" . phpversion();

@mail($mailTo, mb_encode_mimeheader($mailSubject, 'UTF-8'), $mailBody, $headers);

// 3. Send template to user
$userSubject = 'Калькулятор командировочных РБ 2026 — Excel-шаблон + чеклист';
$userBody = <<<EOT
Здравствуйте!

Спасибо что воспользовались калькулятором командировочных на fclass.by.

Excel-шаблон для авансового отчёта и чек-лист бухгалтера на 18 пунктов:
→ https://fclass.by/api/template.xlsx
→ https://fclass.by/api/checklist-buhgaltera-2026.pdf

Ниже — наши топ-материалы по командировкам в 2026:

• Командировка в Россию из Беларуси: документы, суточные, маршруты
  https://fclass.by/blog/komandirovka-v-rossiyu-2026.html

• Командировка в Казахстан 2026
  https://fclass.by/blog/komandirovka-v-kazahstan-2026.html

• Суточные с 4 апреля 2026: Постановление №135
  https://fclass.by/blog/sutochnye-s-4-aprelya-2026.html

Если нужно организовать командировку под ключ — мы делаем это для юрлиц и ИП в РБ:
→ Билеты, гостиница, трансфер, полный пакет закрывающих документов
→ Договор с отсрочкой 14-30 дней (УНП 193582943)
→ Заявка за 15 минут: https://fclass.by/#contact

— First Class Travel
+375 44 772-52-66
marketing@fclass.by
EOT;

$userHeaders = "From: First Class <marketing@fclass.by>\r\n" .
               "Reply-To: marketing@fclass.by\r\n" .
               "MIME-Version: 1.0\r\n" .
               "Content-Type: text/plain; charset=utf-8\r\n";

@mail($email, mb_encode_mimeheader($userSubject, 'UTF-8'), $userBody, $userHeaders);

// 4. Optional: Telegram notification (if BOT_TOKEN env var set)
$tgToken = getenv('TG_BOT_TOKEN');
$tgChat = getenv('TG_CHAT_ID');
if ($tgToken && $tgChat) {
    $tgMsg = "🎯 Новый лид fclass.by\n\n📧 $email\n🏢 " . ($company ?: '—') . "\n🔗 $source";
    @file_get_contents("https://api.telegram.org/bot$tgToken/sendMessage?chat_id=$tgChat&text=" . urlencode($tgMsg));
}

// Done
echo json_encode([
    'ok' => true,
    'message' => 'Шаблон отправлен на email. Проверьте папку «Промоакции» в Gmail если не видите письмо в Inbox.'
]);
