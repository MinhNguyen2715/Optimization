# Optimization Problem: Thesis Defense Jury Assignment
In our problem, we need to divide N theses and M professors into K committees.
* The instructor for each thesis i is called t(i)
* The similarity between 2 theses is called s(i, j)
* The similarity between thesis and professor is called g(i, j)


## The constraints of this problem are:
* The number of theses in each committee must be greater than or equal to a and less than or equal to b.
* The number of professors in each committee must be greater than or equal to c and less than or equal to d.
* Professors are not allowed to sit on the committee of their own theses.
The similarity between the theses in the same committee must be greater than or equal to e
* The similarity between the theses and the professors in the committee must be greater than or equal to f

Our object is to divide professors into committees such that __the total similarity between theses and between theses and professors in a committee must be the greatest.__

## Methods 
### Exact methods
1. Brute Force 
2. Constraint Programming 
3. Integer Programming 

### Heuristic Method
1. Greedy Algorithm 
2. Local search: Hill Climbing 

### Meta-heuristic Method
1. Iterated Local Search


## Conclusion
1. **Exact method and Heuristic methods:**
    * Exact methods: always gives the optimal values; with large data size, run times is high
and sometimes cannot run.
    * Heuristic methods: release the feasible solutions with lower run times compare. They can reach the optimal value with some small sample data.
    
2. **Among exact methods:**
    * Small size (N <= 25), Integer and Constraint Programming return optimal solution with reasonable computation costs (< 1 s).
    * Brute Force is the worst methods since it has the highest run time, can only run with small size.
3. **Among heuristic methods:**
    * Greedy algorithm and Iterated local search give the nearest value to the global optima.
    * With the Iterated local search, the result seems to be more accurate but longer run time
than the others and still don’t satisfy all the constraints.
    * Greedy method run time is more reasonable when the data size grows larger.
