# fclass-landing — fclass.by

## Проект
Статический сайт First Class (fclass.by): авиабилеты для физлиц и юрлиц, организация командировок и визовая поддержка. HTML + inline CSS + JS. Хостинг: ISPmanager (FTP). GitHub → FTP sync через GitHub Actions.

## Сообщение для Claude / следующего агента

Последние изменения от Codex на 2026-05-15:

- `fix(seo): repair FAQ structured data`
  - после конкурентного SEO-аудита Topavia проверена JSON-LD разметка на ключевых коммерческих страницах;
  - исправлен битый `FAQPage` JSON-LD на `/komandirovki/` и `/tickets/aviabilety-dlya-yurlic/`: теперь все `application/ld+json` блоки парсятся валидно;
  - видимый текст страниц не менялся, правка только техническая для поисковой разметки.
- `fix(deploy): replace FTP action with curl uploads`
  - после повторных падений `SamKirkland/FTP-Deploy-Action` с `FTPError: 502 Command not implemented` и зависания `lftp mirror` workflow переведен на прямую загрузку файлов через `curl --ftp-create-dirs`;
  - новый деплой не зависит от `.ftp-deploy-sync-state.json`, который action периодически не видел на FTP-сервере и из-за этого пытался выполнить "первую публикацию";
  - деплой загружает публичные файлы по allow/exclude-списку без удаления старых файлов; публичные внутренние URL по-прежнему закрывает `.htaccess`.
- `fix(conversion): route main contacts through Telegram bot`
  - на главной основной контактный сценарий переведен с формы на `@travelangelby_bot`: nav CTA, hero secondary CTA, contact section, final CTA, floating Telegram, footer/social и mobile sticky Telegram получают `start=lead_*`;
  - старый `contact-form` на главной заменен на карточку Telegram-бота с квалификацией заявки: тип запроса, даты/маршрут/пассажиры, контакт и уведомление менеджеров;
  - JS отправки формы на главной оставлен с guard на случай возврата формы, но сейчас не ломает страницу без `#contact-form`;
  - для реальной отправки квалифицированных лидов в группу нужно, чтобы логика `@travelangelby_bot` передавала ответы в группу/CRM; в n8n уже есть webhook `fc-lead`, но текущий chatId в файле workflow — персональный `543428212`, group chat id нужно подставить отдельно.
- `fix(local): correct Yandex location and calculator rate`
  - главная переведена на точную карточку Яндекс Карт `pervy_klass/68945387734`: отзывы ведут на `/reviews/`, карта использует `oid=68945387734`, адрес в видимом тексте и Schema.org — `г. Минск, просп. Победителей, 11`;
  - в FAQ главной заменено `рейтинг 5.0 на Google Maps` на `рейтинг 5.0 на Яндекс Картах`, чтобы не смешивать источники отзывов;
  - на главной в MICE-блоке убраны `incentive`/тимбилдинг-за-рубежом, оставлены конференции, выставки, деловые встречи и логистика участников;
  - в `/komandirovochnye-kalkulyator/` курс USD/BYN больше не зашит как `3.20`: fallback `2.80`, при загрузке страница пробует подтянуть официальный курс Нацбанка РБ через API, поле остается ручным;
  - неоднозначные ссылки `Калькулятор` в футерах переименованы в `Калькулятор командировочных`, а внутренний SEO-текст на `/komandirovki/` заменен пользовательским описанием услуги.
- `fix(copy): remove fixed discount promises from ticket pages`
  - по замечанию владельца убраны публичные обещания фиксированных скидок `10-25%`, `15-25%`, `15-20%` и похожие формулировки из маршрутных страниц, калькулятора, кейсов, шаблона блога и статей;
  - вместо скидок использовать формулировки: `подберём тариф`, `условия оплаты согласуем до выписки`, `состав документов по НДС согласуем до оплаты`, `для юрлиц — безналичная оплата и пакет документов`;
  - не возвращать в публичный текст обещания вида `скидка 15-25%`, `GDS-скидки 10-25%`, `экономия 15-20%`: это выглядит как неподтверждённая гарантия и конфликтует с текущим позиционированием.
