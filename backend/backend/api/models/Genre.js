/**
 * Genre.js
 *
 * @description :: TODO: You might write a short summary of how this model works and what it represents here.
 * @docs        :: http://sailsjs.org/documentation/concepts/models-and-orm/models
 */

module.exports = {

  attributes: {
    name: {
      type: 'string',
      required: true,
    },
    channels: {
      collection: 'channel',
      via: 'genres'
    },
    artists: {
      collection: 'artist',
      via: 'genres'
    },
    albums: {
      collection: 'album',
      via: 'genres'
    },
    tracks: {
      collection: 'track',
      via: 'genres'
    }
  }
};
