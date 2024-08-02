import numpy as np


def read_wall(wallfile):
    # read first-wall polygone
    wall2d = np.genfromtxt(wallfile, dtype=np.double)[:, :]

    return wall2d


# TODO We will wait till we have new ids then will move these functions under that ids
def read_launching_parameters(filelaunchers):
    # read launching parameters
    # this is preliminary: we use constant parameters
    # the time variation can comes via the ec_waveforms.yaml
    # but also via the scenario.yaml which overwrites the settings in ec_waveforms.yaml
    # As far as I understood Mireille she plans to generate a 'real' ec_waveforms.yaml
    # after the run. When that is available th ereading of ec_waveforms.yaml has to
    # be redone including an itroduction of a time base and its mapping on the time steps
    # of the TORBEAM runs. So far we assume the parameters of the launchers are constant
    # and have no time base (in ec_waveforms.yaml the only time point is 0.0 sec).

    from waveform_cooker import add_dynamic

    from idstools.compute.common import cyl2xyz, xyz2cyl

    launching_parameters = {}

    ec_launchers = add_dynamic(filelaunchers)
    lec_launchers = len(ec_launchers.beam)
    b_p_in = np.zeros((lec_launchers), dtype=np.double)
    br_t = np.zeros((lec_launchers, 3), dtype=np.double)
    be_k = np.zeros((lec_launchers, 3), dtype=np.double)
    bwyb = np.zeros((lec_launchers), dtype=np.double)
    bwzb = np.zeros((lec_launchers), dtype=np.double)
    bw1 = np.zeros((lec_launchers), dtype=np.double)
    bw2 = np.zeros((lec_launchers), dtype=np.double)
    brsyb = np.zeros((lec_launchers), dtype=np.double)
    brszb = np.zeros((lec_launchers), dtype=np.double)
    bgamma = np.zeros((lec_launchers), dtype=np.double)
    for i in range(lec_launchers):
        b_p_in[i] = ec_launchers.beam[i].power_launched.data[0]
        br_t[i, :] = cyl2xyz(
            np.array(
                [
                    ec_launchers.beam[i].launching_position.r[0],
                    ec_launchers.beam[i].launching_position.phi[0],
                    ec_launchers.beam[i].launching_position.z[0],
                ],
                dtype=np.double,
            )
        )
        # the following 4 lines are from torbeam_ids.f90
        # beta  = -ec_launchers_ids%beam(ibeam)%steering_angle_tor(1)
        # alpha =  ec_launchers_ids%beam(ibeam)%steering_angle_pol(1)
        # xpoldeg = asin(cos(beta)*sin(alpha))*180./pi
        # xtordeg = atan(tan(beta)/cos(alpha))*180./pi
        # thus
        beta = -ec_launchers.beam[i].steering_angle_tor[0]
        alpha = ec_launchers.beam[i].steering_angle_pol[0]
        theta = np.arcsin(np.cos(beta) * np.sin(alpha))
        phi = np.arctan(np.tan(beta) / np.cos(alpha))
        be_k_hlp = np.array(
            [
                -np.cos(theta) * np.cos(phi),
                -np.cos(theta) * np.sin(phi),
                -np.sin(theta),
            ],
            dtype=np.double,
        )
        be_k_hlp = xyz2cyl(be_k_hlp)
        be_k_hlp[1] = be_k_hlp[1] + ec_launchers.beam[i].launching_position.phi[0]
        be_k[i, :] = cyl2xyz(be_k_hlp)
        bw1[i] = ec_launchers.beam[i].spot.size[0, 0]
        bw2[i] = ec_launchers.beam[i].spot.size[1, 0]
        bgamma[i] = ec_launchers.beam[i].spot.angle[0]
        # torbeam so far can only handle ellipses with the main axes in horizontal and vertical position
        if np.cos(bgamma[i]) ** 2 > 0.5:
            bwyb[i] = bw1[i]
            bwzb[i] = bw2[i]
            brsyb[i] = 1.0 / ec_launchers.beam[i].phase.curvature[0, 0]
            brszb[i] = 1.0 / ec_launchers.beam[i].phase.curvature[1, 0]
        else:
            bwyb[i] = bw2[i]
            bwzb[i] = bw1[i]
            brsyb[i] = 1.0 / ec_launchers.beam[i].phase.curvature[1, 0]
            brszb[i] = 1.0 / ec_launchers.beam[i].phase.curvature[0, 0]
        bgamma[i] = 0.0

    launching_parameters["lec_launchers"] = lec_launchers
    launching_parameters["br_t"] = br_t
    launching_parameters["be_k"] = be_k
    launching_parameters["bwyb"] = bwyb
    launching_parameters["brsyb"] = brsyb
    launching_parameters["bwzb"] = bwzb
    launching_parameters["brszb"] = brszb
    launching_parameters["bP_in"] = b_p_in
    launching_parameters["bgamma"] = bgamma

    return launching_parameters


