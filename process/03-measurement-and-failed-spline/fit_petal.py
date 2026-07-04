import numpy as np

def cubic_bezier(p0, p1, p2, p3, n=200):
    t = np.linspace(0, 1, n)[:, None]
    return (1-t)**3*np.array(p0) + 3*(1-t)**2*t*np.array(p1) + 3*(1-t)*t**2*np.array(p2) + t**3*np.array(p3)

def petal_path(L, w, f, desc=0.3, tipctrl=0.15, base_ctrl=0.55, rise=0.55):
    py = -L * f
    p_base = (0, 0)
    p_peak = (-w, py)
    p_tip = (0, -L)
    c1 = (-w*base_ctrl, 0)
    c2 = (-w, py*rise)
    curve1 = cubic_bezier(p_base, c1, c2, p_peak)
    c3 = (-w, py + (-L - py) * desc)
    c4 = (-w*tipctrl, -L)
    curve2 = cubic_bezier(p_peak, c3, c4, p_tip)
    return np.vstack([curve1, curve2[1:]])

def width_profile(curve, radii):
    ys = -curve[:, 1]  # radius
    xs = np.abs(curve[:, 0])
    out = []
    for r in radii:
        w = np.interp(r, ys, xs)
        out.append(w)
    return out

def path_string(L, w, f, desc, tipctrl, base_ctrl=0.55, rise=0.55):
    py = -L * f
    c1 = (-w*base_ctrl, 0)
    c2 = (-w, py*rise)
    c3 = (-w, py + (-L - py) * desc)
    c4 = (-w*tipctrl, -L)
    return (
        f"M 0,0 "
        f"C {c1[0]:.2f},{c1[1]:.2f} {c2[0]:.2f},{c2[1]:.2f} {-w:.2f},{py:.2f} "
        f"C {c3[0]:.2f},{c3[1]:.2f} {c4[0]:.2f},{c4[1]:.2f} 0,{-L:.2f} "
        f"C {-c4[0]:.2f},{c4[1]:.2f} {-c3[0]:.2f},{c3[1]:.2f} {w:.2f},{py:.2f} "
        f"C {-c2[0]:.2f},{c2[1]:.2f} {-c1[0]:.2f},{c1[1]:.2f} 0,0 "
        f"Z"
    )

if __name__ == "__main__":
    dark_target = [(30,20.9),(40,27.9),(50,34.9),(60,27.2),(70,24.6),(80,19.1),(85,14.8),(88,10.0)]
    light_target = [(60,2.2),(70,9.7),(80,19.8),(90,35.8),(100,30.7),(110,26.4),(120,18.2),(130,13.0),(136,7.2)]

    best = None
    for f in [0.5, 0.55, 0.6]:
        for desc in [0.1, 0.15, 0.2, 0.25, 0.3]:
            for tipctrl in [0.05, 0.1, 0.15, 0.2]:
                curve = petal_path(90, 35, f, desc, tipctrl)
                radii = [r for r,_ in dark_target]
                pred = width_profile(curve, radii)
                err = sum((p-t)**2 for p,(_,t) in zip(pred, dark_target))
                if best is None or err < best[0]:
                    best = (err, f, desc, tipctrl, pred)
    print("DARK best:", best[:4])
    print(" pred:", [round(v,1) for v in best[4]])
    print(" target:", [t for _,t in dark_target])

    best_l = None
    for f in [0.55, 0.6, 0.65, 0.7]:
        for desc in [0.1, 0.15, 0.2, 0.25, 0.3]:
            for tipctrl in [0.05, 0.1, 0.15, 0.2]:
                curve = petal_path(138, 36, f, desc, tipctrl)
                radii = [r for r,_ in light_target]
                pred = width_profile(curve, radii)
                err = sum((p-t)**2 for p,(_,t) in zip(pred, light_target))
                if best_l is None or err < best_l[0]:
                    best_l = (err, f, desc, tipctrl, pred)
    print("LIGHT best:", best_l[:4])
    print(" pred:", [round(v,1) for v in best_l[4]])
    print(" target:", [t for _,t in light_target])
