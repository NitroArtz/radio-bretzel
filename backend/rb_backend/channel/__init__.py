import random

from flask import request, abort, jsonify

from rb_backend.channel.model import Channel, Channels, validate
from rb_backend.channel import view

def routes(app):
   """ All routes for the channel blueprint """
   @app.route('/channel/', methods=['GET'])
   def get_all_channels():
      channels = Channels.get()
      return jsonify(view.bulk_infos(*channels))

   @app.route('/channel/<_id>', methods=['POST'])
   def create_channel(_id):
      values = request.values
      # validations here
      channel = Channel(_id)
      Channels.save(channel)
      return jsonify(view.infos(channel))

   @app.route('/channel/<_id>', methods=['GET'])
   def get_channel(_id):
      values = request.values
      # validations here
      channel = Channels.get_one(_id)
      if not channel:
         return abort(404)
      return jsonify(view.infos(channel))


   @app.route('/channel/next')
   def select_next_track():
      random_song = random.randint(1, 3)
      return "test%s.mp3" % random_song
