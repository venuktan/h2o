import unittest, random, sys, time
sys.path.extend(['.','..','py'])
import h2o, h2o_cmd, h2o_hosts

class Basic(unittest.TestCase):
    def tearDown(self):
        h2o.check_sandbox_for_errors()

    @classmethod
    def setUpClass(cls):
        global localhost
        localhost = h2o.decide_if_localhost()
        if (localhost):
            h2o.build_cloud()
        else:
            h2o_hosts.build_cloud_with_hosts()

    @classmethod
    def tearDownClass(cls):
        h2o.tear_down_cloud()

    def test_mixed_causes_NA(self):
        csvFilename = 'mixed_causes_NA.csv'
        csvPathname = h2o.find_file('smalldata/' + csvFilename)
        parseKey = h2o_cmd.parseFile(csvPathname=csvPathname, timeoutSecs=15)
        inspect = h2o_cmd.runInspect(None, parseKey['destination_key'])
        missingValuesList = h2o_cmd.infoFromInspect(inspect, csvPathname)
        print missingValuesList
        self.assertEqual(sum(missingValuesList), 0,
                "Single column of data with mixed number/string should not have NAs")

if __name__ == '__main__':
    h2o.unit_main()
