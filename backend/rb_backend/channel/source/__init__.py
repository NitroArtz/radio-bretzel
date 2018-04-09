import abc

class Source(object):
   """ Interface for multiple sources types

      Constructor's arguments :
         name     (Mandatory)    <string> :  source name, uniquely composed of
                                             alphanumeric characters and up to 2 dashes
         stream_host             <string> :  URL of streaming server.
         stream_source_passwd    <string> :  streaming authentication password
         stream_mountpoint       <string> :  streaming mountpoint

   """
   __metaclass__ = abc.ABCMeta

   @abc.abstractmethod
   def create(self, override=False):
      raise NotImplementedError('Need to implement Source.create()')

   @abc.abstractmethod
   def status(self):
      raise NotImplementedError('Need to implement Source.status()')

   @abc.abstractmethod
   def start(self):
      raise NotImplementedError('Need to implement Source.start()')

   @abc.abstractmethod
   def stop(self):
      raise NotImplementedError('Need to implement Source.stop()')

   @abc.abstractmethod
   def delete(self, force=False):
      raise NotImplementedError('Need to implement Source.delete()')
