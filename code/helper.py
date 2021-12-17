###
### IMPORTS
###
import bz2
import json
import pickle as pkl
import datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

from scipy import stats

font_size = 40
plt.rc('ytick', labelsize=font_size) #fontsize of the y tick labels
    

###
### CONSTANTES
###
CHUNK_SIZE = 1e5
    
### PATHs for dataset:
PATH_DATA = './../data/'
PATH_QUOTEBANK = PATH_DATA+'Quotebank/quotes-{}.json.bz2'
# Part 1.a)
PATH_QUOTE_WOMEN         = PATH_DATA+'Quotebank/quotes-{}-filtered.json.bz2'
PATH_QUOTE_WOMEN_MONTHLY = PATH_DATA+'Quotebank/quotes-{}-filtered/{}' # completed in function as it depend on month
PATH_QUOTE_METOO         = PATH_DATA+'Quotebank/metoo/quotes-{}-filtered_metoo.json.bz2'
PATH_QUOTE_METOO_MONTHLY = PATH_DATA+'Quotebank/metoo/quotes-{}-filtered_metoo/{}' # completed in function as it depend on month
# Part 1.b)
PATH_PARQUET = PATH_DATA+'parquet/'
PARQUET_FILE = PATH_DATA+'speaker_attributes.parquet'
WIKIDATA_LABELS_FILE = PATH_DATA+'wikidata_labels_descriptions_quotebank.csv.bz2'
PATH_DATA_GENDER = PATH_DATA+'Quotebank/genders.json.bz2'

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


# ======================================================================
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


# ======================================================================
def generate_data_monthly(src_path, dst_path, keywords):
    with bz2.open(path_to_quotes, 'rb') as s_file:
        for instance in s_file:
            instance = json.loads(instance)
            month = instance['date'][5:7]
            path_per_month = dst_path.format(month)
            with bz2.open(path_per_month, 'ab') as d_file:
                d_file.write((json.dumps(instance)+'\n').encode('utf-8'))


# ======================================================================
def generate_pickles(scr_path, dst_path, chunk_size=1e5):
    with bz2.open(dst_path, 'wb') as f:
        data_reader = pd.read_json(scr_path, lines=True, compression='bz2', chunksize=chunk_size)
        for chunk in data_reader:
            pkl.dump(chunk, f)


# ======================================================================
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


# ======================================================================
def get_week(dataframe, col):
    return dataframe[col].apply(lambda x: datetime.datetime.fromisoformat(x[:-7]).isocalendar()[1])


# ======================================================================
def get_month(dataframe, col):
    return dataframe[col].apply(lambda x: int(x[5:7]))


# ======================================================================
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


