import random as rd
import math
import time
start = time.time()
def input_data(filename):
    with open(filename) as text:
        [N, M, K] = [int(x) for x in text.readline().split()]
        [a, b, c, d, e, f] = [int(x) for x in text.readline().split()]
        s = [[0 for x in range(N + 1)]]
        for i in range(N):
            r = [int(x) for x in text.readline().split()]
            s.append([0] + r)
        g = [[0 for x in range(N + 1)]]
        for j in range(1, M + 1):
            r = [int(x) for x in text.readline().split()]
            g.append([0] + r) 
        t = [0] + [int(x) for x in text.readline().split()]
    return N, M, K, a, b, c, d, e, f, s, g, t 

N, M, K, a, b, c, d, e, f, s, g, t = input_data('data_size_80.txt')

class State():
    def __init__(self):
        self.project = [0 for i in range(N+1)]
        self.teacher = [0 for i in range(M+1)]
        self.penalty = 0
        self.value = 0
    
    def Copy_state(self):
        copy = State()
        copy.project = self.project[:]
        copy.teacher = self.teacher[:]
        return copy

    def initial_state(self):
        x = []
        for i in range(1,K+1):
            for j in range(a):
                x.append(i)
        #round 1
        while len(x) > 0:
            n = rd.choice(x)
            p = rd.randint(1,N)
            if self.project[p] == 0:
                self.project[p] = n
                x.remove(n)
        #round 2
        while self.check():
            can = rd.randint(1,K)
            if self.check_number(can) < b:
                self.project[self.check()] = can
        x = []
        for i in range(1,K+1):
            for j in range(c):
                x.append(i)
         #round 1
        while len(x) > 0:
            n = rd.choice(x)
            p = rd.randint(1,M)
            if self.teacher[p] == 0:
                self.teacher[p] = n
                x.remove(n)
        #round 2
        while self.check2():
            can = rd.randint(1,K)
            if self.check_number_2(can) < d:
                self.teacher[self.check2()] = can

        print(self.teacher)
    #check number of project
    def check_number(self,commitee):
        sum = 0
        for i in range(1,N+1):
            if self.project[i] == commitee:
                sum += 1
        return sum
    def check(self):
        for i in range(1,N+1):
            if self.project[i] == 0:
                return i
        return False
    
    def check_number_2(self,commitee):
        total = 0
        for i in range(1,M+1):
            if self.teacher[i] == commitee:
                total += 1
        return total
    def check2(self):
        for i in range(1,M+1):
            if self.teacher[i] == 0:
                return i
        return False
    #cal objective function
    def calvalue(self,N,M,K):
        sum = 0
        for i in range(1,N):
            for k in range(i+1,N+1):
                if self.project[i] == self.project[k]:
                    sum += s[i][k]
        
        for i in range(1,M+1):
            for j in range(1,N+1):
                if self.project[j] == self.teacher[i]:
                    sum += g[i][j]
        return sum
    
    def constraint3(self):
        sum = 0
        for i in range(1,N+1):
            if self.project[i] == self.teacher[t[i]]:
                sum += 1
        return sum
    #similarity between 2 arbitrary projects in the same room is more than or equal e
    def constraint4(self):
        sum = 0
        for i in range(1,N+1):
            for j in range(i+1,N+1):
                if self.project[i] == self.project[j]:
                    if s[i][j]<e:
                        sum += 1
        return sum
    
    #similarity between 1 teacher and 1 project is more than or equal f
    def constraint5(self):
        sum = 0
        for i in range(1,N+1):
            for j in range(1,M+1):
                if self.project[i] == self.teacher[j]:
                    if g[j][i]<f:
                        sum += 1
        return sum


    def cal_penalty(self):
        penalty = 0
        penalty += self.constraint3()+self.constraint4()+self.constraint5()
        return penalty

def Highest_Successor(state:State):
    new = state.Copy_state()
    total = -1000000000
    temp_prj = []
    temp_teacher = []
    print(new.project)
    for i in range(1,N):
        for j in range(i+1,N+1):
            new.project[i],new.project[j] =  new.project[j],new.project[i]
            p = new.calvalue(N,M,K)
            if p > total:
                total = p
                # print(p)
                temp_prj = new.project[:]
                temp_teacher = new.teacher[:]
            new.project[i],new.project[j] =  new.project[j],new.project[i]
    new.project = temp_prj
    new.teacher = temp_teacher
    return new

def HillClimbing():
    current = State()
    current.initial_state()
    while True:
        neighbor = Highest_Successor(current)
        if neighbor.calvalue(N,M,K) <= current.calvalue(N,M,K) or neighbor.cal_penalty() > current.cal_penalty():
            return current
        current = neighbor
        print(neighbor.cal_penalty())

solution = HillClimbing()
print(solution.calvalue(N,M,K))
end = time.time()
print(end-start)
