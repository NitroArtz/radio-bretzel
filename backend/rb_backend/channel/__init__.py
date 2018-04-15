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

      slug                             :  Channel's global id
      active                           :  Administrative enabled / disabled value
                                          Accepts "True" or "False" (case insensitive)
      soft_deleted                     :  Default to False, shows also soft_deleted items.
                                          Accepts "True" or "False" (case insensitive)
      name                             :  Channel's public name
      description                      :  Channel's description
      source_name                      :  Channel's source name
      source_stream_mountpoint         :  streaming mountpoint
      """
      values = request.values
      channels = Channels.find(**values)
      return view.many(*channels)

   @app.route('/channel/<string:slug>', methods=['GET'])
   def get_channel(slug):
      """
      Return matching channel infos
      Arguments :

      slug               (Mandatory)   :  Channel's global id
      active                           :  Administrative enabled / disabled value
                                          Accepts "True" or "False" (case insensitive)
      soft_deleted                     :  Default to False, shows also soft_deleted items.
                                          Accepts "True" or "False" (case insensitive)
      name                             :  Channel's public name
      description                      :  Channel's description
      source_name                      :  Channel's source name
      source_stream_mountpoint         :  streaming mountpoint
      """
      values = request.values
      try: channel = Channels.find_one(slug, **values)
      except ValidationError as e: return abort(400, str(e))
      except DatabaseError: return abort(404)
      return view.one(channel)

   @app.route('/channel/<string:slug>', methods=['POST'])
   def create_channel(slug):
      """
      Create new channel from given args
      Arguments :

      slug               (Mandatory)   :  Channel's global id
      active                           :  Administrative enabled / disabled value
                                          Accepts "True" or "False" (case insensitive)
      soft_deleted                     :  Default to False, shows also soft_deleted items.
      name                             :  Channel's public name
      description                      :  Channel's description
      source_name                      :  Channel's source name
      source_stream_mountpoint         :  streaming mountpoint
      force_source_creation            :  Default to False, override existing source
                                          if enabled
      """
      values = request.values
      channel = Channels.create(slug, **values)
      return view.one(channel)

   @app.route('/channel/<string:slug>', methods=['PUT', 'UPDATE'])
   def update_channel(slug):
      """
      Update channel named <slug> with given values
      Arguments :

      slug               (Mandatory)   :  Channel's global id
      active                           :  Administrative enabled / disabled value
                                          Accepts "True" or "False" (case insensitive)
      name                             :  Channel's public name
      description                      :  Channel's description
      source_name                      :  Channel's source name
      source_stream_mountpoint         :  streaming mountpoint
      """
      values = request.values
      try: updated_channel = Channels.update(slug, values)
      except ValidationError as e: return abort(400, str(e))
      except DatabaseError: return abort(404)
      return view.one(update_channel)

   @app.route('/channel/<string:slug>', methods=['DELETE'])
   def delete_channel(slug):
      """
      Delete channel named <slug>.
      Arguments :

      slug               (Mandatory)   :  Channel's global id
      hard_delete                      :  Default to False, will force channel deletion
                                          instead of unindexing it
      """
      hard_delete = request.values.get('hard_delete', 'false')
      try: deleted_channel = Channels.delete(slug, **hard_delete)
      except ValidationError as e: return abort(400, str(e))
      except DatabaseError: return abort(404)
      return view.one(deleted_channel)

   @app.route('/channel/<string:slug>/source', methods=['GET'])
   def get_channel_source(slug):
      """
      Returns source information for given channel slug
      Arguments:

      slug               (Mandatory)   :  Channel's global id
      """
      try: channel = Channels.find_one(slug)
      except ValidationError as e: return abort(400, str(e))
      except DatabaseError: return abort(404)
      return view.one_source(channel)

   @app.route('/channel/<string:slug>/source/start', methods=['POST'])
   def start_channel_source(slug):
      """
      Starts and returns source information for given channel slug
      Arguments:

      slug               (Mandatory)   :  Channel's global id
      """
      try:
         channel = Channels.find_one(slug)
         return view.one_source(channel.source.start())
      except ValidationError as e: return abort(400, str(e))
      except DatabaseError: return abort(404)

   @app.route('/channel/<string:slug>/source/stop', methods=['POST'])
   def stop_channel_source(slug):
      """
      Stops and returns source information for given channel slug
      Arguments:

      slug               (Mandatory)   :  Channel's global id
      """
      try:
         channel = Channels.find_one(slug)
         return view.one_source(channel.source.stop())
      except ValidationError as e: return abort(400, str(e))
      except DatabaseError: return abort(404)

   @app.route('/channel/<string:slug>/source/reset', methods=['POST'])
   def reset_channel_source(slug):
      """
      Remove and recreate sourche channel, returning information about source
      Arguments:

      slug               (Mandatory)   :  Channel's global id
      """
      try:
         channel = Channels.find_one(slug)
         channel.init_source(force_creation=True)



   @app.route('/channel/next')
   def select_next_track():
      random_song = random.randint(1, 3)
      return "test%s.mp3" % random_song
