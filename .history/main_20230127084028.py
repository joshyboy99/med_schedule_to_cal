from html.parser import HTMLParser
from pathlib import Path

class MyParser(HTMLParser):
    def __init__(self, *, convert_charrefs: bool = ...) -> None:
        super().__init__(convert_charrefs=convert_charrefs)
        self._tables = []
        self._daterow = True
        self._rowdates = []
        self._rowevents = []
        self._current_tag = ''


    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._current_tag = tag
        if tag == 'td':
            if self._daterow:
                self._rowdates.append()
            else:

            
        return super().handle_starttag(tag, attrs)
    
    def handle_endtag(self, tag: str) -> None:
        if tag == 'table':
            self._tables += 1

        if tag == 'tr':
            self._daterow = ~self._daterow
        return super().handle_endtag(tag)

with Path('Sidoti Roster.htm').open() as f:
    html = f.read()
    parser = HTMLParser()

