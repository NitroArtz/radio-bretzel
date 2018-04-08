import random

from flask import request, abort, jsonify

from rb_backend.channel.model import Channel, Channels, validate
from rb_backend.channel import view
from rb_backend.utils import formats

def routes(app):
   """ All routes for the channel blueprint """
   @app.route('/channel/', methods=['GET'])
   def get_all_channels():
      channels = Channels.get()
      return jsonify(view.bulk_infos(*channels))

   @app.route('/channel/<_id>', methods=['POST'])
   def create_channel(_id):
      """
      Create new channel from given args
      Arguments :
         _id      (Mandatory)    <string> :  Channel's global id, uniquely composed of
                                             alphanumeric characters and up to 2 dashes
         active                  <bool>   :  Administrative enabled / disabled value
         name                    <string> :  Channel's public name
      """
      values = request.values
      # validations here
      source_args = formats.get_prefixed_keys(values, 'source_', pop=True)
      channel = Channel(_id, source_args=source_args)
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
