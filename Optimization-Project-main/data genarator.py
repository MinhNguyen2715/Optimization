import random as rd 
from ortools.linear_solver import pywraplp 

def Generator(N):
  K = rd.randrange(int(N/4), int(N/3), 1)
  M = rd.randrange(int(0.4 * N), int(0.7*N), 1)
  t = [x for x in range(1, N + 1)]
  rd.shuffle(t)
  
  for _ in range(N):
    t[_] %= M
    t[_] += 1 
  t = [0] + t 
  # Build initial solution 
  solver = pywraplp.Solver.CreateSolver('SCIP')
  INF = solver.infinity()
  x = [[0 for j in range(K + 1)] for i in range(N + 1)]
  for i in range(1, N + 1):
    for m in range(1, K + 1):
      x[i][m] = solver.IntVar(0, 1, 'x' + str(i) + ',' + str(m))
  y = [[0 for m in range(K + 1)] for j in range(M + 1)]
  for m in range(1, K + 1):
    for j in range(1, M + 1):
      y[j][m] = solver.IntVar(0, 1, 'y' + str(j) + ',' + str(m))
  z1 = solver.IntVar(1, INF, 'z1')
  z2 = solver.IntVar(1, INF, 'z2')
  for i in range(1, N + 1):
    cstr = solver.Constraint(1, 1)
    for m in range(1, K + 1):
      cstr.SetCoefficient(x[i][m], 1)
  for j in range(1, M + 1):
    cstr = solver.Constraint(1, 1)
    for m in range(1, K + 1):
      cstr.SetCoefficient(y[j][m], 1) 
  for m in range(1, K + 1):
    cstr1 = solver.Constraint(1, INF)
    cstr2 = solver.Constraint(1, INF)

    cstr3 = solver.Constraint(-INF, 0)
    cstr3.SetCoefficient(z1, -1)

    cstr4 = solver.Constraint(-INF, 0)
    cstr4.SetCoefficient(z2, -1)
    for i in range(1, N + 1):
      cstr1.SetCoefficient(x[i][m], 1)
      cstr3.SetCoefficient(x[i][m], 1)
    for j in range(1, M + 1):
      cstr2.SetCoefficient(y[j][m], 1)
      cstr4.SetCoefficient(y[j][m], 1)
  for i in range(1, N + 1):
    for m in range(1, K + 1):
      cstr = solver.Constraint(0, 1)
      cstr.SetCoefficient(x[i][m], 1)
      cstr.SetCoefficient(y[t[i]][m], 1)
  obj = solver.Objective()
  obj.SetCoefficient(z1, 1)  
  obj.SetCoefficient(z2, 1)
  obj.SetMinimization()
  rs = solver.Solve()
  # find a, b, c, d
  minab = INF 
  maxab = 0
  mincd = INF 
  maxcd = 0
  for m in range(1, K + 1):
    count1 = 0
    for i in range(1, N + 1):
      count1 += x[i][m].solution_value()
    minab = min(minab, count1)
    maxab = max(maxab, count1)

    count2 = 0
    for j in range(1, M + 1):
      count2 += y[j][m].solution_value()
    mincd = min(mincd, count2)
    maxcd = max(maxcd, count2)
  a, b, c, d = int(minab), int(maxab), int(mincd), int(maxcd) 
  
  s = [[0 for j in range(N + 1)] for i in range(N + 1)]
  for i1 in range(1, N):
    for i2 in range(i1 + 1, N + 1):
      total = 0
      for m in range(1, K + 1):
        if x[i1][m].solution_value() == 1 and x[i2][m].solution_value() == 1:
          total += x[i1][m].solution_value() + x[i2][m].solution_value() 
      if total == 2:
        s[i1][i2] = rd.choice([7, 8, 9])
      else:
        s[i1][i2] = rd.choice([1, 1, 1, 1, 1, 1, 1, 1, 4, 5, 6, 7, 8, 9])
       # if N >= 20:
        #  s[i1][i2] = 1
      s[i2][i1] = s[i1][i2]
  g = [[rd.choice([1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 5, 6, 7, 8, 9]) for i in range(N + 1)] for j in range(M + 1)]
  for m in range(1, K + 1):
    for j in range(1, M + 1):
      if y[j][m].solution_value() == 1: 
        for i in range(1, N + 1):
          if x[i][m].solution_value() == 1:
            g[j][i] = rd.choice([7, 8, 9])
  for j in range(1, M + 1):
    for i in range(1, N + 1):
      if j == t[i]:
        g[j][i] = 1

  
  # find e, f
  e = INF
  f = INF
  for m in range(1, K + 1):
    for i1 in range(1, N):
      for i2 in range(i1 +1, N + 1):
        if x[i1][m].solution_value() == 1 and x[i2][m].solution_value() == 1 and i1 != i2:
          e = min(e, s[i1][i2])
    for j in range(1, M + 1):
      if y[j][m].solution_value() == 1:
        for i in range(1, N + 1):
          if x[i][m].solution_value() == 1:
            f = min(f, g[j][i])
  e += rd.randrange(0, 1, 1) 
  f += rd.randrange(0, 1, 1)
  e = int(e)
  f = int(f)
  t = t[1:]
  # output data into text
  with open('data_size_' + str(N) + '.txt', 'w') as file:
    file.write(str(N) + ' ' + str(M) + ' ' + str(K) + '\n')
    file.write(str(a) + ' ' + str(b) + ' ' + str(c) + ' ' + str(d) + ' ' + str(e) + ' ' + str(f) + '\n')
    for i in range(1, N + 1):
      for x in s[i][1:]:
        file.write(str(x) + ' ')
      file.write('\n') 
    for j in range(1, M + 1):
      for x in g[j][1:]:
        file.write(str(x) + ' ')
      file.write('\n')
    for i in range(N):
      file.write(str(t[i]) + ' ')
Generator(25)