def read_torbeam_output(launching_parameters, path_result):
    import glob
    import os

    # Sort the list of files according to the time slices
    # TODO This logic can break easily if file names are not according to logic
    def mysort(x):
        return float(os.path.split(x)[1].split("_")[2].replace("t", ""))

    beam_output = {}
    lec_launchers = launching_parameters["lec_launchers"]
    # print(np.array(sorted(glob.glob(path_result + "/s*.txt"))))
    # read torbeam output files
    time_slices = np.array(sorted(glob.glob(path_result + "/s*.txt"), key=mysort))
    launchers = np.genfromtxt(time_slices[0], usecols=0, dtype=str)
    nlaunchers = len(launchers)

    # launchers with zero input power do not appear in the output
    # this reqires a mapping between output and input
    # ec_launchers.beam[mapl[i]] contains the input data for output beam i
    # default is a 1:1 mapping (all launchers active)
    # FIXME EC launchers are not defined, refactoring is needed with discussion with Mireille
    mapl = np.arange(nlaunchers, dtype=np.int_)
    if nlaunchers != lec_launchers:
        j = 0
        for i in range(nlaunchers):
            lc = True
            while lc:
                if launchers[i] == launchers.beam[j].name:
                    mapl[i] = j
                    j = j + 1
                    lc = False
                elif j >= len(launchers.beam):
                    print("error determinimg mapl !!!", i, j)
                    break
                else:
                    j = j + 1

    ntimes = len(time_slices)
    times = np.zeros(ntimes, dtype=float)
    r_t = np.zeros((ntimes, nlaunchers, 3), dtype=np.double)
    e_k = np.zeros((ntimes, nlaunchers, 3), dtype=np.double)
    p_in = np.zeros((ntimes, nlaunchers), dtype=np.double)
    p_abs = np.zeros((ntimes, nlaunchers), dtype=np.double)
    wyb = np.zeros((ntimes, nlaunchers), dtype=np.double)
    wzb = np.zeros((ntimes, nlaunchers), dtype=np.double)
    w1 = np.zeros((ntimes, nlaunchers), dtype=np.double)
    w2 = np.zeros((ntimes, nlaunchers), dtype=np.double)
    rsyb = np.zeros((ntimes, nlaunchers), dtype=np.double)
    rszb = np.zeros((ntimes, nlaunchers), dtype=np.double)
    gamma = np.zeros((ntimes, nlaunchers), dtype=np.double)
    # gamma is the angle with which axis 1 is rotated against horisontal
    # counter clockwise looking along the beam
    # initially we take wyb abd rsyb as axis 1 and gamma=zero
    for j in range(ntimes):
        data = np.genfromtxt(time_slices[j], dtype=np.double)[:, 1:]
        for i in range(nlaunchers):
            (
                p_in[j, i],
                p_abs[j, i],
                xe,
                ye,
                ze,
                vxn,
                vyn,
                vzn,
                wyb[j, i],
                wzb[j, i],
                rsyb[j, i],
                rszb[j, i],
                w1[j, i],
                w2[j, i],
            ) = data[i, :]

            r_t[j, i, :] = [xe, ye, ze]
            e_k[j, i, :] = [vxn, vyn, vzn]
            e_k[j, i, :] = e_k[j, i, :] / np.sqrt(np.sum(e_k[j, i, :] ** 2))
            fstr = time_slices[j]
            times[j] = fstr[fstr.find("_t") + 2 : fstr.find("_p")]
    # collecting data completed

    beam_output["ntimes"] = ntimes
    beam_output["nlaunchers"] = nlaunchers
    beam_output["r_t"] = r_t
    beam_output["e_k"] = e_k
    beam_output["wyb"] = wyb
    beam_output["rsyb"] = rsyb
    beam_output["wzb"] = wzb
    beam_output["rszb"] = rszb
    beam_output["P_in"] = p_in
    beam_output["P_abs"] = p_abs
    beam_output["gamma"] = gamma

    return beam_output, times


def l2r(ldata, edges, lwall):
    ldata_shape = ldata.shape
    ldata = np.reshape(ldata, (-1))
    rdata = np.copy(ldata)
    for i in range(len(ldata)):
        # find larger edge
        il = np.where(lwall >= ldata[i])[0][0]
        # interpolate between lower and larger edge
        rdata[i] = edges[il - 1, 0] + (ldata[i] - lwall[il - 1]) / (lwall[il] - lwall[il - 1]) * (
            edges[il, 0] - edges[il - 1, 0]
        )
        ldata = np.reshape(ldata, ldata_shape)
        rdata = np.reshape(rdata, ldata_shape)
    return rdata


