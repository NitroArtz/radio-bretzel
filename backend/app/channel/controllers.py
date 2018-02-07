import random

from flask import request, abort, jsonify
from flask import current_app as app

from app import utils
from app.channel.models import Channel

from ..channel import channel

def validate(**data):
   """ Validate Channel arguments """
   for field in data:
      if field == '_id':
         try:
            if not data['_id'] or not utils.validate_slug(data['_id']):
               raise ValueError('"name" argument don\'t fit the requirements.')
         except:
            return False
   return True


""" the routes for the channel blueprint """

@channel.route('/', methods=['POST'])
@channel.route('/<_id>', methods=['POST'])
def create_channel():
   _id = request.values.get('_id')
   if not _id:
      abort(400)

   newChannel = Channel(_id)
   return jsonify(newChannel.save())

@channel.route('/next')
def select_next_track():
   random_song = random.randint(1, 3)
   return "test%s.mp3" % random_song