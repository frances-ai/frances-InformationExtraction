import pandas as pd

def get_countries_geo(countries_simple_df, countries_details_df, countries_shapes_df) -> list[dict]:
    countries_info = []
    for index, row in countries_simple_df.iterrows():
        code = row['ISO']
        name = row['Country']
        capital = row['Capital']
        area = row['Area(in sq km)']
        population = row['Population']
        continent_code = row['Continent']
        geoname_id = row['geonameid']
        country = {
            'name': name,
            'capital': capital,
            'area': area,
            'population': population,
            'continent_code': continent_code,
            'geonameid': geoname_id,
            'code': code,
            "latitude": None,
            "longitude": None,
            "boundary": None
        }
        detail_info_df = countries_details_df[countries_details_df[0] == geoname_id]
        if len(detail_info_df) == 1:
            latitude = detail_info_df.iloc[0][4]
            longitude = detail_info_df.iloc[0][5]
            country['latitude'] = latitude
            country['longitude'] = longitude

            # add boundary
            boundary_df = countries_shapes_df[countries_shapes_df['geoNameId'] == geoname_id]
            if len(boundary_df) == 1:
                country["boundary"] = boundary_df.iloc[0]['geoJSON']

            countries_info.append(country)
        else:
            print(f"Failed to extract detail information for country: {name}, code: {code}")
    return countries_info

if __name__ == "__main__":
    # load countries simple info dataframe
    countries_simple_df = pd.read_csv("/Users/lilinyu/Documents/geonames/data/countryInfo.txt", delimiter='\t', keep_default_na=False)
    # load countries details dataframe
    countries_details_df = pd.read_csv('/Users/lilinyu/Documents/geonames/postgresql/data/allCountries.txt', delimiter='\t', header=None)
    # load boundary info
    countries_shapes_df = pd.read_csv("/Users/lilinyu/Documents/geonames/data/shapes_all_low.txt", delimiter='\t')
    countries_info = get_countries_geo(countries_simple_df, countries_details_df, countries_shapes_df)
    countries_info_df = pd.DataFrame(countries_info)
    countries_info_df.to_json("countries_info.json", orient='records', lines=True)
