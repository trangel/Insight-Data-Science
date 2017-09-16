from collections import defaultdict
from gensim import corpora, models, similarities
import nltk

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

def make_lsi_similarity_matrix(tfidf_corpus, dictionary,num_topics):
    """
    construct LSI (latent semantic indexing) model on Tfidf-transformed corpus, print model topics, 
    return similarity matrix.
    """
    # construct model
    lsi = models.lsimodel.LsiModel(tfidf_corpus, id2word=dictionary, num_topics=200) 
    #lsi.save('lsi-model.save')
    # create similarity matrix
    matsim = similarities.MatrixSimilarity(lsi[tfidf_corpus], num_best=1000)
    return(matsim,lsi)

def make_lda_similarity_matrix(corpus, dictionary,num_topics,num_iter):
    """
    Latent Dirichlet Allocation (LDA) model
    """
    # construct model
    lda = models.ldamodel.LdaModel(corpus, id2word=dictionary, num_topics=num_topics,iterations=num_iter)
    #lda.save('lda-model.save')
    # create similarity matrix
    matsim = similarities.MatrixSimilarity(lda[corpus], num_best=1000)
    return(matsim,lda)

#
# See validate model.ipynb
#
def get_model_score(ids,matsim,categories):
    """ Function to evalate the score for a given model, following the equation defined in validate_model.ipynb """
    num_predictions=3
    model_score=0
    for id,doc in zip(ids,matsim.index):
        sims=matsim[doc]
        for other_id,score in sims[:num_predictions+1]:

            #print("ID {} OTHER_ID {} SCORE {}".format(id,other_id,score))
            category1=categories[id]
            category2=categories[other_id]
            if id != other_id:
                if category1 == category2:
                    model_score+=1
    N=len(ids)*num_predictions
    model_score=model_score/N
    return model_score

#
# See validate model.ipynb
#
def get_model_score_wforums(ids,matsim,categories,titles):
    """ Function to evalate the score for a given model, following the equation defined in validate_model.ipynb """
    num_predictions=3
    model_score=0
    N=0
    for id,doc in zip(ids,matsim.index):
        sims=matsim[doc]
        category1=eval(categories[id])
        title1=titles[id]
        if 'forums' in category1:
            continue
        i_pred=0
        for other_id,score in sims:

            #print("ID {} OTHER_ID {} SCORE {}".format(id,other_id,score))
            category2=eval(categories[other_id])
            title2=titles[other_id]
            if 'forums' in category2:
                continue

            # Remove categories which are too general for this test:
            cats_to_remove=['category-magazine-issues','category-general',
                            'category-autism-books','category-podcast','category-autism-news',
                            'category-personal-narrative','autism_advocacy']

            for cat in cats_to_remove:
                category1=set(category1)
                if cat in category1:
                    category1.remove(cat)
                category2=set(category2)
                if cat in category2:
                    category2.remove(cat)
            
            if (len(category1) == 0) | (len(category2) == 0):
                continue
            # Remove also 'magazine issues' are these are general articles:
                
            if id != other_id:
                i_pred=i_pred+1

                if i_pred ==  num_predictions+1 :
                    break
                #print("title1 {}\n title2{}".format(title1,title2))
                #print("ID {} category{} \n ID {} category {}, score {}".format(id,category1,other_id,category2,score))
                N=N+1
                if any( x in category2 for x in category1):
                    model_score+=1
                #else:
                #    print("ID {} category{} \n ID {} category {}, score {}".format(id,category1,other_id,category2,score))
                #print("model_score {}, N {}".format(model_score,N))
    model_score=model_score/N
    return model_score

