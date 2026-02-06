import pandas as pd

def analyze_csv(file):
    df=pd.read_csv(file)

    summary={
        "total_equipment":int(len(df)),
        "average_flowrate":float(df["Flowrate"].mean()),
        "average_pressure":float(df["Pressure"].mean()),
        "average_temperature":float(df["Temperature"].mean()),
        "type_distribution":df["Type"].value_counts().to_dict()
    }
    return summary, df
