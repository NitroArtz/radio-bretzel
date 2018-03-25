import abc

class Source(object):
   """ Interface for multiple sources types """
   __metaclass__ = abc.ABCMeta

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
   def remove(self):
      raise NotImplementedError('Need to implement Source.remove()')
