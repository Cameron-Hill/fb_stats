import json
import pandas as pd
from pathlib import Path
from fb_stats import decorators as dec, lemmatizer as lem, exceptions as ex
import os
import re


class Generator:
    
    def __init__(self, file="message.json"):
        jdata = self._load_json(file)
        self.title = jdata["title"]
        self.columns = self._get_keys(jdata)
        self.data = self._build_dataframe(jdata)
        self.participants = self._get_people(jdata)


    @dec.raise_on_fail(ex.LemmatizerUnavalibleError("ensure packages are installed"))
    def lemmatize(self, text_columns="content"):
        self.data[text_columns] = self.data[text_columns].apply(
            lambda x: lem.lemmatize_string(x) if x is not None else x)
            
    def remove_stopwords(self, text_columns="content"):
        #TODO allow additional stopwords to be defined
        sw = self._generate_stopwords()
        self.data[text_columns] = self.data[text_columns].apply(
            lambda x: " ".join([i for i in x.split() if i not in sw]) if x is not None else x)


    def _load_json(self, file):
        #TODO clean this function: load_json
        edit_file = Path(file[:-5] + "_edit.json")
        if edit_file.is_file():
            with open(edit_file, encoding="utf-8") as f:
                jdata = json.load(f)
            return jdata
        else:
            self._remove_byte_encodings(file)
            return self._load_json(file)

    def _remove_byte_encodings(self, file):
        with open(file, "r", encoding="utf-8") as f:
            removed = [re.sub(r'(?:\\u[0-9a-f]{4})+', "", line) for line in f]
        with open(file[:-5] + "_edit.json", "w", encoding="utf-8") as f:
            for line in removed:
                f.write(line)

    def _build_dataframe(self, jdata):
        #TODO clean this function : build_dataframe, modifying the dictionary by reference isn't cool
        messages = jdata["messages"]
        dic = {key: [] for key in self.columns}
        for m in messages:
            self._add_element(dic, m)
        df = pd.DataFrame().from_dict(dic)
        df = self._clean_text(df)
        return df

    def _get_keys(self, jdata):
        messages = self._get_column(jdata,"messages")
        keys = set()
        for d in messages:
            keys.update(d.keys())
        return keys
    
    def _get_people(self, data):
        return self.data["sender_name"].unique()
    
    @dec.raise_on_fail(ex.InvalidJSONException("Expected Column Not Found"))
    def _get_column(self, jdata, column):
        return jdata[column]


    @staticmethod
    def _add_element(dic, message):
        for key in dic.keys():
            if key in message.keys():
                dic[key].append(message[key])
            else:
                dic[key].append(None)
    
    @staticmethod
    def _generate_stopwords():
        #TODO Clean this function : generate_stopwords
        try:
            from nltk.corpus import stopwords
            sw = stopwords.words("english")
        except:
            with open(os.path.dirname(os.path.abspath(__file__))+"/resources/stopwords.txt") as f:
                sw = [line.split("\n")[0] for line in f]
        return sw

    
    @staticmethod
    #TODO clean this function: _clean_text <priority>
    def _clean_text(df, text_columns="content", remove_digits=True):
        def do(value, *args):
            if len(args) > 1:
                if not args[1]: pass
            return args[0](value) if value is not None else value

        to_alpha = re.compile('([^\s\w]|_)+')
        rm_whitespace = re.compile('\s+')

        operations = [
            [lambda x: x.lower(), ],
            [lambda x: to_alpha.sub('', x), ],
            [lambda x: rm_whitespace.sub(" ", x).strip(), ],
            [lambda x: ''.join([i for i in x if not i.isdigit()]), remove_digits],
        ]

        for func in operations:
            df[text_columns] = df[text_columns].apply(do, args=func)
        return df
