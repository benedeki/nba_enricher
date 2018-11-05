from threading import Thread
from queue import Queue
import logging


class ThreadOnCommandQueue(Thread):
    def __init__(self, command_queue, thread_name = ''):
        # type: (Queue, str) -> None
        Thread.__init__(self)
        self.command_queue = command_queue
        self.thread_name = thread_name
        self._command_functions = {}

    def _bind_command(self, command):
        # type: (str) -> classmethod
        result = self.__getattribute__('_command_%s' % command)
        self._command_functions[command] = result
        logging.debug("Commands '%s' bound to function", command)
        return result

    def _command_stop(self, _):
        return False

    def run(self):
        # type: () -> None
        logging.debug('Thread %s started', self.thread_name)
        go = True
        while go != False:
            command, param = self.command_queue.get()
            try:
                go = self._command_functions.get(command, self._bind_command(command))(param)
                logging.debug("Command '%s' executed with '%s' parameter and returned '%s'",command, param, go)
            finally:
                self.command_queue.task_done()
        self.command_queue.put(('stop', None)) # to stop other threads on the same queue
        logging.debug('Thread %s finished', self.thread_name)
