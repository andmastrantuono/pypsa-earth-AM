import pandas as pd
import pypsa
import os
import numpy as np

# === CONFIGURAZIONE DI BASE ===
network_path = "networks/elec_s_20.nc"
output_path = "data/custom_powerplants.csv"

# === PARAMETRI NUCLEARE ===
EFFICIENCY = 0.33
DATE_IN = 2030
DATE_OUT = 2090

# taglie MW
CAPACITY_LR = 1600     # 1.6 GW
CAPACITY_SMR = 400     # 0.4 GW

TECH_LR = "nuclear_lr"
TECH_SMR = "nuclear_smr"
FUELTYPE = "nuclear"


# === CARICA NETWORK ===
print(f"Loading network from: {network_path}")
n = pypsa.Network(network_path)

# selezione bus low-voltage
if "substation_lv" in n.buses.columns:
    buses_lv = n.buses.query("substation_lv")
else:
    buses_lv = n.buses.copy()

print(f"Found {len(buses_lv)} candidate buses.")


# === GENERAZIONE RIGHE ===
records = []

for bus, row in buses_lv.iterrows():

    # --------------------------
    # REATTORE LR (1.6 GW)
    # --------------------------
    records.append({
        "Name": f"Nuclear_LR_{bus}",
        "Fueltype": FUELTYPE,
        "Technology": TECH_LR,
        "Set": np.nan,
        "Country": row["country"],
        "Capacity": CAPACITY_LR,
        "Efficiency": EFFICIENCY,
        "Duration": np.nan,
        "Volume_Mm3": np.nan,
        "DamHeight_m": np.nan,
        "StorageCapacity_MWh": np.nan,
        "DateIn": DATE_IN,
        "DateRetrofit": np.nan,
        "DateOut": DATE_OUT,
        "lat": row["y"],
        "lon": row["x"],
        "EIC": np.nan,
        "projectID": np.nan,
        "bus": bus,
    })

    # --------------------------
    # REATTORE SMR (0.4 GW)
    # --------------------------
    records.append({
        "Name": f"Nuclear_SMR_{bus}",
        "Fueltype": FUELTYPE,
        "Technology": TECH_SMR,
        "Set": np.nan,
        "Country": row["country"],
        "Capacity": CAPACITY_SMR,
        "Efficiency": EFFICIENCY,
        "Duration": np.nan,
        "Volume_Mm3": np.nan,
        "DamHeight_m": np.nan,
        "StorageCapacity_MWh": np.nan,
        "DateIn": DATE_IN,
        "DateRetrofit": np.nan,
        "DateOut": DATE_OUT,
        "lat": row["y"],
        "lon": row["x"],
        "EIC": np.nan,
        "projectID": np.nan,
        "bus": bus,
    })


# === CONVERSIONE IN DATAFRAME ===
df = pd.DataFrame(records)

# ordine colonne richiesto da PyPSA-Earth
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
print(df.head(6))
