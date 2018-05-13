import abc

from rb_backend.utils import formats

class SourceAbs(object):
   """ This astract source will be used to provide generic methods to source classes
   """

   def reload(self, quiet=True):
      old_status = self.status
      if old_status not in ['non-existent', 'in error']:
         try:
            self.delete(force=True)
            self.create()
            if old_status == 'playing':
               self.start()
         except Exception as e:
            if not quiet:
               raise SourceError("Couldn't reload source after update : " + str(e))
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
