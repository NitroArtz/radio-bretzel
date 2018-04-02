import random

from flask import request, abort, jsonify

from rb_backend.channel.model import Channel, validate

def routes(app):
   """ All routes for the channel blueprint """
   @app.route('/channel/', methods=['GET'])
   def get_all_channels():
      return jsonify(Channel.get_all())

   @app.route('/channel/<_id>', methods=['POST'])
   def create_channel(_id):
      values = request.values
      # validations here
      channel = Channel(_id)
      channel.save()
      return jsonify(channel.info())

   @app.route('/channel/<_id>', methods=['GET'])
   def get_channel(_id):
      values = request.values
      channel = Channel(_id)
      return jsonify(channel.info())


   @app.route('/channel/next')
   def select_next_track():
      random_song = random.randint(1, 3)
      return "test%s.mp3" % random_song
