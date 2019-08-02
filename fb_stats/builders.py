import pandas as pd
import numpy as np
from fb_stats import decorators as dec


class _Builder:
    @staticmethod
    def _to_datetime(df):
        return pd.to_datetime(df, unit="ms")

    @staticmethod
    def _generate_count_time_data(data, exclude=[]):
        df = _Builder._pivot_table_by_sender(data)
        df["timestamp_ms"] = _Builder._to_datetime(pd.to_numeric(df["timestamp_ms"]))
        df.index.rename("index", inplace=True)
        df.columns = df.columns.droplevel()
        df.rename(columns={'': "timestamp_ms"}, inplace=True)
        grouped = df.groupby([df["timestamp_ms"].dt.year, df["timestamp_ms"].dt.month]).sum()
        return grouped.drop(columns=exclude)

    @staticmethod
    def _pivot_table_by_sender(df):
        df = df.set_index(['timestamp_ms', 'sender_name'])
        df = df[["content"]]
        df["content"] = 1
        df = df.unstack(1)
        df = df.fillna(0)
        df.reset_index(inplace=True)
        return df

    def _time_series_js_conversion(self, data):
        d = {"data": []}
        data = data.to_dict("split")
        d["index"] = [str(x) for x in data["index"]]
        for i, name in enumerate(data["columns"]):
            d["data"].append({"name": name, "data": list(np.array(data["data"])[:, i])})
        return d

class UserCounts(_Builder):
    def __init__(self, generator, exclude=[]):
        self.gen = generator
        self.exclude = exclude

    def get_data(self, to_js=False):
        data = self.gen.data["sender_name"].value_counts()
        if to_js:
            data = self._convert_to_js(data)
        return data

    def _convert_to_js(self, data):
        d = {"data": []}
        data = pd.DataFrame(data).to_dict("split")
        for i, name in enumerate(data["index"]):
            d["data"].append({"name": name, "data": list(data["data"][i])})
        return d


class MessageHistogram(_Builder):
    def __init__(self, generator, exclude=[]):
        self.gen = generator
        self.exclude = exclude

    def get_data(self, to_js=False):
        data = self._generate_count_time_data(self.gen.data)
        if to_js:
            data = self._time_series_js_conversion(data)
        return data



class CumulativeFrequency(_Builder):
    def __init__(self, generator, exclude=[]):
        self.gen = generator
        self.exclude = exclude

    def get_data(self, to_js=False):
        data =  self._generate_count_time_data(self.gen.data).cumsum()
        if to_js:
            data = self._time_series_js_conversion(data)
        return data


class WordFrequency(_Builder):
    def __init__(self, generator, exclude=[]):
        self.gen = generator
        self.exclude = exclude

    def get_data(self, to_js=False):
        return self._generate_counts()

    def _generate_counts(self):
        from collections import Counter
        dic = {}
        for member in self.gen.participants:
            counts = Counter()
            messages = self.gen.data.loc[self.gen.data["sender_name"] == member]["content"].dropna().tolist()
            for message in messages:
                counts.update(message.split())
            dic[member] = dict(counts)

        return pd.DataFrame().from_dict(dic).fillna(0)


class HeatMap(_Builder):
    def __init__(self, generator, normalise=True, exclude=None, normalise_percent=False):
        exclude = exclude or []
        self.name = "HeatMap"
        self.gen = generator
        self.exclude = exclude
        self.do_normalisation = normalise
        self.normalise_percent = normalise_percent

    def get_data(self, to_js=False):
        df = self._generate_counts().T
        if self.do_normalisation:
            df = self.normalise_data(df)
        if to_js:
            df = self._convert_to_js(df)
        return df

    def normalise_data(self, df, round_to=3):
        return (df.div(df.sum(axis=1), axis=0) * (100 if self.normalise_percent else 1)).round(round_to)


    def _convert_to_js(self, df):
        return {'index': df.index.tolist(),  'normalised':self.do_normalisation,
                'data': [[i, j, x] for i, a in enumerate(df.values.tolist()) for j, x in enumerate(a)]}


    def _generate_counts(self):
        import numpy as np
        people = self.gen.participants
        ordered_names = self.gen.data[["timestamp_ms", "sender_name"]].dropna().sort_values(by=["timestamp_ms"])[
            "sender_name"].tolist()
        name_map = {member: i for i, member in enumerate(people)}
        reverse_map = {i: member for member, i in name_map.items()}
        indexes = [reverse_map[x] for x in range(len(people))]
        count_matrix = np.zeros((len(people), len(people)))

        last_name = None
        for name in ordered_names:
            if last_name is not None:
                count_matrix[name_map[last_name]][name_map[name]] += 1
            last_name = name

        return pd.DataFrame(data=count_matrix,
                            index=indexes,
                            columns=indexes
                            )


all_builders = {
    UserCounts,
    MessageHistogram,
    CumulativeFrequency,
    WordFrequency,
    HeatMap
}
