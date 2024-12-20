import random as rd
import sys
import math
import time


# start = time.time()

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


class State():
    def __init__(self):
        self.thesis = [0 for i in range(0, N + 1)]
        self.professor = [0 for i in range(0, M + 1)]
        self.penalty = 0
        self.value = 0

    def Copy_state(self):
        copy = State()
        copy.thesis = self.thesis[:]
        copy.professor = self.professor[:]
        return copy

    def initial_state(self):
        x = []
        for i in range(1, K + 1):
            for j in range(a):
                x.append(i)

        # round 1
        while len(x) > 0:
            n = rd.choice(x)
            p = rd.randint(1, N)
            if self.thesis[p] == 0:
                self.thesis[p] = n
                x.remove(n)

        # round 2
        while self.check():
            can = rd.randint(1, K)
            if self.check_number(can) < b:
                self.thesis[self.check()] = can

        x = []
        for i in range(1, K + 1):
            for j in range(c):
                x.append(i)

        # round 1
        while len(x) > 0:
            n = rd.choice(x)
            p = rd.randint(1, M)
            if self.professor[p] == 0:
                self.professor[p] = n
                x.remove(n)
        # round 2
        while self.check2():
            can = rd.randint(1, K)
            if self.check_number_2(can) < d:
                self.professor[self.check2()] = can

    def printf(self):
        print("\n%d" % (len(self.professor) - 1))
        for y in self.professor:
            if (y):
                print(y, end=' ')

    # check number of project
    def check_number(self, commitee):
        sum = 0
        for i in range(1, N + 1):
            if self.thesis[i] == commitee:
                sum += 1
        return sum

    def check(self):
        for i in range(1, N + 1):
            if self.thesis[i] == 0:
                return i
        return False

    def check_number_2(self, commitee):
        total = 0
        for i in range(1, M + 1):
            if self.professor[i] == commitee:
                total += 1
        return total

    def check2(self):
        for i in range(1, M + 1):
            if self.professor[i] == 0:
                return i
        return False

    # cal objective function
    def calvalue(self, N, M, K):
        sum = 0
        for i in range(1, N + 1):
            for k in range(i + 1, N):
                if self.thesis[i] == self.thesis[k]:
                    sum += s[i][k]

        for i in range(0, N):
            for j in range(0, M):
                if self.thesis[i] == self.professor[j]:
                    sum += g[i][j]
        return sum

    def constraint3(self):
        sum = 0
        for i in range(1, N + 1):
            if self.thesis[i] == self.professor[t[i]]:
                sum += 1
        return sum

    # similarity between 2 arbitrary projects in the same room is more than or equal e
    def constraint4(self):
        sum = 0
        for i in range(1, N + 1):
            for j in range(i + 1, N + 1):
                if self.thesis[i] == self.professor[j]:
                    if s[i][j] < e:
                        sum += 1
        return sum

    # similarity between 1 teacher and 1 project is more than or equal f
    def constraint5(self):
        sum = 0
        for i in range(1, N + 1):
            for j in range(1, M + 1):
                if self.thesis[i] == self.professor[j]:
                    if g[i][j] < f:
                        sum += 1
        return sum

    def cal_penalty(self):
        penalty = 0
        penalty += self.constraint3() + self.constraint4() + self.constraint5()
        return penalty


def Highest_Successor(state: State):
    new = state.Copy_state()
    print((len(new.thesis) - 1))
    for x in new.thesis:
        if (x):
            print(x, end=' ')
    total = -1000000000
    temp_thesis = []
    temp_profes = []

    for i in range(1, N + 1):
        for j in range(i + 1, N + 1):
            new.thesis[i], new.thesis[j] = new.thesis[j], new.thesis[i]
            p = new.calvalue(N, M, K)
            if p > total:
                total = p
                temp_thesis = new.thesis[:]
                temp_profes = new.professor[:]
            new.thesis[i], new.thesis[j] = new.thesis[j], new.thesis[i]
    new.project = temp_thesis
    new.teacher = temp_profes
    return new


def HillClimbing():
    current = State()
    current.initial_state()
    while True:
        neighbor = Highest_Successor(current)
        neighbor.printf()

        if neighbor.calvalue(N, M, K) <= current.calvalue(N, M, K) or neighbor.cal_penalty() > current.cal_penalty():
            return current
        current = neighbor
        # print(neighbor.cal_penalty())


solution = HillClimbing()
# print(solution.calvalue(N,M,K))
# end = time.time()
# print(end-start)