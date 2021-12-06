from datetime import datetime

################################################### Keywords for data filtering #########################################
# Talking about women, general women terminology
general_dict = set(['woman', 'women', ' she ', ' she.', ' her ', ' her.', 'girl', 'daughter', 'mother',
                    'sister', 'niece', 'female', 'wife', 'spouse', 'mistress', ' aunt ', ' aunt.', ' aunts ', ' aunts.',
                    ' mom ', ' mom.', ' moms ', ' moms.', ' mum ', ' mum.', ' mums ', ' mums.', ' femme ', ' femme.', 'grandma',
                    ' lady ', ' lady.', ' ladies ', ' ladies.', ' panty ', ' panty.', ' panties ', ' panties.',
                    'madam', ' ms.', ' mrs.', ' ms ', ' mrs ', ' maid ', ' maid.', ' maids ', ' maids.', ' bride ', ' bride.', ' brides ',
                    ' brides.', ' chick ', ' bridesmaid ', ' bridesmaid.', ' bridesmaids ', ' bridesmaids.',
                    ' chick.', ' chicks ', ' chicks.', " she's ", " her's "
                    ])

# Feminine-biased nouns and substrings (Disclaimer: this doesn’t reflect our team’s gender views.)
adj_dict = set(['slut', 'gold digger', 'bitch', 'prostitut', 'bimbo', 'actress',
                ' queen ', ' queen. ', ' queens ', ' queens. ', 'princess', 'whore', ' loca ', 'goddess', 'maiden', ' loca.'
                ' petite ', ' petite.', ' petites ', ' petites.', 'duchess', 'lesbian', 'fashionista', 'doll',
                'nymph', 'cougar', 'milf', 'virgin'])

# Verbs related to women
verb_dict = set(['marri', 'sleep with', 'marry', 'abortion', 'birth control'])

# Terms/actions associated both to MeToo movement and women’s datasets
action_dict = set(['harrass', ' rape ',' rape.',' raped ',' raped.', ' rapes ', ' rapes.', ' rapist ', ' rapist.', ' raping ', ' raping.',
                   'sex', 'domestic violence', 'domestic abuse', 'misogyn'])

# MeToo dictionary
metoo_dict = set(['metoo', 'femin', 'feminism', 'feminist'])

# Personnality MeToo dictionnary
people_dict = set(['harvey weinstein', 'bill cosby', 'tarana burke', 'ambra gutierrez',
                   'anastasia melnichenko', 'alyssa milano', 'r. kelly', 'r kelly','rob kelly', 'robert kelly',
                   'larry nassar', 'reith raniere', 'allison mack',
                   'claude arnault'])

keywords = general_dict\
    .union(adj_dict)\
    .union(verb_dict)\
    .union(action_dict)\
    .union(metoo_dict)\
    .union(people_dict)

################################################# Helper functions ############################################


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
