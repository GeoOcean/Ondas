# /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

from .snell_mono import g, waves_dispersion, Goda, Iro, snell_propagation


# ---------------------------------------------------------------------------
# Criterios de rotura: altura de ola máxima Hb posible en una profundidad h
# ---------------------------------------------------------------------------

def Hb_McCowan(h, gamma=0.78):
    'McCowan (1894): Hb = gamma * h'
    return gamma * h


def Hb_Miche(T, h):
    'Miche (1944): Hb = 0.142 L tanh(kh), con L la longitud de onda local'
    L = waves_dispersion(T, h)[0]
    return 0.142 * L * np.tanh(2 * np.pi * h / L)


def Hb_Goda(T, h, m):
    'Goda (1970): Hb = 0.17 L0 [1 - exp(-1.5 pi h/L0 (1 + 15 m^4/3))], con L0 en indefinidas'
    return Goda(g * T**2 / (2 * np.pi), h, m)


def Hb_Weggel(T, h, m):
    'Weggel (1972): Hb/hb = b - a Hb/(gT^2), despejando Hb'
    a = 43.8 * (1 - np.exp(-19 * m))
    b = 1.56 / (1 + np.exp(-19.5 * m))
    return b * h / (1 + a * h / (g * T**2))


def gamma_KaminskyKraus(m, H0, T):
    'Kaminsky y Kraus (1993): gamma_b = Hb/hb = 1.2 Ir^0.27, con Ir = m / sqrt(H0/L0) (H0 en indefinidas)'
    L0 = g * T**2 / (2 * np.pi)
    return 1.2 * Iro(m, H0, L0)**0.27


def hb_Goda_inversa(Hb, T, m, A=0.17):
    'Profundidad de rotura despejada del criterio de Goda a partir de la altura de rotura Hb'
    L0 = g * T**2 / (2 * np.pi)
    return -L0 / (1.5 * np.pi * (1 + 15 * m**(4/3))) * np.log(1 - Hb / (A * L0))


CRITERIOS = {
    'McCowan': lambda T, h, m: Hb_McCowan(h),
    'Miche':   lambda T, h, m: Hb_Miche(T, h),
    'Goda':    Hb_Goda,
    'Weggel':  Hb_Weggel,
}


# ---------------------------------------------------------------------------
# Profundidad de rotura
# ---------------------------------------------------------------------------

def hb_calculation_vec(H1, T, theta_1, h1, m, criterio='Goda', h_min=0.01, xtol=1e-6):
    '''
    Profundidad de rotura hb (vectorizado): punto en el que la altura de ola propagada con Snell
    desde h1 alcanza la altura de rotura del criterio elegido, H(hb) = Hb(hb).
    Input:  altura, periodo y ángulo relativo [º] en h1 (h1 = np.inf para indefinidas); pendiente;
            criterio de rotura ('McCowan', 'Miche', 'Goda', 'Weggel' o una función Hb(T, h, m))
    Returns: hb [m] (NaN si no hay oleaje)
    '''
    H1, T, theta_1, h1 = np.broadcast_arrays(*(np.asarray(v, dtype=float) for v in (H1, T, theta_1, h1)))
    Hb_criterio = criterio if callable(criterio) else CRITERIOS[criterio]

    def rompe(h):
        H, _ = snell_propagation(H1, T, theta_1, h1, h)
        return H >= Hb_criterio(T, h, m)

    # Bisección entre h_min (ha roto) y h1 (aún no ha roto)
    lo = np.full(H1.shape, float(h_min))
    hi = np.minimum(h1, 100.0)  # el oleaje no rompe a más de 100 m de profundidad
    for _ in range(int(np.ceil(np.log2(hi.max() / xtol)))):
        mid = 0.5 * (lo + hi)
        r = rompe(mid)
        lo = np.where(r, mid, lo)
        hi = np.where(r, hi, mid)
    hb = 0.5 * (lo + hi)

    hb = np.where(rompe(np.minimum(h1, 100.0)), h1, hb)   # ya ha roto antes de llegar a h1
    hb = np.where(H1 > 0, hb, np.nan)  # sin oleaje

    return hb
