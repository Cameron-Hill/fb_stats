import pandas as pd
import os
import unittest
from fb_stats.builders import _Builder
from fb_stats import Generator
class BuilderTests(unittest.TestCase):

    def setUp(self):
        self.builder = _Builder()
        path = os.path.dirname(os.path.abspath(__file__))+"\\test_data\\"
        fname = "singletest1.json"
        self.test_data = Generator(path+fname).data


    def test_the_to_date_time_function_returns_expected_date(self):
        epoch_example = self.test_data["timestamp_ms"][0]
        expected_date = "2018-07-19"
        expected_hour = 17
        expected_minute = 13
        expected_second = 53

        self.assertEqual(expected_date, str(self.builder._to_datetime(epoch_example).date()))
        self.assertEqual(expected_hour, self.builder._to_datetime(epoch_example).hour)
        self.assertEqual(expected_minute, self.builder._to_datetime(epoch_example).minute)
        self.assertEqual(expected_second, self.builder._to_datetime(epoch_example).second)


    def test_that_to_date_time_returns_a_pandas_datetime_object(self):
        pandas_date_time_object = pd.Timestamp
        epoch_example = self.test_data["timestamp_ms"][0]
        self.assertTrue(
            isinstance(
                self.builder._to_datetime(epoch_example),
                pandas_date_time_object
            )
        )

    def test_that_generate_count_time_data(self):
        pass
        #TODO Write some tests comon
        
