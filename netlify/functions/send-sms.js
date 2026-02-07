// Netlify Function: Send SMS via Twilio
// Gated by simple password authentication

const twilio = require('twilio');

exports.handler = async (event) => {
  // CORS headers
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS'
  };

  // Handle preflight
  if (event.httpMethod === 'OPTIONS') {
    return { statusCode: 200, headers, body: '' };
  }

  // Only POST allowed
  if (event.httpMethod !== 'POST') {
    return { statusCode: 405, headers, body: JSON.stringify({ error: 'Method not allowed' }) };
  }

  try {
    const { password, to, message } = JSON.parse(event.body);

    // Verify password
    if (password !== process.env.SMS_ACCESS_PASSWORD) {
      return { 
        statusCode: 401, 
        headers, 
        body: JSON.stringify({ error: 'Invalid password' }) 
      };
    }

    // Validate inputs
    if (!to || !message) {
      return { 
        statusCode: 400, 
        headers, 
        body: JSON.stringify({ error: 'Missing "to" or "message" field' }) 
      };
    }

    // Clean phone number (ensure it has country code)
    let phoneNumber = to.replace(/\s/g, '');
    if (!phoneNumber.startsWith('+')) {
      // Assume Irish number if no country code
      if (phoneNumber.startsWith('0')) {
        phoneNumber = '+353' + phoneNumber.slice(1);
      } else {
        phoneNumber = '+353' + phoneNumber;
      }
    }

    // Initialize Twilio client
    const client = twilio(
      process.env.TWILIO_ACCOUNT_SID,
      process.env.TWILIO_AUTH_TOKEN
    );

    // Send SMS
    const result = await client.messages.create({
      body: message,
      from: process.env.TWILIO_PHONE_NUMBER,
      to: phoneNumber
    });

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({ 
        success: true, 
        sid: result.sid,
        to: phoneNumber,
        status: result.status
      })
    };

  } catch (error) {
    console.error('SMS Error:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({ 
        error: 'Failed to send SMS', 
        details: error.message 
      })
    };
  }
};
