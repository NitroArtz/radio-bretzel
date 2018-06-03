from flask import request, abort

from rb_backend.source import view
from rb_backend.source.model import Sources
from rb_backend.config import get_config
from rb_backend.errors import DatabaseError, ValidationError, DatabaseNotFound

def routes(app):
   """ All routes for source resources"""

   @app.route('/source', methods=['GET'])
   def get_sources():
      """
      Returns all matching sources from given filters
      """
      values = request.args.to_dict()
      try:
         sources = Sources.find(**values)
      except ValidationError as e:
         return abort(400, str(e))
      except:
         raise
      return view.many(*sources)

   @app.route('/source/<string:name>', methods=['GET'])
   def get_source(name):
      values = request.args.to_dict()
      values.update({'name': name})
      try:
         source = Sources.find_one(**values)
      except ValidationError as e:
         return abort(400, str(e))
      except DatabaseNotFound:
         return abort(404)
      except:
         raise
      return view.one(source)

   @app.route('/source', methods=['POST'])
   @app.route('/source/<string:name>', methods=['POST'])
   def create_source(name=None):
      values = request.form.to_dict()
      if name:
         values.update({'name': name})
      try:
         source = Sources.create(**values)
      except ValidationError as e:
         return abort(400, str(e))
      except:
         raise
      return view.one(source)

   @app.route('/source/<string:name>', methods=['PUT', 'UPDATE'])
   def update_source(name):
      values = request.form.to_dict()
      try:
         source = Sources.update(name, **values)
      except ValidationError as e:
         return abort(400, str(e))
      except:
         raise
      return view.one(source)

   @app.route('/source/<string:name>', methods=['DELETE'])
   def delete_source(name):
      values = request.form.to_dict()
      try:
         source = Sources.delete(name, **values)
      except ValidationError as e:
         return abort(400, str(e))
      except:
         raise
      return view.one(source)

   @app.route('/source/<string:name>/start')
   def start_source(name):
      try:
         source = Sources.find_one(**{'name': name})
         source.start()
      except ValidationError as e:
         return abort(400, str(e))
      except:
         raise
      return view.one(source)

   @app.route('/source/<string:name>/stop')
   def stop_source(name):
      try:
         source = Sources.find_one(**{'name': name})
         source.stop()
      except ValidationError as e:
         return abort(400, str(e))
      except:
         raise
      return view.one(source)
