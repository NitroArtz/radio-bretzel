/**
 * Artist.js
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
    teams: {
      collection: 'team',
      via: 'artists'
    },
    tracks: {
      collection: 'track',
      via: 'artist'
    },
    featurings: {
      collection: 'track',
      via: 'featurings'
    },
    albums: {
      collection: 'album',
      via: 'artist'
    },
    genres: {
      collection: 'genre',
      via: 'artists'
    }
    description: {
      type: 'longtext'
    }
    // Add more artist infos here
  }
};
