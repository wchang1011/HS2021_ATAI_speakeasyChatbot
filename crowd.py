# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 20:32:53 2021

@author: Wenqing
"""
## this file get all the crowd data
import pandas as pd
class crowd:
    ## read crowdsource data
    crowdSource = pd.read_csv('Dataset\\ATAI_crowd_data.tsv', sep='\t')
    
    ## filter out malicious workers
    workTime = crowdSource.filter(['HITId','WorkTimeInSeconds', 'WorkerId'],axis=1)
    malHits = workTime.loc[workTime.groupby('HITId')['WorkTimeInSeconds'].idxmin()]
    malWorkers = malHits['WorkerId'].unique()
    cleanCrowd = crowdSource
    for idx, malWk in enumerate(malWorkers):
        cleanCrowd = cleanCrowd.drop(cleanCrowd[(cleanCrowd['WorkerId'] == malWk)].index)
    
    ## aggregate worker answers and get the answer
    aggAns = cleanCrowd.groupby('HITId')['AnswerLabel'].agg(pd.Series.mode).to_frame()
    
    ## count number of pros and cons and compute inter-rater rate
    zdf = cleanCrowd.filter(['HITId','AnswerLabel'])
    numCnt = zdf.groupby('HITId')['AnswerLabel'].value_counts().to_frame()
    counts = zdf.groupby('HITId')['AnswerLabel'].value_counts('counts').to_frame()
    irate = counts.groupby('HITId')['AnswerLabel'].max()