def beam_wall_crossing(wall2d, launching_parameters, beam_output):
    br_t = launching_parameters["br_t"]
    be_k = launching_parameters["be_k"]
    bwyb = launching_parameters["bwyb"]
    brsyb = launching_parameters["brsyb"]
    bwzb = launching_parameters["bwzb"]
    brszb = launching_parameters["brszb"]
    b_p_in = launching_parameters["bP_in"]
    bgamma = launching_parameters["bgamma"]

    r_t = beam_output["r_t"]
    e_k = beam_output["e_k"]
    wyb = beam_output["wyb"]
    rsyb = beam_output["rsyb"]
    wzb = beam_output["wzb"]
    rszb = beam_output["rszb"]
    p_in = beam_output["P_in"]
    p_abs = beam_output["P_abs"]
    gamma = beam_output["gamma"]

    beam_wall = {}

    # Now find the crossings of the outgoing beams with wall2d
    # define function line_polygone_intersection

    # plan:
    # read/define polygone nx5 array R,z,delta_R, delta_z,l=sqrt(delta_r**2 +delta_z**2); circular
    # read torbeam output as above

    # we need several subroutines

    # for points on the rotational polygone
    # convert R,Phi,fl for point on polygone into ns sektor, -pi/18 <= phis <= pi/18, Rphi=R*phis+ Rmax*ns*pi/18 and l
    # Rmax is the maximum R in the polygone
    # input R,Phi,fl,sgn il: polygone point from where to measure li, sgn: direction in which to measure li

    # plot the sector borders in the Rphi, l plane, plus some help lines like z=o on the inside and outside an zmax

    # for a sequence o tb output, calculate the crossing points using   3),
    # the corresponding fractional length lfl using 4)
    # and the coordinates in the Rphi,l representation
    # and over plot them
    # the following for debugging purposes only
    # r_t=r_t[83:85,6:7,:]
    # e_k=e_k[83:85,6:7,:]
    # wyb=wyb[83:85,6:7]
    # wzb=wzb[83:85,6:7]
    # rsyb=rsyb[83:85,6:7]
    # rszb=rszb[83:85,6:7]
    # gamma=gamma[83:85,6:7]
    # P_in=P_in[83:85,6:7]
    # P_abs=P_abs[83:85,6:7]
    # first deal with the rays eciting the torbeam calculation
    nxp, xpdata = line_polygon_intersection(r_t, e_k, wall2d)
    # for exiting rays we only take the closest crossing
    # there may be three crossings if the mathematical ray exits on the HFS
    # and passes also through the opposite part of the torus
    # and even more if the polygone is not convex
    xpout = xpdata[:, :, 0]
    w1l = calcw(wyb, rsyb, xpout["lambda_ray"])
    w2l = calcw(wzb, rszb, xpout["lambda_ray"])
    i0 = (p_in - p_abs) * 2.0 / np.pi * xpout["k_dot_n"] / (w1l * w2l)
    g1l, g2l, rl, sl = ell_on_wall(xpout, w1l, w2l, gamma, e_k, wall2d)

    # now we look at the vacuum beam leaving the launcher
    bxp, bxpdata = line_polygon_intersection(br_t, be_k, wall2d)
    # we expect two crossings: an entry point and a vacuum exit point
    xpentry = bxpdata[:, 0]
    w1e = calcw(bwyb, brsyb, xpentry["lambda_ray"])
    w2e = calcw(bwzb, brszb, xpentry["lambda_ray"])
    i0e = b_p_in * 2.0 / np.pi * xpentry["k_dot_n"] / (w1e * w2e)
    g1e, g2e, re, se = ell_on_wall(xpentry, w1e, w2e, bgamma, be_k, wall2d)
    xpvacout = bxpdata[:, 1]
    w1v = calcw(bwyb, brsyb, xpvacout["lambda_ray"])
    w2v = calcw(bwzb, brszb, xpvacout["lambda_ray"])
    # I0v = bP_in * 2.0 / np.pi * xpvacout["k_dot_n"] / (w1v * w2v)
    g1v, g2v, rv, sv = ell_on_wall(xpvacout, w1v, w2v, bgamma, be_k, wall2d)

    beam_wall["g1e"] = g1e
    beam_wall["g2e"] = g2e
    beam_wall["re"] = re
    beam_wall["se"] = se
    beam_wall["g1l"] = g1l
    beam_wall["g2l"] = g2l
    beam_wall["rl"] = rl
    beam_wall["sl"] = sl
    beam_wall["I0"] = i0
    beam_wall["I0e"] = i0e

    return beam_wall


def check_rays_into_divertor(wall2d, beam_output):
    nwall = wall2d.shape[0]

    ntimes = beam_output["ntimes"]
    nlaunchers = beam_output["nlaunchers"]
    r_t = beam_output["r_t"]

    # check if Torbeam traces rays into the divertor
    rad_t = np.sqrt(r_t[:, :, 0] ** 2 + r_t[:, :, 1] ** 2)
    r_tc = np.stack((rad_t, r_t[:, :, 2]), axis=-1)
    e_d = wall2d[nwall - 1, :] - wall2d[0, :]
    # print(e_d)
    dcnt = 0
    for j in range(ntimes):
        for i in range(nlaunchers):
            # checking the sign of sin angle between 2D vectors
            # ie vector closing divertor (e_D) and R,z of all last points of beam traces r_t
            if (np.cross(r_tc[j, i, :] - wall2d[0, :], e_d)) > -1.0e-6:
                print(
                    j,
                    i,
                    r_tc[j, i, :],
                    wall2d[0, :],
                    np.cross(r_tc[j, i, :] - wall2d[0, :], e_d),
                )
                dcnt = dcnt + 1
    if dcnt > 0:
        print("torbeam followed beams into Divertor")
        print("This post processer cannot handle this yet")
        quit()
    # In the first test case this did not happen
    # Assume for simplification that this never happens
    # In any case above warning will be issued


