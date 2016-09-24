def global_to_japan(wx, wy):
    jx = wy * 1.000106961 - wx * 0.000017467 - 0.004602017
    jy = wx * 1.000083049 + wy * 0.000046047 - 0.010041046

    mjx = int(jx * 3600 * 1000)
    mjy = int(jy * 3600 * 1000)

    return (mjx, mjy)
