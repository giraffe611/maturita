
import pandas as pd
from geopy.geocoders import Nominatim
import time

# Tegyük fel, hogy van egy DataFrame-ed, pl.:
# df = pd.DataFrame({
#     "Név": ["Petőfi Sándor", "Arany János"],
#     "Születési dátum": ["1823-01-01", "1817-03-02"],
#     "Születési hely": ["Kiskőrös", "Nagyszalonta"]
# })
df = pd.read_excel("SlovakAuthors.xlsx")
dfSK = df[df['Country/region2'] == 'Slovakia']
#dfCZ = df[df['Country/region2'] == 'Czech Republic']
#dfAR = df[df['Country/region2'] == 'Argentina']
#dfUSA = df[df['Country/region2'] == 'United States']
#dfCR = df[df['Country/region2'] == 'Croatia']
#dfCAN = df[df['Country/region2'] == 'Canada']
#dfRU = df[df['Country/region2'] == 'Russia']
#dfA = df[df['Country/region2'] == 'Austria']
print(dfSK.head())
def add_coordinates(df, location_column="DiedCity"):
    geolocator = Nominatim(user_agent="hungarian_writers")
    latitudes = []
    longitudes = []

    for place in df[location_column]:
        try:
            location = geolocator.geocode(place + ", Slovakia")
            if location:
                latitudes.append(location.latitude)
                longitudes.append(location.longitude)
            else:
                latitudes.append(None)
                longitudes.append(None)
        except Exception:
            latitudes.append(None)
            longitudes.append(None)
        time.sleep(1)  # API túlterhelés elkerülése

    df["Latitude"] = latitudes
    df["Longitude"] = longitudes
    return df

# Használat:
dfSK = add_coordinates(dfSK)
dfSK.to_csv("szlovakSK_irok_koordinatakkal.csv", index=True)