- `fix(conversion): add lead forms to top SEO articles`
  - по данным Метрики прямые формы добавлены в две SEO-страницы с основным трафиком: `/blog/komandirovka-v-rossiyu-2026.html` и `/blog/sutochnye-komandirovka-2026.html`;
  - формы отправляют заявки в `https://emikss.host/webhook/fc-lead`, цель Метрики `LEAD`, GA event `generate_lead`, источники `blog_komandirovka_rossiya`, `blog_komandirovka_rossiya_bottom`, `blog_sutochnye_komandirovka`;
  - в этих же местах очищены публичные формулировки `корпоративные авиабилеты` в пользу `авиабилеты для юрлиц`/`договор для юрлиц`.
- `fix(conversion): clean direct flights CTA`
  - в `/blog/pryamye-reysy-iz-minska-2026.html` заменен CTA-ссылка на прямую форму подбора билета с `source=blog_pryamye_reysy`;
  - убраны публичные обещания скидки `15–25%` и жесткие обещания документов по НДС; формулировка теперь: документы по НДС/ЭСЧФ согласуются до оплаты там, где они предусмотрены поставщиком и типом услуги;
  - очищены видимые `корпоративные авиабилеты`/`корпоративный договор` в перелинковке и футере этой статьи.
- `fix(copy): clean legal entity ticket contract article`
  - в старой статье `/blog/korporativnye-aviabilety-minsk.html` оставлен SEO-URL, но видимое позиционирование переписано как `договор на авиабилеты для юрлиц`/`договор для юрлиц`;
  - удалены гарантированные скидки `15–25%`, точные обещания отсрочки/НДС/ЭСЧФ и неподтвержденные цифры; условия оплаты, спецтарифы и состав документов теперь описаны как согласуемые до выписки билета;
  - финальный CTA заменен на форму заявки `source=blog_yurlic_contract` в `https://emikss.host/webhook/fc-lead`.
- `fix(copy): remove legacy discount claims`
  - публичные остатки `корпоративные авиабилеты`, `корпоративный договор`, `скидка 15–25%`, фиксированная отсрочка и автоматические документы очищены в: `/blog/belavia-novye-reysy-2026.html`, `/blog/komandirovka-v-moskvu-iz-minska.html`, `/blog/komandirovka-v-sankt-peterburg-iz-minska.html`, `/blog/komandirovka-v-gruziyu-2026.html`, `/blog/komandirovki-belarus-2026.html`, `/blog/organizaciya-komandirovok.html`, `/blog/aviabilety-minsk-stambul.html`, `/blog/komandirovka-v-polshu-2026.html`, `/tickets/minsk-dubai/`, `/tickets/minsk-istanbul/` (редиректный legacy-файл), `/concierge/`, `/resources/calculator/`, `/cases/`;
  - новое правило: не обещать фиксированный процент экономии; писать `договор для юрлиц`, `безналичная оплата`, `условия и документы согласуем до оплаты`.
- `fix(seo): shorten commercial metadata`
  - по sitemap-аудиту сокращены слишком длинные `<title>` и meta description на коммерческих страницах: `/tickets/`, маршрутные посадочные `/tickets/minsk-*`, `/komandirovochnye-kalkulyator/`, `/resources/dogovor-template/`, `/resources/calculator/`, `/cases/`;
  - в OG-описаниях старых маршрутных страниц убраны быстро устаревающие цены/частоты рейсов, оставлены устойчивые формулировки про GDS, оплату для физлиц/юрлиц и подбор тарифа.
  - тем же проходом сокращены длинные title/description в блоговых страницах из sitemap; публичные факты не расширялись, наоборот убраны лишние быстро устаревающие цифры из сниппетов.
  - в JSON-LD `Service` на старых маршрутных страницах `/tickets/minsk-moskva/`, `/minsk-stambul/`, `/minsk-tbilisi/`, `/minsk-batumi/`, `/minsk-tashkent/`, `/minsk-spb/` убраны фиксированные `offers.price` и формулировки `цены от ...`.
  - после проверки Яндекс.Вебмастера добавлен 301 для мусорных root-URL с `token`/`uid`/`status`, прямой `/mobile-preview.html` редиректится на `/`, а blog-title `/blog/aviabilety-minsk-stambul.html` разведен с посадочной `/tickets/minsk-stambul/`.
