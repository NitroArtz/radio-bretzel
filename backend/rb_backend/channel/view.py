from flask import jsonify

def infos(channel):
   info = channel._document()
   info['source'] = {
      'name': channel.source_args['name'],
      'status': channel.source.status()
   }
   info.pop('source_args', False)
   info.pop('soft_deleted', False)
   return info

def infos_many(*channels):
   rv = []
   if channels:
      for channel in channels:
         rv.append(infos(channel))
   return jsonify(rv)

def infos_one(channel):
   return jsonify(infos(channel))
