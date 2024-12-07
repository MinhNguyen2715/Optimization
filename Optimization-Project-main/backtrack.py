import time
import sys

start = time.time()

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

N, M, K, a, b, c, d, e, f, s, g, t = input_data('data/HUSTack/data_6.txt')

project = [0 for i in range(N + 1)]
teacher = [0 for i in range(M+ 1)]
objective = 0
project_answer = []
teacher_answer = []


#check number of project in each council
def constraint1(N, M, K, a, b):
    for j in range(1, K + 1):
        sum = 0
        for i in range(1, N + 1):
            if project[i] == j:
                sum += 1
        if sum < a or sum > b:
            return False
    return True


#check number of teacher in each council
def constraint2(N, M, K, c, d):
    for j in range(1, K + 1):
        sum = 0
        for i in range(1, M + 1):
            if teacher[i] == j:
                sum += 1
        if sum < c or sum > d:
            return False
    return True


#project and its guide teacher is not in the same room
def constraint3(N, M, K):
    for i in range(1, N + 1):
        if project[i] == teacher[t[i]]:
            return False
    return True


#similarity between 2 arbitrary projects in the same room is more than or equal e
def constraint4(N, M, K, e):
    for i in range(1, N + 1):
        for j in range(i + 1, N + 1):
            if project[i] == project[j]:
                if s[i][j] < e:
                    return False
    return True


#similarity between 1 teacher and 1 project is more than or equal f
def constraint5(N, M, K, f):
    for i in range(1, N + 1):
        for j in range(1, M + 1):
            if project[i] == teacher[j]:
                if g[i][j] < f:
                    return False
    return True


def calvalue(N, M, K):
    value = 0
    for i in range(1, N):
        for k in range(i + 1, N + 1):
            if project[i] == project[k]:
                value += s[i][k]

    for i in range(1, M + 1):
        for j in range(1, N + 1):
            if project[j] == teacher[i]:
                value += g[j][i]

    return value


def Try1(k):
    global objective
    global N, M, K, a, b, c, d, e, f, count
    for i in range(1, K + 1):
        project[k] = i
        if k == N:
            Try2(1)
        else:
            Try1(k + 1)


def Try2(k):
    global objective
    global N, M, K, a, b, c, d, e, f, count
    global project_answer, teacher_answer
    for i in range(1, K + 1):
        teacher[k] = i
        if k == M:
            # print(constraint1(N,M,K,a,b) and constraint2(N,M,K,c,d) and constraint3(N,M,K) and constraint4(N,M,K,e) and constraint5(N,M,K,f))
            if (constraint1(N, M, K, a, b) and constraint2(N, M, K, c, d) and
                constraint3(N, M, K) and constraint4(N, M, K, e) and constraint5(N, M, K, f)):
                p = calvalue(N, M, K)
                if p > objective:
                    objective = p
                    project_answer = project[:]
                    teacher_answer = teacher[:]
        else:
            Try2(k + 1)


Try1(1)
end=time.time()
print(objective)
print(N)
thesis_solution = [None for i in range(N)]
pro_solution = [None for i in range(M)]

for i in range(1,N+1):
    thesis_solution[i-1] = project_answer[i]

for i in range(1,M+1):
    pro_solution[i-1] = teacher_answer[i]

print(*thesis_solution)
print(M)
print(*pro_solution)
print(end-start)
