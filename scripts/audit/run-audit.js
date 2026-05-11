#!/usr/bin/env node
/**
 * U-ON Full Audit — fetch all data and save to JSON
 */
require('dotenv').config({ path: require('path').join(__dirname, '../../.env') });
const https = require('https');
const fs = require('fs');
const path = require('path');

const KEY = process.env.UON_API_KEY;
if (!KEY) { console.error('No UON_API_KEY'); process.exit(1); }

function req(method, httpMethod, body) {
  return new Promise((ok, no) => {
    const u = new URL(`https://api.u-on.ru/${KEY}/${method}.json`);
    const o = { hostname: u.hostname, path: u.pathname, method: httpMethod || 'GET', headers: { 'Content-Type': 'application/json' } };
    const r = https.request(o, res => { let d = ''; res.on('data', c => d += c); res.on('end', () => { try { ok(JSON.parse(d)); } catch (e) { no(e); } }); });
    r.on('error', no); if (body) r.write(JSON.stringify(body)); r.end();
  });
}
function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

async function main() {
  console.log('=== U-ON FULL AUDIT ===');

  // Managers
  const mgr = await req('manager');
  const managers = mgr.users || [];
  console.log(`Managers: ${managers.length}`);

  // All requests (paginated)
  const all = [];
  let page = 1;
  while (true) {
    const d = await req('request/search', 'POST', { per_page: 100, page });
    const items = d.requests || [];
    if (!items.length) break;
    all.push(...items);
    process.stdout.write(`\rPage ${page}: ${all.length} requests`);
    if (items.length < 100) break;
    page++;
    await sleep(120);
  }
  console.log(`\nTotal: ${all.length} requests`);

  // Save raw data
  const outDir = path.join(__dirname, '../../docs/audit');
  fs.mkdirSync(outDir, { recursive: true });
  const date = new Date().toISOString().substring(0, 10);
  fs.writeFileSync(path.join(outDir, `uon-raw-${date}.json`), JSON.stringify({ managers, requests: all }, null, 2));
  console.log(`Saved: docs/audit/uon-raw-${date}.json`);

  // Analysis
  const report = analyze(all, managers);
  fs.writeFileSync(path.join(outDir, `uon-audit-${date}.json`), JSON.stringify(report, null, 2));
  console.log(`Saved: docs/audit/uon-audit-${date}.json`);
  printSummary(report);
}

