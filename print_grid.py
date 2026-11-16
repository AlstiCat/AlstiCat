import urllib.request


def remove_tags(text):
    # go through the text one letter at a time and skip anything inside < >
    result = ""
    inside_tag = False
    for letter in text:
        if letter == "<":
            inside_tag = True
        elif letter == ">":
            inside_tag = False
        elif inside_tag == False:
            result = result + letter
    return result.strip()


def print_grid(url):
    # get the web page as text
    response = urllib.request.urlopen(url)
    page = response.read().decode("utf-8")

    # split the page into table rows
    rows = page.split("</tr>")  # each row ends with </tr>

    # save each character and its x and y in a list
    data = []
    # skip the first piece (the header row) and the last piece (the page after the table)
    for row in rows[1:-1]:
        cells = row.split("</td>")  # each cell ends with </td>
        x = int(remove_tags(cells[0]))
        character = remove_tags(cells[1])
        y = int(remove_tags(cells[2]))
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
