from n_dim_matrix import n_dim_matrix

def animate_create_grid(width: int, height: int):
    """ Creates a grid of empty lists as required by the [Animation] class. """

    grid = n_dim_matrix((height, width), fill=None)
    for row in range(height):
        for col in range(width):
            grid[row][col] = []

    return grid