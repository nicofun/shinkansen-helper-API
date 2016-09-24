from decimal import Decimal
def global_to_japan(wx, wy):
    jx = wy * 1.000106961 - wx * 0.000017467 - 0.004602017
    jy = wx * 1.000083049 + wy * 0.000046047 - 0.010041046

    mjx = int(jx * 3600 * 1000)
    mjy = int(jy * 3600 * 1000)

    return (mjx, mjy)


def japan_to_global(jx, jy):
    jx = Decimal(jx) / 3600000
    jy = Decimal(jy) / 3600000

    wx = Decimal(jy) - Decimal(jy) * Decimal(0.00010695) + Decimal(jx) * Decimal(0.000017464) + Decimal(0.0046017)
    wy = Decimal(jx) - Decimal(jy) * Decimal(0.000046038) - Decimal(jx) * Decimal(0.000083043) + Decimal(0.010040)

    return (float(wx), float(wy))
