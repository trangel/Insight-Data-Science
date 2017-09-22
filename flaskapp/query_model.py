from collections import defaultdict
from gensim import corpora, models, similarities
from operator import itemgetter

def filter_posts(sims,readability_fname):
    import pandas as pd
    from operator import itemgetter

    r_score_min = 8.0 #  filter minimum value
    length_filter = 50 # filter below 5th percentile of posts from experts

    df=pd.read_csv(readability_fname,index_col=0)
    # Modify scores:
    for isim in range(len(sims)):
        aid,score = sims[isim]
        r_score=df.loc[aid,'Readability']
        length=df.loc[aid,'Length']
        if r_score < r_score_min :
            score = score * 0.01
        if length < length_filter :
            score = score * 0.01

        sims[isim]=(aid,score)
    #  
    sims2 = sorted(sims,key=itemgetter(1),reverse=True)
    return sims2
    

def list_to_str(list1):
    str1 = ','.join(str(e) for e in list1)
    return str1


def query_model(query,filter_posts_flag):
    import nltk
    import pandas as pd
    import pickle
    import os

    # Sources for forums:
    forum_sources=['http://ehealthforum.com', 
                   'http://www.medhelp.org',
                   'http://www.reditt.com']
    # Sources for articles:
    article_sources=["https://www.autismparentingmagazine.com/"]

    # Path to datafiles 
    path_to_data="flaskapp/data/"
    db_fname=os.path.join(path_to_data,"articles-n-forums-posts.csv")
    lsi_model_fname=os.path.join(path_to_data,"lsi-model.save")
    lsi_matsim_fname=os.path.join(path_to_data,"lsi-matsim.save")
    # 
    lda_model_fname=os.path.join(path_to_data,"lda-model.save")
    lda_matsim_fname=os.path.join(path_to_data,"lda-matsim.save")
    # 
    tfidf_fname=os.path.join(path_to_data,"tfidf.save")    
    dictionary_fname=os.path.join(path_to_data,"dictionary.save")
    readability_fname=os.path.join(path_to_data,"db-readability-length.csv")

    # Get categories and ids from dataset
    df = pd.read_csv(db_fname,index_col=0)
    
    # Read models and evaluate the score
    tfidf = models.TfidfModel.load(tfidf_fname)
    dictionary = pickle.load(open(dictionary_fname, "rb"))

    #
    model="lsi"

    if model == "lsi":
        lsi = models.LsiModel.load(lsi_model_fname)
        matsim = similarities.MatrixSimilarity.load(lsi_matsim_fname)
    if model == "lda":
        lda = models.LdaModel.load(lda_model_fname)
        matsim = similarities.MatrixSimilarity.load(lda_matsim_fname)
    
    # Tokenize data
    tokenizer = nltk.RegexpTokenizer(r'\w+')
    text = query.lower()
    ttext = tokenizer.tokenize(text)
    vec_bow = dictionary.doc2bow(ttext)
    
    if model == "lsi":
	# convert the query to LSI space
        vec_lsi = lsi[tfidf[vec_bow]] 
        sims = matsim[vec_lsi]
    if model == "lda":
	# convert the query to LDA space
        vec_lda = lda[vec_bow] 
        sims = matsim[vec_lda]
   
    # 
    # Filter data with readability score:
    #
    if filter_posts_flag:
        sims=filter_posts(sims,readability_fname)
 
    count_forums=0; count_articles=0;
    result_forums=[]
    result_articles=[]
    for aid,score in sims:
        #title=df['title'][aid]
        source=df['source'][aid]
        #
        # If this is from forums
        #
        if ( source in forum_sources ):
            if count_forums < 3 :
                result_forums.append(aid)
                count_forums=count_forums+1
            if ( count_forums ==  3  ) & ( count_articles == 3 ):
                return list_to_str(result_forums), list_to_str(result_articles)
        # 
        # If this is from articles
        #
        elif ( source in article_sources ):
            if count_articles < 3 :
                result_articles.append(aid)
                count_articles=count_articles+1
            if ( count_forums ==  3  ) & ( count_articles == 3 ):
                return list_to_str(result_forums), list_to_str(result_articles)

    return list_to_str(result_forums), list_to_str(result_articles)

