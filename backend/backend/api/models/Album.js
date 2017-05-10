/**
 * Album.js
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
    name: {
      type: 'string',
      required: true
    },
    artist: {
      model: 'artist',
      required: true
    }
    teams: {
      collection: 'team',
      via: 'albums'
    },
    tracks: {
      collection: 'track',
      via: 'album'
    },
    genres: {
      collection: 'genre',
      via: 'albums'
    },
    description: {
      type: 'logntext'
    },
    year: {
      type: 'integer'
    },
    cover: {
      type: 'string'
    }
  }
};