def line_polygon_intersection(  # input
    line_p,  # arbitrary point on line (3D) [*,3]
    line_dir,  # direction of line  (3D)
    polygon_data,  # input polygon as 2D-array
    # output
    # n_xp,         # number of intersections
    # xp_data,      # countour intersection
    # (max 2, sorted by distance)
    # structured array, see below
    # keyword parameter
    close=True,
):
    # routine to provide points of intersection between contour polygon(2D)
    # and specified line (3D)
    # toroidal symmetry assumed
    # eg (diagnostics line of sight) intersection (vessel contour)

    # data format / coordinate systems
    # line_p [*,3] : x,y,z 3D-cartesian
    # polygon_data (*,2) : R,z 2D-poloidal plane
    inshape = line_p.shape
    line_p = np.reshape(line_p, (-1, 3))
    line_dir = np.reshape(line_dir, (-1, 3))

    # input dimensions
    line_p_dim = len(line_p)
    # output arrays
    n_xp = np.zeros(line_p_dim, dtype=np.int_)
    xp_dt = np.dtype(
        [
            ("icorner", np.int_),
            ("lambda_ray", np.double),
            ("lambda_pol", np.double),
            ("r_hit", np.double, 3),
            ("r_cyl", np.double, 3),
            ("k_dot_n", np.double),
            ("n_c", np.double, 3),
        ]
    )
    xp_data = np.zeros((line_p_dim, 2), dtype=xp_dt)

    # edge structure of polygon
    # careful this implies that the polygone is open
    # otherwise one has to repeat the first point at the end
    # or set the keyword close=True (default)
    n_polygon = len(polygon_data)
    if close:
        n_edges = n_polygon
        cp_edges = np.vstack([polygon_data, polygon_data[0, :]])
    else:
        n_edges = n_polygon - 1
        cp_edges = polygon_data  # since no writing to cp_edges, copy not necessary

    #   loop line_p
    for i_line_p in range(line_p_dim):
        eg = line_dir[i_line_p, :].copy()  # old : r
        eg = eg / np.sqrt(np.sum(eg**2))  # normalize eg
        rg = line_p[i_line_p, :]  # old : x0
        # loop polygon edges
        s_arr = np.ones((2 * n_edges, 11), dtype=np.double) * -1
        rg_r2 = rg[0] ** 2 + rg[1] ** 2  # useful for cc, old x01_x02
        eg_r2 = eg[0] ** 2 + eg[1] ** 2
        egz2 = eg[2] ** 2
        rgegxy = rg[0] * eg[0] + rg[1] * eg[1]
        for i_s in range(n_edges):
            dzrg1 = rg[2] - cp_edges[i_s, 1]
            dz21 = cp_edges[i_s + 1, 1] - cp_edges[i_s, 1]
            dz212 = dz21**2
            d_r21 = cp_edges[i_s + 1, 0] - cp_edges[i_s, 0]
            d_r212 = d_r21**2
            d_rz21 = d_r21 * dz21
            # coefficients of quadratic equation
            aa = dz212 * eg_r2 - d_r212 * egz2
            bb = 2 * (dz212 * rgegxy - d_r212 * eg[2] * dzrg1 - eg[2] * cp_edges[i_s, 0] * d_rz21)
            cc = dz212 * (rg_r2 - cp_edges[i_s, 0] ** 2) - d_r212 * (dzrg1**2) - 2 * cp_edges[i_s, 0] * d_rz21 * dzrg1
            if aa**2 < 1.0e-12:  # assume aa is zero
                if dz212 * egz2 < 1.0e-10:
                    # error: segment is horizontal plate and line is horizontal
                    s_arr[2 * i_s, 1] = -2
                    s_arr[2 * i_s + 1, 1] = -2
                if d_r212 * eg_r2 < 1.0e-10:
                    # error: segment is vertical cylinder and line is vertical
                    s_arr[2 * i_s, 1] = -3
                    s_arr[2 * i_s + 1, 1] = -3
                else:
                    # [egR,egz] (direction of line) parallel to
                    # [dr21, dz21] polygone segment
                    # the plane normal to  [egx,egy,egz] x [egy,-egx,0] through rg
                    # cuts the cone in a parabola : only one solution
                    # s_arr[:,1] : lambda_pol *(r2-r1) = [rR,rz] - r1
                    s_arr[2 * i_s, 1] = -cc / bb  # lambda_ray * eg +rg = r
                    if s_arr[2 * i_s, 1] >= 0.0:
                        rvec = s_arr[2 * i_s, 1] * eg + rg
                        # must lie on cone: radial component rR
                        r_r = np.sqrt(rvec[0] ** 2 + rvec[1] ** 2)
                        dr_r1 = r_r - cp_edges[i_s, 0]
                        drz1 = rvec[2] - cp_edges[i_s, 1]
                        # note that mathematically we are dealing with a double cone
                        # with a singularity somewhere on the z-axis
                        # first we check if our solution lies on the same side
                        # of the cone
                        # as our polygone segment by calculating the cross product
                        # (r2-r1)x(r-r1)
                        # if small enough,
                        # i.e. |dR21*drz1-dz21*drR1|/(dR212+dz212) < 1E-6
                        # we calculate lambda_pol by the normalized dot product
                        # (r2-r1)dot(r-r1)/(r2-r1)^2
                        if np.abs(d_r21 * drz1 - dz21 * dr_r1) / (d_r212 + dz212) < 1.0e-6:
                            s_arr[2 * i_s, 0] = (dr_r1 * d_r21 + drz1 * dz21) / (d_r212 + dz212)
                        # this is lambda_pol, must be between 0 and 1
                        # if segment is relevant
                        if s_arr[2 * i_s, 0] >= 0.0 and s_arr[2 * i_s, 0] < 1.0:
                            # later it is helpful if 0 < lambda_pol < |r2-r1|
                            s_arr[2 * i_s, 0] = s_arr[2 * i_s, 0] * np.sqrt(d_r212 + dz212)
                            r_phi = np.arctan2(rvec[1], rvec[0], dtype=np.double)
                            if r_phi < 0:
                                r_phi = r_phi + 2 * np.pi  # 0 <= rPhi < 2pi
                            # normal on cone segment at rvex
                            n_c = np.array(
                                [dz21 * np.cos(r_phi), dz21 * np.sin(r_phi), -d_r21],
                                dtype=np.double,
                            )
                            n_c = n_c / np.sqrt(np.sum(n_c**2))  # normalize n_c
                            s_arr[2 * i_s, 2] = np.dot(eg, n_c)
                            if s_arr[2 * i_s, 2] < 0:
                                n_c = -n_c
                                s_arr[2 * i_s, 2] = -s_arr[2 * i_s, 2]
                            s_arr[2 * i_s, 3:6] = rvec
                            s_arr[2 * i_s, 6] = r_r
                            s_arr[2 * i_s, 7] = r_phi
                            s_arr[2 * i_s, 8:11] = n_c
                    s_arr[2 * i_s + 1, 1] = -4
            else:
                det = bb**2 - 4 * aa * cc
                if det >= 0.0:
                    # calculate lambda_ray
                    s_arr[2 * i_s, 1] = (-bb + np.sqrt(det)) / (2.0 * aa)
                    s_arr[2 * i_s + 1, 1] = (-bb - np.sqrt(det)) / (2.0 * aa)
                    # if lambda_ray >= 0, calculate lambda_pol
                    if s_arr[2 * i_s, 1] >= 0.0:
                        rvec = s_arr[2 * i_s, 1] * eg + rg
                        # print(rvec)
                        r_r = np.sqrt(rvec[0] ** 2 + rvec[1] ** 2)
                        dr_r1 = r_r - cp_edges[i_s, 0]
                        drz1 = rvec[2] - cp_edges[i_s, 1]
                        # note that mathematically we are dealing with a double cone
                        # with a singularity somewhere on the z-axis
                        # first we check if our solution lies on the same side
                        # of the cone
                        # as our polygone segment by calculating the cross product
                        # (r2-r1)x(r-r1)
                        # if small enough, i.e.
                        # |dR21*drz1-dz21*drR1|/(dR212+dz212) < 1E-6
                        # we calculate lambda_pol by the normalized dot product
                        # (r2-r1)dot(r-r1)/(r2-r1)^2
                        if np.abs(d_r21 * drz1 - dz21 * dr_r1) / (d_r212 + dz212) < 1.0e-6:
                            s_arr[2 * i_s, 0] = (dr_r1 * d_r21 + drz1 * dz21) / (d_r212 + dz212)
                        # this is lambda_pol, must be between 0 and 1 if relevant
                        if s_arr[2 * i_s, 0] >= 0.0 and s_arr[2 * i_s, 0] < 1.0:
                            # later it is helpful if 0 < lambda_pol < |r2-r1|
                            s_arr[2 * i_s, 0] = s_arr[2 * i_s, 0] * np.sqrt(d_r212 + dz212)
                            r_phi = np.arctan2(rvec[1], rvec[0], dtype=np.double)
                            if r_phi < 0:
                                r_phi = r_phi + 2 * np.pi
                            # normal on cone segment at rvex
                            n_c = np.array(
                                [dz21 * np.cos(r_phi), dz21 * np.sin(r_phi), -d_r21],
                                dtype=np.double,
                            )
                            n_c = n_c / np.sqrt(np.sum(n_c**2))  # normalize n_c
                            s_arr[2 * i_s, 2] = np.dot(eg, n_c)
                            if s_arr[2 * i_s, 2] < 0:
                                n_c = -n_c
                                s_arr[2 * i_s, 2] = -s_arr[2 * i_s, 2]
                            s_arr[2 * i_s, 3:6] = rvec
                            s_arr[2 * i_s, 6] = r_r
                            s_arr[2 * i_s, 7] = r_phi
                            s_arr[2 * i_s, 8:11] = n_c
                    if s_arr[2 * i_s + 1, 1] >= 0.0:
                        rvec = s_arr[2 * i_s + 1, 1] * eg + rg
                        r_r = np.sqrt(rvec[0] ** 2 + rvec[1] ** 2)
                        dr_r1 = r_r - cp_edges[i_s, 0]
                        drz1 = rvec[2] - cp_edges[i_s, 1]
                        # note that mathematically we are dealing with a double cone
                        # with a singularity somewhere on the z-axis
                        # first we check if our solution lies on the same side
                        # of the cone
                        # as our polygone segment by calculating the cross product
                        # (r2-r1)x(r-r1)
                        # if small enough,
                        # i.e. |dR21*drz1-dz21*drR1|/(dR212+dz212) < 1E-6
                        # we calculate lambda_pol by the normalized dot product
                        # (r2-r1)dot(r-r1)/(r2-r1)^2
                        if np.abs(d_r21 * drz1 - dz21 * dr_r1) / (d_r212 + dz212) < 1.0e-6:
                            s_arr[2 * i_s + 1, 0] = (dr_r1 * d_r21 + drz1 * dz21) / (d_r212 + dz212)
                        if s_arr[2 * i_s + 1, 0] >= 0.0 and s_arr[2 * i_s + 1, 0] < 1.0:
                            # later it is helpful if 0 < lambda_pol < |r2-r1|
                            s_arr[2 * i_s + 1, 0] = s_arr[2 * i_s + 1, 0] * np.sqrt(d_r212 + dz212)
                            r_phi = np.arctan2(rvec[1], rvec[0], dtype=np.double)
                            if r_phi < 0:
                                r_phi = r_phi + 2 * np.pi
                            # normal on cone segment at rvec
                            n_c = np.array(
                                [dz21 * np.cos(r_phi), dz21 * np.sin(r_phi), -d_r21],
                                dtype=np.double,
                            )
                            n_c = n_c / np.sqrt(np.sum(n_c**2))  # normalize n_c
                            s_arr[2 * i_s + 1, 2] = np.dot(eg, n_c)
                            if s_arr[2 * i_s + 1, 2] < 0:
                                n_c = -n_c
                                s_arr[2 * i_s + 1, 2] = -s_arr[2 * i_s + 1, 2]
                            s_arr[2 * i_s + 1, 3:6] = rvec
                            s_arr[2 * i_s + 1, 6] = r_r
                            s_arr[2 * i_s + 1, 7] = r_phi
                            s_arr[2 * i_s + 1, 8:11] = n_c
        # endfor ; end loop polygon edges
        # find 'useful' lambda_pol values, in that case n_c was calculated and
        # s_arr[:,2] = |n_c|
        # otherwise s_arr[:,2] is -1 as preset
        ind_xp = np.where(s_arr[:, 2] >= 0.0)[0]
        nxp = len(ind_xp)
        # nxp sometimes above two: choose two lowest values
        # (depends on shape of polygon)
        ixp1 = np.int_(-1)
        ixp2 = np.int_(-1)
        if nxp == 1:
            ixp1 = ind_xp[0]
        if nxp >= 2:
            isort_xp = np.argsort(s_arr[ind_xp, 1])
            ixp1 = ind_xp[isort_xp[0]]
            ixp2 = ind_xp[isort_xp[1]]
        # endif
        # write output
        n_xp[i_line_p] = nxp
        if nxp > 0:
            xp_data[i_line_p, 0]["lambda_ray"] = s_arr[ixp1, 1]
            xp_data[i_line_p, 0]["lambda_pol"] = s_arr[ixp1, 0]
            xp_data[i_line_p, 0]["r_hit"] = s_arr[ixp1, 3:6]
            xp_data[i_line_p, 0]["r_cyl"] = [
                s_arr[ixp1, 6],
                s_arr[ixp1, 7],
                s_arr[ixp1, 5],
            ]
            xp_data[i_line_p, 0]["k_dot_n"] = s_arr[ixp1, 2]
            xp_data[i_line_p, 0]["n_c"] = s_arr[ixp1, 8:11]
            xp_data[i_line_p, 0]["icorner"] = ixp1 // 2
        if nxp > 1:
            xp_data[i_line_p, 1]["lambda_ray"] = s_arr[ixp2, 1]
            xp_data[i_line_p, 1]["lambda_pol"] = s_arr[ixp2, 0]
            xp_data[i_line_p, 1]["r_hit"] = s_arr[ixp2, 3:6]
            xp_data[i_line_p, 1]["r_cyl"] = [
                s_arr[ixp2, 6],
                s_arr[ixp2, 7],
                s_arr[ixp2, 5],
            ]
            xp_data[i_line_p, 1]["k_dot_n"] = s_arr[ixp2, 2]
            xp_data[i_line_p, 1]["n_c"] = s_arr[ixp2, 8:11]
            xp_data[i_line_p, 1]["icorner"] = ixp2 // 2
    # endfor  end loop line_p

    line_p = np.reshape(line_p, inshape)
    line_dir = np.reshape(line_dir, inshape)
    nxpshape = inshape[0 : len(inshape) - 1]
    n_xp = np.reshape(n_xp, nxpshape)
    xp_data = np.reshape(xp_data, nxpshape + tuple([2]))
    return n_xp, xp_data