function analyze(requests, managers) {
  const r = { date: new Date().toISOString(), total: requests.length };

  // By manager
  const byMgr = {};
  requests.forEach(req => {
    const name = [req.manager_surname, req.manager_name].filter(Boolean).join(' ') || 'N/A';
    const id = req.manager_id ?? 0;
    const k = `${id}:${name}`;
    if (!byMgr[k]) byMgr[k] = { id, name, count: 0, closed: 0, revenue: 0, sources: {} };
    byMgr[k].count++;
    const st = (req.status ?? '').toLowerCase();
    const price = parseFloat(req.calc_client ?? req.calc_price ?? 0);
    if (st.includes('закрыт') || st.includes('оплачен') || st.includes('выполнен') || st.includes('подтвержд')) {
      byMgr[k].closed++; byMgr[k].revenue += price;
    }
    const src = req.source ?? 'N/A';
    byMgr[k].sources[src] = (byMgr[k].sources[src] ?? 0) + 1;
  });
  r.byManager = Object.values(byMgr).sort((a, b) => b.count - a.count).map(m => ({
    ...m, avgCheck: m.closed > 0 ? Math.round(m.revenue / m.closed) : 0,
    conversion: m.count > 0 ? ((m.closed / m.count) * 100).toFixed(1) + '%' : '0%'
  }));

  // By status
  const bySt = {};
  requests.forEach(req => { const s = req.status ?? 'N/A'; bySt[s] = (bySt[s] ?? 0) + 1; });
  r.byStatus = Object.entries(bySt).sort(([, a], [, b]) => b - a).map(([status, count]) => ({ status, count }));

  // By month
  const byMonth = {};
  requests.forEach(req => {
    const d = req.dat ?? req.dat_request; if (!d) return;
    const m = d.substring(0, 7);
    if (!byMonth[m]) byMonth[m] = { count: 0, revenue: 0 };
    byMonth[m].count++; byMonth[m].revenue += parseFloat(req.calc_client ?? 0);
  });
  r.byMonth = Object.entries(byMonth).sort(([a], [b]) => a.localeCompare(b)).map(([month, d]) => ({ month, count: d.count, revenue: Math.round(d.revenue) }));

  // By source
  const bySrc = {};
  requests.forEach(req => {
    const s = req.source ?? 'N/A';
    if (!bySrc[s]) bySrc[s] = { count: 0, revenue: 0 };
    bySrc[s].count++; bySrc[s].revenue += parseFloat(req.calc_client ?? 0);
  });
  r.bySources = Object.entries(bySrc).sort(([, a], [, b]) => b.count - a.count).map(([source, d]) => ({ source, count: d.count, revenue: Math.round(d.revenue), avgCheck: d.count > 0 ? Math.round(d.revenue / d.count) : 0 }));

  // Revenue
  const prices = requests.map(req => parseFloat(req.calc_client ?? 0)).filter(p => p > 0);
  r.totalRevenue = Math.round(prices.reduce((a, b) => a + b, 0));
  r.avgCheck = prices.length > 0 ? Math.round(r.totalRevenue / prices.length) : 0;

  // Destinations
  const byDest = {};
  requests.forEach(req => {
    const d = req.travel_type ?? req.country ?? null; if (!d) return;
    if (!byDest[d]) byDest[d] = { count: 0, revenue: 0 };
    byDest[d].count++; byDest[d].revenue += parseFloat(req.calc_client ?? 0);
  });
  r.topDestinations = Object.entries(byDest).sort(([, a], [, b]) => b.count - a.count).slice(0, 15).map(([dest, d]) => ({ dest, count: d.count, revenue: Math.round(d.revenue) }));

  // Close time
  const ct = [];
  requests.forEach(req => {
    const c = req.dat ?? req.dat_request; const cl = req.dat_close;
    if (c && cl) { const diff = (new Date(cl) - new Date(c)) / 86400000; if (diff >= 0 && diff < 365) ct.push(diff); }
  });
  r.avgCloseDays = ct.length > 0 ? (ct.reduce((a, b) => a + b, 0) / ct.length).toFixed(1) : null;

  // Clients
  const clientMap = {};
  requests.forEach(req => {
    const cid = req.client_id; if (!cid) return;
    if (!clientMap[cid]) clientMap[cid] = { id: cid, name: [req.client_surname, req.client_name].filter(Boolean).join(' '), count: 0, revenue: 0 };
    clientMap[cid].count++; clientMap[cid].revenue += parseFloat(req.calc_client ?? 0);
  });
  const clients = Object.values(clientMap);
  r.uniqueClients = clients.length;
  r.repeatClients = clients.filter(c => c.count > 1).length;
  r.repeatRate = clients.length > 0 ? ((r.repeatClients / clients.length) * 100).toFixed(1) + '%' : '0%';
  r.topClients = clients.sort((a, b) => b.revenue - a.revenue).slice(0, 10).map(c => ({ ...c, revenue: Math.round(c.revenue) }));

  return r;
}

function printSummary(r) {
  console.log('\n════════════════════════════════');
  console.log('ИТОГИ АУДИТА U-ON');
  console.log('════════════════════════════════');
  console.log(`Заявок:          ${r.total}`);
  console.log(`Выручка:         ${r.totalRevenue}`);
  console.log(`Средний чек:     ${r.avgCheck}`);
  console.log(`Ср. время сделки: ${r.avgCloseDays} дней`);
  console.log(`Клиентов:        ${r.uniqueClients} (повторных: ${r.repeatClients}, ${r.repeatRate})`);
  console.log('\nМенеджеры:');
  r.byManager.forEach(m => console.log(`  ${m.name}: ${m.count} заявок, конв. ${m.conversion}, выручка ${Math.round(m.revenue)}, ср.чек ${m.avgCheck}`));
  console.log('\nСтатусы:');
  r.byStatus.forEach(s => console.log(`  ${s.status}: ${s.count}`));
  console.log('\nИсточники (топ-8):');
  r.bySources.slice(0, 8).forEach(s => console.log(`  ${s.source}: ${s.count}, ср.чек ${s.avgCheck}`));
  console.log('\nМесяцы (последние 6):');
  r.byMonth.slice(-6).forEach(m => console.log(`  ${m.month}: ${m.count} заявок, выручка ${m.revenue}`));
}

main().catch(e => { console.error('ERROR:', e.message); process.exit(1); });
