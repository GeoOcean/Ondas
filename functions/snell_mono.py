# /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

g = 9.81


# ---------------------------------------------------------------------------
# Teoría lineal
# ---------------------------------------------------------------------------

def waves_dispersion(T, h):
    '''
    Resuelve la ecuación de la dispersión  w^2 = g k tanh(kh)  (vectorizado).
    Input:   periodo T [s] y profundidad h [m] (escalares o arrays; h = np.inf para indefinidas)
    Returns: longitud de onda L [m], número de onda k [1/m] y celeridad C [m/s]
    '''
    T, h = np.broadcast_arrays(np.asarray(T, dtype=float), np.asarray(h, dtype=float))
    h = np.minimum(h, 1e5)  # profundidades indefinidas: se admite h = np.inf
    w = 2 * np.pi / T

    # Punto de partida: aproximación explícita de Guo (2002)
    x = w**2 * h / g
    k = x * (1 - np.exp(-x**1.25))**(-0.4) / h

    # Iteraciones de Newton-Raphson
    for _ in range(4):
        th = np.tanh(k * h)
        f = g * k * th - w**2
        df = g * th + g * k * h * (1 - th**2)
        k = k - f / df

    L = 2 * np.pi / k
    C = L / T

    if L.ndim == 0:
        return L.item(), k.item(), C.item()
    return L, k, C


def cg(L, T, h):
    'Celeridad de grupo. Input: longitud de onda, periodo, profundidad'
    k = 2 * np.pi / L
    kh2 = np.minimum(2 * k * h, 700)  # evita overflow en aguas profundas (n -> 0.5)
    n = 0.5 * (1 + kh2 / np.sinh(kh2))
    return n * L / T


def Ks(Cg0, Cg1):
    'Coeficiente de asomeramiento. Input: celeridad de grupo inicial y final'
    return np.sqrt(Cg0 / Cg1)


def Kr(theta_0, theta_1):
    'Coeficiente de refracción. Input: ángulo relativo inicial y final [º]'
    return np.sqrt(np.cos(np.deg2rad(theta_0)) / np.cos(np.deg2rad(theta_1)))


def theta(C0, C1, theta_0):
    'Ley de Snell. Input: celeridad inicial y final, ángulo relativo inicial [º]. Returns: ángulo relativo final [º]'
    return np.rad2deg(np.arcsin(C1 / C0 * np.sin(np.deg2rad(theta_0))))


def Goda(L0, hb, m):
    '''
    Criterio de rotura de Goda.
    Input: longitud de onda en profundidades indefinidas, profundidad, pendiente
    Returns: altura de ola de rotura
    '''
    return L0 * 0.17 * (1 - np.exp(-1.5 * np.pi * (hb / L0) * (1 + 15 * m**(4/3))))


def Iro(m, H, L0):
    'Número de Iribarren. Input: pendiente, altura de ola, longitud de onda en indefinidas'
    return m / (H / L0)**0.5


def snell_propagation(H_ini, T, theta_ini, h_ini, h_fin):
    '''
    Propaga un oleaje monocromático entre dos profundidades (batimetría recta y paralela)
    aplicando dispersión, ley de Snell, asomeramiento y refracción.
    Input:   H, T y ángulo relativo [º] en h_ini; profundidades inicial y final
    Returns: altura de ola y ángulo relativo [º] en h_fin
    '''
    L_i, _, C_i = waves_dispersion(T, h_ini)
    L_f, _, C_f = waves_dispersion(T, h_fin)

    theta_fin = theta(C_i, C_f, theta_ini)
    H_fin = H_ini * Ks(cg(L_i, T, h_ini), cg(L_f, T, h_fin)) * Kr(theta_ini, theta_fin)
    H_fin = np.where(np.asarray(H_ini) > 0, H_fin, 0.0)  # sin oleaje (p. ej. no incide en la costa)

    if H_fin.ndim == 0:
        return H_fin.item(), float(theta_fin)
    return H_fin, theta_fin


# ---------------------------------------------------------------------------
# Direcciones
# ---------------------------------------------------------------------------

def angle_diff(Dir, orientation):
    'Diferencia con signo Dir - orientation, en el rango [-180, 180)'
    return (np.asarray(Dir, dtype=float) - orientation + 180) % 360 - 180


def min_dist(angle1, angle2):
    'Distancia angular mínima entre dos direcciones [º] (entre 0 y 180)'
    return np.abs(angle_diff(angle2, angle1))


def calculate_Dir1(Dir_0, theta_1, orientation):
    '''
    Dirección absoluta del oleaje propagado.
    El oleaje se mantiene en el mismo lado de la normal a la playa que offshore.
    '''
    signo = np.where(angle_diff(Dir_0, orientation) < 0, -1, 1)
    return (orientation + signo * theta_1) % 360


# ---------------------------------------------------------------------------
# Propagación de series de oleaje (DataFrames)
# ---------------------------------------------------------------------------

def theta_0(df_waves, orientation):
    '''
    Ángulo relativo offshore (theta_0) respecto a la normal a la playa.
    Los estados de mar que no se dirigen hacia la costa (|theta_0| > 90º) se anulan (Hs = 0).
    '''
    df_waves['theta_0'] = min_dist(orientation, df_waves['Dir'].values)
    df_waves.loc[df_waves['theta_0'] > 90, 'Hs'] = 0

    return df_waves


def snell_mono_prop(df_waves, h0, h1, m, orientation):
    '''
    Propagación desde la profundidad offshore h0 hasta la profundidad objetivo h1.
    Columnas nuevas:
        H1       altura de ola propagada (sin rotura)
        H1_Goda  altura de ola limitada por el criterio de rotura de Goda
        L0       longitud de onda en profundidades indefinidas
        theta_1  ángulo relativo a la normal en h1 [º]
        Dir1     dirección del oleaje en h1 [º]
    '''
    T = df_waves['Tm'].values
    L0 = g * T**2 / (2 * np.pi)

    H1, theta_1 = snell_propagation(df_waves['Hs'].values, T, df_waves['theta_0'].values, h0, h1)

    df_waves['H1'] = H1
    df_waves['H1_Goda'] = np.minimum(H1, Goda(L0, h1, m))
    df_waves['L0'] = L0
    df_waves['theta_1'] = theta_1
    df_waves['Dir1'] = calculate_Dir1(df_waves['Dir'].values, theta_1, orientation)

    return df_waves


def snell_mono_prop_breaking(df_waves, h1, m, orientation):
    '''
    Propagación desde la profundidad objetivo h1 hasta la profundidad de rotura (columna 'hb').
    Columnas nuevas:
        Hb       altura de ola en rotura
        thetab   ángulo relativo a la normal en rotura [º]
        Dirb     dirección del oleaje en rotura [º]
    '''
    T = df_waves['Tm'].values

    Hb, thetab = snell_propagation(df_waves['H1_Goda'].values, T, df_waves['theta_1'].values,
                                   h1, df_waves['hb'].values)

    df_waves['Hb'] = Hb
    df_waves['thetab'] = thetab
    df_waves['Dirb'] = calculate_Dir1(df_waves['Dir'].values, thetab, orientation)

    return df_waves
