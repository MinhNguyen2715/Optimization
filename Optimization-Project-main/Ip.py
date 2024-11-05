from ortools.linear_solver import pywraplp
from time import perf_counter
import sys
# input data

def input_data(filename):
    with open(filename) as text:
        [N, M, K] = [int(x) for x in text.readline().split()]
        [a, b, c, d, e, f] = [int(x) for x in text.readline().split()]
        s = [[0 for x in range(N + 1)]]
        for i in range(N):
            r = [int(x) for x in text.readline().split()]
            s.append([0] + r)

        g = [[0 for x in range(N + 1)]]
        for j in range(1, N + 1):
            r = [int(x) for x in text.readline().split()]
            g.append([0] + r)
        t = [0] + [int(x) for x in text.readline().split()]
    return N, M, K, a, b, c, d, e, f, s, g, t


def In():
    [N,M,K] = [int(x) for x in sys.stdin.readline().split()]
    [a,b,c,d,e,f] = [int(x) for x in sys.stdin.readline().split()]

    s = [[0 for i in range(N+1)]]
    for i in range(N):
        r = [int(x) for x in sys.stdin.readline().split()]
        s.append([0] + r)

    g = [[0 for x in range(M+1)]]
    for j in range(1, N+1):
        r = [int(x) for x in sys.stdin.readline().split()]
        g.append([0] + r)
    t = [0] + [int(x) for x in sys.stdin.readline().split()]

    return N, M, K, a, b, c, d, e, f, s, g, t

# filename = 'data\\data_size_9.txt'

# N, M, K, a, b, c, d, e, f, s, g, t = input_data(filename)
N, M, K, a, b, c, d, e, f, s, g, t = In()
# print(N,M,K)
# print(a,b,c,d,e,f)
# for i in range(N):
#     print(*s[i])
# for i in range(N):
#     print(*g[i])
# print(*t)

start = perf_counter()

# SET VARIABLES
solver = pywraplp.Solver.CreateSolver('CBC')
INF = solver.infinity()

z = [[0 for i in range(K + 1)]]

for i in range(1, N + 1):
    z.append([0] + [solver.IntVar(0, 1, 'z(' + str(i) + ',' + str(m) + ')')
                                            for m in range(1, K + 1)])


y = [[0 for i in range(K + 1)]]

for j in range(1, M + 1):
    y.append([0] + [solver.IntVar(0, 1, 'y(' + str(j) + ',' + str(m) + ')')
             for m in range(1, K + 1)])

# x(i1,i2,m)
x = [[[0 for m in range(K + 1)] for i2 in range(N + 1)] for i1 in range(N + 1)]
for i1 in range(1, N + 1):
    for i2 in range(1, N + 1):
        for m in range(1, K + 1):
            x[i1][i2][m] = solver.IntVar(
                0, 1, 'x(' + str(i1) + ',' + str(i2) + ',' + str(m) + ')')

# p(i,j,m)

p = [[[0 for m in range(K + 1)] for j in range(M + 1)] for i in range(N + 1)]
for i in range(1, N + 1):
    for j in range(1, M + 1):
        for m in range(1, K + 1):
            p[i][j][m] = solver.IntVar(
                0, 1, 'p(' + str(i) + ',' + str(j) + ',' + str(m) + ')')


# SET CONSTRAINTS

# constraint 1
for m in range(1, K + 1):
    cstr = solver.RowConstraint(a, b)
    for i in range(1, N + 1):
        cstr.SetCoefficient(z[i][m], 1)

# constraint 2
for m in range(1, K + 1):
    cstr = solver.RowConstraint(c, d)
    for j in range(1, M + 1):
        cstr.SetCoefficient(y[j][m], 1)

# constraint 3
for m in range(1, K + 1):
    for i in range(1, N + 1):
        cstr = solver.RowConstraint(0, 1)
        cstr.SetCoefficient(z[i][m], 1)
        cstr.SetCoefficient(y[t[i]][m], 1)


# constraint 4
for m in range(1, K + 1):
    for i1 in range(1, N + 1):
        for i2 in range(i1+1, N + 1):
            cstr = solver.RowConstraint(0, s[i1][i2]/e + 1)
            cstr.SetCoefficient(z[i1][m], 1)
            cstr.SetCoefficient(z[i2][m], 1)

