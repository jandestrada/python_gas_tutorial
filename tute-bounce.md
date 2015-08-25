Using VPython to Simulate a Ball Bouncing in a Box
==================================================

**Sally Lloyd and Stephen Roberts**

Overview
--------

This tutorial will take you through a "toy" problem in computational
science. You will develop a computer program that simulates the motion
of a ball in a box . This program will be written in visual python – a
language designed to make the development of this type of physical
simulation simple.

What is Computational Science?
------------------------------

Computational science involves using mathematical models and computer
programs to improve our understanding of the way the world works. There
are three parts to the process:

-   Find a complete mathematical description of the system that
    will include all the behaviour you are interested in.

-   Construct an efficient computer code that solves these
    equations 

-   Extract results and predictions that can be compared with real
    world, with experiments or with other scientific theories. 

These steps are repeated to refine both the computer program and our
understanding of the problem.

What is VPython?
----------------

VPython is a programming language that is easy to learn and is well
suited to creating simple 3D models and visualisations of physical
systems. VPython has three components that you will deal with directly:

-   [Python](http://www.python.org), a programming language
    invented in 1990 by Guido van Rossem, a Dutch computer scientist.
    Python is a modern, object-oriented language which is easy to
    learn.

-   [VPython](http://www.vpython.org), a 3D graphics module for
    Python created by David Scherer while he was a student at Carnegie
    Mellon University. VPython allows you to create and animate 3D
    objects, and to navigate around in a 3D scene by spinning and
    zooming, using the mouse.

-   IDLE, an interactive editing environment, written by van
    Rossem and modified by Scherer, which allows you to enter computer
    code, try your program, and get information about your program.
    

This tutorial starts with a cut down version of the ’standard’ VPython
tutorial. The tutorial assumes that Python and Visual are installed on
the computer you are using. If you need to install any of these, follow
this link to the [VPython web page](http://www.vpython.org/)

Introduction to Visual python: Simple motion
============================================

The first section of the tutorial introduces you to programming in
visual python by stepping through a program to display a ball bouncing
around inside a box. In the next tutorial this program will be modified
to become a simulation of an ideal gas.

Your First Program
------------------

Start VPython or VIDLE (an editor for creating Python computer code).

If you are using a windows machine this will probably be possible via
the start menu.

If you are working on a Unix (Linux) computer, then type “vpython” at a
prompt on a shell window. This will bring up an interactive Python
window. You then need to select New Window from the File menu of this
first Python window.

Vpython will demand that you save a copy of your working file somewhere
before it will execute the program. Save it in your present working
directory which will probably be /student/\<username\>

A window labelled ’Untitled’ should appear. This is the window in which
you will type your program. Type the following statements (You can
select the text below and then paste it into IDLE.):

    #########################################
    # Import the visual library
    #########################################
    from visual import *

    ##########################################
    # Create Wall(s)
    ##########################################
    wallR = box(pos=vector(6,0,0), length=0.2, height=4, width=4, color = color.red)

    ##########################################
    # Create Ball(s)
    ##########################################
    ball = sphere(pos=vector(-5,0,0), radius=1.0, color=color.green)

IDLE will colour different sections of the program to make it easier to
read. For example comment lines, which begin with the # symbol are red.
The functions sphere and box are
’constructors’ for 3D objects. The position of an object’s centre is
specified in three dimensions using a vector.

Of course there are only 3 lines of actual code. I have added the
comments for two reason,

1.  to tell you what the code does,

2.  to designate regions of your code, so that as the code grows it will
    be easier to describe where to act new features.

Running the Program
-------------------

Now run your program by choosing "Run program" from the "Run" menu. When
you run the program, two new windows appear. There is a window titled
"VPython," in which you should see a green sphere and a red rectangle
(wall), and another window titled "Output".

In the VPython window, hold down the middle mouse button and move the
mouse. You should see that you are able to zoom into and out of the
scene. Now try holding down the right mouse button . You should find
that you are able to rotate your view of the scene.

You can stop the program by choosing "Stop program" from the run menu
(or closing the graphics window).

You might want to play with changing the radius of the ball, the colour
of the ball etc. Make the changes in the code and run the updated
program using run command.

Objects and attributes
----------------------

Sphere and box are types of objects that visual python recognises and
displays. They have some attributes associated with them (such as
position(pos), colour(color) and
radius) which can be set when you first define and name the
object, otherwise the default values will be used.

You can change the radius attribute of ball after it has
been constructed with the statement:

    ball.radius=0.4

You can also add any new attributes you want to associate with the
object, eg:

    ball.velocity=vector(2,.1,0)

Moving Objects
--------------

To move objects you will need a program loop that repeatedly updates the
position. This can be done with a while loop that repeats the indented
lines of code following the while statement, as long as the while
condition remains true.

Add the following assignments and while loop to the bottom of your
program. The setting of the ball velocity should be part of the "Create
Ball(s)" part of the code. The ball should be able to move according to
the velocity specified.

    ball.velocity=vector(2,.1,0)

    ##########################################
    # Time loop for moving Ball(s)
    ###########################################
    timestep=0.05

    while (1==1):
        # Set number of times loop is repeated per second
        rate(100)

        # Move ball(s)
        ball.pos=ball.pos + ball.velocity*timestep

The symbol `=` is used for assignment, to set a new value for
a variable. In Python `==` stands for "is equal to" so the
statement `1==1` always has a value of true, and code inside
the while loop will repeat forever. Loops are a little strange in
Python. Most other languages use some code for the end of a loop, say a
bracket or endwhile. Not in Python, the indentation defines
the extent of the loop. So you are forced into writing indented code.
Other control commands like `for` and `if` also
work using indentation.

In the above example the value of `ball.pos +
ball.velocity*timestep` is calculated and then assigned as the
new value for ball.pos. Python knows how to add vectors and
how to multiply them by a scalar so you don’t have to specify this
element by element.

The rate statement specifies the number of times the loop will be
executed per second. It allows you to control the animation speed so
that the ball doesn’t move too fast on fast computers.

Run your program by choosing "Run program" from the "Run" menu. You
should observe that the ball moves to the right. You can change how fast
either by changing the rate or the timestep.

Note that VPython tries to scale the view so that all the objects can be
seen. So as the ball moves to the right, the camera has to pan back.
This makes the wall look like it is moving backwards.

Making the ball bounce: Logical tests
-------------------------------------

The ball goes straight through the wall. To make the ball bounce off the
wall, we need to detect a collision between the ball and the wall. A
simple approach is to compare the x coordinate of the ball to the x
coordinate of the wall, and reverse the x component of the ball’s
velocity if the ball has moved too far to the right. The components of
vectors are attributes which can be referred to individually as .x, .y
and .z. The logical test we would use to detect a collision and reverse
the velocity might look like:

        #check for collisions with the wall(s)
        #right wall
        if ball.x > wallR.x:
            ball.velocity.x = -ball.velocity.x

The indented line after the if statement will be executed only if the
logical test in the previous line gives "true" for the comparison. If
the result of the logical test is false (that is, if the x coordinate of
the ball is not greater than the x coordinate of the wall), the indented
line will be skipped. Since we want this logical test to be performed
every time the ball is moved, we need put these lines in the while loop.
We add these lines to the end of the code and indent them both so they
become part of the while loop. Your program should now look like this:

    #########################################
    # Import the visual library
    #########################################
    from visual import *

    ##########################################
    # Create Wall(s)
    ##########################################
    wallR = box(pos=vector(6,0,0), length=0.2, height=4, width=4, color=color.red)

    ##########################################
    # Create Ball(s)
    ##########################################
    ball = sphere(pos=vector(-5,0,0), radius=1.0, color=color.green)
    ball.velocity=vector(2,.1,0)

    ##########################################
    # Time loop for moving Ball(s)
    ###########################################
    timestep=0.05

    while (1==1):
        # Set number of times loop is repeated per second
        rate(100)

        # Move ball(s)
        ball.pos=ball.pos + ball.velocity*timestep

        #check for collisions with the wall(s)
        #right wall
        if ball.x > wallR.x:
            ball.velocity.x = -ball.velocity.x

Run your program. You should observe that the ball moves to the right,
bounces off the wall, and then moves to the left, continuing off into
space. Note that our test is not very sophisticated. ball.x
is at the centre of the ball and wallR.x is at the centre
of the wall so the ball penetrates the wall before it bounces.

Adjust the collision test so that the ball bounces when the edge of the
ball reaches the edge of the wall (ie when 
`ball.x > wallR.x-wallR.size.x/2- ball.radius`). Replace the test in the if
statement with this new statement.

For a more realistic bounce you should reflect the position of the ball
as well as its velocity.

You can add another wall at the left side of the display, and make the
ball bounce off that wall also.

We have hard coded in a number of parameters such as the radius of the
ball, the thickness and position of the walls. It is often better to
define variables to hold the value of these types of parameters. In the
following I have set a number of parameters early in the code and then
used them throughout.

With these new variables, `side`, `thk`, `ball_radius`, `maxpos`,
`maxv`, your program should now look something like the following:

    #########################################
    # Import the library(s)
    #########################################
    from visual import *

    ##########################################
    # Create Wall(s)
    ##########################################
    side=4.0
    thk=0.3

    wallR = box (pos=vector( side, 0, 0), length=thk,
                 height=2*side, width=2*side, color = color.red)
    wallL = box (pos=vector(-side, 0, 0), length=thk,
                 height=2*side, width=2*side, color = color.red)

    ##########################################
    # Create Ball(s)
    ##########################################
    ball_radius=1.0
    maxpos=side-thk/2-ball_radius
    maxv=2.0

    ball = sphere(color = color.green, radius = ball_radius)
    ball.velocity = vector(2,.1,0)


    ##########################################
    # Time loop for moving Ball(s)
    ###########################################
    timestep = 0.05

    while (1==1):
        # Set number of times loop is repeated per second
        rate(100)

        # Move ball(s)
        ball.pos = ball.pos + ball.velocity*timestep

        #check for collisions with the walls
        #right wall
        if ball.pos.x > maxpos:
            ball.velocity.x = -ball.velocity.x #reflect velocity
            ball.pos.x=2*maxpos-ball.pos.x     #reflect position
        #left wall
        if ball.pos.x < -maxpos:
            ball.velocity.x = -ball.velocity.x
            ball.pos.x=-2*maxpos-ball.pos.x

This program makes a ball bounce backward and forward between two
parallel walls. Notice that the ball has a little upward (y) velocity
(the z direction is out of the screen). The ball continues to bounce
even when it has passed the top of the walls.

You should add extra walls now so that the ball bounces inside a box.
You also need to extend the walls so they touch so that the simulation
looks nice. You will want to have an invisible front wall so that you
can see inside. Play around with different starting positions and
velocities for the ball, and sizes for the ball and box.

Conclusion
==========

If you have had trouble, or have run out of time, [here is the code for
the bouncing ball in a box](bounce2.py)

Using this bouncing ball program as a base, it is possible to create a
simulation of a gas. Have a look at our [gas simulation
tutorial](tute-gas.md)
