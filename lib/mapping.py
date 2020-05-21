import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
import contextily as ctx
from mplcairo import operator_t
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import patheffects
import cartopy.crs as ccrs
import numpy as np
from math import floor
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from matplotlib.lines import Line2D
import string

mpl.rc("font", family="DejaVu Sans")


def replace_legend_items(legend, mapping):
    for txt in legend.texts:
        k = txt.get_text()
        try:
            txt.set_text(mapping[int(float(k))])
        except ValueError:
            pass


def crop(ax, factor_top, factor_right, factor_bottom, factor_left):
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    new_lim_left = (xlim[0] + xlim[1]) / 2 + np.array((-0.5, 0.5)) * (
        xlim[1] - xlim[0]
    ) * (factor_left)
    new_lim_right = (xlim[0] + xlim[1]) / 2 + np.array((-0.5, 0.5)) * (
        xlim[1] - xlim[0]
    ) * (factor_right)
    new_lim_bottom = (ylim[0] + ylim[1]) / 2 + np.array((-0.5, 0.5)) * (
        ylim[1] - ylim[0]
    ) * (factor_bottom)
    new_lim_top = (ylim[0] + ylim[1]) / 2 + np.array((-0.5, 0.5)) * (
        ylim[1] - ylim[0]
    ) * (factor_top)

    new_lim_left = tuple(new_lim_left)
    new_lim_right = tuple(new_lim_right)
    new_lim_top = tuple(new_lim_top)
    new_lim_bottom = tuple(new_lim_bottom)

    new_ylim = (new_lim_bottom[0], new_lim_top[1])
    new_xlim = (new_lim_left[0], new_lim_right[1])

    ax.set_xlim(new_xlim)
    ax.set_ylim(new_ylim)


def get_bins(df, column, k=5):
    min_v = df[column].min()
    max_v = df[column].max()

    array = []

    for i in range(k + 1):
        step = max_v / (k + 1)
        array.append(round(step * (i + 1), 0))
    return array


def get_quantiles(df, column, k=5):
    step = 1 / k
    quantiles = []
    for i in range(k + 1):
        quantile_at_step = df[column].quantile(step * i)
        quantiles.append(quantile_at_step)
    return quantiles


def utm_from_lon(lon):
    """
    utm_from_lon - UTM zone for a longitude

    Not right for some polar regions (Norway, Svalbard, Antartica)

    :param float lon: longitude
    :return: UTM zone number
    :rtype: int
    """
    return floor((lon + 180) / 6) + 1


def scale_bar(
    ax, proj, length, location=(0.5, 0.04), linewidth=3, units="km", m_per_unit=1000
):

    # find lat/lon center to find best UTM zone
    x0, x1, y0, y1 = ax.get_extent(proj.as_geodetic())
    # Projection in metres
    utm = ccrs.UTM(utm_from_lon((x0 + x1) / 2))
    # Get the extent of the plotted area in coordinates in metres
    x0, x1, y0, y1 = ax.get_extent(utm)
    # Turn the specified scalebar location into coordinates in metres
    sbcx, sbcy = x0 + (x1 - x0) * location[0], y0 + (y1 - y0) * location[1]
    # Generate the x coordinate for the ends of the scalebar
    bar_xs = [sbcx - length * m_per_unit / 2, sbcx + length * m_per_unit / 2]
    # buffer for scalebar
    # buffer = [patheffects.withStroke(linewidth=5, foreground="w")]
    # Plot the scalebar with buffer
    ax.plot(
        bar_xs,
        [sbcy, sbcy],
        transform=utm,
        color="k",
        linewidth=linewidth,
        # path_effects=buffer,
    )
    # buffer for text
    # buffer = [patheffects.withStroke(linewidth=3, foreground="w")]
    # Plot the scalebar label
    t0 = ax.text(
        sbcx,
        sbcy,
        str(length) + " " + units,
        transform=utm,
        horizontalalignment="center",
        verticalalignment="bottom",
        # path_effects=buffer,
        zorder=2,
    )
    left = x0 + (x1 - x0) * (location[0] - 0.12)
    # Plot the N arrow
    t1 = ax.text(
        left,
        sbcy,
        u"\u25B2\nN",
        transform=utm,
        horizontalalignment="center",
        verticalalignment="center",
        # path_effects=buffer,
        zorder=2,
    )

    # Plot the scalebar without buffer, in case covered by text buffer
    ax.plot(
        bar_xs, [sbcy, sbcy], transform=utm, color="k", linewidth=linewidth, zorder=3
    )


def anotate_lotes(ax, plt, lotes_empreendimentos):
    count = 0
    for idx, row in lotes_empreendimentos.iterrows():
        count += 1
        ax.text(
            row.coords[0],
            row.coords[1],
            s=str(count),
            horizontalalignment="center",
            bbox={"facecolor": "none", "edgecolor": "none"},
        )


def anotate_bairros(ax, plt, bairros_recorte, x, y):
    dict_letters = dict(enumerate(string.ascii_uppercase, 1))
    count = 0
    full_string = ""
    for idx, row in bairros_recorte.iterrows():
        count += 1

        ax.text(
            float(row.coordsX),
            float(row.coordsY),
            s=dict_letters[count],
            horizontalalignment="right",
            verticalalignment="top",
            bbox={"facecolor": "none", "edgecolor": "none"},
        )

        full_string += "{0}- {1} \n".format(dict_letters[count], row["NM_BAIRRO"])

    full_string = full_string[:-2]

    plt.annotate(
        full_string, (x, y), xycoords="figure fraction", backgroundcolor="w", alpha=0.7
    )
