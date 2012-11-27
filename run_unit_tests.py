#!/usr/bin/env python
import unittest

if __name__ == '__main__':
    # test source URLs
    from tests.test_source_url import TestSourceURL
    suite = unittest.TestLoader().loadTestsFromTestCase(TestSourceURL)
    unittest.TextTestRunner().run(suite)
