from jinja2 import Environment, FileSystemLoader, select_autoescape
import os
import calendar

from stats import stats

PATH = os.path.dirname(os.path.abspath(__file__))
PREFIX = '/templates'
ENV = Environment(loader=FileSystemLoader(PATH + PREFIX, followlinks=True),
                  autoescape=select_autoescape(['html', 'xml']),
                  trim_blocks=True)

ENV.globals['max'] = max
ENV.globals['min'] = min


def render_page(page, context):
    return ENV.get_template('pages/{}.html'.format(page)).render(context)


def save_html(page, content):
    with open('docs/{}.html'.format(page), encoding='utf-8', mode='w') as f:
        f.write(content)

# Render home
save_html('index', render_page('projects', {
    'projects': stats.projects,
}))

# Render graphs
save_html('graphs', render_page('graphs', {
    'commits': stats.analyze_commit_timing(),
    'day_name': calendar.day_name
}))
