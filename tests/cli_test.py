import re
import os
from fb_stats import cli
from click.testing import CliRunner
import unittest
from bs4 import BeautifulSoup as bs


class CliTest(unittest.TestCase):

    """The HTML Generator forces the builder to coerce the dataframe into a Javascript friendly format.  Where each
        sender in the dataframe represents a series with their own related data. The format is as follows:
            {'name':<'Sender Name'>, 'data' : <[related data]>}
        Where the name and the data for each plot should match the values tested in test_main"""


    def setUp(self):
        self.runner = CliRunner()
        with open("test_data/singletest1.json", "r") as f:
            self.test_data_single = f.read()
        with open("test_data/grouptest1.json","r") as f:
            self.test_data_group = f.read()

    def insert_file(self, group=False):
        file = self.test_data_group if group else self.test_data_single
        with open("message.json", "w") as f:
            f.write(file)

    def get_soup(self):
        html_file = [file for file in os.listdir('.') if file.endswith('.html')]
        with open(html_file[0], encoding="utf-8") as f:
            soup = bs(f, 'html.parser')
        return soup

    def get_scripts(self):
        scripts = self.get_soup().find_all("script")
        return scripts


    def test_build_generates_a_html_file(self):
        with self.runner.isolated_filesystem():
            self.insert_file()
            self.runner.invoke(cli.build, ["--user-counts"])
            html_file = [file for file in os.listdir('.') if file.endswith('.html')]
            self.assertTrue(html_file)


    def test_that_build_user_counts_produces_html_with_valid_user_counts_div(self):
        with self.runner.isolated_filesystem():
            self.insert_file()
            self.runner.invoke(cli.build, ["--user-counts"])
            soup = self.get_soup()
            valid_div = soup.find("div",{"id":"UserCounts"})
            self.assertTrue(valid_div)


    def validation_test_for_single_user_counts(self):
        with self.runner.isolated_filesystem():
            self.insert_file()
            self.runner.invoke(cli.build, ["--user-counts"])
            scripts = self.get_scripts()
            javascript = [x.text for x in scripts if "UserCounts" in x.text][0]
            expected_js_data_for_nicola = r"{'name': 'Nicola Scott', 'data': \[7]}"
            expected_js_data_for_cameron = r"{'name': 'Cameron Hill', 'data': \[3]}"
            self.assertTrue(re.search(expected_js_data_for_cameron,javascript))
            self.assertTrue(re.search(expected_js_data_for_nicola, javascript))


    def validation_test_for_single_message_histogram(self):
        with self.runner.isolated_filesystem():
            self.insert_file()
            self.runner.invoke(cli.build, ["--message-hist"])
            scripts = self.get_scripts()
            javascript = [x.text for x in scripts if "MessageHistogram" in x.text][0]
            expected_js_data_for_cameron = r"{'name': 'Cameron Hill', 'data': \[0.0, 0.0, 2.0, 0.0, 1.0]}"
            expected_js_data_for_nicola = r"'name': 'Nicola Scott', 'data': \[2.0, 2.0, 1.0, 1.0, 1.0]}"
            self.assertTrue(re.search(expected_js_data_for_cameron, javascript))
            self.assertTrue(re.search(expected_js_data_for_nicola, javascript))

    def validation_tests_for_single_message_cum_freq(self):
        with self.runner.isolated_filesystem():
            self.insert_file()
            self.runner.invoke(cli.build, ["--cum-freq"])
            scripts = self.get_scripts()
            javascript = [x.text for x in scripts if "CumulativeFrequency" in x.text][0]
            expected_js_data_for_cameron = r"{'name': 'Cameron Hill', 'data': \[0.0, 0.0, 2.0, 2.0, 3.0]}"
            expected_js_data_for_nicola = r"{'name': 'Nicola Scott', 'data': \[2.0, 4.0, 5.0, 6.0, 7.0]}"
            self.assertTrue(re.search(expected_js_data_for_cameron, javascript))
            self.assertTrue(re.search(expected_js_data_for_nicola, javascript))


    def validation_test_for_group_user_counts(self):
        with self.runner.isolated_filesystem():
            self.insert_file(group=True)
            self.runner.invoke(cli.build, ["--user-counts"])
            scripts = self.get_scripts()
            javascript = [x.text for x in scripts if "UserCounts" in x.text][0]
            expected_js_data_for_lindsay = r"{'name': 'Lindsay Young', 'data': \[9]}"
            expected_js_data_for_cameron = r"{'name': 'Cameron Hill', 'data': \[7]}"
            expected_js_data_for_amelia = r"{'name': 'Amelia Ford', 'data': \[2]}"
            expected_js_data_for_douglas = r"{'name': 'Douglas Matheson', 'data': \[1]}"
            self.assertTrue(re.search(expected_js_data_for_lindsay,javascript))
            self.assertTrue(re.search(expected_js_data_for_cameron, javascript))
            self.assertTrue(re.search(expected_js_data_for_amelia, javascript))
            self.assertTrue(re.search(expected_js_data_for_douglas, javascript))


    def validation_test_for_group_message_histogram(self):
        with self.runner.isolated_filesystem():
            self.insert_file(group=True)
            self.runner.invoke(cli.build, ["--message-hist"])
            scripts = self.get_scripts()
            javascript = [x.text for x in scripts if "MessageHistogram" in x.text][0]
            expected_js_data_for_lindsay = r"{'name': 'Lindsay Young', 'data': \[9.0]}"
            expected_js_data_for_cameron = r"{'name': 'Cameron Hill', 'data': \[7.0]}"
            expected_js_data_for_amelia = r"{'name': 'Amelia Ford', 'data': \[2.0]}"
            expected_js_data_for_douglas = r"{'name': 'Douglas Matheson', 'data': \[1.0]}"
            self.assertTrue(re.search(expected_js_data_for_lindsay, javascript))
            self.assertTrue(re.search(expected_js_data_for_cameron, javascript))
            self.assertTrue(re.search(expected_js_data_for_amelia, javascript))
            self.assertTrue(re.search(expected_js_data_for_douglas, javascript))

    def validation_tests_for_group_message_cum_freq(self):
        with self.runner.isolated_filesystem():
            self.insert_file(group=True)
            self.runner.invoke(cli.build, ["--cum-freq"])
            scripts = self.get_scripts()
            javascript = [x.text for x in scripts if "CumulativeFrequency" in x.text][0]
            expected_js_data_for_lindsay = r"{'name': 'Lindsay Young', 'data': \[9.0]}"
            expected_js_data_for_cameron = r"{'name': 'Cameron Hill', 'data': \[7.0]}"
            expected_js_data_for_amelia = r"{'name': 'Amelia Ford', 'data': \[2.0]}"
            expected_js_data_for_douglas = r"{'name': 'Douglas Matheson', 'data': \[1.0]}"
            self.assertTrue(re.search(expected_js_data_for_lindsay, javascript))
            self.assertTrue(re.search(expected_js_data_for_cameron, javascript))
            self.assertTrue(re.search(expected_js_data_for_amelia, javascript))
            self.assertTrue(re.search(expected_js_data_for_douglas, javascript))
