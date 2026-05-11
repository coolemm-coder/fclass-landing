/**
 * U-ON Travel API Client
 * Docs: https://api.u-on.ru/doc
 * Auth: API key in URL — https://api.u-on.ru/{key}/method.json
 */

const https = require('https');
const UON_BASE = 'https://api.u-on.ru';

class UonClient {
  constructor(apiKey) {
    if (!apiKey) throw new Error('UON_API_KEY required');
    this.apiKey = apiKey;
  }

  _url(method, format = 'json') {
    return `${UON_BASE}/${this.apiKey}/${method}.${format}`;
  }

  _request(url, method = 'GET', body = null) {
    return new Promise((resolve, reject) => {
      const options = { method, headers: { 'Content-Type': 'application/json' } };
      const req = https.request(url, options, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          try {
            resolve(JSON.parse(data));
          } catch (e) {
            reject(new Error(`Parse error: ${data.substring(0, 200)}`));
          }
        });
      });
      req.on('error', reject);
      if (body) req.write(JSON.stringify(body));
      req.end();
    });
  }

  // Поиск заявок (правильный endpoint — POST /request/search)
  // params: { dat_from, dat_to, status_id, manager_id, per_page, page }
  async searchRequests(params = {}) {
    return this._request(this._url('request/search'), 'POST', { per_page: 100, page: 1, ...params });
  }

  // Получить все заявки постранично
  async getAllRequests(params = {}) {
    const results = [];
    let page = 1;
    while (true) {
      const data = await this._request(
        this._url('request/search'), 'POST', { per_page: 100, page, ...params }
      );
      const items = data?.requests ?? data?.data ?? data ?? [];
      if (!Array.isArray(items) || items.length === 0) break;
      results.push(...items);
      console.log(`   Страница ${page}: ${items.length} заявок (итого: ${results.length})`);
      if (items.length < 100) break;
      page++;
      await sleep(110);
    }
    return results;
  }

  // Поиск клиента по телефону или email
  async findUser(phone = null, email = null) {
    const q = phone ? { phone } : { email };
    return this._request(`${this._url('user')}?${new URLSearchParams(q)}`);
  }

  // Создать клиента
  async createUser(data) {
    return this._request(this._url('user/create'), 'POST', data);
  }

  // Создать заявку
  async createRequest(data) {
    return this._request(this._url('request/create'), 'POST', data);
  }

  // Обновить статус заявки
  async updateRequest(id, data) {
    return this._request(this._url(`request/update/${id}`), 'POST', data);
  }

  // Список менеджеров
  async getManagers() {
    return this._request(this._url('manager'));
  }

  // Получить одну заявку
  async getRequest(id) {
    return this._request(this._url(`request/${id}`));
  }
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

module.exports = { UonClient, sleep };
