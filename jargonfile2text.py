#!/usr/bin/env python3

from pathlib import Path
from bs4 import BeautifulSoup
from markdownify import chomp, ASTERISK, MarkdownConverter
import shutil
from markdownify import MarkdownConverter
import re


class JargonFileConverter(MarkdownConverter):
    def convert_a(self, el, text, convert_as_inline):
        prefix, suffix, text = chomp(text)
        if not text:
            return ''
        href = el.get('href')

        # Link to Markdown files instead
        href = re.sub('\\.html', '.md', href)

        title = el.get('title')
        # For the replacement see #29: text nodes underscores are escaped
        if (self.options['autolinks']
                and text.replace(r'\_', '_') == href
                and not title
                and not self.options['default_title']):
            # Shortcut syntax
            return '<%s>' % href
        if self.options['default_title'] and not title:
            title = href
        title_part = ' "%s"' % title.replace('"', r'\"') if title else ''
        return '%s[%s](%s%s)%s' % (prefix, text, href, title_part, suffix) if href else text


def md(soup, **options):
    return JargonFileConverter(**options).convert_soup(soup)


def to_md(f, soup):
    markdown = md(
        soup,
        heading_style='ATX',
        bullets='-',
        strong_em_symbol=ASTERISK,
        wrap=True,
        wrap_width=80
    )

    md_folder = Path(re.sub('jargonfile/html', 'md', str(f.parent)))
    md_path = md_folder / Path(f'{f.stem}.md')

    print(f'to {md_path}')

    with md_path.open('w') as out:
        out.write(markdown)


def clean():
    shutil.rmtree(Path('md'))
    Path('md').mkdir()


def main():
    clean()
    html_path = Path('jargonfile/html')

    for f in html_path.rglob('*'):
        if f.is_dir():
            continue

        print(f'From {f}', end=' ')

        if f.suffix == '.html':
            html = f.read_text()
            soup = BeautifulSoup(html, features='xml')
            to_md(f, soup)
        elif f.suffix == '.html~':
            # Skip ISO-8859-1 encoded files
            # TODO check if a UTF-8 encoded version exists
            continue
        elif f.suffix == '.css':
            continue
        else:
            raise NotImplementedError


if __name__ == '__main__':
    main()
