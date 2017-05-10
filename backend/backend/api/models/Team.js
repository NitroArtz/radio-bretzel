/**
 * Team.js
 *
 * @description :: TODO: You might write a short summary of how this model works and what it represents here.
 * @docs        :: http://sailsjs.org/documentation/concepts/models-and-orm/models
 */

module.exports = {

  attributes: {
    active: {
      type: 'boolean',
      defaultsTo: false,
    },
    activationDate: {
      type: 'datetime',
      columnName: 'activated_at'
    },
    name: {
      type: 'string',
      required: true
    },
    chief: {
      model: 'user'
    },
    members: {
      collection: 'user',
      via : 'team'
    },
    channels: {
      collection: 'channel',
      via: 'team'
    },
    artists: {
      collection: 'artist',
      via: 'teams'
    },
    albums: {
      collection: 'album',
      via: 'teams'
    },
    description: {
      type: 'longtext',
    },
    maxUsers: {
      type: 'integer',
      required: true,
      columnName: 'max_users'
    },
    maxChannels: {
      type: 'integer',
      required: true,
      columnName: 'max_channels'
    }
  }
};
