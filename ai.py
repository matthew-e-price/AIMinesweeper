import random

from cell import Cell


class AI:
    def __init__(self, size):
        self.size = size

        self.revealed_cells = set()
        self.mine_cells = set()
        self.safe_cells = set()

        self.possible_moves = set()
        self.possible_moves = {selected_cell for selected_cell in Cell.all_cells}

        self.knowledge = []

    def label_mine(self, cell):
        self.mine_cells.add(cell)
        cell.handle_right_click(event="<Button-3>")
        for sentence in self.knowledge:
            sentence.label_mine(cell)

    def label_safe(self, cell):
        self.safe_cells.add(cell)
        for sentence in self.knowledge:
            sentence.label_safe(cell)

    def add_knowledge(self, cell, mine_count):
        self.revealed_cells.add(cell)
        self.label_safe(cell)
        self.add_sentence(cell, mine_count)
        self.derive_safe_and_mine_cells()
        self.update_knowledge()

    def add_sentence(self, cell, mine_count):
        known_mines = 0
        unknown_cells = set()
        surrounding_cells = cell.get_surrounding_cells()

        for selected_cell in surrounding_cells:
            if selected_cell in self.mine_cells:
                known_mines += 1
            elif selected_cell not in self.safe_cells:
                unknown_cells.add(selected_cell)

        if len(unknown_cells) > 0:
            self.knowledge.append(Sentence(unknown_cells, mine_count - known_mines))

    def derive_safe_and_mine_cells(self):
        for sentence in self.knowledge:
            safe_cells_copy = sentence.known_safe_cells().copy()
            for selected_cell in safe_cells_copy:
                self.label_safe(selected_cell)

            mine_cells_copy = sentence.known_mines().copy()
            for selected_cell in mine_cells_copy:
                self.label_mine(selected_cell)

            if len(sentence.cells) == 0:
                self.knowledge.remove(sentence)

    def update_knowledge(self):
        for A in self.knowledge:
            for B in self.knowledge:
                if (A is not B) and (A.cells.issubset(B.cells)):
                    B.cells = B.cells.difference(A.cells)
                    B.mine_count = max(0, B.mine_count - A.mine_count)

    def make_safe_move(self):
        for selected_cell in self.safe_cells:
            if selected_cell not in self.revealed_cells:
                selected_cell.handle_left_click(event="<Button-1>", ai=self)
                self.add_knowledge(selected_cell, selected_cell.surrounding_mines)
                return selected_cell
        return None

    def make_random_move(self):
        cell_choices = list(self.possible_moves - self.revealed_cells - self.mine_cells)
        if not cell_choices:
            return None
        selected_cell = random.choice(cell_choices)
        selected_cell.handle_left_click(event="<Button-1>", ai=self)
        self.add_knowledge(selected_cell, selected_cell.surrounding_mines)
        return selected_cell


class Sentence:
    def __init__(self, cells, mine_count):
        self.cells = set(cells)
        self.mine_count = mine_count

    def __eq__(self, other):
        return self.cells == other.cells and self.mine_count == other.mine_count

    def __str__(self):
        return f"{self.cells} = {self.mine_count}"

    def known_mines(self):
        if len(self.cells) <= self.mine_count:
            return self.cells
        return set()

    def known_safe_cells(self):
        if self.mine_count == 0:
            return self.cells
        return set()

    def label_mine(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)
            self.mine_count = max(0, self.mine_count - 1)

    def label_safe(self, cell):
        if cell in self.cells:
            self.cells.remove(cell)
