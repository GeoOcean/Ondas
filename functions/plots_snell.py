# /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from IPython.display import HTML

COLORES_CRIT = {'McCowan': '#1f77b4', 'Miche': '#9467bd', 'Goda': '#2ca02c', 'Weggel': '#ff7f0e',
                'Kaminsky-Kraus': '#d62728'}

COLOR_COSTA = '#e9d8a6'


def _costa(ax, Lx, Ly, texto=True):
    'Franja de arena bajo y = 0'
    ax.axhspan(-0.04 * Ly / 1000, 0, color=COLOR_COSTA)
    if texto:
        ax.text(Lx / 2000, -0.02 * Ly / 1000, 'COSTA', ha='center', va='center', fontsize=11, fontweight='bold',
                color='#7a5c00')


def plot_batimetria(x, y, h, m, Dir0, niveles=(2, 5, 10, 20)):
    '''
    Mapa de la batimetría con la dirección del oleaje incidente.
    Input: ejes x, y [m], profundidad h(y) [m], pendiente m, dirección de procedencia Dir0 [º],
           batimétricas a dibujar [m]
    '''
    Lx, Ly = x[-1], y[-1]
    h2d = np.tile(h[:, None], (1, len(x)))

    fig, ax = plt.subplots(figsize=(12, 6))
    pc = ax.pcolormesh(x / 1000, y / 1000, -h2d, cmap='Blues_r', shading='auto')
    ax.contour(x / 1000, y / 1000, h2d, levels=list(niveles), colors='k', linewidths=0.6)
    for hv in niveles:
        ax.text(0.99 * Lx / 1000, hv / m / 1000, f'{hv} m', ha='right', va='bottom', fontsize=8)
    _costa(ax, Lx, Ly)

    # Flecha con la dirección de propagación offshore
    prop = np.radians(Dir0 + 180)
    x0, y0 = 0.2 * Lx / 1000, 0.85 * Ly / 1000
    largo = 0.12 * Lx / 1000
    ax.annotate('', xy=(x0 + largo * np.sin(prop), y0 + largo * np.cos(prop)), xytext=(x0, y0),
                arrowprops=dict(arrowstyle='-|>', lw=3, color='crimson', mutation_scale=20))
    ax.text(x0, y0 + 0.04 * Ly / 1000, f'Oleaje de {Dir0}º', color='crimson', fontweight='bold', ha='center')
    ax.annotate('N', xy=(0.95 * Lx / 1000, 0.97 * Ly / 1000), xytext=(0.95 * Lx / 1000, 0.82 * Ly / 1000),
                ha='center', fontsize=12, fontweight='bold', arrowprops=dict(arrowstyle='-|>', color='k'))

    fig.colorbar(pc, ax=ax, label='Cota [m]')
    ax.set_xlabel('x (Este) [km]')
    ax.set_ylabel('y (Norte) [km]')
    ax.set_ylim(-0.04 * Ly / 1000, Ly / 1000)
    ax.set_aspect('equal')
    ax.set_title('Batimetría y dirección del oleaje incidente')
    plt.show()


def plot_altura_perfil(y, m, H, H_goda, H0, y_h1=None):
    '''
    Altura de ola a lo largo del perfil en función de la distancia a la costa.
    Input: distancia a la costa y [m], pendiente m (para el eje de profundidades);
           altura propagada con Snell sin rotura H [m] y limitada con el criterio de Goda H_goda [m];
           altura offshore H0 [m]; distancia a la costa de la profundidad objetivo h1 [m] (opcional)
    '''
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.plot(y, H, c='grey', lw=1.8, ls='--', label='H propagada con Snell (sin rotura)')
    ax.plot(y, H_goda, c='#1d6fa3', lw=2.5, label='H limitada por rotura (Goda)')
    ax.axhline(H0, c='k', lw=1, ls=':', label=f'H offshore = {H0} m')
    ax.set_ylim(0, 1.3 * np.nanmax(H_goda))

    # Inicio de la rotura: primer punto (desde mar adentro) en el que Goda limita la altura
    rota = ~np.isclose(H, H_goda)
    if rota.any():
        y_rot = y[rota].max()
        ax.axvline(y_rot, c='crimson', lw=1.5, ls='--')
        ax.text(y_rot, 0.97 * ax.get_ylim()[1], f' rotura\n y ≈ {y_rot:.0f} m', color='crimson', va='top', fontsize=9)
    if y_h1 is not None:
        ax.axvline(y_h1, c='grey', lw=1, ls=':')
        ax.text(y_h1, 0.97 * ax.get_ylim()[1], ' h1', color='grey', va='top')

    ax.invert_xaxis()  # mar adentro a la izquierda, costa a la derecha
    ax.set_xlabel('Distancia a la costa [m]')
    ax.set_ylabel('Altura de ola H [m]')
    prof = ax.secondary_xaxis('top', functions=(lambda d: d * m, lambda hh: hh / m))
    prof.set_xlabel('Profundidad h [m]')
    ax.grid(alpha=0.3)
    ax.legend(loc='lower left')
    ax.set_title('Altura de ola hacia la costa', pad=28)
    plt.show()


