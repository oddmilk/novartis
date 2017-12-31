def guruGroupby(data, groupvar, feats, namer):
        x1 = data.groupby(groupvar)[feats].sum().reset_index()
        x2 = data.groupby(groupvar).size().reset_index(name = namer)
        x3 = x1.merge(x2)
        return x3


def getPopContent(data, measure_by, N):
        x = data.sort_values(by = measure_by, ascending = False)[0:N]
        return x


def get_keymessage(df, list_km_cols):
        km = pd.unique(df[list_km_cols].values.ravel('K'))
        km_cleaned = [x for x in km if x != ' ']
        return km_cleaned