- `fix(conversion): tighten Telegram and lead tracking`
  - заменены нерабочие/неоднородные Telegram-ссылки `t.me/+375447725266`, `firstclass_by`, `firstclassby` на единый `travelangelby_bot`;
  - на внутренних страницах исправлены битые якоря `#services`, `#contact`, `#expertise` на ссылки к главной `/#...`;
  - на старых маршрутных страницах добавлен трекинг успешной отправки формы в Метрику (`LEAD`) и GA (`generate_lead`).
  - в `/resources/dogovor-template/` публичная формулировка `договор с турагентством` заменена на `договор с агентством`.
  - по sitemap-аудиту исправлены критичные SEO-пропуски: добавлен `<title>` на `/blog/visa-guide-2026.html`, canonical/OG URL на `/blog/komandirovka-v-kazahstan-2026.html` и `/blog/komandirovka-v-kitay.html`.
  - исторически в `.github/workflows/deploy.yml` включался `FORCE_JAVASCRIPT_ACTIONS_TO_NODE24=true`; затем workflow переведен с FTP-Deploy-Action на прямой `curl` upload.
- `fix(copy): remove remaining passport and tourism wording`
  - после live-проверки дополнительно очищены регистрозависимые остатки `Загранпаспорт` на `/blog/vizovaya-podderzhka-minsk.html`;
  - в `/blog/komandirovka-v-kitay.html`, `/blog/komandirovka-v-uzbekistan-2026.html`, `/blog/komandirovka-v-gruziyu-2026.html` заменены лишние упоминания `туризм` на частные поездки/сервис там, где это не визовый тип;
  - обновлены `dateModified` и `sitemap.xml` для затронутых страниц.
- `fix(content): clean legacy travel positioning`
  - очищены старые страницы `/blog/delovoy-turizm-belarus-2026.html` и `/blog/mice-belarus-2026.html`: вместо туров/инсентив-туров теперь деловые поездки, MICE-мероприятия, логистика участников и документы;
  - на `/blog/delovoy-turizm-belarus-2026.html` удалены неподтвержденные рейтинги/прогнозы, добавлены canonical, Open Graph и JSON-LD;
  - переписана спорная статья `/blog/viza-v-oae-dlya-belorusov-2026.html`: убраны обещания фиксированных сроков/стоимости визы, старый телефон и фейковый офис, добавлена проверка актуальных правил въезда до оплаты билета;
  - на `/tickets/minsk-dubai/` убраны утверждения про гарантированную визу по прилёту и `загранпаспорт`, оставлена аккуратная проверка правил въезда;
  - на `/tickets/minsk-istanbul/` убраны неподтвержденные утверждения про топ-5/загрузку рейса; на этой же странице, `/blog/komandirovka-v-moskvu-iz-minska.html`, `/blog/komandirovka-v-sankt-peterburg-iz-minska.html` заменены некорректные для РБ формулировки `загранпаспорт`/`внутренний паспорт` на `паспорт гражданина РБ`;
  - дополнительно вычищены остатки `турагентство`/`туристические` там, где это выглядело как продажа туров: `/blog/korporativnye-aviabilety-minsk.html`, `/blog/organizaciya-komandirovok.html`, `/blog/belavia-novye-reysy-2026.html`, `/blog/komandirovka-v-gruziyu-2026.html`, `/blog/komandirovki-belarus-2026.html`, `/blog/loukostery-iz-minska-2026.html`, `/blog/pryamye-reysy-iz-minska-2026.html`, `/blog/aviabilety-minsk-stambul.html`;
  - в `/blog/komandirovka-v-rossiyu-2026.html`, `/blog/komandirovka-v-kazahstan-2026.html`, `/blog/visa-guide-2026.html`, `/blog/vizovaya-podderzhka-minsk.html` очищены публичные формулировки про паспорт гражданина РБ;
  - обновлены `dateModified`/`sitemap.xml` для затронутых страниц.
