module.exports.permissions = {
  name: 'permissions',

  adminEmail: process.env.ADMIN_EMAIL || 'admin@example.com',
  adminUsername: process.env.ADMIN_USERNAME || 'admin',
  adminPassword: process.env.ADMIN_PASSWORD || 'admin1234',
  adminFirstname: process.env.ADMIN_FIRSTNAME || 'Admin',
  adminLastname: process.env.ADMIN_LASTNAME || 'Local',
  
  afterEvents: [
    'hook:auth:initialized'
  ]
};
