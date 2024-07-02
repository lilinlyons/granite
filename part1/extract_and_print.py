import json
import pandas as pd

# Function to search for the correct dictionary in the json file to return based on id value
def find_dict_by_id(dicts, target_id):
    for dictionary in dicts:
        if dictionary['id'] == target_id:
            return dictionary
    return None


class ReturnJsonData:
    def __init__(self, id, subquery, list_of_dictionaries, columns):
        self.id = id
        self.columns = columns
        self.subquery = subquery
        self.dictionaries = list_of_dictionaries

    # Finding the right dictionary corresponding to the id value: geo, time or ranked
    def return_df(self):
        dict = find_dict_by_id(self.dictionaries, self.id)
        return dict

    # Geo and Time relationships nested in the same way so use the below
    # Subquery given as nesting for each element varies but at the same level for geo and time
    def filter_by_column(self):
        dict = self.return_df()['data']['default'][self.subquery]

        # conversion from dictionary to dataframe so columns can be filtered
        df = pd.DataFrame.from_dict(dict)
        df = df[self.columns]
        return df

    def filter_by_column_df_related(self):
        df_ranked = self.return_df()['data']['default'][self.subquery]
        data = []
        for i in df_ranked:
            # Conversion to pandas - data is more easily pivotable too once drilled down to correct level
            df = pd.DataFrame(i['rankedKeyword'])
            df_title = pd.DataFrame(df['topic'].tolist())

            df_combined = df.join(df_title)[self.columns]
            data.append(df_combined)

        df_related = pd.concat(data)
        return df_related



if __name__ == "__main__":
    # accessing json
    with open('AAL.json') as json_data:
        d = json.load(json_data)
    json_data.close()

    # extracting the different data dictionaries
    dictionaries = d['widgets']

    df_timeseries = ReturnJsonData('TIMESERIES', 'timelineData', dictionaries, columns = ['formattedTime', 'value']).filter_by_column()
    df_geo = ReturnJsonData('GEO_MAP', 'geoMapData', dictionaries, columns = ['geoName', 'value']).filter_by_column()
    df_related = ReturnJsonData('RELATED_TOPICS', 'rankedList', dictionaries, columns=['title', 'value', 'link']).filter_by_column_df_related()



