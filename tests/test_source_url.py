import unittest
import fetcher.fetcher as Fetcher
import fetcher.fetcher_runeberg as FetcherRuneberg


class TestSourceURL(unittest.TestCase):
    
    URLs = ("http://runeberg.org/download.pl?mode=txtzip&work=bannlyst",)
    workspace = "workspace/project_runeberg/"
    valid_domains = "runeberg.org"
    title = "TestPublication"

    def setUp(self):
        fetcher = Fetcher.Fetcher(self.workspace, self.valid_domains, None)

        path_info = fetcher.prepare_path_info(self.title)
        self.fetcher_runeberg = FetcherRuneberg.FetcherRuneberg(self.title, path_info, self.valid_domains)

    # testing for success
    def testURLValid(self):
        """ Test that the URL is from valid domains """
        for URL in self.URLs:
            valid = self.fetcher_runeberg.validate_url_source(URL)
            self.assertTrue(valid)


    # testing for failure
    def testURLInvalid(self):
        """ Test that the URL not from valid domains are discarded """
        """   """
        self.assertFalse(self.fetcher_runeberg.validate_url_source("mafia.com"))


    # testing for sanity
    def testURLSane(self):
        self.assertFalse(self.fetcher_runeberg.validate_url_source("not-a-domain-name"))
    

# ==============================================================================
# FUNCTION:
#   __name__
# ==============================================================================
if __name__ == '__main__':
    unittest.main()