def plot_perfil_propagacion(y, L, C, theta, Ks, Kr, y_h1=None):
    '''
    Evolución hacia la costa de L y C, del ángulo θ y de los coeficientes Ks y Kr.
    Input: distancia a la costa y [m]; L [m], C [m/s], |θ| [º], Ks y Kr en cada punto;
           distancia a la costa de la profundidad objetivo h1 [m] (opcional)
    '''
    fig, axs = plt.subplots(1, 3, figsize=(16, 4.5), sharex=True)
    ykm = y / 1000

    axs[0].plot(ykm, L, c='#1d6fa3', lw=2)
    axs[0].set_ylabel('Longitud de onda L [m]')
    ax2 = axs[0].twinx()
    ax2.plot(ykm, C, c='#d95f02', lw=2, ls='--')
    ax2.set_ylabel('Celeridad C [m/s]', color='#d95f02')
    axs[0].set_title('Dispersión: la onda se frena y se acorta')

    axs[1].plot(ykm, theta, c='#4daf4a', lw=2)
    axs[1].set_ylabel('|θ| respecto a la normal [º]')
    axs[1].set_title('Refracción: el oleaje gira hacia la normal')

    axs[2].plot(ykm, Ks, c='#1d6fa3', lw=2, label='Ks (asomeramiento)')
    axs[2].plot(ykm, Kr, c='#4daf4a', lw=2, label='Kr (refracción)')
    axs[2].plot(ykm, Ks * Kr, c='k', lw=2, ls='--', label='Ks · Kr')
    axs[2].set_ylabel('Coeficiente [-]')
    axs[2].set_ylim(0, 2)
    axs[2].legend()
    axs[2].set_title('Coeficientes de propagación')

    for ax in axs:
        if y_h1 is not None:
            ax.axvline(y_h1 / 1000, c='grey', lw=1, ls=':')
        ax.set_xlabel('Distancia a la costa [km]')
        ax.grid(alpha=0.3)
    axs[0].invert_xaxis()  # mar adentro a la izquierda, costa a la derecha
    if y_h1 is not None:
        axs[0].text(y_h1 / 1000, axs[0].get_ylim()[1], ' h1', va='top', color='grey')
    plt.tight_layout()
    plt.show()


def plot_rotura_criterios(y, h, H_snell, tabla_rotura, criterios, T, m, colores=COLORES_CRIT):
    '''
    Altura propagada con Snell frente a la altura de rotura de cada criterio (zoom a la zona de rotura).
    Input: distancia a la costa y [m], profundidad h [m], altura propagada H_snell [m];
           tabla_rotura (índice = criterio, columnas 'Distancia a costa [m]' y 'Hb');
           criterios: diccionario {nombre: Hb(T, h, m)}; periodo T [s]; pendiente m
    '''
    fig, ax = plt.subplots(figsize=(14, 6))
    zona = y <= 1.6 * tabla_rotura['Distancia a costa [m]'].max()

    ax.plot(y[zona], H_snell[zona], c='k', lw=2.5, label='H propagada (Snell)')
    for criterio, fila in tabla_rotura.iterrows():
        col = colores[criterio]
        ax.plot(y[zona], criterios[criterio](T, h[zona], m), c=col, lw=1.5, ls='--', label=f'Hb {criterio}')
        ax.plot(fila['Distancia a costa [m]'], fila['Hb'], 'o', ms=10, color=col, mec='white', mew=1.5, zorder=5)

    ax.set_ylim(0, 1.5 * H_snell[zona].max())
    ax.invert_xaxis()
    ax.set_xlabel('Distancia a la costa [m]')
    ax.set_ylabel('Altura de ola [m]')
    ax.set_title('El oleaje rompe donde la altura propagada corta la curva de cada criterio')
    ax.grid(alpha=0.3)
    ax.legend(ncol=2)
    plt.show()


