# sympy-spring-double-pendulum
This repository hosts a report where we investigate a
spring double pendulum using `sympy` for symbolic computation.
Taking the limits as spring constants go to infinity as well as setting
spring constants to zero is used to reduce the spring double pendulum
system to a regular double pendulum and single pendulum system
respectively, and these special cases are compared to the known theory to
ensure that the spring double pendulum model is behaving correctly.
Then, the chaotic behvaiour of the spring double pendulum system is
investigated by showing that the phase separation of the system
is exponential with time, and calculating the Lyapunov exponent of the system with certain
initial conditions and veriyfing that it is positive, indicating chaos.

The report is written up as a Jupyter notebook, which is titled
`springs.ipynb`. Some of the calculations in the notebook take a long time
to do, and as such I have stored the results of these calculations in files
in the `data` directory, and used boolean flags in the notebook to ensure
that these calculations only rerun if you set these flags to `True`, where
they are `False` by default.

## modules used
* `sympy`
* `numpy`
* `scipy`
* `matplotlib`
* `dill`
* `IPython`
* `time`
* `functools`

