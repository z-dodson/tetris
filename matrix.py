from math import acos, pi

class Matrix:
    '''
    Base matrix class
    Input as a series of lists
    Each row is a new list
    Functions:
        - dimensions
        - determinant
        - transpose
        - inverse
        - cofactors (finds the matrix of cofactors)
        - minors (finds the matrix of minors)
    Can also add, subtract, multiply, and raise to a power
    If selecting or setting a specific item, use [row, column] syntax
    Alegbra not supported
    '''
    def __init__(self, *matrix_list):
        rowlen = max(len(row) for row in matrix_list)
        for row in matrix_list:
            if len(row) != rowlen:
                raise Invalid_Matrix()
        self.vector = False
        self.matrix = []
        for i in range(len(matrix_list)):
            row = [float(num) for num in matrix_list[i]]
            self.matrix.append(row)

    def dimensions(self):
        return (len(self.matrix), len(self.matrix[0]))

    def determinant(self):
        if self.dimensions() == (3, 3):
            # a(ei − fh) − b(di − fg) + c(dh − eg)
            self.det = self.matrix[0][0]*(self.matrix[1][1]*self.matrix[2][2] - self.matrix[1][2]*self.matrix[2][1]) - self.matrix[0][1]*(self.matrix[1][0]*self.matrix[2][2] - self.matrix[1][2]*self.matrix[2][0]) + self.matrix[0][2]*(self.matrix[1][0]*self.matrix[2][1] - self.matrix[1][1]*self.matrix[2][0])
            return self.det
        elif self.dimensions() == (2, 2):
            # ad − bc
            self.det = (self.matrix[0][0]*self.matrix[1][1]) - (self.matrix[0][1]*self.matrix[1][0])
            return self.det
        elif self.dimensions() == (1, 1):
            self.det = self.matrix[0][0]
            return self.det
        else:
            raise Unknow_Determinant(*self.dimensions())

    def transpose(self):
        new_matrix = []
        for i in range(len(self.matrix[0])):
            new_row = []
            for j in range(len(self.matrix)):
                new_row.append(self.matrix[j][i])
            new_matrix.append(new_row)
        return Matrix(*new_matrix)

    def inverse(self):
        if self.dimensions() == (3, 3):
            if self.determinant() == 0:
                raise No_Inverse()
            else:
                mat_minors = self.minors()

                mat_cofactors = self.cofactors(mat_minors)

                mat_tranposed = mat_cofactors.transpose()

                inverse_matrix = (1/self.determinant())*mat_tranposed
                return inverse_matrix

        elif self.dimensions() == (2, 2):
            if self.determinant() == 0:
                raise No_Inverse()
            else:
                a, b, c, d = self.matrix[0][0], self.matrix[0][1], self.matrix[1][0], self.matrix[1][1]
                new_matrix = [[d, -b], [-c, a]]
                inverse_matrix = (1/self.determinant())*Matrix(*new_matrix)
                return inverse_matrix

        elif self.dimensions() == (1, 1):
            reciprocal = 1/self.matrix[0][0]
            return Matrix([reciprocal])

        else:
            raise Unknow_Inverse(*self.dimensions())

    def cofactors(self, mat_minors):
        mat_cofactors = []
        for i in range(len(mat_minors.matrix)):
            new_row = []
            for j in range(len(mat_minors.matrix[i])):
                if (i+j) % 2 == 0:
                    new_row.append(float(mat_minors.matrix[i][j]))
                else:
                    new_row.append(mat_minors.matrix[i][j] * -1)
            mat_cofactors.append(new_row)
        mat_cofactors = Matrix(*mat_cofactors)
        return mat_cofactors

    def minors(self):
        mat_minors = []
        for i in range(len(self.matrix)):
            new_row = []
            for j in range(len(self.matrix[i])):
                if j == 0:
                    if i == 0:
                        matrix2x2 = [[self.matrix[1][1], self.matrix[1][2]], [self.matrix[2][1], self.matrix[2][2]]]
                    elif i == 1:
                        matrix2x2 = [[self.matrix[0][1], self.matrix[0][2]], [self.matrix[2][1], self.matrix[2][2]]]
                    elif i == 2:
                        matrix2x2 = [[self.matrix[0][1], self.matrix[0][2]], [self.matrix[1][1], self.matrix[1][2]]]
                elif j == 1:
                    if i == 0:
                        matrix2x2 = [[self.matrix[1][0], self.matrix[1][2]], [self.matrix[2][0], self.matrix[2][2]]]
                    elif i == 1:
                        matrix2x2 = [[self.matrix[0][0], self.matrix[0][2]], [self.matrix[2][0], self.matrix[2][2]]]
                    elif i == 2:
                        matrix2x2 = [[self.matrix[0][0], self.matrix[0][2]], [self.matrix[1][0], self.matrix[1][2]]]
                elif j == 2:
                    if i == 0:
                        matrix2x2 = [[self.matrix[1][0], self.matrix[1][1]], [self.matrix[2][0], self.matrix[2][1]]]
                    elif i == 1:
                        matrix2x2 = [[self.matrix[0][0], self.matrix[0][1]], [self.matrix[2][0], self.matrix[2][1]]]
                    elif i == 2:
                        matrix2x2 = [[self.matrix[0][0], self.matrix[0][1]], [self.matrix[1][0], self.matrix[1][1]]]
                matrix2x2 = Matrix(*matrix2x2)
                new_row.append(str(matrix2x2.determinant()))
            mat_minors.append(new_row)
        mat_minors = Matrix(*mat_minors)
        return mat_minors

    def adjoint(self):
        return self.cofactors(self.minors()).transpose()

    def round(self, num):
        new_matrix = []
        for row in self.matrix:
            new_matrix.append([round(number, num) for number in row])

        return Matrix(*new_matrix)

    def remove(self,*items):
        for item in items:
            if item in self.matrix: self.matrix.remove(item)
    def append(self,*items):
        for item in items: self.matrix.append(item)
    def replace(self,existingItem, newItem):
        if existingItem in self.matrix: 
            i = self.index(existingItem)
            self.matrix = self.matrix[:i]+[newItem]+self.matrix[i+1:]
    def index(self,item): return self.matrix.index(item)


    def __add__(self, other):
        new_matrix = []
        for i in range(len(self.matrix)):
            new_row = []
            for j in range(len(self.matrix[i])):
                new_row.append(str(self.matrix[i][j] + other.matrix[i][j]))
            new_matrix.append(' '.join(new_row))
        return Matrix(*new_matrix)

    def __sub__(self, other):
        new_matrix = []
        for i in range(len(self.matrix)):
            new_row = []
            for j in range(len(self.matrix[i])):
                new_row.append(str(self.matrix[i][j] - other.matrix[i][j]))
            new_matrix.append(' '.join(new_row))
        return Matrix(*new_matrix)

    def __mul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            if isinstance(self, Vector):
                new_matrix = []
                for i in range(self.dimensions()[1]):
                    new_row = []
                    for j in range(self.dimensions()[0]):
                        new_row.append(self.matrix[i] * other)
                    new_matrix.append(new_row)
                return Matrix(*new_matrix)
            else:
                new_matrix = []
                for i in range(self.dimensions()[0]):
                    new_row = []
                    for j in range(self.dimensions()[1]):
                        new_row.append(self.matrix[i][j] * other)
                    new_matrix.append(new_row)
                return Matrix(*new_matrix)
        # check that matrices are compatible
        elif isinstance(self, Matrix) and isinstance(other, Matrix):
            if self.dimensions()[1] == other.dimensions()[0]:
                if not isinstance(other, Vector) and not isinstance(self, Vector) and isinstance(other, Matrix) and isinstance(self, Matrix): # Check that they are both matrices and not vectors
                    new_matrix = []

                    for i in range(self.dimensions()[0]):
                        new_row = []
                        for j in range(other.dimensions()[1]):
                            new_row.append(sum([self.matrix[i][k] * other.matrix[k][j] for k in range(len(self.matrix[i]))]))
                        new_matrix.append(new_row)

                    return Matrix(*new_matrix)

                elif not all((isinstance(other, Vector), isinstance(self, Vector))) or (isinstance(other, Vector) and not isinstance(self, Vector)) or (isinstance(self, Vector) and not isinstance(other, Vector)):
                    if isinstance(other, Vector):
                        new_matrix = []

                        for i in range(self.dimensions()[0]):
                            new_row = []
                            for j in range(other.dimensions()[1]):
                                new_row.append(sum([self.matrix[i][k] * other.matrix[k] for k in range(len(self.matrix[i]))]))
                            new_matrix.append(new_row)
                    elif isinstance(self, Vector):
                        new_matrix = []

                        for i in range(self.dimensions()[0]):
                            new_row = []
                            for j in range(other.dimensions()[1]):
                                new_row.append(sum([self.matrix[i][k] * other.matrix[k][j] for k in range(len(self.matrix[i]))]))
                            new_matrix.append(new_row)
                    return Matrix(*new_matrix)
            else:
                raise Not_Compatible_Error()

    def __rmul__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return self.__mul__(other)

    def __pow__(self, power):
        if power == -1:
            return self.inverse()
        elif power <= 0 or power % 1 != 0:
            raise Power_Not_Positive_Error()
        new_matrix = self
        for _ in range(power-1):
            new_matrix = self.__mul__(new_matrix)
        return new_matrix

    def __str__(self):
        dim = self.dimensions()

        if dim[1] != 1:
            # Make every item in column the same length
            string_values = []

            for i in range(dim[0]):
                string_values.append([])
                for j in range(dim[1]):
                    string_values[i].append("")

            for i in range(dim[1]):
                lens = []
                column = []

                for j in range(dim[0]):
                    lens.append(len(str(self.matrix[j][i])))
                    column.append(str(self.matrix[j][i]))

                max_length = max(lens)

                for j in range(len(column)):
                    if (max_length - lens[j]) % 2 == 0:
                        column[j] = " " * ((max_length - lens[j])//2) + column[j] + " " * ((max_length - lens[j])//2)
                    else:
                        column[j] = " " + " " * ((max_length - lens[j])//2) + column[j] + " " * ((max_length - lens[j])//2)

                for j in range(len(column)):
                    string_values[j][i] = column[j]

        else:
            # Make every item in column the same length
            string_values = []
            for j in range(dim[0]):
                string_values.append([])

            lens = []
            column = []
            for i in range(dim[0]):

                lens.append(len(str(self.matrix[i][0])))
                column.append(str(self.matrix[i][0]))

            max_length = max(lens)

            for j in range(len(column)):
                if (max_length - lens[j]) % 2 == 0:
                    column[j] = " " * ((max_length - lens[j])//2) + column[j] + " " * ((max_length - lens[j])//2)
                else:
                    column[j] = " " + " " * ((max_length - lens[j])//2) + column[j] + " " * ((max_length - lens[j])//2)

            for i in range(len(column)):
                string_values[i].append(column[i])




        matrix_string = ""
        if dim[0] == 1:
            matrix_string = "[" + " ".join(str(num) for num in string_values[0]) + "] "
        else:
            matrix_string_list = []
            for i in range(len(string_values)):
                matrix_string = ""
                matrix_string = '  '.join(str(num) for num in string_values[i])

                matrix_string_list.append(matrix_string)
            maxlen = max(len(row) for row in matrix_string_list)
            for i in range(len(matrix_string_list)):
                matrix_string_list[i] += " " * (maxlen - len(matrix_string_list[i]))
                if i == 0:
                    matrix_string_list[i] = "|‾ " + matrix_string_list[i] + " ‾|"
                    # matrix_string_list[i] += "‾|"
                elif dim[0]-1 == i:
                    matrix_string_list[i] = "|_ " + matrix_string_list[i] + " _| "
                    # matrix_string_list[i] += "_| "``
                else:
                    matrix_string_list[i] = "|  " + matrix_string_list[i] + "  |"
                    # matrix_string_list[i] += " |"
            matrix_string = "\n".join(matrix_string_list)


        return matrix_string[:-1]

    def __repr__(self):
        string = f"{self.__str__()}\nDimensions: {self.dimensions()}\nMatrix: {self.matrix}"
        return string

    def __eq__(self, other):
        return self.matrix == other.matrix

    def __ne__(self, other):
        return not self.__eq__(other)

    def __neg__(self):
        return self.__mul__(-1)

    def __getitem__(self, index):
        return self.matrix[index]

    def __setitem__(self, index, value):
        self.matrix[index[1]][index[0]] = float(value)

    def __abs__(self):
        return self.determinant()

    def __contains__(self, item):
        if item in self.matrix: return True
        return False


class Vector(Matrix):
    def __init__(self, vector_list):
        self.matrix = [float(num) for num in vector_list]
        self.vector = True

    def round(self, num):
        new_matrix = []
        for number in self.matrix:
            new_matrix.append(round(number, num))

        return Matrix(*new_matrix)

    def angle(self, other, radians=True):
        '''
        Calculates the angle between two vectors
        Angle defaults to radians
        Optional parameter to return in degrees (radians=False)
        '''
        if isinstance(other, Vector):
            if radians:
                return acos(self.dot(other) / (abs(self) * abs(other)))
            else:
                return acos(self.dot(other) / (abs(self) * abs(other))) * 180 / pi
        else:
            raise Not_Compatible_Error()

    def unit(self):
        return self.__mul__(1/abs(self))

    def dot(self, other):
        num = 0
        for i in range(len(self.matrix)):
            num += self.matrix[i] * other.matrix[i]
        return num

    def cross(self, other):
        if len(self.matrix) != 3 or len(other.matrix) != 3:
            raise Cannot_Perform_Cross_Product()
        else:
            return Vector([self.matrix[1] * other.matrix[2] - self.matrix[2] * other.matrix[1],
                          self.matrix[2] * other.matrix[0] - self.matrix[0] * other.matrix[2],
                          self.matrix[0] * other.matrix[1] - self.matrix[1] * other.matrix[0]])

    def __str__(self):
        dim = self.dimensions()


        # Make every item in column the same length
        string_values = []
        for j in range(len(self.matrix)):
            string_values.append([])

        lens = []
        column = []
        for i in range(len(self.matrix)):

            lens.append(len(str(self.matrix[i])))
            column.append(str(self.matrix[i]))

        max_length = max(lens)

        for j in range(len(column)):
            if (max_length - lens[j]) % 2 == 0:
                column[j] = " " * ((max_length - lens[j])//2) + column[j] + " " * ((max_length - lens[j])//2)
            else:
                column[j] = " " + " " * ((max_length - lens[j])//2) + column[j] + " " * ((max_length - lens[j])//2)

        for i in range(len(column)):
            string_values[i].append(column[i])


        matrix_string = ""
        if dim[0] == 1:
            matrix_string = "[" + " ".join(str(num) for num in string_values[0]) + "] "
        else:
            for i in range(dim[0]):
                if i == 0:
                    matrix_string += "|‾ "
                elif dim[0]-1 == i:
                    matrix_string += "|_ "
                else:
                    matrix_string += "|  "
                matrix_string += str(string_values[i][0])
                matrix_string += " "
                if i == 0:
                    matrix_string += "‾|"
                elif dim[0]-1 == i:
                    matrix_string += "_|"
                else:
                    matrix_string += " |"
                matrix_string += "\n"
        return matrix_string[:-1]

    def __abs__(self):
        num = 0
        for i in range(len(self.matrix)):
            num += self.matrix[i]**2
        return num**(1/2)

    def dimensions(self):
        return (len(self.matrix), 1)

    def determinant(self):
        pass

    def transpose(self):
        pass

    def inverse(self):
        pass

    def minors(self):
        pass

    def cofactors(self):
        pass


class Not_Compatible_Error(Exception):
    def __init__(self):
        raise Exception('Matrices are not compatible')


class Power_Not_Positive_Error(Exception):
    def __init__(self):
        raise Exception('Power must be positive integer')


class Unknow_Determinant(Exception):
    def __init__(self, dimx, dimy):
        raise Exception(f'Cannot calculate the determinant for a {dimx}x{dimy} matrix')


class Unknow_Inverse(Exception):
    def __init__(self, dimx, dimy):
        raise Exception(f'Cannot calculate the inverse for a {dimx}x{dimy} matrix')


class No_Inverse(Exception):
    def __init__(self):
        raise Exception('The matrix does not have an inverse')


class Invalid_Matrix(Exception):
    def __init__(self):
        raise Exception("Not every term in the matrix filled in")


class Cannot_Perform_Cross_Product(Exception):
    def __init__(self):
        raise Exception("Cannot perform cross product with these vectors")


def simultaneous_eq(matrix, vector):
    if matrix.dimensions()[1] != (vector.dimensions()[0]):
        raise Not_Compatible_Error()
    else:
        new_matrix = matrix.inverse()*vector
        return new_matrix
