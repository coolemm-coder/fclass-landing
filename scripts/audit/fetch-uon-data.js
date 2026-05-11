#!/usr/bin/env node
/**
 * Аудит U-ON Travel — сбор и анализ данных
 * Запуск: node fetch-uon-data.js
 * Требует: UON_API_KEY в .env или переменных окружения
 */

require('dotenv').config({ path: require('path').join(__dirname, '../../.env') });
const { UonClient, sleep } = require('../utils/uon-client');
const fs = require('fs');
const path = require('path');

const UON_API_KEY = process.env.UON_API_KEY;

async function main() {
  if (!UON_API_KEY) {
    console.error('❌ UON_API_KEY не задан. Добавь в .env файл');
    process.exit(1);
  }

  const uon = new UonClient(UON_API_KEY);
  const report = {};

  // ─── 1. Менеджеры ────────────────────────────────────────
  console.log('📋 Загружаю список менеджеров...');
  const managers = await uon.getManagers();
  const rawMgr = managers?.data ?? managers ?? [];
  report.managers = Array.isArray(rawMgr) ? rawMgr : Object.values(rawMgr);
  console.log(`   Найдено менеджеров: ${report.managers.length}`);
  report.managers.forEach(m => console.log(`   — ${m.id}: ${m.name ?? m.full_name ?? JSON.stringify(m)}`));

  // ─── 2. Все заявки ───────────────────────────────────────
  console.log('\n📦 Загружаю все заявки (может занять время)...');
  const requests = await uon.getAllRequests();
  report.totalRequests = requests.length;
  console.log(`   Всего заявок: ${requests.length}`);

  if (requests.length === 0) {
    console.log('⚠️  Заявки не найдены. Проверь API ключ и права доступа.');
    saveReport(report);
    return;
  }

  // ─── 3. Динамика по месяцам ──────────────────────────────
  const byMonth = {};
  requests.forEach(r => {
    const date = r.dat ?? r.dat_request ?? r.created_at;
    if (!date) return;
    const month = date.substring(0, 7); // YYYY-MM
    if (!byMonth[month]) byMonth[month] = { count: 0, revenue: 0, statuses: {} };
    byMonth[month].count++;
    const price = parseFloat(r.calc_client ?? r.calc_price ?? r.calc_price_netto ?? 0);
    byMonth[month].revenue += price;
    const status = r.status ?? 'unknown';
    byMonth[month].statuses[status] = (byMonth[month].statuses[status] ?? 0) + 1;
  });
  report.byMonth = Object.entries(byMonth)
    .sort(([a], [b]) => a.localeCompare(b))
    .map(([month, data]) => ({ month, ...data }));

  // ─── 4. Статистика по менеджерам ─────────────────────────
  const byManager = {};
  requests.forEach(r => {
    const name = [r.manager_surname, r.manager_name].filter(Boolean).join(' ') || 'unknown';
    const id = r.manager_id ?? 0;
    const key = `${id}:${name}`;
    if (!byManager[key]) byManager[key] = { id, name, count: 0, closed: 0, revenue: 0, sources: {} };
    byManager[key].count++;
    const status = (r.status ?? '').toLowerCase();
    const price = parseFloat(r.calc_client ?? r.calc_price ?? 0);
    if (status.includes('закрыт') || status.includes('оплачен') || status.includes('выполнен') || status.includes('подтверждена')) {
      byManager[key].closed++;
      byManager[key].revenue += price;
    }
    const src = r.source ?? 'unknown';
    byManager[key].sources[src] = (byManager[key].sources[src] ?? 0) + 1;
  });
  report.byManager = Object.values(byManager)
    .sort((a, b) => b.count - a.count)
    .map(data => ({
      ...data,
      avgCheck: data.closed > 0 ? Math.round(data.revenue / data.closed) : 0,
      conversionRate: data.count > 0 ? ((data.closed / data.count) * 100).toFixed(1) + '%' : '0%'
    }));

  // ─── 5. Статусы заявок ───────────────────────────────────
  const byStatus = {};
  requests.forEach(r => {
    const status = r.status ?? 'unknown';
    byStatus[status] = (byStatus[status] ?? 0) + 1;
  });
  report.byStatus = Object.entries(byStatus)
    .sort(([, a], [, b]) => b - a)
    .map(([status, count]) => ({ status, count }));

  // ─── 6. Источники лидов ───────────────────────────────────
  const bySrc = {};
  requests.forEach(r => {
    const src = r.source ?? 'Не указан';
    if (!bySrc[src]) bySrc[src] = { count: 0, revenue: 0 };
    bySrc[src].count++;
    bySrc[src].revenue += parseFloat(r.calc_client ?? 0);
  });
  report.bySources = Object.entries(bySrc)
    .sort(([, a], [, b]) => b.count - a.count)
    .map(([source, d]) => ({ source, count: d.count, revenue: Math.round(d.revenue), avgCheck: d.count > 0 ? Math.round(d.revenue/d.count) : 0 }));

  // ─── 7. Средний чек и топ направления ────────────────────
  const prices = requests
    .map(r => parseFloat(r.calc_client ?? r.calc_price ?? 0))
    .filter(p => p > 0);
  report.avgCheck = prices.length > 0
    ? Math.round(prices.reduce((a, b) => a + b, 0) / prices.length)
    : 0;
  report.totalRevenue = Math.round(prices.reduce((a, b) => a + b, 0));

  const byDestination = {};
  requests.forEach(r => {
    const dest = r.travel_type ?? null;
    if (!dest) return;
    if (!byDestination[dest]) byDestination[dest] = { count: 0, revenue: 0 };
    byDestination[dest].count++;
    byDestination[dest].revenue += parseFloat(r.calc_client ?? 0);
  });
  report.topDestinations = Object.entries(byDestination)
    .sort(([, a], [, b]) => b.count - a.count)
    .slice(0, 15)
    .map(([dest, d]) => ({ dest, count: d.count, revenue: Math.round(d.revenue), avgCheck: d.count > 0 ? Math.round(d.revenue/d.count) : 0 }));

  // ─── 8. Время закрытия сделки ────────────────────────────
  const closeTimes = [];
  requests.forEach(r => {
    const created = r.dat ?? r.dat_request;
    const closed = r.dat_close;
    if (created && closed) {
      const diff = (new Date(closed) - new Date(created)) / (1000 * 60 * 60 * 24);
      if (diff >= 0 && diff < 365) closeTimes.push(diff);
    }
  });
  report.avgCloseDays = closeTimes.length > 0
    ? (closeTimes.reduce((a, b) => a + b, 0) / closeTimes.length).toFixed(1)
    : null;

  // ─── 9. Уникальные клиенты и повторники ──────────────────
  const clientMap = {};
  requests.forEach(r => {
    const cid = r.client_id;
    if (!cid) return;
    if (!clientMap[cid]) clientMap[cid] = { id: cid, name: [r.client_surname, r.client_name].filter(Boolean).join(' '), count: 0, revenue: 0, firstDate: r.dat };
    clientMap[cid].count++;
    clientMap[cid].revenue += parseFloat(r.calc_client ?? 0);
  });
  const clients = Object.values(clientMap);
  report.uniqueClients = clients.length;
  report.repeatClients = clients.filter(c => c.count > 1).length;
  report.repeatRate = clients.length > 0 ? ((clients.filter(c => c.count > 1).length / clients.length) * 100).toFixed(1) + '%' : '0%';
  report.topClients = clients.sort((a, b) => b.revenue - a.revenue).slice(0, 10).map(c => ({...c, revenue: Math.round(c.revenue)}));

  // ─── Вывод итогов ────────────────────────────────────────
  console.log('\n════════════════════════════════════');
  console.log('📊 ИТОГИ АУДИТА U-ON');
  console.log('════════════════════════════════════');
  console.log(`Всего заявок:        ${report.totalRequests}`);
  console.log(`Общая выручка:       ${report.totalRevenue} BYN/USD`);
  console.log(`Средний чек:         ${report.avgCheck} BYN/USD`);
  if (report.avgCloseDays) console.log(`Среднее время сделки: ${report.avgCloseDays} дней`);

  console.log(`Уникальных клиентов:  ${report.uniqueClients}`);
  console.log(`Повторных клиентов:   ${report.repeatClients} (${report.repeatRate})`);
  if (report.avgCloseDays) console.log(`Среднее время сделки: ${report.avgCloseDays} дней`);

  console.log('\nПо статусам:');
  report.byStatus.forEach(s => console.log(`  ${s.status}: ${s.count}`));

  console.log('\nПо менеджерам:');
  report.byManager.forEach(m =>
    console.log(`  ${m.name}: ${m.count} заявок, конверсия ${m.conversionRate}, выручка ${Math.round(m.revenue)}, ср.чек ${m.avgCheck}`)
  );

  console.log('\nПо источникам:');
  report.bySources.slice(0,8).forEach(s => console.log(`  ${s.source}: ${s.count} заявок, ср.чек ${s.avgCheck}`));

  console.log('\nТоп направления:');
  report.topDestinations.slice(0, 8).forEach(d => console.log(`  ${d.dest}: ${d.count} заявок, ср.чек ${d.avgCheck}`));

  console.log('\nДинамика по месяцам (последние 6):');
  report.byMonth.slice(-6).forEach(m =>
    console.log(`  ${m.month}: ${m.count} заявок, выручка ${Math.round(m.revenue)}`)
  );

  // ─── Сохраняем JSON ──────────────────────────────────────
  saveReport(report);
}

function saveReport(data) {
  const outDir = path.join(__dirname, '../../docs/audit');
  const outFile = path.join(outDir, `uon-audit-${new Date().toISOString().substring(0, 10)}.json`);
  fs.mkdirSync(outDir, { recursive: true });
  fs.writeFileSync(outFile, JSON.stringify(data, null, 2), 'utf-8');
  console.log(`\n✅ Данные сохранены: ${outFile}`);
}

main().catch(err => {
  console.error('❌ Ошибка:', err.message);
  process.exit(1);
});
