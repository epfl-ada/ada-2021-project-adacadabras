import bz2
import json
import pickle as pkl
from datetime import datetime
import pandas as pd

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
def generate_data_keyword(src_path, dst_path, keywords):
    with bz2.open(src_path, 'rb') as s_file:
        with bz2.open(dst_path, 'wb') as d_file:
            for instance in s_file:
                instance = json.loads(instance)
                quote = str(instance['quotation']).lower()
                for word in keywords:
                    if word in f' {quote} ':
                        d_file.write((json.dumps(instance)+'\n').encode('utf-8'))
                        break


def generate_data_monthly(src_path, dst_path, keywords):
    with bz2.open(path_to_quotes, 'rb') as s_file:
        for instance in s_file:
            instance = json.loads(instance)
            month = instance['date'][5:7]
            path_per_month = dst_path.format(month)
            with bz2.open(path_per_month, 'ab') as d_file:
                d_file.write((json.dumps(instance)+'\n').encode('utf-8'))


def generate_pickles(scr_path, dst_path, chunk_size=1e5):
    with bz2.open(dst_path, 'wb') as f:
        data_reader = pd.read_json(scr_path, lines=True, compression='bz2', chunksize=chunk_size)
        for chunk in data_reader:
            pkl.dump(chunk, f)


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


def gender_in_parquet(df_parquet, df_qid):
    # Keep the metadata from parquet where a gender is defined (i.e. not None)
    df_parquet_gender_noNa = df_parquet.dropna(subset=['gender'])

    # Creating lists of unique QID's for genders
    unique_gender_id, unique_speaker_index = get_unique_list(df_parquet_gender_noNa.gender)
    speakers_gender_qid = pd.DataFrame({'qids': unique_gender_id}) # sometimes, there are many genders for a speaker -> consider all of them

    # Genders that are in parquet file and Quotebank
    df_gender = df_qid[df_qid.QID.isin(speakers_gender_qid.qids)]

    # Genders of speaker that are in Quotebank but NOT defined in the wikidata labels file
    df_gender_ko = speakers_gender_qid[-speakers_gender_qid.qids.isin(df_gender.QID)]
    
    gender_names, gender_qids, speaker_qids, gender_description = [], [], [], []
    count_not_rep = 0
    for i in unique_speaker_index:
        for j in df_parquet_gender_noNa.gender.iloc[i]:
            speaker_qids.append(df_parquet_gender_noNa.id.iloc[i])
            gender_qids.append(j)
            gender_name = df_qid[df_qid.QID == j].Label.values
            if len(gender_name)>0:
                gender_names.append(gender_name[0])
                gender_description.append(df_qid[df_qid.QID == j].Description.values[0])
            else:
                count_not_rep += 1
                gender_names.append(f'--> Not repertiored [{count_not_rep}] ???')
                gender_description.append('-')

    return pd.DataFrame({'gender_names':gender_names, 'gender_qids':gender_qids, 'speaker_qids':speaker_qids, 'description': gender_description})\
                            .groupby('gender_names').agg('first')
    


def split_quotes_per_gender(chunk, df_selected_parquet, df_qid, qid_male, qid_female, qids_others, qids_wrong, df_weekly_count):
    chunk['week']   = get_week(chunk, 'quoteID')
    chunk['month']  = get_month(chunk, 'quoteID')
    
    #_____
    # ALL
    #`````
    df_weekly_count['all'] = df_weekly_count['all'].add(chunk.week.value_counts(), fill_value=0)
    
    #_________________
    # SPEAKER NONE
    #`````````````````
    q_is_speaker_None = chunk.speaker=='None' # Checker auusi pou les NaN -> isna()
    q_noSpeaker       = chunk[ q_is_speaker_None].copy()
    q_speaker         = chunk[-q_is_speaker_None].copy()
    q_speaker['qid'] = q_speaker.qids.apply(lambda x: x[0]) # 1st homonym
    q_speaker = q_speaker.drop(columns=['qids'])
    
    df_weekly_count.speaker_None = df_weekly_count.speaker_None.add(q_noSpeaker.week.value_counts(), fill_value=0)
    
    # Merge with Parquet
    q_speaker = q_speaker.merge(df_selected_parquet, left_on='qid', right_on='id', how='left')
    
    #______________
    # SPEAKER NO PARQUET
    #``````````````
    q_speaker_not_in_parquet = q_speaker.id.isna()
    q_speaker_noParquet  = q_speaker[q_speaker_not_in_parquet].copy()
    df_weekly_count.speaker_noParquet = df_weekly_count.speaker_noParquet.add(q_speaker_noParquet.week.value_counts(), fill_value=0)
    
    q_speaker  = q_speaker[-q_speaker_not_in_parquet]
    
    '''
    #__________________
    # SPEAKER NO LABEL    -> throw away too much quotes where we might know the speaker gender -> keep them
    #``````````````````
    q_is_speaker_labeled = q_speaker.qid.isin(df_qid.QID)
    q_speaker_noLabel = q_speaker[ -q_is_speaker_labeled]
    q_speaker = q_speaker[ q_is_speaker_labeled]
    '''
    
    #______
    # NONE
    #``````
    q_gender_None = q_speaker.gender.isna()
    q_None    = q_speaker[ q_gender_None].copy()
    q_speaker = q_speaker[-q_gender_None]
    
    q_speaker['gender'] = q_speaker.gender.apply(lambda x: x[0]) # keep only 1st gender
    df_weekly_count.none = df_weekly_count.none.add(q_None.week.value_counts(), fill_value=0)

    
    
    #________________________________
    # MALE - FEMALE - OTHERS - WRONG - NOLABEL
    #````````````````````````````````
    q_is_gender_labeled = q_speaker.gender.isin(df_qid.QID)  # should normaly always be empty by constrution (to verify)
    q_is_gender_male = q_speaker.gender.isin(qid_male)
    q_is_gender_female = q_speaker.gender.isin(qid_female)
    q_is_gender_others = q_speaker.gender.isin(qids_others)
    q_is_gender_wrong = q_speaker.gender.isin(qids_wrong)
    
    
    q_noLabel  = q_speaker[-q_is_gender_labeled]
    q_male     = q_speaker[q_is_gender_male]
    q_female   = q_speaker[q_is_gender_female]
    q_others   = q_speaker[q_is_gender_others]
    q_wrong    = q_speaker[q_is_gender_wrong]
    
    df_weekly_count.noLabel = df_weekly_count.noLabel.add(q_noLabel.week.value_counts(), fill_value=0)
    df_weekly_count.male = df_weekly_count.male.add(q_male.week.value_counts(), fill_value=0)
    df_weekly_count.female = df_weekly_count.female.add(q_female.week.value_counts(), fill_value=0)
    df_weekly_count.others = df_weekly_count.others.add(q_others.week.value_counts(), fill_value=0)
    df_weekly_count.wrong = df_weekly_count.wrong.add(q_wrong.week.value_counts(), fill_value=0)

    
    return q_male, q_female, q_others, q_wrong, q_noLabel, q_None, q_speaker_noParquet, q_noSpeaker