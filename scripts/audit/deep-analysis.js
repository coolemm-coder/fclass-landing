#!/usr/bin/env node
/**
 * Углублённый анализ U-ON — типы заявок, сезонность, менеджеры, направления
 */

require('dotenv').config({ path: require('path').join(__dirname, '../../.env') });
const { UonClient } = require('../utils/uon-client');

const UON_API_KEY = process.env.UON_API_KEY;

async function main() {
  const uon = new UonClient(UON_API_KEY);

  console.log('📦 Загружаю заявки...');
  const requests = await uon.getAllRequests();
  console.log(`   Всего: ${requests.length}\n`);

  // ─── Смотрим структуру одной заявки ───────────────────────
  const sample = requests[0];
  console.log('🔍 Поля заявки:', Object.keys(sample).join(', '));
  console.log('\nПример заявки:');
  console.log(JSON.stringify(sample, null, 2));

  // ─── Типы услуг / направления ─────────────────────────────
  console.log('\n\n📊 ТИПЫ УСЛУГ (service_type / r_type / tour_type):');
  const serviceTypes = {};
  const tourTypes = {};
  const cities = {};

  requests.forEach(r => {
    // Собираем все уникальные значения потенциальных полей типа
    ['r_type', 'service_type', 'tour_type', 'type', 'category'].forEach(f => {
      if (r[f] !== undefined && r[f] !== null && r[f] !== '') {
        const key = `${f}:${r[f]}`;
        serviceTypes[key] = (serviceTypes[key] || 0) + 1;
      }
    });

    // Города вылета
    const city = r.departure_city_name || r.r_city_from || r.city_from || r.depart;
    if (city) cities[city] = (cities[city] || 0) + 1;
  });

  Object.entries(serviceTypes)
    .sort((a,b) => b[1]-a[1])
    .slice(0, 20)
    .forEach(([k,v]) => console.log(`  ${k}: ${v}`));

  // ─── По источникам детально ────────────────────────────────
  console.log('\n\n📊 ИСТОЧНИКИ детально:');
  const sources = {};
  requests.forEach(r => {
    const src = r.source_name || r.r_source || r.source || 'не указан';
    if (!sources[src]) sources[src] = { count: 0, revenue: 0 };
    sources[src].count++;
    sources[src].revenue += parseFloat(r.r_price_netto || r.price || r.total || 0);
  });
  Object.entries(sources)
    .sort((a,b) => b[1].count - a[1].count)
    .forEach(([src, d]) => {
      const avg = d.count > 0 ? Math.round(d.revenue / d.count) : 0;
      console.log(`  ${src}: ${d.count} заявок, ср.чек ${avg}`);
    });

  // ─── Паша детально ────────────────────────────────────────
  console.log('\n\n👤 ПАША (id=810) — все заявки:');
  const pashaReqs = requests.filter(r => r.manager_id == 810 || r.user_id == 810);
  console.log(`   Найдено: ${pashaReqs.length}`);
  pashaReqs.forEach(r => {
    const price = r.r_price_netto || r.price || r.total || 0;
    const dest = r.country_name || r.destination || r.tour_name || '?';
    const date = r.dat || r.dat_request || r.created_at || '?';
    const status = r.status_name || r.r_status_name || r.status || '?';
    const src = r.source_name || r.r_source || '?';
    console.log(`  [${date?.substring(0,10)}] ${dest} | ${price} | ${status} | src: ${src}`);
    console.log(`    Поля: ${Object.keys(r).join(', ')}`);
    console.log(`    Raw: ${JSON.stringify(r).substring(0, 300)}`);
  });

  // ─── Сезонность по всем годам ─────────────────────────────
  console.log('\n\n📅 СЕЗОННОСТЬ (все месяцы):');
  const byMonth = {};
  requests.forEach(r => {
    const date = r.dat || r.dat_request || r.created_at;
    if (!date) return;
    const month = date.substring(0, 7);
    if (!byMonth[month]) byMonth[month] = { count: 0, revenue: 0 };
    byMonth[month].count++;
    byMonth[month].revenue += parseFloat(r.r_price_netto || r.price || 0);
  });
  Object.entries(byMonth)
    .sort((a,b) => a[0].localeCompare(b[0]))
    .forEach(([m, d]) => {
      const bar = '█'.repeat(Math.round(d.count / 5));
      console.log(`  ${m}: ${d.count.toString().padStart(4)} заявок | ${bar}`);
    });

  // ─── ТОП клиенты ──────────────────────────────────────────
  console.log('\n\n👥 ТОП-10 клиентов по выручке:');
  const clients = {};
  requests.forEach(r => {
    const name = r.tourist_name || r.client_name || `client_${r.tourist_id || r.client_id}`;
    const price = parseFloat(r.r_price_netto || r.price || 0);
    if (!clients[name]) clients[name] = { count: 0, revenue: 0 };
    clients[name].count++;
    clients[name].revenue += price;
  });
  Object.entries(clients)
    .sort((a,b) => b[1].revenue - a[1].revenue)
    .slice(0, 10)
    .forEach(([name, d]) => {
      console.log(`  ${name}: ${d.count} поездок, ${Math.round(d.revenue)} BYN`);
    });

  // ─── Направления с чеком ──────────────────────────────────
  console.log('\n\n🌍 ТОП направления с деталями:');
  const dest = {};
  requests.forEach(r => {
    const country = r.country_name || r.destination || '?';
    const price = parseFloat(r.r_price_netto || r.price || 0);
    const status = r.status_name || r.r_status_name || '';
    if (!dest[country]) dest[country] = { count: 0, revenue: 0, closed: 0 };
    dest[country].count++;
    dest[country].revenue += price;
    if (status.includes('закрыт') || status.includes('Закрыт') || status.includes('Оплачен')) {
      dest[country].closed++;
    }
  });
  Object.entries(dest)
    .sort((a,b) => b[1].count - a[1].count)
    .slice(0, 15)
    .forEach(([country, d]) => {
      const avg = d.count > 0 ? Math.round(d.revenue / d.count) : 0;
      const conv = Math.round(d.closed / d.count * 100);
      console.log(`  ${country}: ${d.count} заявок | ср.чек ${avg} | конверсия ${conv}%`);
    });
}

main().catch(console.error);