def plot_barras_rotura(tabla_rotura, colores=COLORES_CRIT):
    '''
    Distancia a la costa, profundidad y altura de rotura de cada criterio (barras).
    Input: tabla_rotura (índice = criterio, columnas 'Distancia a costa [m]', 'hb' y 'Hb')
    '''
    fig, axs = plt.subplots(1, 3, figsize=(15, 4), sharey=True)
    cols = [colores[n] for n in tabla_rotura.index]
    for ax, var, titulo in zip(axs, ['Distancia a costa [m]', 'hb', 'Hb'],
                               ['Distancia a la costa [m]', 'Profundidad de rotura hb [m]', 'Altura de rotura Hb [m]']):
        ax.barh(tabla_rotura.index, tabla_rotura[var], color=cols)
        for j, v in enumerate(tabla_rotura[var]):
            ax.text(v, j, f' {v:.2f}', va='center', fontsize=9)
        ax.set_title(titulo)
        ax.set_xlim(0, 1.2 * tabla_rotura[var].max())
        ax.grid(axis='x', alpha=0.3)
    axs[0].invert_yaxis()
    plt.tight_layout()
    plt.show()


def plot_planta(x, y, h, S, x_inicio, desplaz, tabla_rotura, colores=COLORES_CRIT):
    '''
    Vista en planta: crestas (S = 2πn), rayos y líneas de rotura, con un zoom a la zona de rompientes.
    Input: ejes x, y [m], profundidad h(y) [m], fase S(x, y); puntos de partida de los rayos x_inicio [m]
           y su desplazamiento lateral desplaz(y) [m]; tabla_rotura (columna 'Distancia a costa [m]')
    '''
    Lx, Ly = x[-1], y[-1]
    h2d = np.tile(h[:, None], (1, len(x)))
    zoom_y = 2.2 * tabla_rotura['Distancia a costa [m]'].max() / 1000
    zoom_x = 2.5 * zoom_y

    fig, axs = plt.subplots(2, 1, figsize=(13, 14), gridspec_kw=dict(height_ratios=[2.2, 1.6]))
    for ax in axs:
        pc = ax.pcolormesh(x / 1000, y / 1000, -h2d, cmap='Blues_r', shading='auto', vmin=-1.3 * h.max(), vmax=0)
        ax.contour(x / 1000, y / 1000, S, levels=np.arange(0, S.max(), 2 * np.pi), colors='#0b3c5d', linewidths=0.9)
        for x_i in x_inicio:
            ax.plot((x_i + desplaz) / 1000, y / 1000, c='crimson', lw=1, alpha=0.8)
        for nombre, fila in tabla_rotura.iterrows():
            ax.axhline(fila['Distancia a costa [m]'] / 1000, c=colores[nombre], lw=2.5, ls='--',
                       label=f'Rotura {nombre}')
        _costa(ax, Lx, Ly, texto=False)
        ax.set_aspect('equal')
        ax.set_xlabel('x (Este) [km]')
        ax.set_ylabel('y (Norte) [km]')

    axs[0].set_xlim(0, Lx / 1000)
    axs[0].set_ylim(-0.04 * Ly / 1000, Ly / 1000)
    axs[0].add_patch(plt.Rectangle((0, 0), zoom_x, zoom_y, fill=False, ec='k', lw=1.5, ls=':'))
    axs[0].set_title('Crestas (azul oscuro), rayos (rojo) y líneas de rotura')

    axs[1].set_xlim(0, zoom_x)
    axs[1].set_ylim(-0.08 * zoom_y, zoom_y)
    axs[1].legend(loc='upper right', fontsize=9, framealpha=0.9)
    axs[1].set_title('Zoom a la zona de rompientes')

    fig.colorbar(pc, ax=axs, label='Cota [m]', shrink=0.6)
    plt.show()


