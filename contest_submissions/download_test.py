import unittest
import download

class TestDownload(unittest.TestCase):
    def test_hello(self):
        download.handler({}, {})

    def test_get_contest_status(self):
        res = download.fetch('contest.status?contestId=566&from=1&count=3')
        self.assertEqual(res.status_code, 200)

    def test_parse_contest_submissions(self):
        with open('examples/contest_status_566.json') as f:
            for status in download.parse_contest_submissions(f.read()):
                download.put_firehose(status)
