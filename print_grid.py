import requests
from bs4 import BeautifulSoup


def print_grid(url):
    # get the web page
    response = requests.get(url)
    response.encoding = "utf-8"
    page = BeautifulSoup(response.text, "html.parser")

    # find all the rows in the table
    rows = page.find_all("tr")

    # save each character and its x and y in a list
    data = []
    for row in rows[1:]:  # skip the first row because it is the header
        cells = row.find_all("td")
        x = int(cells[0].text)
        character = cells[1].text
        y = int(cells[2].text)
        data.append([x, character, y])

    # find the biggest x and y so we know how big the grid is
    max_x = 0
    max_y = 0
    for item in data:
        if item[0] > max_x:
            max_x = item[0]
        if item[2] > max_y:
            max_y = item[2]

    # make a grid filled with spaces
    grid = []
    for i in range(max_y + 1):
        line = []
        for j in range(max_x + 1):
            line.append(" ")
        grid.append(line)

    # put each character in the right spot
    for item in data:
        x = item[0]
        character = item[1]
        y = item[2]
        grid[y][x] = character

    # print the grid starting from the top (y = 0 is the bottom)
    for y in range(max_y, -1, -1):
        print("".join(grid[y]))


print_grid("https://docs.google.com/document/d/e/2PACX-1vQiVT_Jj04V35C-YRzvoqyEYYzdXHcRyMUZCVQRYCu6gQJX7hbNhJ5eFCMuoX47cAsDW2ZBYppUQITr/pub")
