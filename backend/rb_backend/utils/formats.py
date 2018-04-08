def id_to_name(_id):
   return _id.replace('-', ' ').title()

def get_prefixed_keys(dictionnary, prefix, pop=False, lowercase=True, trim=True):
   """
   This function parses the given dictionnary in order to extract
   the key/value pairs with keys starting with given prefix.
   It returns a dictionnary of extracted keys.

   Arguments:
      dictionnary (Mandatory) <dict>   :  the dictionnary to parse
      prefix      (Mandatory) <string> :  the prefix used for key matching
      pop                     <bool>   :  if set to True (False by default), the matching
                                          keys will be poped of the given dictionnary
      lowercase               <bool>   :  if set to True (default), all matching
                                          keys will be lowercased
      trim                    <bool>   :  if set to True (default), all matching
                                          keys name will have the given prefix trimed
   """
   rv = {}
   for k, v in dictionnary.items():
      if not k.startswith(prefix):
         continue
      if trim:
         key = k[len(prefix):]
      else:
         key = k
      if lowercase:
         key = key.lower()
      rv[key] = v
      if pop:
         dictionnary.pop(k)
   return rv
