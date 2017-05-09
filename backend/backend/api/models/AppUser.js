/**
 * User.js
 *
 * @description :: TODO: You might write a short summary of how this model works and what it represents here.
 * @docs        :: http://sailsjs.org/documentation/concepts/models-and-orm/models
 */

module.exports = {
  autoUpdatedAt: true,
  attributes: {
    active :{
      type: 'boolean',
      defaultsTo: false
    },
    login: {
      type: 'string',
      required: true
    },
    password: {
      type: 'string',
      required: true
    },
    email: {
      type: 'string',
      required: true
    },
    teamID: {
      model: 'team'
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
      type: 'string'
    },
    activationDate: {
      type: 'datetime',
      columnName: 'activated_at'
    },
    lastConnection: {
      type: 'datetime',
      columnName: 'last_con'
    }

  }
};
