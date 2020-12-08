import math
from math import sqrt
import numbers

def zeroes(height, width):
        """
        Creates a matrix of zeroes.
        """
        g = [[0.0 for _ in range(width)] for __ in range(height)]
        return Matrix(g)

def identity(n):
        """
        Creates a n x n identity matrix.
        """
        I = zeroes(n, n)
        for i in range(n):
            I.g[i][i] = 1.0
        return I

def get_row(matrix, row):
    return matrix[row]

def get_column(matrix, column_number):
    column = []

    for i in range(len(matrix)):
        column.append(matrix[i][column_number])

    return column

def dot_product(vector_one, vector_two):
    # variable for accumulating the sum
    result = 0

    for i in range(len(vector_one)):
        result += vector_one[i] * vector_two[i]

    return result

class Matrix(object):

    # Constructor
    def __init__(self, grid):
        self.g = grid
        self.h = len(grid)
        self.w = len(grid[0])

    #
    # Primary matrix math methods
    #############################
 
    def determinant(self):
        """
        Calculates the determinant of a 1x1 or 2x2 matrix.
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate determinant of non-square matrix.")
        if self.h > 2:
            raise(NotImplementedError, "Calculating determinant not implemented for matrices largerer than 2x2.")
            
        # TODO - your code here
        if self.h == 1:
            return self.g[0][0]
        else:
            # The else Branch means that it is a 2x2 matrix
            # because matrixes with a width or height greater then 2 would have trown an exeption above
            return self.g[0][0] * self.g[1][1] - self.g[1][0] * self.g[0][1]

    def trace(self):
        """
        Calculates the trace of a matrix (sum of diagonal entries).
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate the trace of a non-square matrix.")

        # TODO - your code here
        trace = 0

        for row in range(self.h):
            for column in range(self.w):
                if row == column:
                    trace += self.g[row][column]

        return trace

    def inverse(self):
        """
        Calculates the inverse of a 1x1 or 2x2 Matrix.
        """
        if not self.is_square():
            raise(ValueError, "Non-square Matrix does not have an inverse.")
        if self.h > 2:
            raise(NotImplementedError, "inversion not implemented for matrices larger than 2x2.")

        # TODO - your code here
        
        inversed_matrix = []
        inversed_row = []
              
        if self.h == 1:
            inversed_row.append(1/self.g[0][0])
            inversed_matrix.append(inversed_row)
        else:
            # The else Branch means that it is a 2x2 matrix
            # because matrixes with a width or height greater then 2 would have trown an exeption above
            a = self.g[0][0]
            b = self.g[0][1]
            c = self.g[1][0]
            d = self.g[1][1]
            if a * d == b * c:
                raise ValueError('The matrix has no inverse matrix')

            factor = 1. / ((a * d) - (b * c))
            inversed_matrix.append([factor * d, factor * -b])
            inversed_matrix.append([factor * -c, factor * a])      

        return Matrix(inversed_matrix)
        

    def T(self):
        """
        Returns a transposed copy of this Matrix.
        """
        # TODO - your code here
        
        transposed_matrix = []
    
        for column in range(len(self.g[0])):
            transposed_matrix.append(get_column(self.g, column))
        
        return Matrix(transposed_matrix)
        

    def is_square(self):
        return self.h == self.w
    

    #
    # Begin Operator Overloading
    ############################
    def __getitem__(self,idx):
        """
        Defines the behavior of using square brackets [] on instances
        of this class.

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > my_matrix[0]
          [1, 2]

        > my_matrix[0][0]
          1
        """
        return self.g[idx]

    def __repr__(self):
        """
        Defines the behavior of calling print on an instance of this class.
        """
        s = ""
        for row in self.g:
            s += " ".join(["{} ".format(x) for x in row])
            s += "\n"
        return s

    def __add__(self,other):
        """
        Defines the behavior of the + operator
        """
        if self.h != other.h or self.w != other.w:
            raise(ValueError, "Matrices can only be added if the dimensions are the same") 
        #   
        # TODO - your code here
        #
        
        added_matrix = []
        
        for row in range(self.h):
            added_matrix.append([self.g[row][column] + other.g[row][column] for column in range(self.w)])

        return Matrix(added_matrix)

    def __neg__(self):
        """
        Defines the behavior of - operator (NOT subtraction)

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > negative  = -my_matrix
        > print(negative)
          -1.0  -2.0
          -3.0  -4.0
        """
        #   
        # TODO - your code here
        #
        
        negative = []
        
        for row in range(self.h):
            negative.append([self.g[row][column] * -1 for column in range(self.w)])
            
        return Matrix(negative)
            
        
    def __sub__(self, other):
        """
        Defines the behavior of - operator (as subtraction)
        """
        #   
        # TODO - your code here
        #
        
        subtracted_matrix = []
        
        for row in range(self.h):
            subtracted_matrix.append([self.g[row][column] - other.g[row][column] for column in range(self.w)])

        return Matrix(subtracted_matrix)
    

    def __mul__(self, other):
        """
        Defines the behavior of * operator (matrix multiplication)
        """
        #   
        # TODO - your code here
        #
        
        self_rows = len(self.g)
        other_columns = len(other.g[0])
        row_result = []
        
        # empty list that will hold the product of self x other
        result = []
        
        for self_row in range(self_rows):
            for other_column in range(other_columns):
                rowSelf = get_row(self.g, self_row)
                columnOther = get_column(other.g, other_column)
                
                dotProd = dot_product(rowSelf, columnOther)
                
                row_result.append(dotProd)
            
            result.append(row_result)
            row_result = []
        
        return Matrix(result)
    

    def __rmul__(self, other):
        """
        Called when the thing on the left of the * is not a matrix.

        Example:

        > identity = Matrix([ [1,0], [0,1] ])
        > doubled  = 2 * identity
        > print(doubled)
          2.0  0.0
          0.0  2.0
        """
        if isinstance(other, numbers.Number):
            multiplied_matrix = []

            for row in range(self.h):
                multiplied_matrix.append([self.g[row][column] * other for column in range(self.w)])

            return Matrix(multiplied_matrix)