- `feat(seo): add route landing pages and clean business travel copy`
  - добавлены посадочные страницы `/tickets/minsk-kaliningrad/`, `/tickets/minsk-sochi/`, `/tickets/minsk-baku/`, `/tickets/minsk-sharm-el-sheikh/`;
  - для новых route pages вынесены общие стили и JS в `/tickets/route-page.css` и `/tickets/route-page.js`, формы отправляют заявки в `https://emikss.host/webhook/fc-ticket-request`;
  - обновлена перелинковка в `/tickets/`, `/tickets/direct-flights/` и `sitemap.xml`;
  - в GitHub Actions verify deploy добавлены проверки новых route pages;
  - `/visa-support/` добавлен как 301-редирект на актуальную статью `/blog/vizovaya-podderzhka-minsk.html`, чтобы старые nav-ссылки не вели в 404;
  - добавлена техническая страница `/privacy/` для старых футерных ссылок и форм заявок (`noindex,follow`);
  - старая статья `/blog/komandirovka-v-kaliningrad-iz-minska.html` обновлена под актуальную логику: сначала прямой рейс, стыковка через Москву/СПб только запасной вариант;
  - в `/blog/organizaciya-komandirovok.html` убраны туровые формулировки из текста про командировки (`туристическая страховка`, `деловые встречи + туризм`, `застраховывают туристов`);
  - в старом футере `/blog/aviabilety-minsk-stambul.html` ссылка `B2C туры` заменена на авиабилеты для частных клиентов.
- `fix(deploy): exclude internal runtime artifacts from FTP`
  - после push `d4a8924` GitHub Actions упал на FTP `502 Command not implemented` при создании `/api/`;
  - дополнительно исключены из FTP deploy: `/api/`, `/n8n-workflows/`, `package*.json`, `vercel.json`, `robots-vercel.txt`, `meta-*.md`, `firstclass-growth-playbook.html`, `firstclass-gtm-plan.html`;
  - эти же внутренние/служебные URL закрыты через `.htaccess` с HTTP 410;
  - verify deploy теперь проверяет, что внутренние URL не отдают публичный 200.
- `fix(seo): close public artifacts and tighten ticket pages`
  - закрыты публичные внутренние URL через `.htaccess`: `/docs/`, `/web-panel/`, `/questionnaires/`, `/content/`, `/scripts/`, вложенный `/fclass-landing/`, `/blog/_template.html`;
  - эти же внутренние папки исключены из FTP deploy в `.github/workflows/deploy.yml`, чтобы они не публиковались повторно;
  - `/tickets/minsk-istanbul/` канонизирован 301-редиректом на основной `/tickets/minsk-stambul/`;
  - в `sitemap.xml` добавлены `/tickets/direct-flights/`, `/tickets/minsk-dubai/` и новые статьи про командировки в Москву, Санкт-Петербург и Калининград;
  - на `/tickets/direct-flights/` добавлена форма заявки прямо в CTA-блок, отправка идет в `https://emikss.host/webhook/fc-ticket-request`, цель Метрики `LEAD`, GA event `generate_lead` с `event_label=direct_flights`;
  - битые/неверсионируемые OG-картинки в блоге, `/cases/` и `/resources/` заменены на `/hero-bg.jpg`;
  - в репозиторий возвращены публичные ассеты из live/локальных копий: `logo.png`, `hero-bg.jpg`, `hero-bg.webp`, `about-bg.jpg`, `about-bg.webp`, `favicon.ico`, `favicon.png`, изображения блога в `images/blog/`;
  - сокращены meta description/title на `/tickets/` и `/tickets/aviabilety-dlya-yurlic/`;
  - старая статья `/blog/korporativnye-aviabilety-minsk.html` частично смещена в сторону "договор/авиабилеты для юрлиц", без усиления термина "корпоративные авиабилеты" в title/H1;
  - `blog/_template.html` переведен в `noindex,nofollow` как дополнительная страховка, хотя он также закрыт через `.htaccess` и исключен из deploy.
