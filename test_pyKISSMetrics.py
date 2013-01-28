# Quick-n-dirty test suite, can be run with py.test or Nose.

from KISSmetrics import KM

import KISSmetrics

class Fake: pass

def test_construction():
    API = KISSmetrics.API
    try:
        km = KM('fake-key')
        KISSmetrics.API = Fake
        km.identify('fake@example.com')
        km.record('An event', {'foo': 'bar'})
    finally:
        KISSmetrics.API = API
