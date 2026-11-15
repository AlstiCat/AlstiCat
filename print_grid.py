"""
Retrieve a published Google Doc containing a table of
(x-coordinate, Character, y-coordinate) rows, and print the
characters as a grid in a fixed-width layout.

Uses only the Python standard library (no pip installs needed).
"""

from html.parser import HTMLParser
from urllib.request import urlopen


class _TableParser(HTMLParser):
    """Collects the text of every table cell, grouped by row."""

    def __init__(self):
        super().__init__()
        self.rows = []        # list of rows; each row is a list of cell strings
        self._row = None      # the row currently being read
        self._cell = None     # text pieces of the cell currently being read

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self._row = []
        elif tag in ("td", "th") and self._row is not None:
            self._cell = []

    def handle_endtag(self, tag):
        if tag in ("td", "th") and self._cell is not None:
            self._row.append("".join(self._cell).strip())
            self._cell = None
        elif tag == "tr" and self._row is not None:
            self.rows.append(self._row)
            self._row = None

    def handle_data(self, data):
        if self._cell is not None:
            self._cell.append(data)


def print_grid_from_url(url):
    # 1. Retrieve the document
    with urlopen(url) as response:
        html = response.read().decode("utf-8")

    # 2. Parse the table rows
    parser = _TableParser()
    parser.feed(html)

    points = {}  # (x, y) -> character
    for row in parser.rows:
        if len(row) < 3:
            continue
        x_text, char, y_text = row[0], row[1], row[2]
        if not (x_text.isdigit() and y_text.isdigit()):
            continue  # skip the header row ("x-coordinate", ...)
        points[(int(x_text), int(y_text))] = char

    if not points:
        print("No grid data found.")
        return

    # 3. Build the grid; empty positions are spaces
    width = max(x for x, _ in points) + 1
    height = max(y for _, y in points) + 1

    # y = 0 is the bottom row, so print from the highest y down to 0
    for y in range(height - 1, -1, -1):
        line = "".join(points.get((x, y), " ") for x in range(width))
        print(line)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python print_grid.py <published-google-doc-url>")
    else:
        print_grid_from_url(sys.argv[1])
