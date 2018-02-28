import random

from flask import request, abort, jsonify
from flask import current_app as app

from app.database import get_collection

from .model import Channel, validate
from ..channel import channel


""" All routes for the channel blueprint """
@channel.route('/', methods=['GET'])
def get_all_channels():
   return Channel.get_all()


@channel.route('/<_id>', methods=['POST'])
def create_channel(_id):
   form = request.form()
   channel = Channel(_id)
   channel.get_or_create_source()
   channel.save()
   response = channel.document()
   response['source'] = {
      'name': channel.source.name,
      'status': channel.source.status
   }
   return jsonify(response)

@channel.route('/next')
def select_next_track():
   random_song = random.randint(1, 3)
   return "test%s.mp3" % random_song
