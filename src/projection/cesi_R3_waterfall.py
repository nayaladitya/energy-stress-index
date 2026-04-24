"""
F9 - R3 mechanism-attribution waterfall.
Decomposes the Central 2024-2050 CESI rise into contributions from
EROI, Demand, R/P, and residual/interaction using the causal-isolation scenarios.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

paths = pd.read_csv("C:/Users/OMU/Desktop/Energy/cesi_R3_paths.csv")
paths = paths.set_index("year")

cesi_2023 = 612.0  # historical anchor
central_2050 = paths.loc[2050, "Central"]
total_rise = central_2050 - cesi_2023

# Contribution of each mechanism = (Central rise) - (scenario with that mechanism frozen's rise)
# i.e., how much of Central's rise DISAPPEARS when we freeze that mechanism
c1_2050 = paths.loc[2050, "C1 EROI freeze"]
c2_2050 = paths.loc[2050, "C2 R/P stabilises"]
c3_2050 = paths.loc[2050, "C3 Demand plateau"]
c4_2050 = paths.loc[2050, "C4 All frozen"]

eroi_contrib   = (central_2050 - cesi_2023) - (c1_2050 - cesi_2023)   # rise removed by freezing EROI
rp_contrib     = (central_2050 - cesi_2023) - (c2_2050 - cesi_2023)   # rise removed by freezing R/P (negative = worsens)
demand_contrib = (central_2050 - cesi_2023) - (c3_2050 - cesi_2023)   # rise removed by freezing demand
interaction    = total_rise - (eroi_contrib + rp_contrib + demand_contrib)

labels = ["CESI 2023",
          "EROI decline\n(+%.0f)" % eroi_contrib,
          "Demand growth\n(+%.0f)" % demand_contrib,
          "R/P dynamics\n(%+.0f)" % rp_contrib,
          "Interaction /\nresidual (%+.0f)" % interaction,
          "CESI 2050\n(Central)"]

vals = [cesi_2023, eroi_contrib, demand_contrib, rp_contrib, interaction, central_2050]

# Waterfall geometry
fig, ax = plt.subplots(figsize=(11, 6.5))
x = np.arange(len(labels))
running = cesi_2023
bar_colors = []

# Start bar
ax.bar(0, cesi_2023, color="#4C72B0", edgecolor="black", linewidth=0.8)
ax.text(0, cesi_2023 + 40, f"{cesi_2023:.0f}", ha="center", fontsize=11, fontweight="bold")

# Increments
cum = cesi_2023
for i, (name, val) in enumerate(zip(labels[1:-1], vals[1:-1]), start=1):
    color = "#C44E52" if val > 0 else "#55A868"  # red = adds stress, green = removes
    bottom = cum if val >= 0 else cum + val
    ax.bar(i, abs(val), bottom=bottom, color=color, edgecolor="black", linewidth=0.8)
    mid = bottom + abs(val) / 2
    sign = "+" if val >= 0 else ""
    ax.text(i, bottom + abs(val) + 40, f"{sign}{val:.0f}", ha="center", fontsize=11, fontweight="bold")
    # connector line
    ax.plot([i - 0.4, i + 0.4], [cum + val, cum + val], color="grey", linestyle=":", linewidth=0.9)
    cum += val

# End bar
ax.bar(len(labels) - 1, central_2050, color="#4C72B0", edgecolor="black", linewidth=0.8)
ax.text(len(labels) - 1, central_2050 + 40, f"{central_2050:.0f}", ha="center", fontsize=11, fontweight="bold")

# Baseline connector
ax.plot([0 + 0.4, 1 - 0.4], [cesi_2023, cesi_2023], color="grey", linestyle=":", linewidth=0.9)

ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=10)
ax.set_ylabel("CESI (1980 = 100)", fontsize=11)
ax.set_title("R3: Mechanism attribution of the Central 2024–2050 CESI rise\n"
             "Within the CESI decomposition framework", fontsize=12, pad=12)
ax.grid(axis="y", linestyle="--", alpha=0.4)
_peak = max(cesi_2023 + eroi_contrib + demand_contrib, central_2050) + 250
ax.set_ylim(0, _peak)
ax.set_axisbelow(True)

# Caption
caption = (f"EROI decline contributes +{eroi_contrib:.0f} ({eroi_contrib/total_rise*100:.0f}% of total rise of {total_rise:.0f}); "
           f"demand growth +{demand_contrib:.0f} ({demand_contrib/total_rise*100:.0f}%); "
           f"R/P dynamics {rp_contrib:+.0f} ({rp_contrib/total_rise*100:+.0f}%). "
           "R/P contribution is negative because reserves grow modestly in the Central baseline, lifting R/P above 2023.")
fig.text(0.5, -0.02, caption, ha="center", fontsize=8.5, style="italic", wrap=True)

plt.tight_layout()
plt.savefig("C:/Users/OMU/Desktop/Energy/CESI_R3_waterfall.png", dpi=300, bbox_inches="tight")
plt.savefig("C:/Users/OMU/Desktop/Energy/CESI_R3_waterfall.svg", bbox_inches="tight")
print(f"Total rise: {total_rise:.0f}")
print(f"EROI: {eroi_contrib:.0f} ({eroi_contrib/total_rise*100:.0f}%)")
print(f"Demand: {demand_contrib:.0f} ({demand_contrib/total_rise*100:.0f}%)")
print(f"R/P: {rp_contrib:+.0f} ({rp_contrib/total_rise*100:+.0f}%)")
print(f"Interaction: {interaction:+.0f}")
print("Saved CESI_R3_waterfall.png / .svg")
