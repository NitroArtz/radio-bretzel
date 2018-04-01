
def id_to_name(_id, name=None):
   if not name:
      name = _id.replace('-', ' ')
   return name.title()
