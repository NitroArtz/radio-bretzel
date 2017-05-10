// api/models/User.js

var _ = require('lodash');
var _super = require('sails-permissions/api/models/User');

_.merge(exports, _super);
_.merge(exports, {

  // Extend with custom logic here by adding additional fields, methods, etc.

  attributes: {
    active: {
      type: 'boolean',
      defaultsTo: false,
    },
    activationDate: {
      type: 'datetime',
      columnName: 'activated_at'
    },
    team: {
      model: 'team'
    },
    channels: {
      collection: 'channel',
      via: 'users'
    },
    firstName: {
      type: 'string',
      required: true,
      columnName: 'first_name'
    },
    lastName: {
      type: 'string',
      required: true,
      columnName: 'last_name'
    },
    description: {
      type: 'longtext'
    },
    lastConnection: {
      type: 'datetime',
      columnName: 'last_con'
    }
  }
});