# constraint 5
for m in range(1, K + 1):
    for i in range(1, N + 1):
        for j in range(1, M + 1):
                cstr = solver.RowConstraint(0, g[i][j]/f + 1)
                cstr.SetCoefficient(z[i][m], 1)
                cstr.SetCoefficient(y[j][m], 1)

# constraint 6
for i in range(1, N + 1):
    cstr = solver.RowConstraint(1, 1)
    for m in range(1, K + 1):
        cstr.SetCoefficient(z[i][m], 1)

# constraint 7
for j in range(1, M + 1):
    cstr = solver.RowConstraint(1, 1)
    for m in range(1, K + 1):
        cstr.SetCoefficient(y[j][m], 1)

# constraint 8
for m in range(1, K + 1):
    for i1 in range(1, N):
        for i2 in range(i1 + 1, N + 1):
            cstr1 = solver.RowConstraint(0, INF)
            cstr1.SetCoefficient(z[i1][m], 1)
            cstr1.SetCoefficient(z[i2][m], 1)
            cstr1.SetCoefficient(x[i1][i2][m], -2)

            cstr2 = solver.RowConstraint(-1, INF)
            cstr2.SetCoefficient(x[i1][i2][m], 1)
            cstr2.SetCoefficient(z[i1][m], -1)
            cstr2.SetCoefficient(z[i2][m], -1)

            cstr3 = solver.RowConstraint(0, 0)
            cstr3.SetCoefficient(x[i1][i2][m], 1)
            cstr3.SetCoefficient(x[i2][i1][m], -1)
# constraint 9
for m in range(1, K + 1):
    for i in range(1, N + 1):
        for j in range(1, M + 1):
            cstr1 = solver.RowConstraint(0, INF)
            cstr1.SetCoefficient(y[j][m], 1)
            cstr1.SetCoefficient(z[i][m], 1)
            cstr1.SetCoefficient(p[i][j][m], -2)

            cstr2 = solver.RowConstraint(-1, INF)
            cstr2.SetCoefficient(p[i][j][m], 1)
            cstr2.SetCoefficient(y[j][m], -1)
            cstr2.SetCoefficient(z[i][m], -1)

# constraint 10
for i in range(1, N + 1):
    for m in range(1, K + 1):
        cstr = solver.RowConstraint(0, 0)
        cstr.SetCoefficient(p[i][t[i]][m], 1)

obj = solver.Objective()
for m in range(1, K + 1):
    for i1 in range(1, N):
        for i2 in range(i1 + 1, N + 1):
            obj.SetCoefficient(x[i1][i2][m], s[i1][i2])

for m in range(1, K + 1):
    for i in range(1, N + 1):
        for j in range(1, M + 1):
            obj.SetCoefficient(p[i][j][m], g[i][j])
obj.SetMaximization()

rs = solver.Solve()
end = perf_counter()


thesis_solution = [None for i in range(N)]
pro_solution = [None for i in range(M)]

for m in range(1,K+1):
    for i in range(1,N+1):
        if z[i][m].solution_value() == 1.0:
            thesis_solution[i-1] = m
    for i in range(1,M+1):
        if y[i][m].solution_value() == 1.0:
            pro_solution[i-1] = m

print(N)
print(*thesis_solution)
print(M)
print(*pro_solution)
# 6
# 2 2 1 1 1 2
# 4
# 1 2 1 2
# output data
# def print_solution():
#     for m in range(1, K + 1):
#         print('_________________')
#         print('|COUNCIL: ' + '\t' + str(m) + '\t' + '|')
#         print('_________________')
#         for i in range(1, N + 1):
#             if z[i][m].solution_value() == 1:
#                 print('|Thesis ' + '\t' + str(i) + '\t' + '|')
#         print('_________________')
#         for j in range(1, M + 1):
#             if y[j][m].solution_value() == 1:
#                 print('|Teacher ' + '\t' + str(j) + '\t' + '|')
#         print('_________________')
#         print()
#         print()
#     print()
#     print('____________________________________')
# #   print('Total similarity value: ' + '\t' + str(total.solution_value()))
#     print('Total similarity value:', solver.Objective().Value())
# #   print('Value of e: ' + '\t' + str(E.solution_value()))
# #   print('Value of f: ' + '\t' + str(F.solution_value()))
#     print('____________________________________')
#     print()


# print_solution()
# print('Time :'+str(end-start), 's' + '\n' +
#       '____________________________________')
