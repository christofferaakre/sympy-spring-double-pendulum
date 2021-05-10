# utils.py
# This file contains a number of helper functions I wrote whose implementations would only
# distract from the main project work, and whose names should be clear enough
# that looking at the implementation should not be required. Nevertheless, I have
# commented the code and added docstrings to all functions just in case the reader
# wants to look at the implementation details anyway.

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.animation import PillowWriter
from IPython.display import HTML

def rad_to_deg(x: float) -> float:
    """
    Converts a radian angle to degrees
    
    x: Angle in radians (float)
    
    returns: Angle in degres (float)
    """
    return x * 180 / np.pi

def deg_to_rad(x: float) -> float:
    """
    Converts a degree angle to radians
    
    x: Angle in degrees (float)
    
    returns: Angle in radians (float)
    """
    return x * np.pi / 180

def show_animation(animation_path: str):
    """
    Shows the animation located at the given path.
    
    animation_path: Path to animation (str)
    
    returns: nothing (None)
    """
    # I said we return None in the docstring since this function should only ever be
    # used to display an animation, not to save the result to a variable
    # for further use
    return HTML(f'<img alt="spring double pendulum animation" src={animation_path}>')

def make_animation(
                   t: np.ndarray,
                   position: np.ndarray,
                   save_path: str,
                   circle_radius: float = None,
                   fps: float = 50,
                   n_seconds: float = 20,
                   decay_time: float = 250,
                   xpad: float = None,
                   ypad: float = None,
                   xlim: float = None,
                   ylim: float = None
                  ) -> None:
    """
    Creates and animation and saves it to the given location.
    
    t: Time (array)
    position: Positions of the two pendulums (array)
    save_path: Path to save animation to (str)
    circle_radius: Optional argument to draw a circle centered at the origin
    with the given radius. This can be useful if you want to draw a circle
    which you think the two pendulums will never exit. (Useful for figuring out the maximum spring extensions)
    fps: FPS (frames per second), i.e. framerate, of animation. Defaults to 50.
    n_seconds: Length of the animation in seconds (float). Defaults to 20.
    decay_time: Parameter determining how long the trajectory traces stay on the screen before they vanish (float).
    The higher the decay_time, the longer they stay. Defaults to 250.
    xpad: Optional argument to specify horizontal padding for the x range (float).
    Does nothing if you are manually specifying the xlim.
    ypad: Optional argument to specify horizontal padding for the y range (float).
    Does nothing if you are manually specifying the ylim.
    xlim: Optional argument to specify the xlim of the animation. (float)
    ylim: Optional argument to specify the ylim of the animation. (float)
    
    returns: nothing (None)
    """
    fig, ax, = plt.subplots(1, 1, figsize=(8, 8))
    ax.grid()

    x1, y1 , x2, y2 = position
   
    # Two lines, one for each pendulum
    line1, = plt.plot([], [], 'ro--', lw=3, markersize=8)
    line2, = plt.plot([], [], 'ro--', lw=3, markersize=8)
   
    # two scatters, representing the two decaying trajectories of the
    # pendulums
    scatter1 = plt.scatter([], [], s=1, c='green')
    scatter2 = plt.scatter([], [], s=1, c='purple')

    x_min, x_max, y_min, y_max = np.min(x2), np.max(x2), np.min(y2), np.max(y2)
    
    # calculating default xpad and ypad 
    if not xpad: 
        xpad = 0.1 * abs(x_min)
    if not ypad:
        ypad = 0.1 * abs(y_min)
   

    plt.xlim(x_min - xpad, x_max + xpad)
    plt.ylim(y_min - ypad, y_max + ypad)
   
    if xlim:
        plt.xlim(xlim)
    
    if ylim:
        plt.ylim(ylim)

    # plot circle on animation if circle_radius is specified
    if circle_radius: 
        angle = np.linspace(0, 2*np.pi, 1000)
        ax.scatter(circle_radius * np.cos(angle), circle_radius * np.sin(angle))

    # total number of frames  
    total_frames = len(t)
    
    # numer of frames to show given fps and length of animation
    n_frames = fps * n_seconds
    
    # we need to skip this many frames every frame for total_frames and n_frames
    # to matc up
    skip = int(total_frames / n_frames)

    # this nested functions is defined
    # according to the specifications requried by
    # matplotlib.animation.funcAnimation (https://matplotlib.org/stable/api/_as_gen/matplotlib.animation.FuncAnimation.html)
    # It must take the frame number as an argument, and update the contents on the screen accordingly.
    # Additionally it returns a list of all artists that were modified or created, so that we can
    # use blit=True when we call matplotlib.animation.funcAnimation to speed up the process quite a bit.
    def animate(frame_number):
        i = frame_number * skip
        
        # updating positions of pendula
        line1.set_data([0, x1[i]], [0, y1[i]])
        line2.set_data([x1[i], x2[i]], [y1[i], y2[i]])

        # computing updated traces
        trace_length = decay_time * skip
        start = max(0, i - trace_length)
        scatter1_data = np.array([x1[start:i:skip], y1[start:i:skip]]).T
        scatter2_data = np.array([x2[start:i:skip], y2[start:i:skip]]).T

        # replacing old traces with new ones
        scatter1.set_offsets(scatter1_data)
        scatter2.set_offsets(scatter2_data)

        # return all artists
        return [line1, line2, scatter1, scatter2]

    # create animation
    ani = animation.FuncAnimation(fig, animate, frames=n_frames, interval=50, blit=True)
    
    # save animation, using writer='pillow' for no particular reason
    ani.save(save_path, writer='pillow', fps=fps)