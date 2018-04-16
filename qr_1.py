import meep as mp
import math
import argparse

def main(args):
    resolution = 20 # 20 pixels per unit 1 um
    eps = 80 # epsilon of cylinder medium
    Mat1 = mp.Medium(epsilon=eps) # definition of the material
    dimensions = mp.CYLINDRICAL

    r = args.r # the value of cylinder radius
    rl = args.rl # the r/l ration is given, to obtain the l value l=r/rl
    x = args.x
    dpml = args.dpml
    dair = args.dair
    m=args.m

    w=1*x  
    h = r/rl # the height of the cylinder
    sr = r + dair + dpml
    sz = h + 2*dair + 2*dpml
    w_max=1.8
    w_min=0.2
    dw=w_max-w_min

    boundary_layers = [mp.PML(dpml)]
    Cyl = mp.Cylinder(material=Mat1, radius=r, height=h, center=mp.Vector3(0,0,0)) # make a cylinder with given parameters
    geometry = [Cyl]
    cell_size = mp.Vector3(sr,0,sz)

    #sources = [ mp.Source(mp.ContinuousSource(frequency = w), component=mp.Hz, center=mp.Vector3(r+dair,0,0)) ]
    sources = [mp.Source(mp.GaussianSource(w, fwidth=dw), component=mp.Hz, center=mp.Vector3(r+dair,0,0))]
    sim = mp.Simulation(resolution=resolution,
                        cell_size=cell_size,
                        boundary_layers=boundary_layers,
                        geometry=geometry,
                        sources=sources,
                        dimensions=dimensions,
                        m=m)
    sim.run(mp.in_volume(mp.Volume(center=mp.Vector3(), size=mp.Vector3(sr,0,sz)),
            mp.at_end(mp.output_epsilon, mp.output_efield_z)),
            mp.after_sources(mp.Harminv(mp.Hz, mp.Vector3(), w, dw)),
            until_after_sources=100)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', type=float, default=1.0, help='radius of the cylinder')
    parser.add_argument('-rl', type=float, default=0.2, help='r/l ratio value')
    parser.add_argument('-x', type=float, default=1, help='size parameter x equals to w*r/c')
    parser.add_argument('-dpml', type=float, default=16, help='thickness of dpml')
    parser.add_argument('-dair', type=float, default=2.0,help='thickness of air padding')
    parser.add_argument('-m', type=int, default=1, help='mode parameter m')
    args=parser.parse_args()
    main(args)
