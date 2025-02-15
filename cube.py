def draw_line(x1, y1, x2, y2):
    # Create a 2D array of spaces
    grid = [[' ' for _ in range(50)] for _ in range(50)]

    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    x, y = x1, y1
    sx = -1 if x1 > x2 else 1
    sy = -1 if y1 > y2 else 1

    if dx > dy:
        err = dx / 2.0
        while x != x2:
            grid[y][x] = '*'
            err -= dy
            if err < 0:
                y += sy
                err += dx
            x += sx
    else:
        err = dy / 2.0
        while y != y2:
            grid[y][x] = '*'
            err -= dx
            if err < 0:
                x += sx
                err += dy
            y += sy
    grid[y][x] = '*'

    # Print the grid as ASCII art
    for row in grid:
        print(''.join(row))

# Draw a line from (5, 5) to (20, 15)
draw_line(5, 5, 20, 15)
