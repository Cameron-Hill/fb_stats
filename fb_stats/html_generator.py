from jinja2 import Environment, PackageLoader, select_autoescape


def generate(data):
    env = Environment(loader=PackageLoader("fb_stats", 'templates'))
    html = env.get_template('head.html').render(title=data["title"])

    for option in data["options"]:
        context = data[option]
        template = env.get_template(option + '.html')
        html += template.render(data=context, title=data["title"])

    html += env.get_template('tail.html').render()

    with open(data["title"] + ".html", "w") as f:
        f.write(html)
