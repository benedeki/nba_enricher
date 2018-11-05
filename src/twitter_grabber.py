import tweepy
import logging
from queue import  Queue
from .aho_corasick import Replace, ReplacementResult
from .thread_on_command_queue import ThreadOnCommandQueue


class TweetEnricher(ThreadOnCommandQueue):
    def __init__(self, enriching, command_queue, ignore_case=False, thread_name=''):
        # type: (dict, Queue, bool, str) -> None
        ThreadOnCommandQueue.__init__(self, command_queue, thread_name)
        self._search_engine = Replace(enriching, ignore_case)

    def _add_full_text(self, status):
        # not the nicest way to ensure full_text property is present
        try: # full text directly exists
            status.full_text
            return status
        except AttributeError:
            pass
        try: # part of retweeted_status
            status.full_text = status.retweeted_status.extended_tweet['full_text']
            return status
        except AttributeError:
            pass
        try: # part of extended_tweet
            status.full_text = status.extended_tweet['full_text']
            return status
        except AttributeError:
            pass
        status.full_text = status.text
        return status

    def _output(self, status, replacement_result):
        logging.info('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        logging.info("%s" % status.full_text)
        logging.info(':------------------------------->')
        logging.info("%s" % replacement_result.result)
        logging.info('=================================')

    def _command_enrich(self, status):
        self._add_full_text(status)
        result = self._search_engine.replace(status.full_text)
        if result:
            self._output(status, result)
            return result.result
        else:
            logging.info('No hit in %s', status.full_text)
            return True


class TwitterListener(tweepy.StreamListener):
    def __init__(self, queue, api=None):
        # type: (Queue, object) -> None
        tweepy.StreamListener.__init__(self, api)
        self._queue = queue


    def on_status(self, status):
        logging.debug('Tweet captured and queued: %s', status)
        self._queue.put(('enrich', status))

    def on_error(self, status_code):
        if status_code == 420:
            logging.error('Rate limit breached (Twitter API Error 420')
            self._queue.put(('stop', None)) # stop the enrichers
            return False # returning False in on_error disconnects the stream
        else:
            logging.warning('Twitter API experienced error %d. Reconnecting...', status_code)
            return True # returning non-False reconnects the stream, with backoff


class TwitterGrabber(tweepy.Stream):
    def __init__(self, api, enrichers_count, enriching, ignore_case=False):
        # type: (tweepy.API, int, dict, bool) -> None
        self._queue = Queue()
        self._listener = TwitterListener(self._queue)
        self._enrichers = []
        for i in range(enrichers_count):
            _enricher = TweetEnricher(enriching, self._queue, ignore_case, "TweetEnricher_%d" % i)
            self._enrichers.append(_enricher)
            _enricher.start()
        tweepy.Stream.__init__(self, auth=api.auth, listener=self._listener)

    def _wait_for_enrichers(self):
        # type () -> None
        for enricher in self._enrichers:
            enricher.join()

    def shutdown(self):
        # type: () -> None
        self._queue.put(('stop', None)) # stop the enrichers
        self._wait_for_enrichers()
