from datetime import datetime

def get_unique_list(serie):
    '''
    find unique element, and corresponding index, of a Serie with values of type List()
    
    input  : [serie]  : Serie with list for value (might be empty list
    output : [unique] : List of unique element in the Serie serie
             [idx]    : index of 1st row of serie containing the corresponding [unique] value
    '''
    unique = []
    idx = []
    for iiter, i in enumerate(serie.values):
        for j in i:
            if not (j in unique):
                unique.append(j)
                idx.append(iiter)
    return unique, idx


def get_week(dataframe, col):
    return dataframe[col].apply(lambda x: datetime.fromisoformat(x[:-7]).isocalendar()[1])

def get_month(dataframe, col):
    return dataframe[col].apply(lambda x: int(x[5:7]))