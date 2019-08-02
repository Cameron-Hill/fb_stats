"""testing the new oo api design"""
import unittest
from fb_stats import main, StatTypes as st, Generator, builders
import os
import pandas as pd


class RedesignTests(unittest.TestCase):
    def setUp(self):
        self.fpath = self.path = os.path.dirname(os.path.abspath(__file__)) + "\\test_data\\singletest1.json"
        self.path = os.path.dirname(os.path.abspath(__file__)) + "\\test_data\\"
        self.single_test_json = "singletest1.json"
        self.group_test_json = "grouptest1.json"

    def test_that_generating_message_histogram_data_has_accurate_values(self):
        message_histogram_df = main.run(self.path + self.single_test_json, types=[st.MESSAGE_HISTOGRAM])
        camerons_june_17_messages = 2
        nicolas_july_18_messages = 1
        self.assertEqual(camerons_june_17_messages, message_histogram_df["Cameron Hill"][(2017, 6)])
        self.assertEqual(nicolas_july_18_messages, message_histogram_df["Nicola Scott"][(2018, 7)])

    def test_that_generating_user_histogram_data_has_7_nicola_3_cameron(self):
        occurences_of_cameron_in_data = 3
        occurences_of_nicola_in_data = 7
        user_histogram_df = main.run(self.path + self.single_test_json, types=[st.USER_HISTOGRAM])
        self.assertEqual(occurences_of_cameron_in_data, user_histogram_df["Cameron Hill"])
        self.assertEqual(occurences_of_nicola_in_data, user_histogram_df["Nicola Scott"])

    def test_that_generating_cumulative_frequency_data_produces_expected_values(self):
        cumulative_frequency_df = main.run(self.path + self.single_test_json, types=[st.CUMULATIVE_FREQUENCY])
        camerons_messages_sent_by_june_17 = 2
        nicolas_messages_sent_by_june_17 = 5
        camerons_messages_sent_by_july_18 = 3
        nicolas_messages_sent_by_july_18 = 7
        self.assertEqual(camerons_messages_sent_by_june_17, cumulative_frequency_df["Cameron Hill"][(2017, 6)])
        self.assertEqual(nicolas_messages_sent_by_june_17, cumulative_frequency_df["Nicola Scott"][(2017, 6)])
        self.assertEqual(camerons_messages_sent_by_july_18, cumulative_frequency_df["Cameron Hill"][(2018, 7)])
        self.assertEqual(nicolas_messages_sent_by_july_18, cumulative_frequency_df["Nicola Scott"][(2018, 7)])

    def test_that_nicola_uses_the_word_laters_twice_word_frequency(self):
        word_frequency_df = main.run(self.path + self.single_test_json, types=[st.WORD_FREQUENCY])
        expected_value = 2
        self.assertEqual(expected_value, word_frequency_df["Nicola Scott"]["laters"])
        self.assertEqual(0, word_frequency_df["Cameron Hill"]["laters"])

    def test_that_link_matrix_describes_accurate_interactions_when_not_normalised(self):
        gen = Generator(self.path + self.single_test_json)
        link_matrix_df = builders.HeatMap(gen, normalise=False).get_data()
        expected_times_nicola_followed_nicola = 4
        expected_times_nicola_followed_cameron = 2
        expected_times_cameron_followed_cameron = 1
        expected_times_cameron_followed_nicola = 2
        self.assertEqual(expected_times_nicola_followed_nicola, link_matrix_df["Nicola Scott"]["Nicola Scott"])
        self.assertEqual(expected_times_nicola_followed_cameron, link_matrix_df["Cameron Hill"]["Nicola Scott"])
        self.assertEqual(expected_times_cameron_followed_cameron, link_matrix_df["Cameron Hill"]["Cameron Hill"])
        self.assertEqual(expected_times_cameron_followed_nicola, link_matrix_df["Nicola Scott"]["Cameron Hill"])


    def test_that_normalised_matrix_reports_accurate_fractions(self):
        gen = Generator(self.path + self.single_test_json)
        link_matrix_df = builders.HeatMap(gen, normalise=True).get_data()
        total_nicola = 6
        total_cameron = 3

        expected_times_nicola_followed_cameron = 2 / total_nicola
        expected_times_nicola_followed_nicola = 4 / total_nicola
        expected_times_cameron_followed_cameron = 1 / total_cameron
        expected_times_cameron_followed_nicola = 2 / total_cameron

        self.assertEqual(expected_times_nicola_followed_nicola, link_matrix_df["Nicola Scott"]["Nicola Scott"])
        self.assertEqual(expected_times_nicola_followed_cameron, link_matrix_df["Cameron Hill"]["Nicola Scott"])
        self.assertEqual(expected_times_cameron_followed_cameron, link_matrix_df["Cameron Hill"]["Cameron Hill"])
        self.assertEqual(expected_times_cameron_followed_nicola, link_matrix_df["Nicola Scott"]["Cameron Hill"])

    def test_that_requesting_a_single_data_frame_returns_only_that_data_frame(self):
        word_frequency_df = main.run(self.path + self.single_test_json, types=[st.CUMULATIVE_FREQUENCY])
        self.assertEqual(type(pd.DataFrame()), type(word_frequency_df))

    def test_that_generating_user_histogram_on_group_data_data_has_expected_results(self):
        occurences_of_lindsay_in_data = 9
        occurences_of_cameron_in_data = 7
        occurences_of_ameilia_in_data = 2
        occurences_of_douglas_in_data = 1
        user_histogram_df = main.run(self.path + self.group_test_json, types=[st.USER_HISTOGRAM])
        self.assertEqual(occurences_of_lindsay_in_data, user_histogram_df["Lindsay Young"])
        self.assertEqual(occurences_of_cameron_in_data, user_histogram_df["Cameron Hill"])
        self.assertEqual(occurences_of_douglas_in_data, user_histogram_df["Douglas Matheson"])
        self.assertEqual(occurences_of_ameilia_in_data, user_histogram_df["Amelia Ford"])

    def test_that_generating_message_histogram_on_group_data_has_accurate_values(self):
        message_histogram_df = main.run(self.path + self.group_test_json, types=[st.MESSAGE_HISTOGRAM])

        expected_values_for_lindsay = {"2015": 9}
        expected_values_for_cameron = {"2015": 7}
        expected_values_for_amelia = {"2015": 2}
        expected_values_for_douglas = {"2015": 1}

        self.assertEqual(expected_values_for_lindsay["2015"], message_histogram_df["Lindsay Young"][(2015, 3)])
        self.assertEqual(expected_values_for_cameron["2015"], message_histogram_df["Cameron Hill"][(2015, 3)])
        self.assertEqual(expected_values_for_amelia["2015"], message_histogram_df["Amelia Ford"][(2015, 3)])
        self.assertEqual(expected_values_for_douglas["2015"], message_histogram_df["Douglas Matheson"][(2015, 3)])

    def test_that_generating_cumulative_frequency_group_data_produces_expected_values(self):
        cumulative_frequency_df = main.run(self.path + self.group_test_json, types=[st.CUMULATIVE_FREQUENCY])

        expected_values_for_lindsay = {"2015": 9
                                       }
        expected_values_for_cameron = {"2015": 7}
        expected_values_for_amelia = {"2015": 2}
        expected_values_for_douglas = {"2015": 1}

        self.assertEqual(expected_values_for_lindsay["2015"], cumulative_frequency_df["Lindsay Young"][(2015, 3)])
        self.assertEqual(expected_values_for_cameron["2015"], cumulative_frequency_df["Cameron Hill"][(2015, 3)])
        self.assertEqual(expected_values_for_amelia["2015"], cumulative_frequency_df["Amelia Ford"][(2015, 3)])
        self.assertEqual(expected_values_for_douglas["2015"], cumulative_frequency_df["Douglas Matheson"][(2015, 3)])


    def test_that_link_matrix_describes_accurate_interactions_for_group_when_not_normalised(self):
        gen = Generator(self.path + self.group_test_json)
        link_matrix_df = builders.HeatMap(gen, normalise=False).get_data()
        expected_times_lindsay_followed_cameron = 5
        expected_times_cameron_followed_douglas = 1
        expected_times_douglas_followed_amelia = 0
        expected_times_amelia_followed_lindsay = 1
        self.assertEqual(expected_times_lindsay_followed_cameron, link_matrix_df["Cameron Hill"]["Lindsay Young"])
        self.assertEqual(expected_times_cameron_followed_douglas, link_matrix_df["Douglas Matheson"]["Cameron Hill"])
        self.assertEqual(expected_times_douglas_followed_amelia, link_matrix_df["Amelia Ford"]["Douglas Matheson"])
        self.assertEqual(expected_times_amelia_followed_lindsay, link_matrix_df["Lindsay Young"]["Amelia Ford"])


    def test_that_normalised_matrix_reports_accurate_fractions_for_group(self):
        gen = Generator(self.path + self.group_test_json)
        link_matrix_df = builders.HeatMap(gen, normalise=True).get_data()
        total_lindsay = 8
        total_cameron = 7
        total_amelia = 2
        total_douglas = 1
        expected_times_lindsay_followed_cameron = 5 /total_lindsay
        expected_times_cameron_followed_douglas = 1 /total_cameron
        expected_times_douglas_followed_amelia = 0 /total_douglas
        expected_times_amelia_followed_lindsay = 1 /total_amelia
        self.assertEqual(expected_times_lindsay_followed_cameron, link_matrix_df["Cameron Hill"]["Lindsay Young"])
        self.assertEqual(expected_times_cameron_followed_douglas, link_matrix_df["Douglas Matheson"]["Cameron Hill"])
        self.assertEqual(expected_times_douglas_followed_amelia, link_matrix_df["Amelia Ford"]["Douglas Matheson"])
        self.assertEqual(expected_times_amelia_followed_lindsay, link_matrix_df["Lindsay Young"]["Amelia Ford"])

