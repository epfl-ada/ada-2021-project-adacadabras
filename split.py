from datetime import datetime

def split_quotes_per_gender(chunk, df_selected_parquet, qid_male, qid_female, qids_others, qids_wrong):
    chunk['week']   = get_week(chunk, 'quoteID')
    chunk['month']  = get_month(chunk, 'quoteID')
    
    #_________________
    # SPEAKER NONE
    #`````````````````
    q_is_speaker_None = chunk.speaker=='None' # Checker auusi pou les NaN -> isna()
    q_noSpeaker       = chunk[ q_is_speaker_None].copy()
    q_speaker         = chunk[-q_is_speaker_None]
    q_speaker['qid'] = q_speaker.qids.apply(lambda x: x[0]) # 1st homonym
    q_speaker = q_speaker.drop(columns=['qids'])
    
    
    # Merge with Parquet
    q_speaker = q_speaker.merge(df_selected_parquet, left_on='qid', right_on='id', how='left')
    
    #______________
    # SPEAKER NO PARQUET
    #``````````````
    q_speaker_not_in_parquet = q_speaker.id.isna()
    q_speaker_noParquet  = q_speaker[q_speaker_not_in_parquet].copy()
    
    q_speaker  = q_speaker[-q_speaker_not_in_parquet]
    
    '''
    #__________________
    # SPEAKER NO LABEL
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
    
    #________________________________
    # MALE - FEMALE - OTHERS - WRONG - NOLABEL
    #````````````````````````````````
    q_is_gender_labeled = q_speaker.gender.isin(df_qid.QID)
    q_is_gender_male = q_speaker.gender.isin(qid_male)
    q_is_gender_female = q_speaker.gender.isin(qid_female)
    q_is_gender_others = q_speaker.gender.isin(qids_others)
    q_is_gender_wrong = q_speaker.gender.isin(qids_wrong)
    
    
    q_noLabel  = q_speaker[q_is_gender_labeled].copy()
    q_male     = q_speaker[q_is_gender_male].copy()
    q_female   = q_speaker[q_is_gender_female].copy()
    q_others   = q_speaker[q_is_gender_others].copy()
    q_wrong    = q_speaker[q_is_gender_wrong].copy()
    
    return q_male, q_female, q_others, q_wrong, q_noLabel, q_None, q_speaker_noParquet, q_noSpeaker
