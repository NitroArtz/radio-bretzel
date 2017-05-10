/**
 * Track.js
 *
 * @description :: TODO: You might write a short summary of how this model works and what it represents here.
 * @docs        :: http://sailsjs.org/documentation/concepts/models-and-orm/models
 */

module.exports = {

  attributes: {
    active: {
      type: 'boolean',
      defaultsTo: false
    },
    name: {
      type: 'string',
      required: true
    },
    artist: {
      model: 'artist',
      required: true
    },
    album: {
      model: 'album',
      required: true
    },
    genres:{
      collection: 'genre',
      via: 'tracks'
    },
    featurings: {
      collection: 'artist',
      via: 'featurings'
    },
    teams: {
      collection: 'team',
      via: 'tracks'
    },
    addedBy:{
      model: 'user',
      required: true,
      columnName: 'added_by'
    },
    description: {
      type: 'longtext'
    },
    duration: {
      type: 'string',
      required: true
    },
    year: {
      type: 'integer'
    },
    path: {
      type: 'string',
      required: true
    },
    weight: {
      type: 'integer',
      defaultsTo: 5000
    }
  }
};