# calculate beam width for given w,Rcur and length along ray (lambda_ray)
def calcw(wt, rt, lambda_ray, freq=np.double(170.0e9)):
    # wt, Rt width and curvature radius at start point in m
    # Rt < 0 : beam will pass focus, >0 : purely diverging
    # the focus is at lambda_ray = -Rt
    # lambda_ray length along ray in m
    # freq: wave frequency im Hz (not rad/s)
    c = np.double(2.998e8)  # speed of light in vacuum in m/s
    # assume vacuum conditionas at edge of plasma
    sr = np.pi * wt**2 / (c / freq)
    w = wt * np.sqrt((1.0 + lambda_ray / rt) ** 2 + (lambda_ray / sr) ** 2)
    return w


# calculate ellipses on wall segment
def ell_on_wall(xpout, w1, w2, gamma, e_k, wall2d):
    # input:  xpout   array of data type xp_dt
    #                 (as defined in routine line_polygon_intersection above)
    #         w1,w2   widths of beam at cross section (calculated with calcw)
    #         gamma   rotation of the ellipse
    #         e_k     unit vector direction of ray
    #         wall2d  R,z values of Polygone
    # output: rl      center of the Ellipse (R*Phi [m], l(ength along polygone) [m]
    #         g1l,g2l generating vectors of the ellips (not orthogonal)
    # Ellipse rl + g1l*cos(t) + g2l*sin(t)
    #         xpout,w1,w2,gamma are assumed to have the same shape
    #         e_k has the same shape but is a 3d vector
    #         rl,g1l,g2l same shape, 2d vectors
    #
    # First we collapse to 1-D vectors
    xp_shape = xpout.shape
    xpout = np.reshape(xpout, (-1))
    w1 = np.reshape(w1, (-1))
    w2 = np.reshape(w2, (-1))
    gamma = np.reshape(gamma, (-1))
    e_k = np.reshape(e_k, (-1, 3))
    # next we need to summ the lengths of the wall segments
    lwall = np.zeros((len(wall2d)), dtype=np.double)
    for i in range(len(wall2d)):
        if i == 0:
            lwall[i] = 0.0
        else:
            lwall[i] = lwall[i - 1] + np.sqrt(
                (wall2d[i, 0] - wall2d[i - 1, 0]) ** 2 + (wall2d[i, 1] - wall2d[i - 1, 1]) ** 2
            )

    rl = np.zeros((len(e_k), 2), dtype=np.double)
    sl = np.zeros((len(e_k)), dtype=np.double)
    g1l = np.zeros((len(e_k), 2), dtype=np.double)
    g2l = np.zeros((len(e_k), 2), dtype=np.double)
    eh = np.zeros((3), dtype=np.double)
    for i in range(e_k.shape[0]):
        # we find the horizontal and vertical axis perp tp e_k
        if np.abs(e_k[i, 2]) > 0.999999:
            # horizontal axis not well defined if e_k || [0,0,1]
            # use toroidal axis instead
            eh[0] = 1.0
            eh[1] = xpout["r_cyl"][i, 1] + np.pi / 2.0
            eh[2] = 0.0
            eh = cyl2xyz(eh)
        else:
            eh = np.cross(np.array([0.0, 0.0, 1.0], dtype=np.double), e_k[i, :])
        # normalize eh
        eh = eh / np.sqrt(np.sum(eh**2))
        ev = np.cross(e_k[i, :], eh)
        ev = ev / np.sqrt(np.sum(ev**2))
        #        print(eh,ev,e_k[i,:])
        # parallel projection of elipsis on wall segment with surface normal n_c
        peh = eh - np.dot(eh, xpout["n_c"][i, :]) / xpout["k_dot_n"][i] * e_k[i, :]
        pev = ev - np.dot(ev, xpout["n_c"][i, :]) / xpout["k_dot_n"][i] * e_k[i, :]
        # g1, g2 define ellipsis on local tangent plane to segment
        g1 = w1[i] * (np.cos(gamma[i]) * peh + np.sin(gamma[i]) * pev)
        g2 = w2[i] * (-np.sin(gamma[i]) * peh + np.cos(gamma[i]) * pev)
        # begin test purposes only, tests ok
        #        print('test g1,g2')
        #        tg2t=2.*np.dot(g1,g2)/(np.sum(g1**2)-np.sum(g2**2))
        # print(xpout[i]['icorner'],np.dot(ga,gb),np.sum(ga**2),np.sum(gb**2),(np.sum(ga**2)-np.sum(gb**2)))
        # print(i,tg2t)
        #        t1=0.5*np.arctan(tg2t,dtype=np.double)
        #        t2=t1+np.pi/2.
        # print(i,t1,t2)
        #        a1=g1* np.cos(t1)+ g2* np.sin(t1)
        #        a2=g1* np.cos(t2)+ g2* np.sin(t2)
        #        sa1=np.sqrt(np.sum(a1**2))
        #        sa2=np.sqrt(np.sum(a2**2))
        #        print(i,w1[i],w2[i],sa1,sa2,sa1*sa2*xpout['k_dot_n'][i],w1[i]*w2[i])
        #        print(np.dot(xpout['n_c'][i,:],peh),np.dot(xpout['n_c'][i,:],pev))
        # tests ok
        #        x-direction on tangential plane
        ephi = cyl2xyz(np.array([1.0, xpout["r_cyl"][i, 1] + np.pi / 2.0, 0.0], dtype=np.double))
        #        y-direction on tangential plane in direction of wall2d[i+1]-wall2d[i]
        if xpout["icorner"][i] < len(wall2d) - 1:
            el = wall2d[xpout["icorner"][i] + 1, :] - wall2d[xpout["icorner"][i], :]
        else:
            el = wall2d[0, :] - wall2d[xpout["icorner"][i], :]
        el = el / np.sqrt(np.sum(el**2))
        el3 = cyl2xyz(np.array([el[0], xpout["r_cyl"][i, 1], el[1]], dtype=np.double))
        g1l[i, 0] = np.dot(g1, ephi)
        g1l[i, 1] = np.dot(g1, el3)
        g2l[i, 0] = np.dot(g2, ephi)
        g2l[i, 1] = np.dot(g2, el3)
        # begin test purposes only, tests ok
        #        print('test g1l,g2l')
        #        tg2t=2.*np.dot(g1l[i],g2l[i])/(np.sum(g1l[i]**2)-np.sum(g2l[i]**2))
        # print(xpout[i]['icorner'],np.dot(ga,gb),np.sum(ga**2),np.sum(gb**2),(np.sum(ga**2)-np.sum(gb**2)))
        # print(i,tg2t)
        #        t1=0.5*np.arctan(tg2t,dtype=np.double)
        #        t2=t1+np.pi/2.
        # print(i,t1,t2)
        #        a1=g1l[i]* np.cos(t1)+ g2l[i]* np.sin(t1)
        #        a2=g1l[i]* np.cos(t2)+ g2l[i]* np.sin(t2)
        #        sa1=np.sqrt(np.sum(a1**2))
        #        sa2=np.sqrt(np.sum(a2**2))
        #        print(i,w1[i],w2[i],sa1,sa2,sa1*sa2*xpout['k_dot_n'][i],w1[i]*w2[i])
        #        print(np.dot(xpout['n_c'][i,:],peh),np.dot(xpout['n_c'][i,:],pev))
        # tests ok
        # now rl: first determine sector
        sl[i] = xpout["r_cyl"][i, 1] // (np.pi / 9.0)
        # dPhi with respect to midlle of sector
        d_phi = xpout["r_cyl"][i, 1] - (sl[i] + 0.5) * (np.pi / 9.0)
        # x - length scale relative to middle of sector
        rl[i, 0] = d_phi * xpout["r_cyl"][i, 0]
        # y-length: length along polygone
        rl[i, 1] = lwall[xpout["icorner"][i]] + xpout["lambda_pol"][i]
    # Reshape input and output vectors to initial shape
    xpout = np.reshape(xpout, xp_shape)
    w1 = np.reshape(w1, xp_shape)
    w2 = np.reshape(w2, xp_shape)
    gamma = np.reshape(gamma, xp_shape)
    sl = np.reshape(sl, xp_shape)
    e_k = np.reshape(e_k, xp_shape + tuple([3]))
    rl = np.reshape(rl, xp_shape + tuple([2]))
    g1l = np.reshape(g1l, xp_shape + tuple([2]))
    g2l = np.reshape(g2l, xp_shape + tuple([2]))
    return g1l, g2l, rl, sl


def cyl2xyz(rcyl):
    rcyl_shape = rcyl.shape
    rvec = np.reshape(rcyl, (-1, 3))
    x = rvec[:, 0] * np.cos(rvec[:, 1])
    rvec[:, 1] = rvec[:, 0] * np.sin(rvec[:, 1])
    rvec[:, 0] = x
    rvec = np.reshape(rvec, rcyl_shape)
    return rvec
