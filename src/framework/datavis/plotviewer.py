import matplotlib
import os

if "DISPLAY" not in os.environ:
    matplotlib.use("agg")
else:
    matplotlib.use("TKagg")
import matplotlib.pyplot as plt

# Tick size and X and Y axes
ticksize = 15

# Font definition
font = {
    "family": "serif",
    "color": "darkred",
    "weight": "normal",
    "size": 18,
}



import imas
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def overlay_coils(ax, pf_active):

    for coil in pf_active.coil:
        for element in coil.element:
            cew = element.geometry.rectangle.width
            ceh = element.geometry.rectangle.height
            if cew>0. and ceh>0.:
                cec = (element.geometry.rectangle.r-cew/2.0,element.geometry.rectangle.z-ceh/2.0)
                rectangle = Rectangle(cec,cew,ceh)
                ax.add_patch(rectangle)
                rx, ry = rectangle.get_xy()
                cx = rx + rectangle.get_width()/2.0
                cy = ry + rectangle.get_height()/2.0
                ax.annotate(coil.identifier, (cx, cy), color='black', weight='bold', ha='center', va='center')


                
def overlay_limiters(ax, wall):

    for unit in wall.description_2d[0].limiter.unit:
        ax.plot(unit.outline.r,unit.outline.z,'r-',linewidth=2)
    
    
def overlay_vessel(ax, wall):

    for unit in wall.description_2d[0].vessel.unit:
        ax.plot(unit.annular.centreline.r,unit.annular.centreline.z,'k-',linewidth=2)
    
    


if __name__=="__main__":

    fig,ax = plt.subplots()

    md=imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,"ITER_MD",111001,202,"public")
    err,n=md.open()
    pfa = md.get("pf_active")

    overlay_coils(ax, pfa)

    md=imas.DBEntry(imas.imasdef.MDSPLUS_BACKEND,"ITER_MD",116000,2,"public")
    err,n=md.open()
    wall = md.get("wall")

    overlay_limiters(ax, wall)
    overlay_vessel(ax, wall)

    plt.axis('equal')
    plt.autoscale(enable=True)
    plt.show()