# ======================================================================
def split_quotes_per_gender(chunk, df_selected_parquet, qid_male, qid_female, qids_others, qids_wrong, df_weekly_count):
    ## To parse the full QuoteBank dataset:

    #| YEAR | SIZE [GB] |   QUOTES    |  TIME [min] |
    #|------|-----------|-------------|-------------|
    #| 2015 |    3.3    |  20'874'338 |     22      |
    #| 2016 |    2.3    |  13'862'129 |     20      |
    #| 2017 |    5.2    |  26'611'588 |     47      |
    #| 2018 |    4.8    |  27'228'451 |     46      |
    #| 2019 |    3.6    |  21'763'302 |     36      |
    #| 2020 |     .8    |   5'244'449 |      6      |
    #|------|-----------|-------------|-------------|
    #| SUM  |   20.0    | 115'584'257 |    177      |
    
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
    q_speaker_noParquet  = q_speaker[q_speaker_not_in_parquet]
    df_weekly_count.speaker_noParquet = df_weekly_count.speaker_noParquet.add(q_speaker_noParquet.week.value_counts(), fill_value=0)
    
    q_speaker  = q_speaker[-q_speaker_not_in_parquet]
    
    '''
    #__________________
    # SPEAKER NO LABEL    ---> "throw away" too much quotes where we might know the speaker gender -> keep them
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
    # MALE - FEMALE - OTHERS - WRONG
    #````````````````````````````````
    # NOLABELED gender are in OTHER - done in part 2) Parquet Analyse
    q_is_gender_male = q_speaker.gender.isin(qid_male)
    q_is_gender_female = q_speaker.gender.isin(qid_female)
    q_is_gender_others = q_speaker.gender.isin(qids_others)
    q_is_gender_wrong = q_speaker.gender.isin(qids_wrong)
    
    q_male     = q_speaker[q_is_gender_male]
    q_female   = q_speaker[q_is_gender_female]
    q_others   = q_speaker[q_is_gender_others]
    q_wrong    = q_speaker[q_is_gender_wrong]
    
    df_weekly_count.male = df_weekly_count.male.add(q_male.week.value_counts(), fill_value=0)
    df_weekly_count.female = df_weekly_count.female.add(q_female.week.value_counts(), fill_value=0)
    df_weekly_count.others = df_weekly_count.others.add(q_others.week.value_counts(), fill_value=0)
    df_weekly_count.wrong = df_weekly_count.wrong.add(q_wrong.week.value_counts(), fill_value=0)

    
    return q_male, q_female, q_others, q_wrong, q_None, q_speaker_noParquet, q_noSpeaker


# ======================================================================
def create_D2_male_2020(quote_column, df_selected_parquet, qid_male, qid_female, qids_others, qids_wrong, df_weekly_count):
    path = PATH_QUOTE_WOMEN.format(2020)
    reader = pd.read_json(path, lines=True, compression='bz2', chunksize=CHUNK_SIZE)

    for chunk in reader:
        chunk = chunk.filter(items=quote_column)
        q_male, _, _, _, _, _, _ = \
        split_quotes_per_gender(chunk, df_selected_parquet, qid_male, qid_female, qids_others, qids_wrong, df_weekly_count)

        # write a file for each month
        for month in q_male.month.unique():
            chunk_month = q_male[q_male.month==month]
            path_per_month = f'./../data/Quotebank/male_{month}.json.bz2'
            with bz2.open(path_per_month, 'ab') as month_file:
                chunk_month.to_json(path_per_month, orient='records', lines=True)

                
# ======================================================================
def create_weekly_count(path, idx_weekly, col_weekly, quote_column, df_selected_parquet, qid_male, qid_female, qids_others, qids_wrong, df_weekly_count):
    data_path = path.format(year)
    df_weekly_count = pd.DataFrame(0, index=idx_weekly, columns=col_weekly)
    reader = pd.read_json(data_path, lines=True, compression='bz2', chunksize=CHUNK_SIZE)
    
    for chunk in reader:
        chunk = chunk.filter(items=quote_column)
        split_quotes_per_gender(chunk, df_selected_parquet, qid_male, qid_female, qids_others, qids_wrong, df_weekly_count)

    # record count
    df_weekly_count.loc['sum'] = df_weekly_count.sum()
    df_weekly_count = df_weekly_count.astype(int)
    df_weekly_count.reset_index(inplace=True) # Json format do not like str index (last one is 'sum')
    df_weekly_count.rename(columns = {'index':'week'}, inplace = True)
    new_file_path = data_path[:-9] + '_weekly_count' + data_path[-9:]
    with bz2.open(new_file_path, 'wb') as file:
        df_weekly_count.to_json(file, orient='records', lines=True)


# ======================================================================
def csv_to_json(year):
    df = pd.read_csv(PATH_DATA + f'/counts/{year}_count.csv', index_col='Unnamed: 0')
    df.reset_index(inplace=True) # Json format do not like str index (last one is 'sum')
    df.rename(columns = {'index':'week'}, inplace = True)
    path_year = path_quotebank.format(year)
    path_data = path_year[:-9] + '_weekly_count' + path_year[-9:]
    with bz2.open(path_data, 'wb') as file: 
        df.to_json(file, orient='records', lines=True)

# ======================================================================
def add_weekly_percentage(path, year):
    path_year = path.format(year)
    path_data = path_year[:-9] + '_weekly_count' + path_year[-9:]
    df = pd.read_json(path_data, lines=True)
    df['male_female'] = df.male + df.female
    # Might have null denominator -> NAN
    df['percent_male']   = df.male/df.male_female
    df['percent_female'] = df.female/df.male_female
    df.drop(columns=['male_female'], inplace=True)
    with bz2.open(path_data, 'wb') as file:
        df.to_json(file, orient='records', lines=True)


# ======================================================================
def every_year_weekly_count(years, data_paths):
    plot_df_list = [] # correspond to dataset from previous line
    for data_path in data_paths:
        data_path = data_path[:-9] + '_weekly_count' + data_path[-9:]
        count_paths = [data_path.format(year) for year in years]
        df_counts = []
        for path in count_paths:
            df_counts.append(pd.read_json(path, lines=True).iloc[:-1].set_index('week'))

        df_all = pd.DataFrame()
        week53 = [0]*df_counts[0].shape[1]
        for df, year in zip(df_counts, years):
            df.iloc[0] = [sum(x) for x in zip(df.iloc[0], week53)]
            week53 = df.iloc[-1]
            df['year'] = year
            df['week'] = df.index
            df['idx'] = str(year) + ' - ' + df.index.astype(str)
            df_all = df_all.append(df.iloc[:-1]) # lost week 53 of last year (but as it ends at week 16: OK)
        plot_df_list.append(df_all.copy().set_index('idx'))
    return plot_df_list


# ======================================================================
def plot_count_log_scale(df):
    plt.rcParams['figure.figsize'] = (80,15)
    plt.xticks(rotation=90)
    
    # Vertical line to separate years
    plt.axvline(x=0) # 2015
    plt.axvline(x=52) # 2016
    plt.axvline(x=52*2) # 2017
    plt.axvline(x=52*3) # 2018
    plt.axvline(x=52*4) # 2019
    plt.axvline(x=52*5) # 2020
    # plot datas
    ax = sns.barplot(x=df.index, y=df.male,   label='male',   color='lightblue')
    ax = sns.barplot(x=df.index, y=df.female, label='female', color='lightpink')
    ax = sns.barplot(x=df.index, y=df.others, label='others')
    
    plt.yscale('log')
    plt.xlabel('Time', fontsize=font_size)
    plt.ylabel('Number of quotes', fontsize=font_size)
    plt.title('Distribution of quotes among genders per week', fontsize=font_size)
    plt.legend(fontsize=font_size)
    plt.show()


# ======================================================================
def plot_count_lin_scale(df):
    plt.rcParams['figure.figsize'] = (80,15)
    plt.xticks(rotation=90)
    
    # Vertical line to separate years
    plt.axvline(x=0) # 2015
    plt.axvline(x=52) # 2016
    plt.axvline(x=52*2) # 2017
    plt.axvline(x=52*3) # 2018
    plt.axvline(x=52*4) # 2019
    plt.axvline(x=52*5) # 2020
    
    ax = sns.barplot(x=df.index, y=df.male,   label='male',   color='lightblue')
    ax = sns.barplot(x=df.index, y=df.female, label='female', color='lightpink')
    plt.xticks(rotation=90)
    plt.xlabel('Time', fontsize=font_size)
    plt.ylabel('Number of quotes', fontsize=font_size)
    plt.legend(fontsize=font_size)
    
    ax2 = ax.twinx()
    ax2 = sns.lineplot(data=df.male/(df.male+df.female), linewidth=6) # can not directly take df.percent_male as week53 is summed with week1
    ax2 = sns.lineplot(data=df.female/(df.male+df.female), linewidth=6)
    plt.ylabel('proportion of male/female quotes', fontsize=font_size)
    
    
    plt.title('Distribution of male/female quotes percentage per week', fontsize=font_size)
    plt.show()


# ======================================================================
def create_compounds(sia, path, year, age_limite1, age_limite2, compound_limite, quote_column, df_selected_parquet):
    data_path = path.format(year)
    print(data_path)
    reader = pd.read_json(data_path, lines=True, compression='bz2', chunksize=CHUNK_SIZE)
    
    for chunk in reader:
        chunk = chunk.filter(items=quote_column)
        # remove unknown speaker
        q_is_speaker_None = chunk.speaker=='None'
        q_speaker         = chunk[-q_is_speaker_None].copy()
        q_speaker['qid'] = q_speaker.qids.apply(lambda x: x[0]) # 1st homonym
        q_speaker = q_speaker.drop(columns=['qids'])
        q_speaker = q_speaker.merge(df_selected_parquet, left_on='qid', right_on='id', how='left')

        # age
        q_is_speaker_DOB = q_speaker.date_of_birth.notna()
        q_speaker        = q_speaker[q_is_speaker_DOB]
        q_speaker['age']     = q_speaker.date_of_birth.apply(lambda x: year - int(x[0][1:5])) # we consider speaker is born the 01/01/XXXX - and article of year YYYY have been published the 01/01/YYYY
        q_speaker['age_cat'] = q_speaker.age.apply(lambda x: '0_40' if x <= age_limite1 else '41_60' if x <= age_limite2 else '61_inf')

        # sentiment
        q_speaker['compound']  = q_speaker.quotation.apply(lambda x: sia.polarity_scores(x)['compound'])
        q_speaker['sentiment'] = q_speaker.compound.apply(lambda x: 'neg' if x <= -compound_limite else 'neu' if x <= compound_limite else 'pos')

        # drop unused column
        q_speaker.drop(columns=['date_of_birth','id'], inplace=True)

        # record result
        new_file_path = data_path[:-9] + '_sentiment_age' + data_path[-9:]
        with bz2.open(new_file_path, 'ab') as file: ## Need to delete existing file as open in "Append" mode   --> !!! !!! !!! <--
            q_speaker.to_json(file, orient='records', lines=True)


# ======================================================================
def create_mean_compounds_per_gender_age(path, year, qid_male, qid_female):
    data_path = path.format(year)
    data_path = data_path[:-9] + '_sentiment_age' + data_path[-9:]
    reader = pd.read_json(data_path, lines=True, compression='bz2', chunksize=CHUNK_SIZE)
    i = 0
    for chunk in reader:
        chunk_is_gender = chunk.gender.notna()
        chunk = chunk[chunk_is_gender]
        chunk['gender'] = chunk.gender.apply(lambda x: x[0])
        q_male_female   = chunk[chunk.gender.isin(qid_male+qid_female)].copy()
        q_male_female.gender.replace([qid_male[0], qid_female[0]],['male','female'], inplace=True)

        # general : count and avg compound per gender per age_cat
        male_female_mean = q_male_female[['gender', 'age_cat', 'compound']].groupby(['gender','age_cat']).agg({'sum', 'count', 'std'})
        male_female_mean = male_female_mean.droplevel(0, axis=1) # drop "compounds" primary index
        # to compute the average std later (pooled variation)
        male_female_mean['std'] = male_female_mean['std']*male_female_mean['count']

        # detailed : count and agv compound per gender per age_cat per sentiment
        male_female = q_male_female[['gender', 'age_cat','sentiment', 'compound']].groupby(['sentiment','age_cat','gender']).agg({'sum', 'count', 'std'})
        male_female = male_female.droplevel(0, axis=1) # drop "compounds" primary index
        # to compute the average std later (pooled variation)
        male_female['std'] = male_female['std']*male_female['count']

        if i==0:
            df_compound_count_detail = male_female.copy()
            df_compound_count_general= male_female_mean.copy()
        else:
            df_compound_count_detail = df_compound_count_detail.add(male_female, fill_value=0)
            df_compound_count_general = df_compound_count_general.add(male_female_mean, fill_value=0)
        i += 1

    # general
    df_compound_count_general['mean'] = df_compound_count_general['sum']/df_compound_count_general['count']
    df_compound_count_general['std']  = df_compound_count_general['std']/df_compound_count_general['count']
    df_compound_count_general.drop(columns=['sum'], inplace=True)
    new_file_path_general = data_path[:-9] + '_compounds_per_gender_age' + data_path[-9:]
    with bz2.open(new_file_path_general, 'wb') as file:
        df_compound_count_general.reset_index().to_json(file, orient='records', lines=True)

    # detailed
    df_compound_count_detail['mean'] = df_compound_count_detail['sum']/df_compound_count_detail['count']
    df_compound_count_detail['std']  = df_compound_count_detail['std']/df_compound_count_detail['count']
    df_compound_count_detail.drop(columns=['sum'], inplace=True)
    new_file_path_detail = data_path[:-9] + '_compounds_per_gender_age_sentiment' + data_path[-9:]
    with bz2.open(new_file_path_detail, 'wb') as file:
        df_compound_count_detail.reset_index().to_json(file, orient='records', lines=True)


# ======================================================================
#### read this ######
def create_mean_compound_at_date(path, year, date):
    day = date[0]
    month = date[1]
    data_path = path.format(year)
    data_path = data_path[:-9] + '_sentiment_age' + data_path[-9:]
    reader = pd.read_json(data_path, lines=True, compression='bz2', chunksize=CHUNK_SIZE)
    i = 0
    for chunk in reader:
        begin_chunk = time()

        chunk_is_gender = chunk.gender.notna()
        chunk = chunk[chunk_is_gender]
        chunk['gender'] = chunk.gender.apply(lambda x: x[0])
        q_male_female   = chunk[chunk.gender.isin(qid_male+qid_female)].copy()
        q_male_female.gender.replace([qid_male[0], qid_female[0]],['male','female'], inplace=True)

        # Keep only quotes which are close to selected date
        date_event_begin = datetime.datetime(year, month, day)
        date_event1_end = datetime.datetime(year, month, day+4)
        is_consider = (q_male_female.date>=date_event_begin) & (q_male_female.date<=date_event1_end)
        q_male_female = q_male_female[is_consider]

        # general : count and avg compound per gender per age cat
        male_female_mean = q_male_female[['gender', 'age_cat', 'compound']].groupby(['gender','age_cat']).agg({'sum', 'count', 'std'})
        male_female_mean = male_female_mean.droplevel(0, axis=1)
        male_female_mean['std'] = male_female_mean['std']*male_female_mean['count']


        # detailed : count and agv compound per gender per age cat per sentiment
        male_female = q_male_female[['gender', 'age_cat','sentiment', 'compound']].groupby(['sentiment','age_cat','gender']).agg({'sum', 'count', 'std'})
        male_female = male_female.droplevel(0, axis=1)
        male_female['std'] = male_female['std']*male_female['count']


        if i==0:
            df_compound_count_detail = male_female.copy()
            df_compound_count_general= male_female_mean.copy()
        else:
            df_compound_count_detail = df_compound_count_detail.add(male_female, fill_value=0)
            df_compound_count_general = df_compound_count_general.add(male_female_mean, fill_value=0)
        i += 1

    # general : count and avg compound per gender per age cat
    df_compound_count_general['mean'] = df_compound_count_general['sum']/df_compound_count_general['count']
    df_compound_count_general['std']  = df_compound_count_general['std']/df_compound_count_general['count']
    df_compound_count_general.drop(columns=['sum'], inplace=True)
    new_file_path_general = data_path[:-9] + f'_compounds_per_gender_age_{day}_{month}' + data_path[-9:]
    with bz2.open(new_file_path_general, 'wb') as file:
        df_compound_count_general.reset_index().to_json(file, orient='records', lines=True)

    # detailed
    df_compound_count_detail['mean'] = df_compound_count_detail['sum']/df_compound_count_detail['count']
    df_compound_count_detail['std']  = df_compound_count_detail['std']/df_compound_count_detail['count']
    df_compound_count_detail.drop(columns=['sum'], inplace=True)
    new_file_path_detail = data_path[:-9] + f'_compounds_per_gender_age_sentiment_{day}_{month}' + data_path[-9:]
    with bz2.open(new_file_path_detail, 'wb') as file:
        df_compound_count_detail.reset_index().to_json(file, orient='records', lines=True)
        
        
        
        
###
### T-test
###

# ======================================================================
def ttest_list_general(years, qid_male, qid_female):
    # one element per year
    male_per_age_lst     = [[],[],[]] # 1st dim: age category | 2nd dim: year
    female_per_age_lst   = [[],[],[]]
    
    for i, year in enumerate(years):
        data_path = PATH_QUOTE_WOMEN.format(year)
        path = data_path[:-9] + '_sentiment_age' + data_path[-9:]
        df = pd.read_json(path, lines=True)[['gender','age_cat','compound', 'sentiment']]
        df_is_gender = df.gender.notna()
        df = df[df_is_gender]
        df['gender'] = df.gender.apply(lambda x: x[0])
        df_male_female   = df[df.gender.isin(qid_male+qid_female)].copy()
        df_male_female.gender.replace([qid_male[0], qid_female[0]],['male','female'], inplace=True)

        # mask per category
        mask_male   = df_male_female.gender=='male'
        mask_female = df_male_female.gender=='female'
        mask_0_40   = df_male_female.age_cat=='0_40'
        mask_41_60  = df_male_female.age_cat=='41_60'
        mask_61_inf = df_male_female.age_cat=='61_inf'
        # add to list
        male_per_age_lst[0].append(df_male_female[mask_male & mask_0_40])
        male_per_age_lst[1].append(df_male_female[mask_male & mask_41_60])
        male_per_age_lst[2].append(df_male_female[mask_male & mask_61_inf])
        female_per_age_lst[0].append(df_male_female[mask_female & mask_0_40])
        female_per_age_lst[1].append(df_male_female[mask_female & mask_41_60])
        female_per_age_lst[2].append(df_male_female[mask_female & mask_61_inf])
    
    # T-test: for Male
    p_male = [[],[],[]] # 1st dim: per age category  -      0_40       |       41_60      |      61_inf
                        # 2dn dim: year comparaison  - (2015 vs 2017)  |  (2017 vs 2019)  |  (2015 vs 2019)
                        # exemple : p_male[1][0] is male_41_60, 2015 vs 2017
    for i,male in enumerate(male_per_age_lst):
        for j, _ in enumerate(years):
            first_year = j
            second_year = (first_year+1)%len(years)
            p_male[i].append(stats.ttest_ind(male[first_year].compound, male[second_year].compound))
    
    # T-test: for Female
    p_female = [[],[],[]] # same as for p_male
    for i,female in enumerate(female_per_age_lst):
        for j, _ in enumerate(years):
            first_year = j
            second_year = (first_year+1)%len(years)
            p_female[i].append(stats.ttest_ind(female[first_year].compound, female[second_year].compound))
    
    return p_male, p_female


# ======================================================================
def ttest_list_for_date(years, chosen_date, qid_male, qid_female):
    # one element per year
    male_per_age_lst     = [[],[],[]] # one list per age category
    female_per_age_lst   = [[],[],[]]
    
    for year in years:
        data_path = PATH_QUOTE_WOMEN.format(year)
        path = data_path[:-9] + '_sentiment_age' + data_path[-9:]
        df = pd.read_json(path, lines=True)[['date','gender','age_cat','compound', 'sentiment']]
        df_is_gender = df.gender.notna()
        df = df[df_is_gender]
        df['gender'] = df.gender.apply(lambda x: x[0])
        df_male_female   = df[df.gender.isin(qid_male+qid_female)].copy()
        df_male_female.gender.replace([qid_male[0], qid_female[0]],['male','female'], inplace=True)
        
        # Keep only quote of date date
        date = datetime.datetime(year, chosen_date[1], chosen_date[0]) # year, month, day
        is_consider = df_male_female.date.apply(lambda x: x.date())==date.date()
        df_male_female = df_male_female[is_consider]
        
    
        # mask per category
        mask_male   = df_male_female.gender=='male'
        mask_female = df_male_female.gender=='female'
        mask_0_40   = df_male_female.age_cat=='0_40'
        mask_41_60  = df_male_female.age_cat=='41_60'
        mask_61_inf = df_male_female.age_cat=='61_inf'
        # add to list
        male_per_age_lst[0].append(df_male_female[mask_male & mask_0_40])
        male_per_age_lst[1].append(df_male_female[mask_male & mask_41_60])
        male_per_age_lst[2].append(df_male_female[mask_male & mask_61_inf])
        female_per_age_lst[0].append(df_male_female[mask_female & mask_0_40])
        female_per_age_lst[1].append(df_male_female[mask_female & mask_41_60])
        female_per_age_lst[2].append(df_male_female[mask_female & mask_61_inf])
    
    # T-test: for Male
    p_male = [[],[],[]] # 1st dim: per age category  -      0_40       |       41_60      |      61_inf
                        # 2dn dim: year comparaison  - (2015 vs 2017)  |  (2017 vs 2019)  |  (2015 vs 2019)
                        # exemple : p_male[1][0] is male_41_60, 2015 vs 2017
    for i,male in enumerate(male_per_age_lst):
        for j, _ in enumerate(years):
            first_year = j
            second_year = (first_year+1)%len(years)
            p_male[i].append(stats.ttest_ind(male[first_year].compound, male[second_year].compound))
    
    # T-test: for Female
    p_female = [[],[],[]] # same as for p_male
    for i,female in enumerate(female_per_age_lst):
        for j, _ in enumerate(years):
            first_year = j
            second_year = (first_year+1)%len(years)
            p_female[i].append(stats.ttest_ind(female[first_year].compound, female[second_year].compound))
    
    return p_male, p_female


# ======================================================================
def print_p_values_comp(p_male, p_female):
    print('| gender |    age   ||  2015 vs 2017  |  2017 vs 2019  |  2015 vs 2019  |',
      '|'+'-'*8+'|'+'-'*10+'||'+'-'*16+'|'+'-'*16+'|'+'-'*16+'|',
      '|        |  0 -> 40 ||' + ' '*6 + f'{p_male[0][0].pvalue:.2g}'+' '*6+'|'+ ' '*6 + f'{p_male[0][1].pvalue:.2g}'+' '*6+'|'+ ' '*6 + f'{p_male[0][2].pvalue:.2g}'+' '*6+'|',
      '|  male  | 41 -> 60 ||' + ' '*5 + f'{p_male[1][0].pvalue:.2g}'+' '*5+'|'+ ' '*6 + f'{p_male[1][1].pvalue:.2g}'+' '*5+'|'+ ' '*6 + f'{p_male[1][2].pvalue:.2g}'+' '*6+'|',
      '|        | 61 -> ++ ||' + ' '*6 + f'{p_male[2][0].pvalue:.2g}'+' '*6+'|'+ ' '*5 + f'{p_male[2][1].pvalue:.2g}'+' '*4+'|'+ ' '*5 + f'{p_male[2][2].pvalue:.2g}'+' '*4+'|',
      '|'+'-'*8+'|'+'-'*10+'||'+'-'*16+'|'+'-'*16+'|'+'-'*16+'|',
      '|        |  0 -> 40 ||' + ' '*4 + f'{p_female[0][0].pvalue:.2g}'+' '*5+'|'+ ' '*5 + f'{p_female[0][1].pvalue:.2g}'+' '*4+'|'+ ' '*4 + f'{p_female[0][2].pvalue:.2g}'+' '*5+'|',
      '| female | 41 -> 60 ||' + ' '*4 + f'{p_female[1][0].pvalue:.2g}'+' '*5+'|'+ ' '*5 + f'{p_female[1][1].pvalue:.2g}'+' '*4+'|'+ ' '*5 + f'{p_female[1][2].pvalue:.2g}'+' '*6+'|',
      '|        | 61 -> ++ ||' + ' '*6 + f'{p_female[2][0].pvalue:.2g}'+' '*6+'|'+ ' '*5 + f'{p_female[2][1].pvalue:.2g}'+' '*4+'|'+ ' '*5 + f'{p_female[2][2].pvalue:.2g}'+' '*5+'|',
      sep='\n')