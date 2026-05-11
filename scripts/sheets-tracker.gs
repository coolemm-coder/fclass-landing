/**
 * FC Email Tracker — Google Apps Script
 *
 * КАК УСТАНОВИТЬ:
 * 1. Создай Google Таблицу: https://sheets.new
 * 2. Открой Extensions → Apps Script
 * 3. Вставь этот код целиком
 * 4. Нажми Deploy → New deployment → Web app
 *    - Execute as: Me
 *    - Who has access: Anyone
 * 5. Скопируй URL → вставь в n8n в ноду "Write to Sheets"
 */

var SHEET_ID = SpreadsheetApp.getActiveSpreadsheet().getId();

function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    var action = data.action;

    if (action === 'logSent') {
      return logSent(data.row);
    } else if (action === 'logEvent') {
      return logEvent(data);
    } else {
      return jsonResponse({ok: false, error: 'Unknown action: ' + action});
    }
  } catch(err) {
    return jsonResponse({ok: false, error: err.toString()});
  }
}

function doGet(e) {
  // Stats endpoint
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sent = ss.getSheetByName('Sent');
  var events = ss.getSheetByName('Events');

  var stats = {
    sent: sent ? sent.getLastRow() - 1 : 0,
    events: events ? events.getLastRow() - 1 : 0
  };

  // Count opens and clicks from Events sheet
  if (events && events.getLastRow() > 1) {
    var evData = events.getRange(2, 1, events.getLastRow()-1, 3).getValues();
    var opens = 0, clicks = 0, replies = 0;
    evData.forEach(function(row) {
      var ev = row[1];
      if (ev === 'open') opens++;
      if (ev === 'click') clicks++;
      if (ev === 'reply') replies++;
    });
    stats.opens = opens;
    stats.clicks = clicks;
    stats.replies = replies;
    stats.openRate = stats.sent > 0 ? Math.round(opens / stats.sent * 100) + '%' : '0%';
    stats.clickRate = stats.sent > 0 ? Math.round(clicks / stats.sent * 100) + '%' : '0%';
    stats.replyRate = stats.sent > 0 ? Math.round(replies / stats.sent * 100) + '%' : '0%';
  }

  return jsonResponse(stats);
}

function logSent(row) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName('Sent');

  if (!sheet) {
    sheet = ss.insertSheet('Sent');
    sheet.appendRow(['email', 'company', 'category', 'sent_at', 'subject', 'progress', 'status', 'notes']);
    sheet.getRange(1, 1, 1, 8).setFontWeight('bold').setBackground('#1a237e').setFontColor('#ffffff');
    sheet.setFrozenRows(1);
  }

  sheet.appendRow(row);
  return jsonResponse({ok: true, action: 'logSent'});
}

function logEvent(data) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName('Events');

  if (!sheet) {
    sheet = ss.insertSheet('Events');
    sheet.appendRow(['email', 'event', 'timestamp', 'detail', 'ip']);
    sheet.getRange(1, 1, 1, 5).setFontWeight('bold').setBackground('#1a237e').setFontColor('#ffffff');
    sheet.setFrozenRows(1);

    // Also update Sent sheet status
    updateSentStatus(data.email, data.event);
  }

  sheet.appendRow([
    data.email || '',
    data.event || '',
    data.timestamp || new Date().toISOString(),
    data.detail || '',
    data.ip || ''
  ]);

  updateSentStatus(data.email, data.event);
  return jsonResponse({ok: true, action: 'logEvent', event: data.event});
}

function updateSentStatus(email, event) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName('Sent');
  if (!sheet || !email) return;

  var data = sheet.getDataRange().getValues();
  for (var i = 1; i < data.length; i++) {
    if (data[i][0] === email) {
      var statusCol = 7; // column G (status)
      var currentStatus = data[i][statusCol - 1] || 'sent';

      // Priority: reply > click > open > sent
      var priority = {sent: 0, open: 1, click: 2, reply: 3};
      if ((priority[event] || 0) > (priority[currentStatus] || 0)) {
        sheet.getRange(i + 1, statusCol).setValue(event);
        if (event === 'reply') {
          sheet.getRange(i + 1, statusCol).setBackground('#c8e6c9'); // green
        } else if (event === 'click') {
          sheet.getRange(i + 1, statusCol).setBackground('#fff9c4'); // yellow
        } else if (event === 'open') {
          sheet.getRange(i + 1, statusCol).setBackground('#e3f2fd'); // blue
        }
      }
      break;
    }
  }
}

function jsonResponse(data) {
  return ContentService
    .createTextOutput(JSON.stringify(data))
    .setMimeType(ContentService.MimeType.JSON);
}
