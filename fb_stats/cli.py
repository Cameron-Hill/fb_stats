"""This program works with JSON data that can be downloaded from facebook.
Navigate to the folder with the json file upon which you wish to run the analysis or pass the path as an argument"""
import click
from fb_stats import Generator, builders, html_generator


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
@click.argument("File", type=click.Path(exists=True), required=False, default="message.json")
def build(exclude, user_counts, message_hist,cum_freq, file):
    """Build an HTML file summarizing the results of the analysis,
        When no Stat Types are specified, All Stat Types are used to generate the report"""

    generator = Generator(file)
    stat_types_to_generate = set()

    if user_counts:
        stat_types_to_generate.add(builders.UserCounts(generator))

    if message_hist:
        stat_types_to_generate.add(builders.MessageHistogram(generator))

    if cum_freq:
        stat_types_to_generate.add(builders.CumulativeFrequency(generator))

    if exclude:
        stat_types_to_generate = builders.all_builders - stat_types_to_generate

    data = {type(x).__name__: x.get_data(to_js=True) for x in stat_types_to_generate}
    data["options"] = list(data.keys())
    data["title"] = generator.title
    html_generator.generate(data)

    click.echo("Report Generated: " + data["title"] + ".html")