def animacion_superficie(x, y, S, H, T, y_b, criterio, n_frames=24, paso=3, zoom=True):
    '''
    Animación de la superficie libre  η(x, y, t) = H(y)/2 · cos(S(x, y) - ωt)  durante un periodo.
    Input: ejes x, y [m], fase S(x, y), altura de ola H(y) [m], periodo T [s];
           distancia a la costa de la rotura y_b [m] y nombre del criterio (para la etiqueta);
           número de fotogramas y submuestreo espacial;
           zoom=True añade un segundo panel ampliado en la zona de rompientes (a resolución completa)
    Returns: animación en HTML
    '''
    Lx, Ly = x[-1], y[-1]
    omega = 2 * np.pi / T
    vlim = H.max() / 2
    H2d = np.tile(H[:, None], (1, len(x)))

    # Paneles: dominio completo (submuestreado) y, opcionalmente, zoom a la zona de rompientes
    paneles = [(slice(None, None, paso), slice(None, None, paso))]
    zoom_y = 3 * y_b
    zoom_x = min(2.5 * zoom_y, Lx)
    if zoom:
        paneles.append((slice(0, np.searchsorted(y, zoom_y) + 1), slice(0, np.searchsorted(x, zoom_x) + 1)))

    alturas = [Ly / Lx] + ([zoom_y * 1.08 / zoom_x] if zoom else [])
    fig, axs = plt.subplots(len(paneles), 1, figsize=(11, 9.2 * sum(alturas) + 0.8 * len(paneles)),
                            gridspec_kw=dict(height_ratios=alturas), squeeze=False)
    axs = axs[:, 0]

    ims, datos = [], []
    for ax, (sy, sx) in zip(axs, paneles):
        Ss, Hs = S[sy, sx], H2d[sy, sx]
        im = ax.pcolormesh(x[sx] / 1000, y[sy] / 1000, Hs / 2 * np.cos(Ss), cmap='RdBu_r', vmin=-vlim, vmax=vlim,
                           shading='auto')
        ims.append(im)
        datos.append((Ss, Hs))
        ax.axhline(y_b / 1000, c='k', lw=1.5, ls='--')
        ax.text(0.01 * x[sx][-1] / 1000, y_b / 1000, f'rotura ({criterio})', va='bottom', fontsize=9, fontweight='bold',
                bbox=dict(fc='white', ec='none', alpha=0.8, pad=1.5))
        _costa(ax, Lx, Ly, texto=False)
        ax.set_aspect('equal')
        ax.set_xlabel('x (Este) [km]')
        ax.set_ylabel('y (Norte) [km]')

    axs[0].set_xlim(0, Lx / 1000)
    axs[0].set_ylim(-0.04 * Ly / 1000, Ly / 1000)
    if zoom:
        axs[0].add_patch(plt.Rectangle((0, 0), zoom_x / 1000, zoom_y / 1000, fill=False, ec='k', lw=1.5, ls=':'))
        axs[1].set_xlim(0, zoom_x / 1000)
        axs[1].set_ylim(-0.08 * zoom_y / 1000, zoom_y / 1000)
        axs[1].set_title('Zoom a la zona de rompientes')
    fig.colorbar(ims[0], ax=axs, label='η [m]', shrink=0.6)
    titulo = axs[0].set_title('')

    def actualizar(i):
        t = i * T / n_frames
        for im, (Ss, Hs) in zip(ims, datos):
            im.set_array((Hs / 2 * np.cos(Ss - omega * t)).ravel())
        titulo.set_text(f'Superficie libre η   ·   t = {t:4.1f} s')
        return (*ims, titulo)

    anim = animation.FuncAnimation(fig, actualizar, frames=n_frames, interval=120, blit=False)
    plt.close(fig)
    return HTML(anim.to_jshtml())
