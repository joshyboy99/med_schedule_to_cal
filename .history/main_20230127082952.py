from html.parser import HTMLParser
from pathlib import Path

class MyParser(HTMLParser):
    def __init__(self, *, convert_charrefs: bool = ...) -> None:
        super().__init__(convert_charrefs=convert_charrefs)
        self._daterow = True
        self._tables = []


    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == 'tr':

            
        return super().handle_starttag(tag, attrs)
    
    def handle_endtag(self, tag: str) -> None:
        if tag == 'table':
            self._tables += 1

        return super().handle_endtag(tag)

with Path('Sidoti Roster.htm').open() as f:
    html = f.read()
    parser = HTMLParser()

