import threading
import time

import coloredlogs, logging
import grbfunk.utils.log

logger = logging.getLogger("grbfunk.processcounter")

#
# This should be a singleton!
#


class ProcessCounter(object):
    _instance = None


    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
        #    print('Creating the object')
            cls._instance = super(ProcessCounter, cls).__new__(cls)
            # Put any initialization here.
        return cls._instance
    
    def __init__(self, max_procs=1000, report_interval=60 * 5):
        """
        
        Keeps track of all the proccess running

        :param max_procs: warn me of I exceed this
        :param report_interval: how long before I start yelling
        :returns: 
        :rtype: 

        """

        self._max_procs = max_procs
        self._report_interval = report_interval

        self._n_procs_running = 0

        self._total_procs_launched = 0
        self._total_procs_killed = 0

        thread = threading.Thread(target=self._run, args=())
        thread.daemon = True
        thread.start()

        # we just started a thread!

        self.add_proccess()

    def _run(self):
        """

        This runs and reports at a given interval about all the threads
        running to make sure things do not get out of hand

        :returns: 
        :rtype: 

        """

        total_time = 0

        while True:

            logger.info(
                f"There are currently {self._n_procs_running} proccesses running"
            )

            time.sleep(self._report_interval)

    def add_proccess(self):
        """

        should be called every time we kick off a background process

        :returns: 
        :rtype: 

        """

        logger.info('A thread was just launched')
        
        self._n_procs_running += 1
        self._total_procs_launched += 1
        if self._n_procs_running > self._max_procs:

            logger.warning(f"you are running more than {self._max_procs}!!")

    def kill_process(self):
        """

        should be called every time we kill off a background process

        :returns: 
        :rtype: 

        """
        
        

        self._n_procs_running -= 1
        self._total_procs_killed += 1
        assert self._n_procs_running >= 0, "why do we have negative processess??"

        logger.info('A thread was just killed')



_global_proccess_counter = ProcessCounter()
