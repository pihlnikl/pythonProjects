#!/usr/bin/env python3
import pandas as pd
from sklearn.linear_model import LinearRegression

def split_date(df):
    d = df['Päivämäärä'].str.split(expand=True)
    d.columns = ['Weekday', 'Day', 'Month', 'Year', 'Hour']
 
    h2m = d['Hour'].str.split(':', expand=True)
    d['Hour'] = h2m.iloc[:, 0]

    day = {'ma':'Mon', 'ti':'Tue', 'ke':'Wed', 'to':'Thu', 'pe':'Fri', 'la':'Sat','su':'Sun'}
    d['Weekday'] = d['Weekday'].map(day)

    val = {'tammi':1, 'helmi':2, 'maalis':3, 'huhti':4, 'touko':5, 'kesä':6, 'heinä':7, 'elo':8, 'syys':9, 'loka':10, 'marras':11, 'joulu':12}
    d['Month'] = d['Month'].map(val)

    d = d.astype({"Weekday": object, "Day": float, "Month": float, "Year": float, "Hour": float})
 
    return d

def split_date_continues():
    dataC = pd.read_csv("src/Helsingin_pyorailijamaarat.csv", sep=";")
    d = split_date(dataC)
    df = dataC.drop('Päivämäärä', axis=1)

    return pd.concat([d, df], axis=1)

def cycling_weather():
    df_c = split_date_continues()
    res = df_c.groupby(['Year', 'Month', 'Day']).sum()
    res = res.drop(['Hour'], axis=1)
    res = res.loc[(2017),:,:]
    res = res.reset_index()

    df_w = pd.read_csv("src/kumpula-weather-2017.csv", sep=",")
    m = pd.merge(df_w,res, left_on=['Year','m','d'],right_on=['Year','Month','Day'])
    m = m.drop(['Time zone','m','d','Time'],axis=1)
    m = m.fillna(method = 'ffill')
    return m


def cycling_weather_continues(station):
    df = cycling_weather()
    x = df[['Precipitation amount (mm)', 'Snow depth (cm)', 'Air temperature (degC)']]
    y = df[[station]]

    model = LinearRegression(fit_intercept=True)
    model.fit(x, y)
    score = round(model.score(x,y),2)
    return model.coef_[0], score
    
def main():
    station = 'Baana'
    ans = cycling_weather_continues(station)
    a,b,c = ans[0]
    score = ans[1]
    print(f"Measuring station: {station}")
    print(f"Regression coefficient for variable 'precipitation': {a:.1f}")
    print(f"Regression coefficient for variable 'snow depth': {b:.1f}")
    print(f"Regression coefficient for variable 'temperature': {c:.1f}")
    print(f"Score: {score}")

if __name__ == "__main__":
    main()
