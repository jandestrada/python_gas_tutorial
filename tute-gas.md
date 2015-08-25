Using VPython to Simulate a Gas
===============================

**Sally Lloyd and Stephen Roberts**

This tutorial follows on from the [bouncing ball
tutorial](tute-bounce.html) which introduces VPython as a computational
environment and develops a program to simulate a ball bouncing in a box.
You should start with the previous tutorial before starting on this
tutorial as this tutorial is based on the solution obtained from the
previous tutorial.

A clean version of the bouncing ball program can be obtained from the
link below. [Example bouncing ball program](bounce2.py)

Start IDLE by clicking on the snake icon on the panel at the bottom of
your desktop. A window labelled ’Untitled’ should appear. This is the
window in which you will type your program. Open your bouncing ball
program, or cut and paste the [clean version with 6 walls](bounce2.py)
into VIDLE. Check to see if it is working. You see a ball bouncing in a
box.

Simulating particle motion in a gas
-----------------------------------

Now you will extend the bouncing ball program so that it simulates the
motion of atoms in a gas. There will need to be many atoms in the box
and they should bounce off each other as well as off the sides of the
box. We will need to set the initial distribution of atom positions and
velocities, but these distributions may evolve as the simulation
progresses. The velocity distribution of the atoms in the simulation
will be compared with the expected Maxwellian velocity distribution.

Random numbers
--------------

You can make the velocity of the ball different each time the program is
run by using a random number generator. The random number generator is
not part of standard python and needs to be imported from the random
module. The random module contains random number generator for several
different distributions. You can import just a uniform distribution
random number generator by inserting the line

    from random import uniform

at the beginning of the program; in the "Import Library(s)" section of
the code.

The function `uniform(-1,1)` will give a random number
between -1 and 1. You can set a random ball velocity by replacing the
line setting the ball’s velocity with:

    ball.velocity=maxv*vector(uniform(-1,1),uniform(-1,1),uniform(-1,1))

Multiple balls: Using lists
---------------------------

To simulate a gas we will need many particles inside the box. One easy
way of dealing with many particles is to put them into a list.

Replace the "Create Ball(s)'' section of code with the following code (it
should be instead of the code defining the ball and its velocity):

    ##########################################
    # Create Ball(s)
    ##########################################
    no_particles=10
    ball_radius=0.4
    maxpos=side-.5*thk-ball_radius
    maxv=1.0

    ball_list=[]
    for i in range(no_particles):
        ball=sphere(color=color.green,radius=ball_radius)
        ball.pos=maxpos*vector(uniform(-1,1),uniform(-1,1),uniform(-1,1))
        ball.velocity=maxv*vector(uniform(-1,1),uniform(-1,1),uniform(-1,1))
        ball_list.append(ball)


The construction of a `for` loop in python is slightly
different from many other programming languages which cycle through a
set of numbers. Python iterates through a list. To get the more usual
counted for loop you use `range` to create a list of integers
between 0 and `no_particles-1`.

This gives a list called `ball_list` containing 10 balls.
Any type of object can go into a list. In fact a list can be made up of
several different types of object. If you run the code now you will see
10 balls within the box but the “Time Loop” section of code only moves
one of the balls (the last one created in the `for` loop,
which is called `ball`).

To move all the balls in a list you use another `for` loop.
In python a `for` loop cycles through the elements of a list.
We need to loop through all the balls in the list `balls`.
The loop to move all the balls in the list would look like:

    while (1==1):
        # Set number of times loop is repeated per second
        rate(100)

        ######################################
        # Loop over list of particles
        # Move and check wall collisions
        ######################################
        for ball in ball_list:

            # Move ball(s)
            ball.pos = ball.pos + ball.velocity*timestep

            #check for collisions with the walls
                                       . . .

Here you **only** have to add in the following code and get the
indentation right.

    ######################################
    # Loop over list of particles
    # Move and check wall collisions
    ######################################
    for ball in ball_list:


The code within the for loop is indented by two levels since it is also
inside the while loop (with code inside the if indented an additional
level). You can indent a whole section by selecting it and then choosing
"indent section" from the format menu. (Try running the program now to
see 10 balls bouncing within your box)


Maybe you would like to play with increasing the number of balls, or
changing the radii of the balls, or the colours or what ever.

Particle interactions
---------------------

You should now have a program that shows many particles bouncing around
inside a box. At the moment the balls are simply passing through each
other. For this to be a realistic model of a gas, the particles need to
interact in some fashion.

Different "interaction potentials" could be used depending on the type
of molecule making up the gas. For an ideal gas an appropriate
interaction is "hard sphere collisions" — the balls bounce off each
other the same way they bounce off the walls.

### Detecting a collision

