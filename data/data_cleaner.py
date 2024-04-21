import pandas as pd
'''This Python script is designed to clean data downloaded from the NYC Open Data portal. 
The cleaning process is outlined as follows:
1. Column Evaluation: We assess the columns in the original dataset and retain those that are relevant to our analysis.
2. Null Value Filtering and Date Simplification: We filter out any rows containing null values across all columns. Additionally, dates in the format of mm/dd/yyyy are simplified to retain only the month (mm).
3. Conversion to Dummy Values: The data is then transformed into dummy variables for further analysis.
'''

require_columns = [
    "ARREST_DATE","OFNS_DESC",
    "LAW_CAT_CD","ARREST_BORO","AGE_GROUP","PERP_SEX", "PERP_RACE"
]



def main():
    print("start")
    df = pd.read_csv("NYPD_Arrest_Data__Year_to_Date__20240418.csv")
    print(len(df))
    df = df[require_columns]
    df = df[df[require_columns].notnull().all(1)]
    # df['KY_CD'] = df['KY_CD'].apply(lambda x:str(int(x)))
    # df['ARREST_PRECINCT'] = df['ARREST_PRECINCT'].apply(lambda x:str(int(x)))
    df['ARREST_DATE'] = df['ARREST_DATE'].apply(lambda x: x[:2])
    df = pd.get_dummies(df)
    print(df.columns)
    df.to_csv('INTEGRATED-DATASET.csv', index=False)  

if __name__ == "__main__":
    main()