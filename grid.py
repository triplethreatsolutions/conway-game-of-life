import collections

ALIVE = "$"
DEAD = "."

class LifeGrid:
    def __init__(self, pattern):
        self.pattern = pattern

    def evolve(self):
        neighbors = (
            (-1, -1), # above left
            (-1, 0), # above
            (-1, 1), # above right
            (0, -1), # left
            (0, 1), # right
            (1, -1), # below left
            (1, 0), # below
            (1, 1), # below right
        )
        num_neighbors = collections.defaultdict(int)
        for row, col in self.pattern.alive_cells:
            for drow, dcol in neighbors:
                # Walk thru each neighbor for this alive cell and increase touch count
                num_neighbors[(row + drow), (col + dcol)] += 1


        stay_alive = {
            # Cell needs to stay alive if it has 2 or more touches
            cell for cell, num in num_neighbors.items() if num in {2, 3}
        } & self.pattern.alive_cells # Only keep the cell alive if its already alive and meets criteria


        come_alive = {
            # Cell needs to come alive if it has 3 touches
            cell for cell, num in num_neighbors.items() if num == 3
        } - self.pattern.alive_cells # Remove current alive cells so we only know new live cells


        #
        self.pattern.alive_cells = stay_alive | come_alive

    def as_string(self, bbox):
        # bbox are bounding box size
        start_col, start_row, end_col, end_row = bbox
        # start display by centering the pattern name
        display = [self.pattern.name.center(2 * (end_col - start_col), "+")]
        for row in range(start_row, end_row):
            display_row = [
                # if (row, col) tuple is contained in the alive cells, insert ALIVE character
                ALIVE if (row, col) in self.pattern.alive_cells else DEAD
                for col in range(start_col, end_col)
            ]
            # append row pattern
            display.append(" ".join(display_row))
        # add carriage return after walking through bbox matrix
        return "\n ".join(display)

    def __str__(self):
        return (
            f"{self.pattern}:\n"
            f"Alive cells -> {sorted(self.pattern.alive_cells)}"
        )