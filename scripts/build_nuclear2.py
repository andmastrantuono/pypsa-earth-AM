import pandas as pd
import pypsa
import os
import numpy as np

# === CONFIGURAZIONE DI BASE ===
# percorso del network di base (adattalo se usi un altro RDIR)
network_path = "networks/elec_s_20.nc"
output_path = "data/custom_powerplants.csv"

# parametri del generatore nucleare
efficiency = 0.33
date_in = 2030
date_out = 2080
capacity_placeholder = 0.001  # MW
technology = "nuclear"
fueltype = "nuclear"

# === CARICA IL NETWORK ===
print(f"Loading network from: {network_path}")
n = pypsa.Network(network_path)

# filtra solo i bus "low voltage" (solitamente candidati per generazione)
if "substation_lv" in n.buses.columns:
    buses_lv = n.buses.query("substation_lv")
else:
    # fallback: tutti i bus terrestri
    buses_lv = n.buses.copy()

print(f"Found {len(buses_lv)} candidate buses.")

# === CREA IL DATAFRAME ===
df = pd.DataFrame({
    "Name": [f"Nuclear_{b}" for b in buses_lv.index],
    "Fueltype": fueltype,
    "Technology": technology,
    "Set": np.nan,
    "Country": buses_lv["country"].values,
    "Capacity": capacity_placeholder,
    "Efficiency": efficiency,
    "Duration": np.nan,
    "Volume_Mm3": np.nan,
    "DamHeight_m": np.nan,
    "StorageCapacity_MWh": np.nan,
    "DateIn": date_in,
    "DateRetrofit": np.nan,
    "DateOut": date_out,
    "lat": buses_lv["y"].values,
    "lon": buses_lv["x"].values,
    "EIC": np.nan,
    "projectID": np.nan,
    "bus": buses_lv.index.values,
})

# assicurati che le colonne siano nell’ordine corretto
cols = [
    "Name", "Fueltype", "Technology", "Set", "Country", "Capacity",
    "Efficiency", "Duration", "Volume_Mm3", "DamHeight_m",
    "StorageCapacity_MWh", "DateIn", "DateRetrofit", "DateOut",
    "lat", "lon", "EIC", "projectID", "bus"
]
df = df[cols]

# === SALVA ===
os.makedirs(os.path.dirname(output_path), exist_ok=True)
df.to_csv(output_path, index=False)

print(f"✅ File salvato in: {output_path}")
print(df.head(3))
