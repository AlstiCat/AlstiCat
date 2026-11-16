import pandas as pd


def print_grid(url):
    # Read the table from the doc; the first row is the header
    table = pd.read_html(url, header=0, encoding="utf-8")[0]

    # Make a grid of spaces big enough to hold every character
    width = table.iloc[:, 0].max() + 1
    height = table.iloc[:, 2].max() + 1
    grid = [[" "] * width for _ in range(height)]

    # Put each character at its (x, y) spot
    for x, char, y in table.values:
        grid[y][x] = char

    # y = 0 is the bottom row, so print the top row first
    for row in reversed(grid):
        print("".join(row))


print_grid("https://docs.google.com/document/d/e/2PACX-1vQiVT_Jj04V35C-YRzvoqyEYYzdXHcRyMUZCVQRYCu6gQJX7hbNhJ5eFCMuoX47cAsDW2ZBYppUQITr/pub")
