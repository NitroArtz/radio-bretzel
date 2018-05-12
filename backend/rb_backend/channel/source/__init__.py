import abc

from rb_backend.utils import formats

class SourceAbs(object):
   """ This astract source will be used to provide generic methods to source classes
   """

   def setup(self, status):
      if status == 'in error' or self.status == status:
         return self
      if status == 'non-existent':
         # return self.delete(force=True)
         return self.delete(force=True, quiet=True)
      if self.status == 'non-existent':
         self.create()
      if status == 'playing':
         self.start()
      else:
         self.stop(quiet=True)
      return self

   def reload(self):
      old_status = self.status
      if old_status == 'non-existent':
         return self
      self.delete(force=True, quiet=True)
      self.setup(status=old_status)
      return self

   def _document(self):
      """ This function generates source's document """
      return {
         'name': self.name,
         'channel': self.channel,
         'status': self.status,
         'stream_mountpoint': self.stream_mountpoint
      }

   @abc.abstractmethod
   def create(self, force=False):
      raise NotImplementedError('Need to implement Source.create()')

   @property
   @abc.abstractmethod
   def status(self):
      raise NotImplementedError('Need to implement Source.status')

   @abc.abstractmethod
   def start(self, quiet=False):
      raise NotImplementedError('Need to implement Source.start()')

   @abc.abstractmethod
   def stop(self, quiet=False):
      raise NotImplementedError('Need to implement Source.stop()')

   @abc.abstractmethod
   def delete(self, force=False, quiet=False):
      raise NotImplementedError('Need to implement Source.delete()')
