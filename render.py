from jinja2 import Environment, FileSystemLoader, select_autoescape
import os

from stats import stats

PATH = os.path.dirname(os.path.abspath(__file__))
PREFIX = '/templates'
ENV = Environment(loader=FileSystemLoader(PATH + PREFIX, followlinks=True),
                  autoescape=select_autoescape(['html', 'xml']),
                  trim_blocks=True)


def render_page(page, context):
    return ENV.get_template(page).render(context)


html = render_page('pages/projects.html', {
    'projects': stats.projects,
})

with open('docs/index.html', encoding='utf-8', mode='w') as f:
    f.write(html)
