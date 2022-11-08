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
            print("known_mine: ", [*self.cells])
            return self.cells
        else:
            return None

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.

        """
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
        self.board = []

        for i in range(self.height):
            for j in range(self.width):
                self.board.append((i, j))

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        # TESTJPF try loggin mostly when something is marked safe by ai or marked mine and see if you agree

        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        # TESTJPF try loggin mostly when something is marked safe by ai or marked mine and see if you agree
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
        print("__ADDED__ cell: ", cell)
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

        _sentence = Sentence(neighbors.difference(_moves_made), count)
        print("_sentence.cells: ", _sentence.cells,
              "_sentence.count: ", _sentence.count, "for cell: ", _cell)
        if len(_sentence.cells) > 0:
            self.knowledge.append(_sentence)
        _safes = copy.deepcopy(_sentence.known_safes())
        _mines = copy.deepcopy(_sentence.known_mines())

        if len(_sentence.cells) == _sentence.count:
            print("should mark mine for: ", [*_sentence.cells])
            print("_mines: ", [*_mines])
        if _safes is not None:
            _safes = _safes.difference(_moves_made)
            for cell in _safes:
                _cell = copy.deepcopy(cell)
                self.mark_safe(_cell)
        if _mines is not None:
            print("_mines length A: ", len(_mines))
            _mines = _mines.difference(self.mines)
            print("_mines length B: ", len(_mines))
            for cell in _mines:
                _cell = copy.deepcopy(cell)
                self.mark_mine(_cell)

        sortedKnowledge = copy.copy(self.knowledge)
        sortedKnowledge.sort(key=lambda x: x.count, reverse=True)
        #print(*self.knowledge, sep="\n")

        for i, sentence in enumerate(sortedKnowledge[:-1]):
            if sortedKnowledge[i+1].cells.issubset(sentence.cells) and len(sortedKnowledge[i+1].cells) > 0:
                # TODO: TESTJPF log both sets and make sure they actually subsets
                print(sortedKnowledge[i+1].cells,
                      " is subset of ", sentence.cells)
                solos = sentence.cells.difference(sortedKnowledge[i+1].cells)
                diffs = sentence.cells.difference(solos)
                solos = solos.difference(self.safes)
                if len(solos) > 0:
                    newCount = sentence.count-sortedKnowledge[i+1].count
                    print("Big set: ", sentence.count,
                          "little set: ", sortedKnowledge[i+1].count)
                    print(
                        "Sentence(solos: ", [*solos], ", newcount: ", newCount)
                    # TODO: TESTJPF probably need to loop this
                    newSentence = Sentence(solos, newCount)

                    self.knowledge.append(newSentence)
                    if newCount == 0:
                        for cell in solos:
                            print("!!!! __enumerate__ marked safe: ", cell)
                            self.mark_safe(cell)
                if len(diffs) > 0 and len(diffs) == sentence.count:
                    for cell in diffs:
                        print("!!!! __enumerate__ marked MINE: ", cell)
                        self.mark_mine(cell)

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
            if len(available) > 0:
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
        _available = {*_self.board}.difference(_self.moves_made)
        _available = _available.difference(_self.mines)
        if len(_available) > 0:
            return random.choice([*_available])
        else:
            return None
