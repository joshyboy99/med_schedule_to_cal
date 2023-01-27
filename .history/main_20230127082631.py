from html.parser import HTMLParser
from pathlib import Path

class MyParser(HTMLParser):
    def __init__(self, *, convert_charrefs: bool = ...) -> None:
        super().__init__(convert_charrefs=convert_charrefs)
        self._tablecount = 0
        self._tables = []


    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == 
        return super().handle_starttag(tag, attrs)

with Path('Sidoti Roster.htm').open() as f:
    html = f.read()
    parser = HTMLParser()

