from flask import current_app as app

from app.database import Document
from app.channel.source import Source

class Channel(Source):

   def __init__(self,
                  _id,
                  name=None):
      self._id = _id
      if name:
         self.name = name.title()
      else:
         name = _id.replace('-', ' ')
         self.name = name.title()
      self.source = self.get_or_create_source()

   def document(self):
      document = {
         '_id': self._id,
         'name': self.name,
      }
      return document

   def save(self):
      return Document.save(app.mongo.db.channels, self.document())

   def delete(self):
      return Document.delete(app.mongo.db.channels, self.document())
