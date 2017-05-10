/**
 * Channel.js
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
    team: {
      model: 'team'
    },
    description: {
      type: 'longtext'
    },
    mountpoint: {
      type: 'string',
      required: true
    },
    imagePath: {
      type: 'string'
    },
    genres: {
      collection: 'genre',
      via: 'channels',
      dominant: true
    },
    tracks: {
      collection: 'track',
      via: 'channels'
    },
    users:{
      collection: 'user',
      via: 'channels'
    }
  }
};
