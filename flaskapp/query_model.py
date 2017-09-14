from collections import defaultdict
from gensim import corpora, models, similarities

def list_to_str(list1):
    str1 = ','.join(str(e) for e in list1)
    return str1


def make_dictionary(documents):
    """
    construct a dictionary, i.e. mapping btwn word ids and their freq of occurence in the whole corpus
    filter dictionary to remove stopwords and words occuring < min_count times
    
    input: documents is an iterable consisting of all the words in the corpus 
    output: filtered dictionary
    """

    
    dictionary = corpora.Dictionary(documents)

    stop_words = nltk.corpus.stopwords.words('english') 
    min_count = 2
    stop_ids = [dictionary.token2id[word] for word in stop_words
               if word in dictionary.token2id]
    rare_ids = [id for id, freq in dictionary.dfs.items()
                if freq < min_count]
    dictionary.filter_tokens(stop_ids + rare_ids)
    dictionary.compactify()
    return(dictionary)

def make_corpus(documents):
    """
    """
    dictionary = make_dictionary(documents)
    # convert corpus to vectors using bag-of-words representation, i.e. tuples of word indices and word counts
    corpus = [dictionary.doc2bow(words) for words in documents]
    return(corpus, dictionary)

def query_model(query):
    import nltk
    import pandas as pd
    import pickle
    import os

    # Sources for forums:
    forum_sources=["http://www.medhelp.org"]
    # Sources for articles:
    article_sources=["https://www.autismparentingmagazine.com/"]

    # Path to datafiles 
    path_to_data="flaskapp/data/"
    db_fname=os.path.join(path_to_data,"articles-n-forums-posts.csv")
    lsi_model_fname=os.path.join(path_to_data,"lsi-model.save")
    lsi_matsim_fname=os.path.join(path_to_data,"lsi-matsim.save") 
    tfidf_fname=os.path.join(path_to_data,"tfidf.save")    
    dictionary_fname=os.path.join(path_to_data,"dictionary.save")

    # Get categories and ids from dataset
    df = pd.read_csv(db_fname,index_col=0)
    df.head(2)
    #ids=df.index
    
    # Read models and evaluate the score
    lsi = models.LsiModel.load(lsi_model_fname)
    tfidf = models.TfidfModel.load(tfidf_fname)
    dictionary = pickle.load(open(dictionary_fname, "rb"))
    matsim = similarities.MatrixSimilarity.load(lsi_matsim_fname)
    
    # Tokenize data
    tokenizer = nltk.RegexpTokenizer(r'\w+')
    text = query.lower()
    ttext = tokenizer.tokenize(text)
    vec_bow = dictionary.doc2bow(query.lower().split())
    
    vec_lsi = lsi[tfidf[vec_bow]] # convert the query to LSI space
    
    sims = matsim[vec_lsi]
    
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
