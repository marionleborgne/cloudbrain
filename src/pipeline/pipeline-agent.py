import logging
import time
import sys
from os import getpid
from os.path import dirname, abspath, isdir
from multiprocessing import Queue
from daemon import runner

# add the shared settings file to namespace
sys.path.insert(0, dirname(dirname(abspath(__file__))))
import settings

from listen import Listen
from roomba import Roomba
from worker import Worker

# TODO: http://stackoverflow.com/questions/6728236/exception-thrown-in-multiprocessing-pool-not-detected


class pipeline():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = settings.LOG_PATH + '/pipeline.log'
        self.stderr_path = settings.LOG_PATH + '/pipeline.log'
        self.pidfile_path = settings.PID_PATH + '/pipeline.pid'
        self.pidfile_timeout = 5

    def run(self):
        logger.info('starting pipeline agent')
        listen_queue = Queue(maxsize=settings.MAX_QUEUE_SIZE)
        pid = getpid()

        #If we're not using oculus, don't bother writing to mini
        try:
            skip_mini = True if settings.OCULUS_HOST == '' else False
        except Exception:
            skip_mini = True

        # Start the workers
        for i in range(settings.WORKER_PROCESSES):
            if i == 0:
                Worker(listen_queue, pid, skip_mini, canary=True).start()
            else:
                Worker(listen_queue, pid, skip_mini).start()


        # Start the listeners
        #Listen(settings.PICKLE_PORT, listen_queue, pid, type="pickle").start()
        Listen(settings.UDP_PORT, listen_queue, pid, type="udp").start()

        # Start the roomba
        #Roomba(pid, skip_mini).start()

        # Warn the Mac users
        try:
            listen_queue.qsize()
        except NotImplementedError:
            logger.info('WARNING: Queue().qsize() not implemented on Unix platforms like Mac OS X. Queue size logging will be unavailable.')

        # Keep yourself occupied
        while 1:
            time.sleep(1)

if __name__ == "__main__":
    """
    Start the pipeline agent.
    """
    if not isdir(settings.PID_PATH):
        print 'pid directory does not exist at %s' % settings.PID_PATH
        sys.exit(1)

    if not isdir(settings.LOG_PATH):
        print 'log directory does not exist at %s' % settings.LOG_PATH
        sys.exit(1)

    pipeline = pipeline()

    logger = logging.getLogger("pipelineLog")
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s :: %(process)s :: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    handler = logging.FileHandler(settings.LOG_PATH + '/pipeline.log')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    if len(sys.argv) > 1 and sys.argv[1] == 'run':
        pipeline.run()
    else:
        daemon_runner = runner.DaemonRunner(pipeline)
        daemon_runner.daemon_context.files_preserve = [handler.stream]
        daemon_runner.do_action()
