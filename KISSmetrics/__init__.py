"""
KISSmetrics API client
======================

Example usage:

km = KM('my-api-key')
km.identify('simon')
km.record('an event', {'attr': '1'})

"""
import urllib
import httplib
import logging
from datetime import datetime


class KM(object):
    """ KISSmetrics API client. """
    def __init__(self, key, host='trk.kissmetrics.com:80', http_timeout=2,
            logging=False):
        self._id = None
        self._key = key
        self._host = host
        self._http_timeout = http_timeout
        self._logging = logging

    def identify(self, id):
        self._id = id

    def record(self, action, props=None):
        """ Record `action` with the KISSmetrics API.

            :param str action: Action to record
            :param dict props: Additional information to include

        """
        props = props or {}
        self.check_id_key()
        if isinstance(action, dict):
            self.set(action)

        props.update({'_n': action})
        return self.request('e', props)

    def set(self, data):
        """ Set a data key. """
        self.check_id_key()
        return self.request('s', data)

    def alias(self, name, alias_to):
        """ Create an identity alias. """
        self.check_init()
        return self.request('a', {'_n': alias_to, '_p': name}, False)

    def reset(self):
        """ Reset client instance, forgetting the identity and API key. """
        self._id = None
        self._key = None

    def check_identify(self):
        """ Check if we have an identity set. """
        if self._id is None:
            raise RuntimeError("Need to identify first (KM.identify('<user>'))")

    def check_init(self):
        """ Check if we have been initialized with an API key. """
        if self._key is None:
            raise RuntimeError("Need to initialize first (KM.init('<your_key>'))")

    def now(self):
        """ Return the current UTC time. """
        return datetime.utcnow()

    def check_id_key(self):
        """ Check that we have an `identity` and that the client has been
            properly initialized.

        """
        self.check_init()
        self.check_identify()

    def logm(self, msg):
        """ Log a message.

            :param str msg: Message to log.

        """
        if not self._logging:
            return
        log = logging.getLogger('kissmetrics')
        log.info(msg)

    def request(self, type, data, update=True):
        """ Make HTTP request to KISSmetrics API.

            :param str type: Request type
            :param dict data: Data params

        """
        # if user has defined their own _t, then include necessary _d
        if '_t' in data:
            data['_d'] = 1
        else:
            data['_t'] = self.now().strftime('%s')

        # add customer key to data sent
        data['_k'] = self._key

        if update:
            data['_p'] = self._id

        try:
            connection = httplib.HTTPConnection(self._host, timeout=self._http_timeout)
            connection.request('GET', '/%s?%s' % (type, urllib.urlencode(data)))
            response = connection.getresponse()
            return response
        except:
            self.logm("Could not transmit to " + self._host)
        finally:
            connection.close()
