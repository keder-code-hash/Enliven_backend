import requests 
 
url1 = "https://smartassessment-keder-code-hash.cloud.okteto.net/saq1/analyze"
url2 = "https://smartassessment-keder-code-hash.cloud.okteto.net/saq2/analyze"

def make_prediction(student_answer,standard_answer,depth): 
    headers = {
        'content-type': 'application/json'
    }
    req=requests.post(
        url= url2,
        headers=headers,
        json=
            {
                "standard_answer":standard_answer,
                "student_answer":student_answer
            } 
    )
    respond=req.json()
    keyword_similarity_metric=respond.get("keyword_matching_result")
    student_keyword=list(respond.get("student_keyword"))
    standard_keyword=list(respond.get("standard_keyword")) 
    entailment=respond.get("entailment")
    contradiction=respond.get("contradiction")
    neutral=respond.get("neutral")

    # setting dominant index

    dominant_index=0.15

    if (entailment-neutral)>=dominant_index and (entailment-contradiction)>=dominant_index:
        # entailment 
        entail_perc=(2*entailment+neutral)/2
        return True,"right",entail_perc*100, respond

    elif (contradiction-entailment)>=dominant_index and (contradiction-neutral)>=dominant_index:
        # contradiction
        return True,"wrong",0, respond

    elif (neutral-entailment)>=dominant_index and (neutral-contradiction)>=dominant_index:
        # print("hii")
        if depth==2:
            return True,"inconclusive",-1
        # again check 
        stn_answer=""
        std_answer=""
        for i in student_keyword:
            stn_answer+=i+" "
        for i in standard_keyword:
            std_answer+=i+" "
        stn_answer+='.'
        std_answer+='.'
        # print(stn_answer,std_answer)
        d=depth+1
        return make_prediction(student_answer=stn_answer,standard_answer=std_answer,depth=d)
    else:
        return False,"inconclusive",-1, respond



# standard_ans="Energy is the ability to do work."
# student_ans="Energy the capacity for doing work."
# standard_ans="My name is keder."
# student_ans="My name is purnadip."

# standard_answer="A force is an influence that can change the motion of an object. "
# student_answer="friction of an object is considered a push."


# print(make_prediction(student_answer=student_answer,standard_answer=standard_answer,depth=0))

 

 
        