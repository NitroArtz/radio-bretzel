import random

from flask import request, abort, jsonify
from flask import current_app as app

from .model import Channel, validate
from ..channel import channel


""" All routes for the channel blueprint """
@channel.route('/', methods=['GET'])
def get_all_channels():
   return jsonify(Channel.get_all())

@channel.route('/<_id>', methods=['POST'])
def create_channel(_id):
   values = request.values
   channel = Channel(_id)
   channel.source.start()
   channel.save()
   return jsonify(channel.info())

@channel.route('/<_id>', methods=['GET'])
def get_channel(_id):
   values = request.values
   channel = Channel(_id)
   return jsonify(channel.info())


@channel.route('/next')
def select_next_track():
   random_song = random.randint(1, 3)
   return "test%s.mp3" % random_song
