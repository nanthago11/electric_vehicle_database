from random import random
ev_id=random()*1000
def getEvIDSequence():
    global ev_id
    ev_id+=1
    return int(ev_id)