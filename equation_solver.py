#requesting user for the number of variables
from fractions import Fraction
import copy
num_variables = ''
while not num_variables.isdigit():
    num_variables = input("Enter the number of variables: ")
    if not num_variables.isdigit():
        print('Please enter a number!')
num_variables = int(num_variables)

#function to accept input from user
def user_input(matrix, a):
        count = 0
        while count < num_variables:
            while True:
                row = input()
                if len(row.split()) != a:
                    print(f"The row should have exactly {a} elements.")
                else:
                    try:
                        matrix.append([*map(Fraction, row.split())])
                        count+=1
                        break
                    except:
                        print("The elements must be a number!")


#requesting user for the coefficients of variables in each equation
coefficient_matrix = []
print('''Please enter the coefficients of each equation in the following manner:
X  Y  Z  ...
a1 a2 a3 ...
a4 a5 a6 ...
a7 a8 a9 ...
.
.
.

There can be infinite number of variables.
For N number of variables, there should be N number of equations.

''')
user_input(coefficient_matrix, num_variables)
temp_coefficient_matrix = copy.deepcopy(coefficient_matrix)

#requesting user for the constant terms in each equation
constant_matrix = []
print('''Please enter the constant terms of each equation in the following manner:
b1
b2
b3
.
.
.
''')
user_input(constant_matrix, 1)
temp_constant_matrix = copy.deepcopy(constant_matrix)

#function to calculate the determinant of a matrix
def determinant_calculator(matrix):
    det_matrix = copy.deepcopy(matrix)
    #presenting matrix
    def present_matrix(num_variables):
        print("The matrix is as follows:")
        for i in range(num_variables):
            print(' '.join(str(num) for num in matrix[i]))

    #making the matrix an upper triangular matrix 
    row, column = 0, 0
    while row < num_variables:
        for i in range(1,num_variables-row):
            try:
                current_factor = Fraction(det_matrix[row+i][column]/det_matrix[row][column]).limit_denominator()
            except:
                current_factor = 0
            for j in range(0,num_variables-row):
                det_matrix[row+i][column+j] -= det_matrix[row][column+j] * current_factor
        row += 1
        column += 1
    
    row,column = 1,1
    while row < num_variables-1:
        if det_matrix[row][column] == 0:
            for temp_column in range(0, num_variables):
                det_matrix[row][temp_column] += det_matrix[row+1][temp_column]
                det_matrix[row+1][temp_column] -= det_matrix[row][temp_column]
            row+=1
            column+=1
        else:
            row+=1
            column+=1

    #calculating determinant by multiplying the principal diagonal elements
    determinant = 1
    row, column = 0, 0
    while row < num_variables:
        determinant *= det_matrix[row][column]
        row += 1
        column += 1
    return determinant


determinant = determinant_calculator(coefficient_matrix)
#calculating coeff-con matrices determinants
coeff_con_det = []
temp_row, temp_column= 0, 0
while temp_column < num_variables:
    temp_matrix = copy.deepcopy(temp_coefficient_matrix)
    while temp_row < num_variables:
        temp_matrix[temp_row][temp_column] = temp_constant_matrix[temp_row][0]
        temp_row+=1

    temp_determinant = determinant_calculator(temp_matrix)
    coeff_con_det.append(temp_determinant)
    temp_column+=1
    temp_row = 0

if determinant != 0:
    print("The value of the variables in order are: \n")
    for det in coeff_con_det:
        print(det/determinant)
else:
    all_zero = False
    for i in coeff_con_det:
        if i != 0:
            print("The system of equations is inconsistent. It has no solution.")
            break
        all_zero = True
    if all_zero:
        print("The system of equations has infinitely many solutions.")