- `08918ed fix(copy): clean up VAT wording on legal entity tickets`
  - на `/tickets/aviabilety-dlya-yurlic/` убрать любые внутренние SEO-формулировки вроде `Wordstat`;
  - формулировать НДС клиентски: "состав документов согласуем заранее", "ЭСЧФ по услугам, где НДС предусмотрен";
  - не писать на публичной странице фразы вроде "лучше уточнять" или "в Wordstat есть спрос".
- `6c5d63f fix(seo): sharpen legal entity ticket terms`
  - усилена `/tickets/aviabilety-dlya-yurlic/` под Wordstat-запросы `авиабилеты для юридических лиц`, `авиабилеты по безналичному расчету`, `авиабилеты с ндс для юридических лиц`, `купить авиабилеты по безналу`;
  - добавлены блоки про покупку по безналу, документы по НДС/ЭСЧФ с аккуратной оговоркой "если применимо", FAQ и внутренний переход из старой статьи `/blog/korporativnye-aviabilety-minsk.html`;
  - не обещать НДС для каждого билета: состав документов зависит от маршрута, перевозчика, поставщика и типа услуги.
- `6883be1 feat(seo): add business travel and legal entity ticket pages`
  - добавлены `/komandirovki/` и `/tickets/aviabilety-dlya-yurlic/`;
  - добавлены ссылки с главной, `/tickets/`, `/blog/` и `sitemap.xml`;
  - новые формы отправляют в тот же webhook `https://emikss.host/webhook/fc-lead` с `source=landing_komandirovki` и `source=landing_tickets_yurlic`;
  - деплой GitHub Actions прошёл успешно, живые URL проверены.
- `be01b9e fix(positioning): clarify ticket service audience`
  - очищены формулировки про "корпоративные авиабилеты";
  - позиционирование: авиабилеты для физлиц и юрлиц, командировки для бизнеса;
  - старая ссылка `/tours/` в билетном футере заменена на `/tickets/direct-flights/`.

Wordstat-выгрузки лежат рядом с репозиторием в `/Users/admin/Documents/Codex/2026-05-13/fclass-by/`:

- `wordstat-fclass-services-2026-05-13.md`
- `service-wordstat-seo-priorities-2026-05-13.md`
- `wordstat-yurlic-beznal-2026-05-13.md`
- `wordstat-fclass-avia-2026-05-13.md`

Важный вывод по SEO: основной трафиковый кластер — авиабилеты/рейсы из Минска; самый коммерческий B2B-кластер — командировки и авиабилеты для юридических лиц по безналичному расчёту. Туров у компании нет, не возвращать туровое позиционирование.

При будущих изменениях обновлять этот блок короткой строкой: коммит, что поменялось, какие URL затронуты, деплой/проверка.

## Дизайн-система: Sapphire Dreams

| Токен | Значение |
|-------|----------|
| --primary | #0c1825 (тёмно-синий) |
| --primary-light | #1a3a5c |
| --accent | #c9a962 (золото) |
| --cream | #f8f9fa |
| --font-sans | 'DM Sans', sans-serif |
| --font-serif | 'Playfair Display', serif |

## Белорусская специфика — ОБЯЗАТЕЛЬНО

### Запрещённые термины (российские реалии → белорусские)

| НЕ писать | Писать | Почему |
|-----------|--------|--------|
| загранпаспорт | паспорт / паспорт гражданина РБ | В РБ один паспорт (серия AB/BM/MC/MP) для всех целей |
| СНИЛС | страховое свидетельство | Российский документ |
| ИНН (для физлиц) | учётный номер плательщика (УНП) | В РБ другая система |
| полис ОМС | — (не упоминать) | В РБ медицина бесплатная без полиса |
| МФЦ | — (нет аналога в РБ) | Российская структура |
| ФМС | ОГиМ (отдел по гражданству и миграции) | Белорусский орган |
| ГИБДД | ГАИ | Белорусское название |
| прописка | регистрация по месту жительства | Юридически корректно |
| внутренний паспорт | паспорт | В РБ нет деления на внутренний/заграничный |

