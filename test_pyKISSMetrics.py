# Quick-n-dirty test suite, can be run with py.test or Nose.

import KISSmetrics

def test_can_init():
    API = KISSmetrics.API
    try:
        KISSmetrics.API = lambda *args: 'can-init'
        assert KISSmetrics.KM('fake-key').api == 'can-init'
    finally:
        KISSmetrics.API = API
