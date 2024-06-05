import seaborn as sns
from dfpac import settings
from dfpac.utils.misc import shorten
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator

PALETTE = {"RV-based": "#888888", "Likelihood-based": "#33A4AC"}


def plot_discovery_curves(
    df,
    height=4,
    aspect=1.0,
    filename=None,
    top=0.88,
    bottom=0.1,
):
    df = df.copy()

    g = sns.FacetGrid(
        df,
        col="Species",
        col_wrap=5,
        height=height,
        aspect=aspect,
        sharex=False,
        sharey=False,
        despine=False,
        legend_out=False,
    )

    methods = list(PALETTE.keys())
    species = [shorten(s) for s in settings.SPECIES]

    g = g.map(
        sns.lineplot,
        "Pre-clinical trials",
        "Antigens Discovered",
        "Method",
        hue_order=methods,
        palette=PALETTE,
    )

    g.set_titles(template="{col_name}")

    axes = g.axes.flatten()
    for i, ax in enumerate(axes):
        species_data = df[df.Species == species[i]].reset_index(drop=True)
        ax.yaxis.set_major_locator(MaxNLocator(integer=True))
        px = species_data["Pre-clinical trials"].max()
        py = species_data["Antigens Discovered"].max()
        ax.axline((0.0, 0.0), (px, py), linestyle="--", c="k")

    handles = g._legend_data.values()
    labels = g._legend_data.keys()
    g.figure.legend(handles=handles, labels=labels, loc="lower center", ncol=len(methods))
    g.figure.subplots_adjust(top=top, bottom=bottom)

    if filename is not None:
        # plt.tight_layout()
        fig = plt.gcf()
        fig.savefig(filename)
