from flask import jsonify

def infos(channel):
   info = channel._document()
   info['source'] = source_infos(channel)
   info.pop('source_args', False)
   info.pop('soft_deleted', False)
   return info

def source_infos(channel):
   return {
      'name': channel.source_args['name'],
      'status': channel.source.status()
   }


# Views

def many(*channels):
   rv = []
   for channel in channels:
      rv.append(infos(channel))
   return jsonify(rv)

def one(channel):
   return jsonify(infos(channel))

def one_source(channel):
   return jsonify(source_infos(channel))
