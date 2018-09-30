"""
"""
from fb_stats import builders, Generator


def run(file="message.json", types=[]):
    generator = Generator(file)
    data = {type_: get_builder(type_, generator) for type_ in types}
    if len(data) == 1:
        data = list(data.values())[0]
    return data


def get_gen(fpath, fname=""):
    return Generator(fpath, fname)


def get_builder(type_, generator):
    return StatTypes.builders.get(type_)(generator).get_data()


class StatTypes:
    # TODO would this not make more sense if the top level attribute were references to the classes? for the sake of the API let cli handle input valid and such
    USER_HISTOGRAM = "USER_HISTOGRAM"
    MESSAGE_HISTOGRAM = "MESSAGE_HISTOGRAM"
    CUMULATIVE_FREQUENCY = "CUMULATIVE_FREQUENCY"
    WORD_FREQUENCY = "WORD_FREQUENCY"
    LINK_MATRIX = "LINK_MATRIX"
    builders = {
        "USER_HISTOGRAM": builders.UserCounts,
        "MESSAGE_HISTOGRAM": builders.MessageHistogram,
        "CUMULATIVE_FREQUENCY": builders.CumulativeFrequency,
        "WORD_FREQUENCY": builders.WordFrequency,
        "LINK_MATRIX": builders.LinkMatrix,
    }
