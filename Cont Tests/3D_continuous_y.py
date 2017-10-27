#!/usr/bin/env python
"""Controller synthesis for system with continuous (linear) dynamics.

This example is an extension of `robot_discrete.py`,
by including continuous dynamics with disturbances.
The dynamics is linear over a bounded set that is a polytope.
"""
# Petter Nilsson (pettni@kth.se)
# August 14, 2011
# NO, system and cont. prop definitions based on TuLiP 1.x
# 2 Jul, 2013
# NO, TuLiP 1.x discretization
# 17 Jul, 2013

# Note: This code is commented to allow components to be extracted into
# the tutorial that is part of the users manual.  Comments containing
# strings of the form @label@ are used for this purpose.

# @import_section@
import logging
import time

import numpy as np
from tulip import spec, synth, hybrid
from polytope import box2poly
from tulip.abstract import prop2part, discretize
from tulip.abstract.plot import plot_partition
# @import_section_end@


logging.basicConfig(level=logging.WARNING)
show = False

# @dynamics_section@
# Problem parameters
input_bound = 1.0
uncertainty = 0.0

# Continuous state space
cont_state_space = box2poly([[0., 3.], [0., 3.], [0., 3.]])

# Continuous dynamics - 3D
A = np.array([[1.0, 0., 0.], [ 0., 1.0, 0.], [0., 0., 1.0]])
B = np.array([[0.5, 0., 0.], [ 0., 0.5, 0.], [0., 0., 0.5]])
E = np.array([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.]])

# Available control, possible disturbances
U = input_bound *np.array([[-1., 1.], [-1., 1.], [-1., 1.]])
W = uncertainty *np.array([[-1., 1.], [-1., 1.], [-1., 1.]])

# Convert to polyhedral representation
U = box2poly(U)
W = box2poly(W)

# Construct the LTI system describing the dynamics
sys_dyn = hybrid.LtiSysDyn(A, B, E, None, U, W, cont_state_space)
# @dynamics_section_end@

# @partition_section@
# Define atomic propositions for relevant regions of state space
cont_props = {}
cont_props['home'] = box2poly([[0., 1.], [0., 1.], [0., 1.]]) #X0
cont_props['gl0'] = box2poly([[2., 3.], [2., 3.], [2., 3.]])
cont_props['ob0'] = box2poly([[1., 2.], [0., 1.], [0., 1.]]) #X1
cont_props['ob1'] = box2poly([[1., 2.], [1., 2.], [0., 1.]]) #
cont_props['ob2'] = box2poly([[1., 2.], [2., 3.], [0., 1.]])
cont_props['ob3'] = box2poly([[1., 2.], [0., 1.], [1., 2.]])
cont_props['ob4'] = box2poly([[1., 2.], [1., 2.], [1., 2.]])
cont_props['ob5'] = box2poly([[1., 2.], [2., 3.], [1., 2.]])
cont_props['ob6'] = box2poly([[1., 2.], [0., 1.], [2., 3.]])
cont_props['ob7'] = box2poly([[1., 2.], [1., 2.], [2., 3.]])
cont_props['ob8'] = box2poly([[1., 2.], [2., 3.], [2., 3.]])
#cont_props['obsX10'] = box2poly([[2., 3.], [4., 5.], [1., 2.]])
#cont_props['obsX11'] = box2poly([[2., 3.], [0., 1.], [2., 3.]])
#cont_props['obsX12'] = box2poly([[2., 3.], [1., 2.], [2., 3.]])
#cont_props['obsX13'] = box2poly([[2., 3.], [2., 3.], [2., 3.]])
#cont_props['obsX14'] = box2poly([[2., 3.], [3., 4.], [2., 3.]])
#cont_props['obsX15'] = box2poly([[2., 3.], [4., 5.], [2., 3.]])
#cont_props['obsX16'] = box2poly([[2., 3.], [0., 1.], [3., 4.]])
#cont_props['obsX17'] = box2poly([[2., 3.], [1., 2.], [3., 4.]])
#cont_props['obsX18'] = box2poly([[2., 3.], [2., 3.], [3., 4.]])
#cont_props['obsX19'] = box2poly([[2., 3.], [3., 4.], [3., 4.]])
#cont_props['obsX20'] = box2poly([[2., 3.], [4., 5.], [3., 4.]])
#cont_props['obsX21'] = box2poly([[2., 3.], [0., 1.], [4., 5.]])
#cont_props['obsX22'] = box2poly([[2., 3.], [1., 2.], [4., 5.]])
#cont_props['obsX23'] = box2poly([[2., 3.], [2., 3.], [4., 5.]])
#cont_props['obsX24'] = box2poly([[2., 3.], [3., 4.], [4., 5.]])
#cont_props['obsX25'] = box2poly([[2., 3.], [4., 5.], [4., 5.]])

# Compute the proposition preserving partition of the continuous state space
cont_partition = prop2part(cont_state_space, cont_props)
plot_partition(cont_partition) if show else None
# @partition_section_end@

# @discretize_section@
# Given dynamics & proposition-preserving partition, find feasible transitions
disc_dynamics = discretize(
    cont_partition, sys_dyn, closed_loop=True,
    N=8, min_cell_volume=1, plotit=show
)
# @discretize_section_end@

# Visualize transitions in continuous domain (optional)
plot_partition(disc_dynamics.ppp, disc_dynamics.ts,
               disc_dynamics.ppp2ts) if show else None

env_vars = {'obs_a':range(9),'obs_b':range(9)}
#,'obs_c': range(9),'obs_d': range(9),'obs_e': range(9)}
env_init = set()
env_prog = set()
env_safe = set()

sys_vars = set()
sys_init = {'home'}
sys_prog = {'gl0'}               # []<>home
sys_safe = {'((obs_a = 0|obs_b = 0) -> X (!ob0))',
            '((obs_a = 1|obs_b = 1) -> X (!ob1))',
            '((obs_a = 2|obs_b = 2) -> X (!ob2))',
            '((obs_a = 3|obs_b = 3) -> X (!ob3))',
            '((obs_a = 4|obs_b = 4) -> X (!ob4))',
            '((obs_a = 5|obs_b = 5) -> X (!ob5))',
            '((obs_a = 6|obs_b = 6) -> X (!ob6))',
            '((obs_a = 7|obs_b = 7) -> X (!ob7))',
            '((obs_a = 8|obs_b = 8) -> X (!ob8))',
}

# Create the specification
specs = spec.GRSpec(env_vars, sys_vars, env_init, sys_init,
                    env_safe, sys_safe, env_prog, sys_prog)
specs.qinit = '\E \A'

# @synthesize_section@
# Synthesize
start = time.time()
ctrl = synth.synthesize('omega', specs,
                        sys=disc_dynamics.ts, ignore_sys_init=True)
assert ctrl is not None, 'unrealizable'
print 'It took', time.time()-start, 'seconds.'
#print ctrl

#print disc_dynamics.ppp.regions[disc_dynamics.ppp2ts.index(0)]

#print disc_dynamics.ppp.regions[disc_dynamics.ppp2ts.index(8)]

print disc_dynamics.ppp.regions[disc_dynamics.ppp2ts.index(1)]

# print disc_dynamics.ppp.regions[disc_dynamics.ppp2ts.index(0)]
# Generate a graphical representation of the controller for viewing
# if not ctrl.save('continuous.png'):
#     print(ctrl)
# @synthesize_section_end@

# Simulation
import dumpsmach_mod1_1
dumpsmach_mod1_1.write_python_case("Cont_controller_3D_multiObs.py", ctrl,disc_dynamics, classname = "ExampleCtrl")