At each time step we need to check whether any particles have collided.
For each pair of particles we need to check whether the distance between
them is less than the sum of their radii. For example add the following
lines to the end of your program, after you have updated the position of
all the particles. The indentation should place it within the time
`while` loop but outside the wall collision `for` loop.

        ######################################
        # Ball Collision Detection
        ######################################
        for ball in ball_list:
            for otherball in ball_list:
                if not ball == otherball:
                    distance=mag(otherball.pos-ball.pos)
                    if distance<(ball.radius+otherball.radius):
                        print 'collision' , distance

`mag` is a function that returns the size (magnitude) of a
vector.

Run your program. Notice that every time a pair of balls collide in the
display window the word ’collision’ is printed twice to the output
window. This is because the loop goes through every pair of balls twice.
To check each pair only once the second loop should only check against
balls with higher index than the first. To do this replace the ball
collision detection code with:

        ######################################
        # Ball Collision Detection
        ######################################
        for i in range(no_particles):
            for j in range(i+1,no_particles):
                distance=mag(ball_list[i].pos-ball_list[j].pos)
                if distance<(ball_list[i].radius+ball_list[j].radius):
                    print 'collision', distance

Now when you run the program, "collision" should be written once for
each collision.

### Exchanging momentum: more vector calculations

When two objects collide elastically (without losing energy) in one
dimension they swap momentum. If their masses are equal this means they
should swap velocity. Since we are modelling the interaction between
particles as hard spheres, with no friction, the force at impact is only
along the line joining the centres of the balls. The balls exchange
momentum in this direction, leaving the perpendicular velocity
components unchanged. The result is similar to the way billiard balls
collide. The section of code that detects a collision and swaps the
velocity component of the two balls in the collision direction looks
like:

        ######################################
        # Ball Collision Detection
        ######################################
        #loop through all pairs
        for i in range(no_particles):
            for j in range(i+1,no_particles):
                distance=mag(ball_list[i].pos-ball_list[j].pos)
                #check collision
                if distance<(ball_list[i].radius+ball_list[j].radius):
                    #unit vector in collision direction
                    direction=norm(ball_list[j].pos-ball_list[i].pos)
                    vi=dot(ball_list[i].velocity,direction)
                    vj=dot(ball_list[j].velocity,direction)
                    #impact velocity
                    exchange=vj-vi
                    #exchange momentum
                    ball_list[i].velocity=ball_list[i].velocity + exchange*direction
                    ball_list[j].velocity=ball_list[j].velocity - exchange*direction


The function `norm` returns a vector with the same direction
as the input but with its magnitude normalised to one. The function
`dot` returns the dot product of the two input vectors, in
this case the component of the ball’s velocity that is in the collision
direction.

You should now have a program that shows ten spheres bouncing around
inside a box and bouncing off each other. You might find that balls get
stuck together, particularly if three or more balls collide at the same
time. This problem is reduced by making the time step smaller. We can
also make the collisions more accurate, and stop balls sticking
together, by adjusting the position of the balls after a collision, in
much the same way we did for collisions with the sides of the box.

------------------------------------------------------------------------

                    #adjust position
                    overlap=2*ball_radius-distance
                    ball_list[i].pos=ball_list[i].pos - overlap*direction
                    ball_list[j].pos=ball_list[j].pos + overlap*direction

------------------------------------------------------------------------

[Example solution](manybounce1.py)

Program speed
-------------

The program you have written shows a simple model of the behaviour of
particles within a gas. Play around with changing the number and size of
particles and their average velocities. As you add more particles the
speed of the program slows down significantly. Doubling the number of
particles increases the time to run the program by about four times.
This is because the number of steps to check for collisions increases as
the square of the number of particles. Many computational science models
which are based on interacting particles have this $N^2$ speed
dependence. Models with large numbers of particles need high speed
computers and efficient programs.

Increasing the speed of a simulation program can make up a large part of
the work of a computational scientist. Tactics for improving the
efficiency of a program include:

-   removing unnecessary calculations (eg the calculation of the
    distance between particles involves calculating a square root which
    is quite slow. The comparison of particle separation for detecting
    collisions could be made just as easily with the square of the
    distance which is much quicker to calculate.)

-   Saving results of calculations instead of repeating them.

-   Using more efficient data constructions (eg the elements of
    lists in python are not necessarily all the same data type. This
    makes them flexible for many different programming tasks but the
    program takes longer to access this data. Python arrays have each
    element the same data type and are faster to work with.)

-   Improved mathematical algorithms which allow larger step sizes
    for the same accuracy.

-   Minimise the number of particles needed by the model

-   Include only the most important interactions.

[Here](quickbounce1.py) is a faster version of the ideal gas
simulation program.

Extracting useful information
-----------------------------

The visualisation of a model can be useful in itself to get insight into
its behaviour. But the program might be more useful as a computational
science ’experiment’ if we could extract from it predictions of gas
behaviour that could be measured in a physical experiment or were
relevant in some real world application. Alternatively we could use the
results to confirm some theory about ideal gasses.

