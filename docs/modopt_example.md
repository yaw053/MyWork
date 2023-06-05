# A simple example (unconstrained)

## Define your problem

Let's start with a simple problem of minimizing $x_1^4 + x_2^4$ with respect to $x_1$ and $x_2$.

The mathematical problem statement is : 


$$
\underset{x_1, x_2 \in \mathbb{R}}{\text{minimize}} \quad x_1^4 + x_2^4
$$

We know the solution of this problem is $x_1=0$, and $x_2=0$.
However, we start from an intial guess of $x_1=0.3$, and $x_2=0.3$ for the purposes of this tutorial.

The problem is written in modOpt using the **Problem()** class as follows:


```py
import numpy as np
from modopt.api import Problem


class X4(Problem):
    def initialize(self, ):
        # Name your problem
        self.problem_name = 'x^4'

    def setup(self):
        # Add design variables of your problem
        self.add_design_variables('x',
                                  shape=(2, ),
                                  vals=np.array([.3, .3]))
        self.add_objective('f')

    def setup_derivatives(self):
        # Declare objective gradient and its shape
        self.declare_objective_gradient(wrt='x', )

    # Compute the value of the objective with given design variable values
    def compute_objective(self, dvs, obj):
        obj['f'] = np.sum(dvs['x']**4)

    def compute_objective_gradient(self, dvs, grad):
        grad['x'] = 4 * dvs['x']**3
```

## Develop/Build your optimization algorithm

Here we look at the **steepest descent** algorithm for unconstrained problems. 
We will later (in the next section) use it to solve the unconstrained  optimization problem defined above.

For a general unconstrained optimization problem stated as: 

$$
\underset{x \in \mathbb{R^n}}{\text{minimize}} \quad f(x)
$$

the steepest descent algorithms computes the new iterate recursively by using the formula

$$
x_{k+1} = x_{k} - \nabla f(x_k) .
$$

Given an initial guess $x_0$, we can write an optimizer using the steepest descent algorithm using the **Optimizer()** class in modOpt as follows:

```py
import numpy as np
import time
from modopt.api import Optimizer


class SteepestDescent(Optimizer):
    def initialize(self):

        # Name your algorithm
        self.solver_name = 'steepest_descent'

        self.obj = self.problem._compute_objective
        self.grad = self.problem._compute_objective_gradient

        self.options.declare('max_itr', default=1000, types=int)
        self.options.declare('opt_tol', default=1e-5, types=float)

        # Specify format of outputs available from your optimizer after each iteration
        self.default_outputs_format = {
            'itr': int,
            'obj': float,
            # for arrays from each iteration, shapes need to be declared
            'x': (float, (self.problem.nx, )),
            'opt': float,
            'time': float,
        }

        # Enable user to specify, as a list, which among the available outputs
        # need to be stored in memory and written to output files
        self.options.declare('outputs',
                             types=list,
                             default=['itr', 'obj', 'x', 'opt', 'time'])

    def solve(self):
        nx = self.problem.nx
        x = self.problem.x.get_data()
        opt_tol = self.options['opt_tol']
        max_itr = self.options['max_itr']

        obj = self.obj
        grad = self.grad

        start_time = time.time()

        # Setting intial values for initial iterates
        x_k = x * 1.
        f_k = obj(x_k)
        g_k = grad(x_k)

        # Iteration counter
        itr = 0

        # Optimality
        opt = np.linalg.norm(g_k)

        # Initializing outputs
        self.update_outputs(itr=0,
                            x=x_k,
                            obj=f_k,
                            opt=opt,
                            time=time.time() - start_time)

        while (opt > opt_tol and itr < max_itr):
            itr_start = time.time()
            itr += 1

            # ALGORITHM STARTS HERE
            # >>>>>>>>>>>>>>>>>>>>>

            p_k = -g_k

            x_k += p_k
            f_k = obj(x_k)
            g_k = grad(x_k)

            opt = np.linalg.norm(g_k)

            # <<<<<<<<<<<<<<<<<<<
            # ALGORITHM ENDS HERE

            # Append arrays inside outputs dict with new values from the current iteration
            self.update_outputs(itr=itr,
                                x=x_k,
                                obj=f_k,
                                opt=opt,
                                time=time.time() - start_time)

        # Run post-processing for the Optimizer() base class
        self.run_post_processing()

        end_time = time.time()
        self.total_time = end_time - start_time
```

The **Optimizer()** class records all the data needed using the `outputs` dictionary.

## Solve your problem using your optimizer

Now that we have modeled the problem and developed the optimizer, the task remaining is to solve the problem with the optimizer.
For this, we need to set up our optimizer with the problem and pass in optimizer-specific parameters. 
Default values will be assumed if the optimizer parameters are not passed in.

```py

# Set your optimality tolerance
opt_tol = 1E-8
# Set maximum optimizer iteration limit
max_itr = 100

prob = X4()

# Set up your optimizer with your problem and pass in optimizer parameters
# And declare outputs to be stored
optimizer = SteepestDescent(prob,
                            opt_tol=opt_tol,
                            max_itr=max_itr,
                            outputs=['itr', 'obj', 'x', 'opt', 'time'])

# Check first derivatives at the initial guess, if needed
optimizer.check_first_derivatives(prob.x.get_data())

# Solve your optimization problem
optimizer.solve()

# Print results of optimization (summary_table contains information from each iteration)
optimizer.print_results(summary_table=True)

# Print any output that was declared
# Since the arrays are long, here we only print the last entry and
# verify it with the print_results() above

print('\n')
print(optimizer.outputs['itr'][-1])
print(optimizer.outputs['x'][-1])
print(optimizer.outputs['time'][-1])
print(optimizer.outputs['obj'][-1])
print(optimizer.outputs['opt'][-1])

```