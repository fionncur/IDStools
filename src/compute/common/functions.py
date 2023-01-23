"""
This is a common module which has common functions which can be used across ll IDSes

"""
import numpy as np


def find_nearest(array: np.ndarray, value: float) -> tuple:
    """
    Get index and nearest value from value asked from an array

    Args:
        array ([np.ndarray]): [numpy array]
        value ([float]): [value requested]

    Returns:
        [int]: [index found for value]
        [float]: [nearest value from value requested]
    """
    if array is None:
        return None
    if len(array) == 0:
        return None
    index = abs(array - value).argmin()
    return array.flat[index], index


def middle(array: np.ndarray) -> tuple:
    """Get middle value from an array along with index

    Args:
        array (np.ndarray): [description]

    Returns:
        [type]: [description]
    """
    if array is None:
        return None
    if len(array) == 0:
        return None
    length = len(array)
    index = int(length / 2)
    value = array[index]
    return index, value


def xyz2cyl(rvec):
    rvec_shape = rvec.shape
    rcyl = np.reshape(rvec, (-1, 3))
    R = np.sqrt(rcyl[:, 0] ** 2 + rcyl[:, 1] ** 2)
    Phi = np.arctan2(rcyl[:, 1], rcyl[:, 0], dtype=np.double)
    ind_phi = np.where(Phi < 0.0)[0]
    if ind_phi.shape[0] > 0:
        Phi[ind_phi] = Phi[ind_phi] + 2 * np.pi
    rcyl[:, 0] = R
    rcyl[:, 1] = Phi
    rcyl = np.reshape(rcyl, rvec_shape)
    return rcyl


