def get_unique_list(serie):
    out = []
    for i in serie.values:
        for j in i:
            if not j in out:
                out.append(j)
    return out