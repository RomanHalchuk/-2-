class Matrix:
    def __init__(self, data):
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0]) if self.rows > 0 else 0

    def print_matrix(self):
        for row in self.data:
            print(' '.join(map(lambda x: str(round(x, 2)), row)))

    def add(self, other):
        if self.rows != other.rows or self.cols != other.cols:
            print("ERROR")
            return None
        result = [[self.data[i][j] + other.data[i][j] for j in range(self.cols)]
                  for i in range(self.rows)]
        return Matrix(result)

    def multiply_constant(self, c):
        result = [[elem * c for elem in row] for row in self.data]
        return Matrix(result)

    def multiply_matrix(self, other):
        if self.cols != other.rows:
            print("The operation cannot be performed.")
            return None
        result = [[sum(self.data[i][k] * other.data[k][j] for k in range(self.cols))
                   for j in range(other.cols)] for i in range(self.rows)]
        return Matrix(result)

    def transpose(self, mode=1):
        if mode == 1:
            result = [[self.data[j][i] for j in range(self.rows)] for i in range(self.cols)]
        elif mode == 2:
            result = [[self.data[self.rows-1-j][self.cols-1-i] for j in range(self.rows)]
                      for i in range(self.cols)]
        elif mode == 3:
            result = [list(reversed(row)) for row in self.data]
        elif mode == 4:
            result = list(reversed(self.data))
        else:
            print("Invalid transpose mode")
            return None
        return Matrix(result)

    def determinant(self):
        if self.rows != self.cols:
            print("Cannot calculate determinant of non-square matrix.")
            return None
        return self._det_recursive(self.data)

    def _det_recursive(self, matrix):
        n = len(matrix)
        if n == 1:
            return matrix[0][0]
        if n == 2:
            return matrix[0][0]*matrix[1][1] - matrix[0][1]*matrix[1][0]
        det = 0
        for c in range(n):
            minor = [row[:c] + row[c+1:] for row in matrix[1:]]
            det += ((-1)**c) * matrix[0][c] * self._det_recursive(minor)
        return det

    def inverse(self):
        det = self.determinant()
        if det == 0:
            print("This matrix doesn't have an inverse.")
            return None
        n = self.rows
        cofactors = []
        for r in range(n):
            cofactor_row = []
            for c in range(n):
                minor = [row[:c] + row[c+1:] for i, row in enumerate(self.data) if i != r]
                cofactor_row.append(((-1) ** (r + c)) * self._det_recursive(minor))
            cofactors.append(cofactor_row)
        cofactors_T = [[cofactors[j][i] for j in range(n)] for i in range(n)]
        inv = [[cofactors_T[i][j] / det for j in range(n)] for i in range(n)]
        return Matrix(inv)


def read_matrix():
    while True:
        try:
            n, m = map(int, input("Enter matrix size (rows cols): > ").split())
            break
        except ValueError:
            print("Please enter exactly two integers separated by space.")

    data = []
    for i in range(n):
        while True:
            row_input = input(f"Enter row {i+1}: > ").split()
            if len(row_input) != m:
                print(f"Please enter exactly {m} numbers.")
                continue
            try:
                row = list(map(float, row_input))
                data.append(row)
                break
            except ValueError:
                print("Please enter valid numbers.")
    return Matrix(data)

def main():
    while True:
        print("\n1. Add matrices")
        print("2. Multiply matrix by a constant")
        print("3. Multiply matrices")
        print("4. Transpose matrix")
        print("5. Calculate a determinant")
        print("6. Inverse matrix")
        print("0. Exit")
        choice = input("Your choice: > ")

        if choice == '1':
            print("For example: 2 2\nEnter first matrix:")
            A = read_matrix()
            print("Enter second matrix:")
            B = read_matrix()
            result = A.add(B)
            if result:
                print("The result is:")
                result.print_matrix()

        elif choice == '2':
            A = read_matrix()
            c = float(input("Enter constant: > "))
            result = A.multiply_constant(c)
            print("The result is:")
            result.print_matrix()

        elif choice == '3':
            print("Enter first matrix:")
            A = read_matrix()
            print("Enter second matrix:")
            B = read_matrix()
            result = A.multiply_matrix(B)
            if result:
                print("The result is:")
                result.print_matrix()

        elif choice == '4':
            print("Transpose modes:\n1. Main diagonal\n2. Side diagonal\n3. Vertical\n4. Horizontal")
            mode = int(input("Your choice: > "))
            A = read_matrix()
            result = A.transpose(mode)
            if result:
                print("The result is:")
                result.print_matrix()

        elif choice == '5':
            A = read_matrix()
            det = A.determinant()
            if det is not None:
                print("The result is:")
                print(round(det, 2))

        elif choice == '6':
            A = read_matrix()
            inv = A.inverse()
            if inv:
                print("The result is:")
                inv.print_matrix()

        elif choice == '0':
            break

        else:
            print("Invalid option")


if __name__ == "__main__":
    main()