/**
 * DV ANALYTICS - GOOGLE APPS SCRIPT BACKGROUND EMAIL DISPATCHER
 * =============================================================
 * Use this script to enable 1-click silent background email sending
 * directly from your Google Sheet without opening Outlook or any browser popups.
 * 
 * SETUP INSTRUCTIONS (Takes ~30 seconds):
 * 1. Open your live Google Sheet:
 *    https://docs.google.com/spreadsheets/d/1z7897mcMyPRWyvRiXG5tPziXkLnkaE_6/edit
 * 2. In the top menu, click: Extensions -> Apps Script
 * 3. Delete any default code in Code.gs, paste this entire file, and click Save (💾).
 * 4. Click the blue 'Deploy' button (top right) -> 'New deployment'.
 * 5. Click the gear icon next to 'Select type' and choose 'Web app'.
 * 6. Set Description: 'Recovery Email Webhook'
 * 7. Set 'Execute as': 'Me'
 * 8. Set 'Who has access': 'Anyone'
 * 9. Click 'Deploy', then 'Authorize access' (sign in with your Google account).
 * 10. Copy the 'Web app URL' (it ends in /exec).
 * 11. Open the Collection & Recovery Dashboard -> Go to 'Settings' -> Paste into 'Cloud Webhook URL' -> Click 'Save Template'.
 * 
 * Done! Now whenever you click '✉️ Send', emails are dispatched instantly in the background!
 */

function doPost(e) {
  try {
    var data = {};
    if (e && e.postData && e.postData.contents) {
      try {
        data = JSON.parse(e.postData.contents);
      } catch(parseErr) {
        data = e.parameter || {};
      }
    } else if (e && e.parameter) {
      data = e.parameter;
    }

    var to = data.to;
    var cc = data.cc || '';
    var subject = data.subject || 'Important: Pending Fee Recovery Notice | DV Analytics';
    var body = data.body || '';

    if (!to) {
      return ContentService.createTextOutput(JSON.stringify({
        status: 'error',
        message: 'Recipient email address (to) is required.'
      })).setMimeType(ContentService.MimeType.JSON);
    }

    // Send email directly through Google Mail service
    MailApp.sendEmail({
      to: to,
      cc: cc,
      subject: subject,
      body: body,
      name: 'Team DV Analytics'
    });

    return ContentService.createTextOutput(JSON.stringify({
      status: 'success',
      message: 'Email sent successfully to ' + to
    })).setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({
      status: 'error',
      message: err.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  return ContentService.createTextOutput(JSON.stringify({
    status: 'active',
    service: 'DV Analytics Recovery Email Dispatcher',
    timestamp: new Date().toISOString()
  })).setMimeType(ContentService.MimeType.JSON);
}
