import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variable in self.domains:
            for word in self.domains[variable].copy():
                if len(word) != variable.length:
                    self.domains[variable].remove(word)
        

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """     
        removed = False
        my_set = set()
        if self.crossword.overlaps[(x,y)] == None:
            return False
        i,j = self.crossword.overlaps[(x,y)]
    
        for word in self.domains[y]:
            if len(word) >= j + 1:
                my_set.add(word[j])
            

        for xi in self.domains[x].copy():
            if len(xi) < i + 1:
                self.domains[x].remove(xi)
                removed = True
                continue
            if xi[i] not in my_set:
                self.domains[x].remove(xi)
                removed = True

        return removed 


                

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        arc = set()

        if arcs == None:
            for i in self.crossword.variables:
                for j in self.crossword.neighbors(i):
                    arc.add((i,j))
        else:
            for i in self.domains:
                for j in self.crossword.neighbors(i):
                    arc.add((i,j))
            if self.consistent(arcs):
                return False

        while len(arc) != 0:
            x,y = arc.pop()
            if self.revise(x,y):
                if len(self.domains[x]) == 0:
                    return False
                for z in self.crossword.neighbors(x):
                    if z != y:
                        arc.add((z,x))
        return True


        

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        if len(assignment) != len(self.crossword.variables):
            return False
        
        for element1 in assignment:
            for element2 in assignment:
                if (assignment[element1] in self.crossword.words) and (assignment[element2] in self.crossword.words) and (element1 != element2):
                        if assignment[element1] == assignment[element2]:
                            return False
                    
                        else:
                            continue
                        
        return True
    

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for value in assignment:
            for next_value in assignment:
                if (value != next_value) and (assignment[value] == assignment[next_value]):
                    return False
                
        for value in assignment:
            if len(assignment[value]) != value.length:
                return False
            
            for neighbor in self.crossword.neighbors(value):   
                if neighbor in assignment:
                    i,j = self.crossword.overlaps[value,neighbor]
                    if assignment[value][i] != assignment[neighbor][j]:
                        return False

                else:
                    continue


        return True
    

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        '''my_list = []
        for word in self.domains[var]:
            my_list.append(word)

        return my_list'''
        my_list = []
        my_dict = dict()
        count = 0
        for word in self.domains[var]:
            count = 0
            for neighbor in self.crossword.neighbors(var):
                if neighbor not in assignment:
                    if word in self.domains[neighbor]:
                        count += 1
            my_dict.update({word:count})

        my_dict = dict(sorted(my_dict.items(),key=lambda elment: elment[1]))

        for word in my_dict:
            my_list.append(word)

        return my_list

        

        

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        my_dict = dict()
        solution = []
        for variable in self.crossword.variables:
            if variable not in assignment:
                my_dict[variable] = len(self.domains[variable])

        my_dict = dict(sorted(my_dict.items(),key=lambda element: element[1]))
        for element in my_dict:
            if my_dict[element] == my_dict[list(my_dict.keys())[0]]:
                solution.append((element,len(self.crossword.neighbors(element))))

        solution = sorted(solution,key=lambda element: element[1])
        
        return solution[0][0]

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        
        if self.assignment_complete(assignment=assignment):
            return assignment
        
        if self.consistent(assignment=assignment):
            variable = self.select_unassigned_variable(assignment=assignment)
            for value in self.order_domain_values(var=variable,assignment=assignment):
                if self.consistent(assignment=assignment):
                    assignment[variable] = value
                    result = self.backtrack(assignment=assignment)
                    if result != None:
                        return result
        assignment.popitem()

        return None
                    
       
        


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
