# PYTHON
import sys
import random

def Inp():
    [N, M, K] = [int(i) for i in sys.stdin.readline().split()]
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


N, M, K, a, b, c, d, e, f, s, g, t = Inp()

res = []
for _ in range(20):
    while True:
        # student divide - round 1:
        student_list = random.sample(range(1, N + 1), N)
        commitee = [[[], []] for _ in range(K)]

        for room in range(K):
            commitee[room][0].append(student_list.pop(0))
            while len(commitee[room][0]) < a:  # add a students to all commitee
                queue = []
                for i in student_list:
                    sumcal = 0
                    for stud in commitee[room][0]:
                        sumcal += s[stud - 1][i - 1]
                    queue.append((i, sumcal))
                queue.sort(key=lambda tup: tup[1], reverse=True)
                commitee[room][0].append(queue[0][0])
                student_list.remove(queue[0][0])

        # student divide - round 2:
        while len(student_list) != 0:
            queue = []
            for room in range(K):
                sumcal = 0
                for stud in commitee[room][0]:
                    sumcal += s[stud - 1][student_list[0] - 1]
                queue.append((room, sumcal))
            queue.sort(key=lambda tup: tup[1], reverse=True)
            for tup in queue:
                if len(commitee[tup[0]][0]) == b:
                    continue
                else:
                    commitee[tup[0]][0].append(student_list[0])
                    break
            student_list.pop(0)

        # prof divide - round 1:
        prof_list = random.sample(range(1, M + 1), M)
        # prof_list = [y for y in range(1,M+1)]
        for room in range(K):
            while len(commitee[room][1]) < c:
                cand = []
                for prof in prof_list:
                    sumcal = 0
                    for stud in commitee[room][0]:
                        if (prof != t[stud - 1]):
                            sumcal += g[stud - 1][prof - 1]
                        else:
                            break
                    cand.append((prof, sumcal))
                cand.sort(key=lambda tup: tup[1], reverse=True)
                commitee[room][1].append(cand[0][0])
                prof_list.remove(cand[0][0])

        # prof divide - round 2:
        while len(prof_list) != 0:
            cand = []
            for room in range(K):
                sumcal = 0
                for stud in commitee[room][0]:
                    if (prof_list[0] != t[stud - 1]):
                        sumcal += g[stud - 1][prof_list[0] - 1]
                    else:
                        break
                cand.append((room, sumcal))
            cand.sort(key=lambda tup: tup[1], reverse=True)
            for tup in cand:
                if len(commitee[tup[0]][1]) == d:
                    continue
                else:
                    commitee[tup[0]][1].append(prof_list[0])
                    break
            prof_list.pop(0)

        # print(commitee)
        satisfied = True
        x = [0 for i in range(N)]
        y = [0 for i in range(M)]
        for i in range(K):
            for j in range(len(commitee[i][0])):
                if t[commitee[i][0][j] - 1] in commitee[i][1]:
                    satisfied = False
                    break

            for j in range(2):
                for k in range(len(commitee[i][j])):
                    if j == 0:
                        x[commitee[i][j][k] - 1] = i + 1
                    else:
                        y[commitee[i][j][k] - 1] = i + 1

        # print(satisfied)
        if satisfied == True:
            res.append([x, y])
            break

def max_similar(res, N, M):
    compare = []
    for i in range(len(res)):
        thesis_val = 0
        prof_val = 0
        tmp = res[i]
        for j in range(N - 1):
            for k in range(j + 1, N):
                if tmp[0][j] == tmp[0][k]:
                    thesis_val += s[j][k]

        for j in range(N):
            for k in range(M):
                if tmp[0][j] == tmp[1][k]:
                    prof_val += g[j][k]

        compare.append(thesis_val + prof_val)

    return res[compare.index(max(compare))]


[x, y] = max_similar(res, N, M)

print(N)
print(*x)
print(M)
print(*y)
