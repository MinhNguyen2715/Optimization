import time
import sys
start = time.time()
# with open('data/tmp.txt','r') as f :
#   m = []
#   for i in f:
#     m.append(list (map(int, i.split())))
#   [N,M,K] = m[0]
#   [a, b, c, d, e, f] = m[1]
#   t = m[-1]
#   s = (m[2:2+N])
#   g = (m[N+2:N+N+2])

def In():
  [N, M, K] = [int(x) for x in sys.stdin.readline().split()]
  [a, b, c, d, e, f] = [int(x) for x in sys.stdin.readline().split()]

  s = [[0 for i in range(N)]]
  for i in range(N):
    r = [int(x) for x in sys.stdin.readline().split()]
    s.append(r)

  g = [[0 for x in range(M)]]
  for j in range(N):
    r = [int(x) for x in sys.stdin.readline().split()]
    g.append(r)
  t = [int(x) for x in sys.stdin.readline().split()]

  return N, M, K, a, b, c, d, e, f, s, g, t


N, M, K, a, b, c, d, e, f, s, g, t = In()


#student divide - round 1:
student_list = [x+1 for x in range(N)]
divide = [[[],[]] for _ in range(K)]
for room in range(K):
  divide[room][0].append(student_list.pop(0))
  while len(divide[room][0])<a:
    queue = []
    for i in student_list:
      sumcal = 0
      for stud in divide[room][0]:
        sumcal += s[stud-1][i-1]
      queue.append((i,sumcal))
    queue.sort(key=lambda tup:tup[1],reverse=True)
    divide[room][0].append(queue[0][0])
    student_list.remove(queue[0][0])

#student divide - round 2:
while len(student_list)!=0:
  queue = []
  for room in range(K):
    sumcal = 0
    for stud in divide[room][0]:
      sumcal += s[stud-1][student_list[0]-1]
    queue.append((room,sumcal))
  queue.sort(key = lambda tup: tup[1],reverse = True)
  for tup in queue:
    if len(divide[tup[0]][0])==b:
      continue
    else:
      divide[tup[0]][0].append(student_list[0])
      break
  student_list.pop(0)

#prof divide - round 1:
prof_list = [x+1 for x in range(M)]
for room in range(K):
  while len(divide[room][1])<c:
    cand = []
    for prof in prof_list:
      sumcal = 0
      for stud in divide[room][0]:
        # sumcal += g[prof-1][stud-1] ori
        sumcal += g[stud - 1][prof - 1]
      cand.append((prof,sumcal))
    cand.sort(key=lambda tup:tup[1],reverse=True)
    divide[room][1].append(cand[0][0])
    prof_list.remove(cand[0][0])

#prof divide - round 2:
while len(prof_list)!=0:

  cand = []
  for room in range(K):
    sumcal = 0
    for stud in divide[room][0]:
      sumcal += g[prof_list[0] - 1][prof - 1]

      # sumcal += g[prof_list[0] - 1][stud - 1] ori
    cand.append((room,sumcal))
  cand.sort(key = lambda tup:tup[1],reverse = True)
  for tup in cand:
    if len(divide[tup[0]][1])==b:
      continue
    else:
      divide[tup[0]][1].append(prof_list[0])
      break
  prof_list.pop(0)


sum = 0
for room in range(K):
  for i in range(len(divide[room][0])-1):
    for j in range(i+1,len(divide[room][0])):
      sum+= s[divide[room][0][i]-1][divide[room][0][j]-1]
  for i in range(len(divide[room][0])):
    for j in range(len(divide[room][1])):
      # sum+= g[divide[room][1][j]-1][divide[room][0][i]-1] ori
      sum += g[divide[room][0][1] - 1][divide[room][1][j] - 1]


# for room in range(K):
#   print (f'committee: {room+1}')
#   for i in divide[room][0]:
#     print(f'\tstudent {i}')
#   print()
#   for i in divide[room][1]:
#     print(f'\tprofessor {i}')
# print(f'Total similarity = {sum}')
# end = time.time()
# print ('Time: ',end-start)


# committee: 1
# 	student 1
# 	student 6
#
# 	professor 4
# committee: 2
# 	student 2
# 	student 3
# 	student 4
# 	student 5
#
# 	professor 1
# 	professor 2
# 	professor 3
# Total similarity = 66
# [[[1, 6], [4]], [[2, 3, 4, 5], [1, 2, 3]]]

thesis_solution = [0 for i in range(N)]
pro_solution = [0 for i in range(M)]

for i in range(len(divide)):
  for j in range(2):
    for k in range(len(divide[i][j])):

      if j == 0:
        thesis_solution[divide[i][j][k]-1] = i+1
      else:
        pro_solution[divide[i][j][k]-1] = i+1

print(N)
print(*thesis_solution)
print(M)
print(*pro_solution)