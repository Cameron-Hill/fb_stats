import unittest
import pandas as pd
import json
from fb_stats import Generator
from fb_stats import exceptions as ex
import os
import pandas as pd

class TestSuite(unittest.TestCase):
    def setUp(self):
        self.path = os.path.dirname(os.path.abspath(__file__))+"\\test_data\\"
        self.single_test_json = "singletest1.json"
        self.group_test_json = "grouptest1.json"
        self.gen = Generator(self.path+ self.single_test_json)

    def test_that_generate_class_assigns_title_on_init(self):
        gen = Generator(self.path+ self.single_test_json)
        self.assertEqual("Nicola Scott", gen.title)

    def test_that_loading_a_file_that_does_not_exist_raises_file_not_found_error(self):
        with self.assertRaises(FileNotFoundError):
            gen = Generator("doesnot/exist.json")

    def test_that_participents_is_nicola_and_cameron(self):
        self.assertTrue("Cameron Hill" in self.gen.participants)
        self.assertTrue("Nicola Scott" in self.gen.participants)

    def test_that_columns_is_as_expected(self):
        expected_value = set(["sender_name","timestamp_ms","content","type","photos","sticker","videos"])
        self.assertEqual(expected_value,self.gen.columns)

    def test_that_data_is_pandas_dataframe(self):
        self.assertEqual(type(pd.DataFrame()), type(self.gen.data))
        
    def test_that_dates_and_contents_are_paired_correctly(self):
        timestamp_of_first_entry = 1532020433175
        expected_value_of_first_entry = "laters"
        timestamp_of_seventh_entry = 1467664471126
        expected_value_of_seventh_entry = "alrightyy byeeee x"
        timestamp_of_last_entry = 1429787357468
        expected_value_of_last_entry = None
        
        data = self.gen.data
        self.assertEqual(expected_value_of_first_entry,
            data.loc[data["timestamp_ms"]==timestamp_of_first_entry]["content"].iloc[0])
        self.assertEqual(expected_value_of_seventh_entry,
            data.loc[data["timestamp_ms"]==timestamp_of_seventh_entry]["content"].iloc[0])
        self.assertEqual(expected_value_of_last_entry,
            data.loc[data["timestamp_ms"]==timestamp_of_last_entry]["content"].iloc[0])

        
    def test_that_data_with_no_messages_raises_invalid_json_exception(self):
        with self.assertRaises(ex.InvalidJSONException):
            badgen = Generator(self.path+ "no_messages.json")

    def test_that_byte_encodings_are_automatically_removed(self):
        if os.path.isfile("test_data/singletest1_edit.json"):
            os.remove("test_data/singletest1_edit.json")
        gen = Generator(self.path+self.single_test_json)
        index_with_known_byte_encoding=1
        encoded_bytes = ["\u00f0","\u009f","\u0098","\u0084"]
        for byte in encoded_bytes:
            self.assertTrue(byte not in gen.data["content"][index_with_known_byte_encoding])

    def test_that_punctuation_is_automatically_removed(self):
        data_with_punctuation=0
        punctuations=["!",".",")",":"]
        for punctuation in punctuations:
            self.assertTrue(punctuation not in self.gen.data["content"][data_with_punctuation])

    def test_that_data_is_all_lower_case(self):
        for text in self.gen.data["content"]:
            if text is not None:
                self.assertTrue(text.islower())
