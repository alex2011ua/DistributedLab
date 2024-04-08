import collections
import random

from colorama import Fore, Style


class Maze:
    """
    A maze is a 2d matrix.
    Entrance - "E" (only one and must be on some outer side of the maze)
    Exit - "X"  (only one and must be on some outer side of the maze)
    Road - "." (a cell that the player can pass through)
    Wall - "#" (a cell that the player can not pass through)
    Trap - "T" (a cell that the player can pass through,
                but passing 3 such cells will kill the player. Optional)
    Treasure - "$" (just a cell with some treasure. Optional).
    """

    def __init__(self, width: int, height: int):
        self.width: int = width
        self.height: int = height
        self.maze: list[list[str]] = [["#" for _ in range(width)] for _ in range(height)]
        self.path = []  # from start through treasure to finish
        self.traps = []
        self.treasure = None
        self.finish = None
        self.start = None

    def create_maze(self, trap_count: int = 5, treasure: bool = True):
        """Create maze with Entrance, Exit, Traps, Treasure."""

        self.maze_generate()
        self.add_cycles()
        self.add_start_and_finish()
        if treasure:
            self.add_treasure()
        if not self.add_path():
            print("Maze is wrong")
            return
        self.add_traps(trap_count)
        self.print_maze()
        print("Path from start to finish through treasure: ", self.path)
        print("Treasure: ", self.treasure)
        print("Traps: ", self.traps)

    def maze_generate(self, x: int = 0, y: int = 0):
        """Generate Road and Wall"""
        dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(dirs)
        for dx, dy in dirs:
            nx, ny = x + dx * 2, y + dy * 2
            if 0 <= nx < self.width and 0 <= ny < self.height and self.maze[ny][nx] == "#":
                self.maze[ny][nx] = "."
                self.maze[ny - dy][nx - dx] = "."
                self.maze_generate(nx, ny)

    def add_start_and_finish(self):
        self.maze[0][0] = "E"
        self.start = (0, 0)

        if self.width % 2 == 0 and self.height % 2 == 0:
            self.maze[-1][-2] = "X"
            self.finish = (self.width - 2, self.height - 1)

        else:
            self.maze[-1][-1] = "X"
            self.finish = (self.width - 1, self.height - 1)

    def add_treasure(self):
        """Random location search and treasure placement"""
        while True:
            tx, ty = random.randrange(1, self.width - 1), random.randrange(1, self.height - 1)
            if self.maze[ty][tx] == ".":
                self.maze[ty][tx] = "$"
                self.treasure = (tx, ty)
                break

    def print_maze(self):
        """Enter end Exit is green
        Treasure is yellow
        Trap is a red
        Way is magenta
        """

        print(f"Maze size is {self.width} x {self.height}:")
        print()
        for i in range(self.width):
            print(Fore.WHITE + str(i), end=" ")
        print()
        for x, row in enumerate(self.maze):
            for y, cell in enumerate(row):
                if cell == "$":
                    print(Fore.YELLOW + cell, end="")
                elif cell == "T":
                    print(Fore.RED + cell, end="")
                elif cell == "X" or cell == "E":
                    print(Fore.GREEN + cell, end="")
                elif (y, x) in self.path:
                    print(Fore.CYAN + cell, end="")
                else:
                    print(Fore.RESET + cell, end="")
                print(" ", end="")
            print()
        print(Style.RESET_ALL)

    def add_path(self) -> bool:
        """Add a path from start to finish. If treasure is present,
        the path will go through the treasure."""

        if self.treasure:
            path_exists_to_treasure, shortest_path_treasure = self._find_path(m.start, m.treasure)
            path_exists_to_finish, shortest_path_finish = self._find_path(m.treasure, m.finish)
            if path_exists_to_treasure and path_exists_to_finish:
                self.path = shortest_path_treasure + shortest_path_finish[:-1]
                return True
        else:
            path_exists, shortest_path = self._find_path(m.start, m.finish)
            if path_exists:
                self.path = shortest_path
                return True
        return False

    def add_traps(self, count_traps: int):
        """Add traps to maze. 2 traps on the path, another traps out of the way."""

        traps_list: list[tuple[int, int]] = []
        traps_on_path: int = 2 if count_traps > 2 else count_traps
        for _ in range(traps_on_path):
            while True:
                tx, ty = random.choice(self.path)
                if self.maze[ty][tx] == ".":
                    self.maze[ty][tx] = "T"
                    traps_list.append((tx, ty))
                    break
        traps_out_of_path: int = count_traps - traps_on_path
        for _ in range(traps_out_of_path):
            while True:
                tx, ty = random.randrange(1, self.width - 1), random.randrange(1, self.height - 1)
                if self.maze[ty][tx] == "." and (tx, ty) not in self.path:
                    self.maze[ty][tx] = "T"
                    traps_list.append((tx, ty))
                    break

        self.traps = traps_list

    def _find_path(self, start: tuple, finish: tuple) -> (bool, list | None):
        """
        Find a path from two pints.
        :param start:
        :param finish:
        :return: the path exists(bool), path(list)
        """

        visited = [[False for _ in range(self.width)] for _ in range(self.height)]
        queue = collections.deque([start])
        parents = {}  # Dictionary to store parent nodes for each cell
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        while queue:
            x, y = queue.popleft()
            if (x, y) == finish:  # Exit found
                # Reconstruct the shortest path
                path = []
                while (x, y) != start:
                    path.append((x, y))
                    x, y = parents[(x, y)]
                path.reverse()
                return True, path

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (
                    0 <= nx < self.width and 0 <= ny < self.height
                    and not visited[ny][nx]
                    and self.maze[ny][nx] in (".", "X", "T", "$", "E")
                ):
                    visited[ny][nx] = True
                    queue.append((nx, ny))
                    parents[(nx, ny)] = (x, y)  # Save parent node for current cell

        return False, None  # No path found

    def add_cycles(self):
        """Adds closure to the maze by removing some walls."""

        cycle_count = (self.height + self.width) // 6
        while cycle_count:
            x, y = random.randrange(1, self.width - 1), random.randrange(1, self.height - 1)
            if self.maze[y][x] == "#":
                if (
                    self.maze[y + 1][x] == "#" and self.maze[y - 1][x] == "#"
                    and self.maze[y][x + 1] == "." and self.maze[y][x - 1] == "."
                ):
                    self.maze[y][x] = "."
                    cycle_count -= 1
                elif (
                    self.maze[y][x + 1] == "#" and self.maze[y][x - 1] == "#"
                    and self.maze[y + 1][x] == "." and self.maze[y - 1][x] == "."
                ):
                    self.maze[y][x] = "."
                    cycle_count -= 1


if __name__ == "__main__":
    width, height = map(int, input("Enter maze size (width height): ").split())
    m = Maze(width, height)
    m.create_maze(trap_count=5, treasure=True)
