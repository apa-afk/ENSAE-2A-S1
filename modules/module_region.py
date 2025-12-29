def excel_fix(df):
    # header is on row 1
    df.columns = df.iloc[1].astype(str)

    # clean column names:
    # - keep first column as-is (region)
    # - clean years: remove * and force string
    cols = df.columns.tolist()
    cols[1:] = [str(int(float(c.replace("*", "").strip()))) for c in cols[1:]]
    df.columns = cols

    # keep data rows
    df = df.iloc[2:].reset_index(drop=True)
    df = df.iloc[:17].copy()

    # rename first column
    df = df.rename(columns={df.columns[0]: "region"})

    # clean region names
    df["region"] = df["region"].astype(str).str.strip()

    # normalize TOTAL
    df["region"] = df["region"].replace({
        "NOMBRE TOTAL": "TOTAL",
        "MONTANT TOTAL": "TOTAL"
    })

    region_order = [
        "ILE-DE-FRANCE",
        "CENTRE VAL DE LOIRE",
        "BOURGOGNE FRANCHE COMTE",
        "NORMANDIE",
        "HAUTS DE FRANCE",
        "GRAND EST",
        "PAYS DE LA LOIRE",
        "BRETAGNE",
        "NOUVELLE AQUITAINE",
        "OCCITANIE",
        "AUVERGNE RHONE ALPES",
        "PROVENCE-ALPES-COTE -D'AZUR",
        "CORSE",
        "OUTRE-MER",
        "RÉSIDENTS ÉTRANGERS",
        "TOTAL",
    ]

    region_id_map = {name: i + 1 for i, name in enumerate(region_order)}
    df["region_id"] = df["region"].map(region_id_map)

    # drop unmapped rows + force int
    df = df[df["region_id"].notna()].copy()
    df["region_id"] = df["region_id"].astype(int)

    # reorder columns
    cols = ["region_id", "region"] + [c for c in df.columns if c not in ["region_id", "region"]]
    df = df[cols]

    return df





def compute_richesse(df1_fixed, df2_fixed):
    # copy structure
    richesse_df = df2_fixed.copy()

    # numeric part: all columns except region_id and region
    value_cols = richesse_df.columns[2:]

    # element-wise division
    richesse_df[value_cols] = df2_fixed[value_cols] / df1_fixed[value_cols]

    return richesse_df