### Исключение
- "загранкомандировка" — КОРРЕКТНЫЙ термин в белорусском трудовом праве, НЕ менять.
- Когда речь о гражданах ДРУГИХ стран (россияне, казахстанцы) — использовать терминологию ИХ страны ("загранпаспорт РФ" допустим).

### Авиация — проверять ВСЕГДА через WebSearch
- Прямые рейсы из Минска: расписание меняется, ВСЕГДА проверять актуальность
- ЕС-санкции: нет прямых рейсов Минск↔ЕС с мая 2021
- Belavia НЕ летает в ЕС. LOT, Wizz Air, Lufthansa НЕ летают в Минск.
- В Европу — ТОЛЬКО с пересадкой (Москва, Стамбул, Дубай, Баку)
- НЕ рекомендовать: Skyscanner, Aviasales, Google Flights — только First Class

## Блог-посты: ПРАВИЛА

**ПЕРЕД СОЗДАНИЕМ ЛЮБОГО ПОСТА — ОБЯЗАТЕЛЬНО:**
1. Прочитай `blog/_template.html` из ЭТОГО репозитория через `mcp__github__get_file_contents`
2. Скопируй его полностью
3. Замени ТОЛЬКО контент (title, meta, article, Schema.org)
4. НЕ МЕНЯЙ: nav, footer, CSS, hero-структуру, шрифты, цвета

### Обязательные элементы
- Google Analytics: G-500FTKX6V9 (в head)
- Яндекс.Метрика: 107237229 (в head)
- Schema.org JSON-LD: BreadcrumbList + BlogPosting + FAQPage (мин. 3 вопроса)
- Canonical URL: `https://fclass.by/blog/slug.html`
- Open Graph: og:title, og:description, og:type, og:url, og:image
- Шрифты: Google Fonts — DM Sans + Playfair Display
- Hero: класс `article-hero`, gradient primary→primary-light, текст по центру
- Nav: фиксированный, logo.png, 6 ссылок + CTA "Связаться"
- Footer: 4 колонки (Бренд | Услуги | Для бизнеса | Контакты)
- CTA: класс `cta-box` + `cta-btn`, ссылка `/#contact`
- ВСЕ стили INLINE в <style> теге

### Контакты (ТОЛЬКО ЭТИ)
- Email: marketing@fclass.by
- Телефон: +375 44 772-52-66
- WhatsApp: wa.me/375447725266
- CTA ссылка: /#contact

### Правила контента
- WebSearch по КАЖДОМУ факту перед написанием
- НЕ выдумывать авиакомпании, маршруты, цены, визовые правила
- Проверять терминологию по таблице "Белорусская специфика" выше
- Авиасанкции ЕС: с мая 2021 нет прямых рейсов Минск↔ЕС
- НЕ рекомендовать Skyscanner, Aviasales, Google Flights — только First Class

### Формат файлов
- Блог-посты: `blog/slug.html` (ОДИН файл, НЕ папка с index.html)
- При создании нового поста — обновить `blog/index.html` и `sitemap.xml`

## Деплой
Push в main → GitHub Actions → валидация HTML → FTP деплой на ISPmanager.
FTP credentials в GitHub Secrets: FTP_SERVER, FTP_USERNAME, FTP_PASSWORD.

### Валидация (чеклист перед деплоем)
- [ ] Шрифты: DM Sans + Playfair Display
- [ ] Hero: gradient #0c1825 → #1a3a5c, текст по центру
- [ ] CTA: класс cta-box + cta-btn, ссылка /#contact
- [ ] Footer: 4 колонки
- [ ] Email = marketing@fclass.by
- [ ] GA (G-500FTKX6V9) + Метрика (107237229)
- [ ] Schema JSON-LD: BlogPosting + FAQPage + BreadcrumbList
- [ ] Все факты проверены через WebSearch
- [ ] Терминология проверена по таблице "Белорусская специфика"
- [ ] Нет слова "загранпаспорт" (если текст про граждан РБ)

## Эталонный пост
`blog/vizovaya-podderzhka-minsk.html` — 34KB, правильный стиль Sapphire Dreams.
