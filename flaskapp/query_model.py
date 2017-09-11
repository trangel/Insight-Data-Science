from collections import defaultdict
from gensim import corpora, models, similarities
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

    # Path to datafiles 
    path_to_data="flaskapp/data/"
    db_fname=os.path.join(path_to_data,"AutismParentMagazine-posts-tokens.csv")
    lsi_model_fname=os.path.join(path_to_data,"lsi-model.save")
    lsi_matsim_fname=os.path.join(path_to_data,"lsi-matsim.save") 
    tfidf_fname=os.path.join(path_to_data,"tfidf.save")    
    dictionary_fname=os.path.join(path_to_data,"dictionary.save")

    # Get categories and ids from dataset
    df = pd.read_csv(db_fname,index_col=0)
    df.head(2)
    ids=df.index
    
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
    
    result=""
    for aid,score in sims:
        title=df['title'][aid]
        #print("{}: {}".format(title,score))
        sentence="{}: {}\n".format(title,score)
        result=result+sentence
    return result 
