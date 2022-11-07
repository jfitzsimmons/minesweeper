import itertools
import random
import copy
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """
        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
            return self.cells
        else:
            return None

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.

        """
        print("SENTENCE known_safes self.count: ", self.count)
        if self.count == 0:
            return self.cells
        else:
            return None

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        _cell = copy.deepcopy(cell)
        self.moves_made.add(_cell)
        _moves_made = copy.deepcopy(self.moves_made)
        self.mark_safe(_cell)
        neighbors = set()

        for i in range(_cell[0] - 1, _cell[0] + 2):
            for j in range(_cell[1] - 1, _cell[1] + 2):
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighbor = (i, j)
                    if neighbor not in _moves_made:
                        neighbors.add(neighbor)
        print("count: ", count)
        _sentence = Sentence(neighbors.difference(_moves_made), count)
        print("_sentence.cells: ", _sentence.cells,
              "_sentence.count: ", _sentence.count)
        self.knowledge.append(_sentence)
        _safes = copy.deepcopy(_sentence.known_safes())
        _mines = copy.deepcopy(_sentence.known_mines())

        if _safes is not None:
            _safes = _safes.difference(_moves_made)
            for cell in _safes:

                _cell = copy.deepcopy(cell)
                self.mark_safe(_cell)
        if _mines is not None:
            _mines = _mines.difference(_moves_made)
            for cell in _mines:
                _cell = copy.deepcopy(cell)
                self.mark_mine(_cell)

        """
        the point is, if their are prior sentences that need to be updated, that would now equal zero or whatever length, they need to be considered

        """
        sortedKnowledge = copy.deepcopy(self.knowledge)
        sortedKnowledge.sort(key=lambda x: x.count)
        # for sentence in sortedKnowledge:
        print(*sortedKnowledge, sep="\n")

        # TODO: 5) add any new sentences to the AI's knowledge base
        # if they can be inferred from existing knowledge

    def make_safe_move(self):
        _self = copy.deepcopy(self)
        if len(_self.safes) > 0:
            print("AI make safe move")
            available = _self.safes.difference(_self.moves_made)
            # TODO testjpf: out of available moves and get this error:
            """
            line 247, in make_safe_move
            move = random.choice([*available])
            File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/random.py", line 261, in choice
            raise IndexError('Cannot choose from an empty sequence') from None
            IndexError: Cannot choose from an empty sequence
            """
            move = random.choice([*available])
            print("safe: ", move)
            return move
        else:
            None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        print("MAKE RANDOM MOVE")
        _self = copy.deepcopy(self)
        if len(Minesweeper.board) > 0:
            _board = {*Minesweeper.board}
            return random.sample((_board.difference(_self.moves_made)), 1)
        else:
            return None
