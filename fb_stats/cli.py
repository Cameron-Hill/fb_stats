"""This program works with JSON data that can be downloaded from facebook.
Navigate to the folder with the json file upon which you wish to run the analysis or pass the path as an argument"""
import click
from fb_stats import Generator, builders, html_generator
import numpy as np
import sys


@click.group()
@click.version_option()
def cli():
    click.echo("Facebook Stat Generator")


@cli.command()
@click.option("--exclude", is_flag=True,
              help="When set, will exclude any stat types that are passed as options rather than the default"
                   " behaviour of including only these options.")
@click.option("--user-counts", "-u", is_flag=True,
              help="Includes a bar chart describing the total messages sent for each user")
@click.option("--message-hist", "-m", is_flag=True,
              help="Includes a Histogram detailing how many messages per month a user sends over the course of the chat")
@click.option("--cum-freq", "-c", is_flag=True,
              help="Include a cumulative total of the messages sent per person, per month.")
@click.option("--heat-map", "-h", is_flag=True,
              help="Include A Matrix-Heatmap detailing how often a user replies directly after other users.")
@click.argument("File", type=click.Path(exists=True), required=False, default="message.json")
def build(file, exclude, **options):
    """Build an HTML file summarizing the results of the analysis,
        When no Stat Types are specified, All Stat Types are used to generate the report"""

    options = {k: not v if not any(options.values()) else v for k, v in options.items()}
    generator = Generator(file)
    stat_types_to_generate = set()
    if options["user_counts"]:
        stat_types_to_generate.add(builders.UserCounts(generator))

    if options["message_hist"]:
        stat_types_to_generate.add(builders.MessageHistogram(generator))

    if options["cum_freq"]:
        stat_types_to_generate.add(builders.CumulativeFrequency(generator))

    if options["heat_map"]:
        stat_types_to_generate.add(builders.HeatMap(generator, normalise=True, normalise_percent=True))
    # #     # stat_types_to_generate.add(builders.HeatMap(generator, ))
    # #     #     "norm":builders.HeatMap(generator, normalise=True),
    # #     #     "base":builders.HeatMap(generator, normalise=False),
    # #     # })

    data = {type(x).__name__: x.get_data(to_js=True) for x in stat_types_to_generate}
    data["options"] = list(data.keys())
    data["title"] = generator.title
    html_generator.generate(data)

    click.echo("Report Generated: " + data["title"] + ".html")

if __name__ == '__main__':
    from click.testing import CliRunner
    result = CliRunner().invoke(build, args=sys.argv[1:],
                     mix_stderr=True)
    print(result.output)