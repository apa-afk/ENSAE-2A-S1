def excel_fix(df):
    # Use the second row as column names
    df.columns = df.iloc[1]

    
    return df