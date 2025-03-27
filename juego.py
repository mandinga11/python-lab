# Pseudo-código (similar a GDScript)
class GameOfLife:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [
            [0 for _ in range(width)] for _ in range(height)
        ]  # Matriz inicializada con 0s (células muertas)

    def set_cell(self, x, y, state):
        self.grid[y][x] = state  # 1 para viva, 0 para muerta

    def get_cell(self, x, y):
        return self.grid[y][x]

    def count_neighbors(self, x, y):
        count = 0
        for i in range(max(0, y - 1), min(self.height, y + 2)):
            for j in range(max(0, x - 1), min(self.width, x + 2)):
                if (i, j) != (y, x) and self.get_cell(j, i) == 1:
                    count += 1
        return count

    def update(self):
        new_grid = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for y in range(self.height):
            for x in range(self.width):
                neighbors = self.count_neighbors(x, y)
                cell = self.get_cell(x, y)
                if cell == 1 and (neighbors < 2 or neighbors > 3):
                    new_grid[y][x] = 0  # Muere
                elif cell == 0 and neighbors == 3:
                    new_grid[y][x] = 1  # Nace
                else:
                    new_grid[y][x] = cell  # Permanece igual
        self.grid = new_grid


# Ejemplo de uso
game = GameOfLife(10, 10)
game.set_cell(5, 5, 1)  # Célula viva en el centro
# game.update()

for i in range(10):
    print(game.grid[i])