def cyl2xyz(rcyl):
    rcyl_shape = rcyl.shape
    rvec = np.reshape(rcyl, (-1, 3))
    x = rvec[:, 0] * np.cos(rvec[:, 1])
    rvec[:, 1] = rvec[:, 0] * np.sin(rvec[:, 1])
    rvec[:, 0] = x
    rvec = np.reshape(rvec, rcyl_shape)
    return rvec


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
        rgR2 = rg[0] ** 2 + rg[1] ** 2  # useful for cc, old x01_x02
        egR2 = eg[0] ** 2 + eg[1] ** 2
        egz2 = eg[2] ** 2
        rgegxy = rg[0] * eg[0] + rg[1] * eg[1]
        for i_s in range(n_edges):
            dzrg1 = rg[2] - cp_edges[i_s, 1]
            dz21 = cp_edges[i_s + 1, 1] - cp_edges[i_s, 1]
            dz212 = dz21**2
            dR21 = cp_edges[i_s + 1, 0] - cp_edges[i_s, 0]
            dR212 = dR21**2
            dRz21 = dR21 * dz21
            # coefficients of quadratic equation
            aa = dz212 * egR2 - dR212 * egz2
            bb = 2 * (
                dz212 * rgegxy
                - dR212 * eg[2] * dzrg1
                - eg[2] * cp_edges[i_s, 0] * dRz21
            )
            cc = (
                dz212 * (rgR2 - cp_edges[i_s, 0] ** 2)
                - dR212 * (dzrg1**2)
                - 2 * cp_edges[i_s, 0] * dRz21 * dzrg1
            )
            if aa**2 < 1.0e-12:  # assume aa is zero
                if dz212 * egz2 < 1.0e-10:
                    # error: segment is horizontal plate and line is horizontal
                    s_arr[2 * i_s, 1] = -2
                    s_arr[2 * i_s + 1, 1] = -2
                if dR212 * egR2 < 1.0e-10:
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
                        rR = np.sqrt(rvec[0] ** 2 + rvec[1] ** 2)
                        drR1 = rR - cp_edges[i_s, 0]
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
                        if np.abs(dR21 * drz1 - dz21 * drR1) / (dR212 + dz212) < 1.0e-6:
                            s_arr[2 * i_s, 0] = (drR1 * dR21 + drz1 * dz21) / (
                                dR212 + dz212
                            )
                        # this is lambda_pol, must be between 0 and 1
                        # if segment is relevant
                        if s_arr[2 * i_s, 0] >= 0.0 and s_arr[2 * i_s, 0] < 1.0:
                            # later it is helpful if 0 < lambda_pol < |r2-r1|
                            s_arr[2 * i_s, 0] = s_arr[2 * i_s, 0] * np.sqrt(
                                dR212 + dz212
                            )
                            rPhi = np.arctan2(rvec[1], rvec[0], dtype=np.double)
                            if rPhi < 0:
                                rPhi = rPhi + 2 * np.pi  # 0 <= rPhi < 2pi
                            # normal on cone segment at rvex
                            n_c = np.array(
                                [dz21 * np.cos(rPhi), dz21 * np.sin(rPhi), -dR21],
                                dtype=np.double,
                            )
                            n_c = n_c / np.sqrt(np.sum(n_c**2))  # normalize n_c
                            s_arr[2 * i_s, 2] = np.dot(eg, n_c)
                            if s_arr[2 * i_s, 2] < 0:
                                n_c = -n_c
                                s_arr[2 * i_s, 2] = -s_arr[2 * i_s, 2]
                            s_arr[2 * i_s, 3:6] = rvec
                            s_arr[2 * i_s, 6] = rR
                            s_arr[2 * i_s, 7] = rPhi
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
                        rR = np.sqrt(rvec[0] ** 2 + rvec[1] ** 2)
                        drR1 = rR - cp_edges[i_s, 0]
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
                        if np.abs(dR21 * drz1 - dz21 * drR1) / (dR212 + dz212) < 1.0e-6:
                            s_arr[2 * i_s, 0] = (drR1 * dR21 + drz1 * dz21) / (
                                dR212 + dz212
                            )
                        # this is lambda_pol, must be between 0 and 1 if relevant
                        if s_arr[2 * i_s, 0] >= 0.0 and s_arr[2 * i_s, 0] < 1.0:
                            # later it is helpful if 0 < lambda_pol < |r2-r1|
                            s_arr[2 * i_s, 0] = s_arr[2 * i_s, 0] * np.sqrt(
                                dR212 + dz212
                            )
                            rPhi = np.arctan2(rvec[1], rvec[0], dtype=np.double)
                            if rPhi < 0:
                                rPhi = rPhi + 2 * np.pi
                            # normal on cone segment at rvex
                            n_c = np.array(
                                [dz21 * np.cos(rPhi), dz21 * np.sin(rPhi), -dR21],
                                dtype=np.double,
                            )
                            n_c = n_c / np.sqrt(np.sum(n_c**2))  # normalize n_c
                            s_arr[2 * i_s, 2] = np.dot(eg, n_c)
                            if s_arr[2 * i_s, 2] < 0:
                                n_c = -n_c
                                s_arr[2 * i_s, 2] = -s_arr[2 * i_s, 2]
                            s_arr[2 * i_s, 3:6] = rvec
                            s_arr[2 * i_s, 6] = rR
                            s_arr[2 * i_s, 7] = rPhi
                            s_arr[2 * i_s, 8:11] = n_c
                    if s_arr[2 * i_s + 1, 1] >= 0.0:
                        rvec = s_arr[2 * i_s + 1, 1] * eg + rg
                        rR = np.sqrt(rvec[0] ** 2 + rvec[1] ** 2)
                        drR1 = rR - cp_edges[i_s, 0]
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
                        if np.abs(dR21 * drz1 - dz21 * drR1) / (dR212 + dz212) < 1.0e-6:
                            s_arr[2 * i_s + 1, 0] = (drR1 * dR21 + drz1 * dz21) / (
                                dR212 + dz212
                            )
                        if s_arr[2 * i_s + 1, 0] >= 0.0 and s_arr[2 * i_s + 1, 0] < 1.0:
                            # later it is helpful if 0 < lambda_pol < |r2-r1|
                            s_arr[2 * i_s + 1, 0] = s_arr[2 * i_s + 1, 0] * np.sqrt(
                                dR212 + dz212
                            )
                            rPhi = np.arctan2(rvec[1], rvec[0], dtype=np.double)
                            if rPhi < 0:
                                rPhi = rPhi + 2 * np.pi
                            # normal on cone segment at rvec
                            n_c = np.array(
                                [dz21 * np.cos(rPhi), dz21 * np.sin(rPhi), -dR21],
                                dtype=np.double,
                            )
                            n_c = n_c / np.sqrt(np.sum(n_c**2))  # normalize n_c
                            s_arr[2 * i_s + 1, 2] = np.dot(eg, n_c)
                            if s_arr[2 * i_s + 1, 2] < 0:
                                n_c = -n_c
                                s_arr[2 * i_s + 1, 2] = -s_arr[2 * i_s + 1, 2]
                            s_arr[2 * i_s + 1, 3:6] = rvec
                            s_arr[2 * i_s + 1, 6] = rR
                            s_arr[2 * i_s + 1, 7] = rPhi
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
def calcw(wt, Rt, lambda_ray, freq=np.double(170.0e9)):
    # wt, Rt width and curvature radius at start point in m
    # Rt < 0 : beam will pass focus, >0 : purely diverging
    # the focus is at lambda_ray = -Rt
    # lambda_ray length along ray in m
    # freq: wave frequency im Hz (not rad/s)
    c = np.double(2.998e8)  # speed of light in vacuum in m/s
    # assume vacuum conditionas at edge of plasma
    sr = np.pi * wt**2 / (c / freq)
    w = wt * np.sqrt((1.0 + lambda_ray / Rt) ** 2 + (lambda_ray / sr) ** 2)
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
                (wall2d[i, 0] - wall2d[i - 1, 0]) ** 2
                + (wall2d[i, 1] - wall2d[i - 1, 1]) ** 2
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
        ##        print(xpout[i]['icorner'],np.dot(ga,gb),np.sum(ga**2),np.sum(gb**2),(np.sum(ga**2)-np.sum(gb**2)))
        ##    print(i,tg2t)
        #        t1=0.5*np.arctan(tg2t,dtype=np.double)
        #        t2=t1+np.pi/2.
        ##    print(i,t1,t2)
        #        a1=g1* np.cos(t1)+ g2* np.sin(t1)
        #        a2=g1* np.cos(t2)+ g2* np.sin(t2)
        #        sa1=np.sqrt(np.sum(a1**2))
        #        sa2=np.sqrt(np.sum(a2**2))
        #        print(i,w1[i],w2[i],sa1,sa2,sa1*sa2*xpout['k_dot_n'][i],w1[i]*w2[i])
        #        print(np.dot(xpout['n_c'][i,:],peh),np.dot(xpout['n_c'][i,:],pev))
        ## tests ok
        #        x-direction on tangential plane
        ephi = cyl2xyz(
            np.array([1.0, xpout["r_cyl"][i, 1] + np.pi / 2.0, 0.0], dtype=np.double)
        )
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
        ##        print(xpout[i]['icorner'],np.dot(ga,gb),np.sum(ga**2),np.sum(gb**2),(np.sum(ga**2)-np.sum(gb**2)))
        ##    print(i,tg2t)
        #        t1=0.5*np.arctan(tg2t,dtype=np.double)
        #        t2=t1+np.pi/2.
        ##    print(i,t1,t2)
        #        a1=g1l[i]* np.cos(t1)+ g2l[i]* np.sin(t1)
        #        a2=g1l[i]* np.cos(t2)+ g2l[i]* np.sin(t2)
        #        sa1=np.sqrt(np.sum(a1**2))
        #        sa2=np.sqrt(np.sum(a2**2))
        #        print(i,w1[i],w2[i],sa1,sa2,sa1*sa2*xpout['k_dot_n'][i],w1[i]*w2[i])
        #        print(np.dot(xpout['n_c'][i,:],peh),np.dot(xpout['n_c'][i,:],pev))
        ## tests ok
        # now rl: first determine sector
        sl[i] = xpout["r_cyl"][i, 1] // (np.pi / 9.0)
        # dPhi with respect to midlle of sector
        dPhi = xpout["r_cyl"][i, 1] - (sl[i] + 0.5) * (np.pi / 9.0)
        # x - length scale relative to middle of sector
        rl[i, 0] = dPhi * xpout["r_cyl"][i, 0]
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
