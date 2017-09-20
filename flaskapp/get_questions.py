def get_questions():

    f = open("./flaskapp/data/questions.dat","r")
    questions_raw = f.readlines()
    f.close()

    questions=[]
    for text in questions_raw:
        ttext = text.replace("?","%3F").split(" ")
        tokens="+".join(ttext)
        href="http://127.0.0.1:5000/output?autism_query={}".format(tokens)
        questions.append(dict(text=text,href=href))
    return questions 
