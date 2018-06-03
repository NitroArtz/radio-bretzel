import random

from flask import request, abort

from rb_backend.channel.model import Channel, Channels
from rb_backend.channel import view
from rb_backend.errors import DatabaseError, ValidationError
from rb_backend.source import Sources
from rb_backend.utils import formats, validations

def routes(app):
   """ All routes for channel resources"""

   @app.route('/channel/', methods=['GET'])
   def get_channels():
      values = request.args.to_dict()
      try: channels = Channels.find(**values)
      except ValidationError as e: return abort(400, str(e))
      except DatabaseError: return abort(404)
      return view.many(*channels)

   @app.route('/channel/<string:slug>', methods=['GET'])
   def get_channel(slug):
      values = request.args.to_dict()
      values.update({'slug': slug})
      try: channel = Channels.find_one(**values)
      except ValidationError as e: return abort(400, str(e))
      except DatabaseError: return abort(404)
      return view.one(channel)

   @app.route('/channel/<string:slug>', methods=['POST'])
   def create_channel(slug):
      values = request.form.to_dict()
      values.update({'slug': slug})
      try: channel = Channels.create(**values)
      except ValidationError as e: return abort(400, str(e))
      except DatabaseError: return abort(404)
      return view.one(channel)

   @app.route('/channel/<string:slug>', methods=['PUT', 'UPDATE'])
   def update_channel(slug):
      values = request.form.to_dict()
      try: updated_channel = Channels.update(slug, values)
      except ValidationError as e: return abort(400, str(e))
      except DatabaseError: return abort(404)
      return view.one(update_channel)

   @app.route('/channel/<string:slug>', methods=['DELETE'])
   def delete_channel(slug):
      values = request.form.to_dict()
      try: deleted_channel = Channels.delete(slug, **values)
      except ValidationError as e: return abort(400, str(e))
      except DatabaseError: return abort(404)
      return view.one(deleted_channel)
   #
   # @app.route('/channel/<string:slug>/source', methods=['GET'])
   # def get_channel_source(slug):
   #    """
   #    Returns source information for given channel slug
   #    Arguments:
   #
   #    slug               (Mandatory)   :  Channel's global id
   #    """
   #    try: channel = Channels.find_one(slug)
   #    except ValidationError as e: return abort(400, str(e))
   #    except DatabaseError: return abort(404)
   #    return view.one_source(channel)
   #
   # @app.route('/channel/<string:slug>/source', methods=['POST'])
   # def create_channel_source(slug):
   #    """
   #    Starts and returns source information for given channel slug
   #    Arguments:
   #
   #    slug               (Mandatory)   :  Channel's global id
   #    force                            :  Default to false, override potential
   #                                        existing source
   #    """
   #    values = request.form
   #    try:
   #       channel = Channels.find_one(slug)
   #       force = validations.bool(values.get('force', 'false'))
   #       if force or channel.source.status() != 'non-existent':
   #          return abort(500, 'source is '+ channel.source.status())
   #          try: channel.source.delete(force=True)
   #          except: pass
   #          channel.init_source(force_creation=True)
   #          return view.one_source(channel)
   #    except ValidationError as e: return abort(400, str(e))
   #    except DatabaseError: return abort(404)
   #
   # @app.route('/channel/<string:slug>/source', methods=['DELETE'])
   # def delete_channel_source(slug):
   #    """ Delete channel's source and return sourceless channel object
   #    """
   #    values = request.form
   #    force = validations.bool(values.get('force', 'false'))
   #    try:
   #       channel = Channels.find_one(slug)
   #       channel.source.delete(force)
   #       return view.one_source(channel)
   #    except ValidationError as e: return abort(400, str(e))
   #    except DatabaseError: return abort(404)
   #
   # @app.route('/channel/<string:slug>/source/start', methods=['POST'])
   # def start_channel_source(slug):
   #    """
   #    Starts and returns source information for given channel slug
   #    Arguments:
   #
   #    slug               (Mandatory)   :  Channel's global id
   #    """
   #    try:
   #       channel = Channels.find_one(slug)
   #       return view.one_source(channel.source.start())
   #    except ValidationError as e: return abort(400, str(e))
   #    except DatabaseError: return abort(404)
   #
   # @app.route('/channel/<string:slug>/source/stop', methods=['POST'])
   # def stop_channel_source(slug):
   #    """
   #    Stops and returns source information for given channel slug
   #    Arguments:
   #
   #    slug               (Mandatory)   :  Channel's global id
   #    """
   #    try:
   #       channel = Channels.find_one(slug)
   #       return view.one_source(channel.source.stop())
   #    except ValidationError as e: return abort(400, str(e))
   #    except DatabaseError: return abort(404)
   #
   # @app.route('/channel/<string:slug>/source/reset', methods=['POST'])
   # def reset_channel_source(slug):
   #    """
   #    Remove and recreate sourche channel, returning information about source
   #    Arguments:
   #
   #    slug               (Mandatory)   :  Channel's global id
   #    """
   #    try:
   #       channel = Channels.find_one(slug)
   #       channel.init_source(force_creation=True)
   #       return view.one_source(channel)
   #    except ValidationError as e: return abort(400, str(e))
   #    except DatabaseError: return abort(404)
   #
   # @app.route('/channel/next')
   # def select_next_track():
   #    random_song = random.randint(1, 3)
   #    return "test%s.mp3" % random_song
