import itertools
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

    def __sub__(self,sentence):
        new_cells = self.cells - sentence.cells
        new_count = self.count - sentence.count

        return Sentence(cells=new_cells,count=new_count)


    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        mines = set()
        for element in self.cells:
            if element :
                mines.add(element)
        return mines


    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        safe = set()
        for element in self.cells:
            if element == False :
                safe.add(element)
        return safe


    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.discard(cell)
            self.count = self.count - 1


    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.discard(cell)



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


    def all_cells(self):
        cells = set()
        for i in range(8):
            for j in range(8):
                cells.add((i,j))

        return cells

    def neigbour(self,cell):
        all_index = [0,1,2,3,4,5,6,7]
        cell_neighbours = set()
        for i in range(-1,2):
            for j in range(-1,2):
                if ((cell[0] + i ) in all_index) and ((cell[1]+ j) in all_index):
                        cell_neighbours.add((cell[0] + i ,cell[1] + j ))

        cell_neighbours.discard(cell)
        return cell_neighbours


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

        self.moves_made.add(cell)
        self.mark_safe(cell)

        neighbour = self.neigbour(cell)
        neighbour -= self.moves_made
        neighbour -= self.safes
        for cells in neighbour.copy():
            if cells in self.mines:
                neighbour.discard(cells)
                count = count - 1
        new_sentence = Sentence(neighbour,count)
        self.knowledge.append(new_sentence)

        for sentence in self.knowledge:
            if sentence.count == 0:
                for cells in sentence.cells.copy():
                    self.mark_safe(cells)
            if len(sentence.cells) == sentence.count:
                for cells in sentence.cells.copy():
                    self.mark_mine(cells)

        for sentence1 in self.knowledge:
            for sentence2 in self.knowledge:
                if sentence2.cells in sentence1.cells:
                    self.knowledge.append(sentence1 - sentence2)



    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        if (self.safes) != 0:
            for cell in self.safes:
                if cell not in self.moves_made :
                    return cell
        else:
            return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """

        # Create a list of all possible cells


        # Shuffle the list randomly
        all_cells = list(self.all_cells())
        random.shuffle(all_cells)

        # Loop through the list and return the first cell that meets the criteria
        for cell in all_cells:
            if cell not in self.moves_made and cell not in self.mines:
                return cell

        # If no such cell exists, return None
        return None