To do either of these we need to extract the sort of information that
can normally be measured since you don’t get to watch the particles of a
real gas bouncing around.

Examples of some measurements we could extract from our simulation:

-   measure how the pressure on the walls varies with gas
    temperature and density

-   distribution of particle velocities

-   collision frequency

Velocity distribution: using graphs
===================================

We gave our particles a uniform initial velocity distribution for each
direction. A statistical analysis suggests that the "most likely"
velocity distribution for each component will have more low energy
particles and a long tail of high energy particles. Does our gas evolve
to this "most likely" velocity distribution.

Graphing in visual python
-------------------------

We will need the graphing functions contained in the visual.graph
module, so insert a line at the beginning of your program

    from visual.graph import *

Several types of graph are available. We will use a histogram that
displays how many particles fit into each velocity range. This graph is
set up before the main time while loop with:

    graphwindow=gdisplay(xtitle='v_x',ytitle='N',ymax=no_particles/2)
    
    velocity_dist=ghistogram(bins=arange(0,2*maxv,maxv/5))

`velocity_dist` defines a histogram with a set of ten
velocity "bins" into which the list of particle velocities will be
sorted. You might want to adjust the number of bins depending on the
number of particles in your gas. The graph will be displayed in a new
graphing window.

To plot the distribution of particle speeds in the x direction you would
form a list and use this list as data for the histogram

        v_list=[]
        for ball in ball_list:
            v_list.append(abs(ball.velocity.x))
        velocity_dist.plot(data=v_list)

You can put these lines within the while loop and see the velocity
distribution evolve. Unless you have many particles in your gas the
velocity distribution will jump around a lot.

You can reduce this problem by averaging the distribution over time.
Change the code which defines `velocity_dist` using:

    velocity_dist=ghistogram(bins=arange(0,2*maxv,maxv/5),accumulate=1,average=1)

(You may find that displaying the graph slows down the simulation
considerably. If this is a problem, turn your while loop into a for loop
so that it runs for a limited time and put all the graphing parts of the
program after the loop finishes.)

If you are using the quick version of the code the velocity is stored as
in `p_array`, which can be fed directly to the histogram as:

         velocity_dist.plot(data=abs(p_array[:,0]))

Compare with expected result
----------------------------

The expected "most likely" velocity distribution can be plotted for
comparison as a curve set up with:

    expected_distribution=gcurve(color=color.green)
    for vx in arange(0,2*maxv,maxv/20):
           expected_distribution.plot(pos = (vx,.27*no_particles*exp(-vx**2/maxv**2*3/2)))

(plot only once - so just before while loop. You may need to rescale
this graph if you used a different number of velocity bins)

[Here](quickbouncepdist.py) is an example of graphing with the quick
program.

[Here](manybouncepdist.py) is an example of graphing with the slower
program.

Some questions that you could use this program to investigate:

-   Is the initial velocity distribution different from the final
    velocity distribution?

-   Does the final velocity distribution match the expected
    result?

-   Does changing the initial velocity distribution effect the
    final distribution?

-   Consider the ways this simulation is different from a real
    gas. What changes might you need to make to model a real gas more
    closely? How might this effect the behaviour of the
    simulation?

More complicated simulations
============================

You could extend this simulation to investigate more complex situations.

-   Mixing of two ideal gasses (diffusion)(eg look at
    [quicktwogas](quicktwogas.py))

-   Heat conduction

-   Other interaction potentials including some attraction may
    give phase change to solid or liquid phases

-   Include effects of earth’s gravity to get height variations in
    pressure and temperature - or better simulation of liquid/gas
    interface

-   Velocity distribution when a gas includes molecules of
    different masses

-   Movable or elastic walls (eg look at
    [quickbounce2](quickbounce2.html))

Other situations that can be modelled using similar techniques
==============================================================

The technique of following individual particles, calculating their
accelerations due to their position and the position of other particles
around them can be used to simulate a wide variety of situations.

-   Molecular dynamics and computational chemistry can determine
    the shape of molecules, their resonant frequencies and their
    potential reactions. The most difficult part is to determine the
    interaction potentials which can depend on relative positions of
    more than two particles, and also on angles between them.

-   Gravitational interactions determine the orbits of planets in
    the solar system. Precise calculations of these orbits determine
    whether the solar system is stable or chaotic, whether orbits may
    change drastically at some future time, give clues as to how the
    solar system form, and whether any asteroid is likely to hit the
    earth. With large objects like planets their shape and rotation may
    need to be taken into account.

-   Animal behaviour. Animals use the positions of other animals
    and objects around them to decide how they should move in order to
    achieve their goals. The goals might include getting food, fleeing
    predators, staying in a group and avoiding collisions. This
    simulations apply to people and traffic flow and can be used to
    design adequate escape routes from burning buildings and sinking
    ships, road systems that minimise congestions, or to suggest driving
    techniques that avoid collisions.


