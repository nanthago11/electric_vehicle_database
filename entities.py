from google.appengine.ext import ndb


# For Verification
class User(ndb.Model):
    username = ndb.StringProperty()
    password = ndb.StringProperty()


class EV(ndb.Model):
    ev_id=ndb.IntegerProperty()
    name = ndb.StringProperty()
    manufacturer = ndb.StringProperty()
    year = ndb.IntegerProperty()
    # kwh
    battery_size = ndb.FloatProperty()
    # (km)
    WLTP_range = ndb.FloatProperty()
    cost = ndb.FloatProperty()
    # kw
    power = ndb.FloatProperty()
    #rating of ev
    rating=ndb.IntegerProperty()

class Review(ndb.Model):
    ev_id=ndb.IntegerProperty()
    #review text
    review_text = ndb.StringProperty()
    #rating of ev
    rating=ndb.IntegerProperty()
