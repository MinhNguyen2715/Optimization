from ortools.sat.python import cp_model
import time
start = time.time()
with open('data/data_size_25.txt','r') as f :
  m = []
  for i in f:
    m.append(list(map(int, i.split())))
  [N,M,K] = m[0]
  [a, b, c, d, e, f] = m[1]
  t = m[-1]
  s = (m[2:2+N])
  g = (m[N+2:N+N+2])

model = cp_model.CpModel()

#variables
x_bin = [[model.NewIntVar(0,1, 'x_bin['+str(i)+']['+str(j)+']') for j in range(K)] for i in range(N)]     #student binary
x_int = [model.NewIntVar(0,K-1, 'x_int['+str(u)+']') for u in range(N)]
y_bin = [[model.NewIntVar(0,1, 'y_bin['+str(m)+']['+str(n)+']') for n in range(K)] for m in range(M)]
y_int = [model.NewIntVar(0,K-1, 'y_int['+str(v)+']') for v in range(M)]

student = [[model.NewIntVar(0,1, 'student['+str(i)+']['+str(j)+']') for j in range(N)] for i in range(N)]
prof = [[model.NewIntVar(0,1, 'prof['+str(m)+']['+str(n)+']') for n in range(N)] for m in range(M)]

for j in range(N):
  for i in range(N):
      model.Add(student[i][j] == student[j][i] )
      if i==j:
          model.Add(student [i][j] == 0)

#constraints
#1
for j in range(K):
  model.Add(a <= sum([x_bin[i][j] for i in range(N)]))
  model.Add(b >= sum([x_bin[i][j] for i in range(N)]))

for j in range(K):
  model.Add(c <= sum([y_bin[i][j] for i in range(M)]))
  model.Add(d >= sum([y_bin[i][j] for i in range(M)]))

for i in range(N):
    for j in range(K):
        model.Add(x_int[i] == j).OnlyEnforceIf(x_bin[i][j])
        model.Add(x_int[i] != j).OnlyEnforceIf(x_bin[i][j].Not())

for m in range(M):
    for n in range(K):
        model.Add(y_int[m] == n).OnlyEnforceIf(y_bin[m][n])
        model.Add(y_int[m] != n).OnlyEnforceIf(y_bin[m][n].Not())

#2: teacher != student
for i in range(N):
  model.Add(x_int[i]!=y_int[t[i]-1])

#3: similarity

for i in range(N-1):
  for j in range(i+1, N):
    model.Add(x_int[i]==x_int[j]).OnlyEnforceIf(student[i][j])
    model.Add(x_int[i]!=x_int[j]).OnlyEnforceIf(student[i][j].Not())
    model.Add(e<=s[i][j]).OnlyEnforceIf(student[i][j])

for m in range(M):
  for i in range(N):
    model.Add(y_int[m]==x_int[i]).OnlyEnforceIf(prof[m][i])
    model.Add(y_int[m]!=x_int[i]).OnlyEnforceIf(prof[m][i].Not())
    model.Add(f<=g[i][m]).OnlyEnforceIf(prof[m][i])

objective_terms = []
for i in range(N-1):
    for j in range(i+1,N):
        objective_terms.append(s[i][j] * student[i][j])

for i in range(M):
    for j in range(N):
        objective_terms.append(g[j][i] * prof[i][j])

#set parameter
model.Maximize(sum(objective_terms))

      
solver = cp_model.CpSolver()
status = solver.Solve(model)

# if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
#     print(f'Total similarity = {solver.ObjectiveValue()}\n')
#     for room in range(K):
#       print ('committee:', room+1)
#       for i in range(N):
#         if solver.Value(x_bin[i][room]) == 1:
#           print ('\tstudent',i+1)
#       print()
#       for j in range(M):
#         if solver.Value(y_bin[j][room]) == 1:
#           print ('\tprofessor',j+1)
# end = time.time()
# print(end-start)

thesis = [0 for i in range(N)]
prof = [0 for i in range(M)]

if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    # print(f'Total similarity = {solver.ObjectiveValue()}\n')
    for room in range(K):
        # print('committee:', room + 1)
        for i in range(N):
            if solver.Value(x_bin[i][room]) == 1:
                thesis[i] = room+1
                # print('\tstudent', i + 1)
        # print()
        for j in range(M):
            if solver.Value(y_bin[j][room]) == 1:
                prof[j] = room+1
                # print('\tprofessor', j + 1)


print(N)
print(*thesis)
print(M)
print(*prof)