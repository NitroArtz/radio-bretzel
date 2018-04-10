import random

from flask import request, abort, jsonify

from rb_backend.channel.model import Channel, Channels
from rb_backend.channel import view
from rb_backend.errors import DatabaseError, ValidationError
from rb_backend.utils import formats

def routes(app):
   """ All routes for the channel blueprint """

   @app.route('/channel/', methods=['GET'])
   def get_channels():
      """
      Returns all matching channels from given filters
      Arguments :

      slug               (Mandatory)   :  Channel's global id, uniquely composed of
                                          alphanumeric characters and up to 2 dashes
      active                           :  Administrative enabled / disabled value
                                          Accepts "True" or "False" (case insensitive)
      soft_deleted                     :  Default to False, shows also soft_deleted items.
                                          Accepts "True" or "False" (case insensitive)
      name                             :  Channel's public name
      description                      :  Channel's description
      source_name                      :  Channel's source name
      source_stream_host               :  URL of streaming server.
      source_stream_source_passwd      :  streaming authentication password
      source_stream_mountpoint         :  streaming mountpoint
      """
      values = request.values
      channels = Channels.find(**values)
      return view.infos_many(*channels)

   @app.route('/channel/<string:slug>', methods=['POST'])
   def create_channel(slug):
      """
      Create new channel from given args
      Arguments :

      slug               (Mandatory)   :  Channel's global id, uniquely composed of
                                          alphanumeric characters and up to 2 dashes
      active                           :  Administrative enabled / disabled value
                                          Accepts "True" or "False" (case insensitive)
      name                             :  Channel's public name
      description                      :  Channel's description
      source_name                      :  Channel's source name
      source_stream_host               :  URL of streaming server.
      source_stream_source_passwd      :  streaming authentication password
      source_stream_mountpoint         :  streaming mountpoint
      force_source_creation            :  Default to False, override existing source
                                          if enabled
      """
      values = request.values
      channel = Channels.create(slug, **values)
      return view.infos_one(channel)

   @app.route('/channel/<string:slug>', methods=['GET'])
   def get_channel(slug):
      """
      Return matching channel infos
      Arguments :

      slug               (Mandatory)   :  Channel's global id, uniquely composed of
                                          alphanumeric characters and up to 2 dashes
      active                           :  Administrative enabled / disabled value
                                          Accepts "True" or "False" (case insensitive)
      soft_deleted                     :  Default to False, shows also soft_deleted items.
                                          Accepts "True" or "False" (case insensitive)
      name                             :  Channel's public name
      description                      :  Channel's description
      source_name                      :  Channel's source name
      source_stream_host               :  URL of streaming server.
      source_stream_source_passwd      :  streaming authentication password
      source_stream_mountpoint         :  streaming mountpoint
      """
      values = request.values
      try: channel = Channels.find_one(slug, **values)
      except ValidationError as e: return abort(400, str(e))
      except DatabaseError: return abort(404)
      return view.infos_one(channel)

   # @app.route('/channel/<string:slug>/source', methods=['GET'])
   # def get_channel_source(slug):
   #    values = request.values
   #
   #    # Validations here
   #    channel = Channels.find_one(slug, **values)
   #    if not channel:
   #       abort(404)


   @app.route('/channel/next')
   def select_next_track():
      random_song = random.randint(1, 3)
      return "test%s.mp3" % random_song
