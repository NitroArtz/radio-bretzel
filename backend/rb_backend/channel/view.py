def infos(channel):
   info = channel._document()
   info['source'] = {
      'name': channel.source.name,
      'status': channel.source.status()
   }
   info.pop('source_args', False)
   return info

def bulk_infos(*channels):
   rv = []
   if channels:
      for channel in channels:
         rv.append(infos(channel))
   return rv
