import webapp2
import os
from google.appengine.ext.webapp import template
from evconstants import *
from google.appengine.ext import ndb
from entities import User,EV,Review
from idmanager import getEvIDSequence
from google.appengine.api import users

nouser = True


# Sample user creation
def sampleUserCreate():
    newUser = User()
    newUser.username = 'admin'
    newUser.password = 'admin'
    newUser.put()
    global nouser
    nouser = False
    pass


class LoginVerify(webapp2.RedirectHandler):
    def get(self):
        logging.info("Checking Login")
        print "Checking Login"
        username = self.request.get('username')
        password = self.request.get('password')
        print "logging in ::", username, "/", password
        userQuery = User.query()
        for user in userQuery.fetch():
            if username == user.username and password == user.password:
                print "Login Success"
                path = os.path.join(os.path.dirname(__file__), 'templates/userdashboard.html')
                self.response.out.write(template.render(path, {}))
                return
        print "Login Failed!"
        path = os.path.join(os.path.dirname(__file__), 'templates/login.html')
        self.response.out.write(template.render(path, {}))


class HomePage(webapp2.RedirectHandler):
    def get(self):
        logging.info("Loading HomePage")
        path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
        self.response.out.write(template.render(path, {}))


class Login(webapp2.RedirectHandler):
    def get(self):
        logging.info("Loading HomePage")
        path = os.path.join(os.path.dirname(__file__), 'templates/login.html')
        self.response.out.write(template.render(path, {}))


class About(webapp2.RedirectHandler):
    def get(self):
        if nouser == True:
            sampleUserCreate()
        logging.info("Loading HomePage")
        path = os.path.join(os.path.dirname(__file__), 'templates/about.html')
        self.response.out.write(template.render(path, {}))


class UserDashboard(webapp2.RedirectHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates/userdashboard.html')
        self.response.out.write(template.render(path, {}))

class ViewEV(webapp2.RedirectHandler):
    def get(self):
        evQuery=EV.query()
        if len(evQuery.fetch()) == 0 :
            print "No EV Data"
            template_values = {
            'evs': []
            }

        else :
            evs=evQuery.fetch()
            template_values = {
            'evs': evs
            }
        
        path = os.path.join(os.path.dirname(__file__), 'templates/viewev.html')
        self.response.out.write(template.render(path, template_values))
        

class AddEV(webapp2.RedirectHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates/addev.html')
        self.response.out.write(template.render(path, []))



#Add New EV To Datastore
class AddEVSubmit(webapp2.RedirectHandler):
    def get(self):
        newEv=EV()
        newEv.ev_id=getEvIDSequence()
        newEv.name=self.request.get('evname')
        newEv.manufacturer=self.request.get('manufacturer')
        newEv.year=int(self.request.get('year'))
        newEv.battery_size=float(self.request.get('batterysize'))
        newEv.WLTP_range=float(self.request.get('wltprange'))
        newEv.cost=float(self.request.get('cost'))
        newEv.power=float(self.request.get('power'))
        newEv.rating=0
        newEVKey=newEv.put()
        if newEVKey != -1:
            messgage='Successfully Added EV with Key :: '+str(newEVKey.get().ev_id)
            path = os.path.join(os.path.dirname(__file__), 'templates/addevsubmit.html')
            self.response.out.write(template.render(path, {'message':messgage}))
        else:
            messgage='Error Adding EV'
            path = os.path.join(os.path.dirname(__file__), 'templates/addevsubmit.html')
            self.response.out.write(template.render(path, {'message':messgage}))

#Delete EV Handler
class DeleteEV(webapp2.RedirectHandler):
    def get(self):
        evQuery=EV.query()
        if len(evQuery.fetch()) == 0 :
            print "No EV Data"
            ev_data = {
            'ev_data': []
            }

        else :
            evs=evQuery.fetch()
            ev_data = {
            'ev_data': evs
            }

        path = os.path.join(os.path.dirname(__file__), 'templates/deleteev.html')
        self.response.out.write(template.render(path, ev_data))

#Login Using Google App Engine
class GoogleAppEngineLogin(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            nickname = user.nickname()
            logout_url = users.create_logout_url('/')
            greeting = 'Welcome, {}! (<a href="{}">sign out</a>)'.format(
                nickname, logout_url)
        else:
            login_url = users.create_login_url('/')
            greeting = '<a href="{}">Sign in</a>'.format(login_url)
        self.response.write(
            '<html><body>{}</body></html>'.format(greeting))
class DeleteEVData(webapp2.RequestHandler):
     def get(self):
        evQuery=EV.query()
        evs=evQuery.fetch()
        for ev in evs:
            if ev.ev_id == int(self.request.get('ev_id')):
                ev.key.delete()
                break
        evQuery=EV.query()
        if len(evQuery.fetch()) == 0 :
            print "No EV Data"
            ev_data = {
            'ev_data': []
            }

        else :
            evs=evQuery.fetch()
            ev_data = {
            'ev_data': evs
            }
        path = os.path.join(os.path.dirname(__file__), 'templates/deleteev.html')
        self.response.out.write(template.render(path, ev_data))
class CompareEV(webapp2.RequestHandler):
     def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates/compareev.html')
        self.response.out.write(template.render(path, []))

class CompareEVSubmit(webapp2.RequestHandler):
     def get(self):
        evQuery=EV.query()
        evs=evQuery.fetch()
        evList=[]
        ratingList=[]
        logging.info("EV Data")
        for ev in evs:
            logging.info(ev.ev_id)
            if ev.ev_id == int(self.request.get('ev1')) or ev.ev_id == int(self.request.get('ev2')):
                evList.append(ev)
                logging.info(str(ev.ev_id )+"Added")
        if len(evList)>1:
            if evList[0].rating == 0:
                temp=0
                ratingList.append(temp)
            else:
                temp=int(evList[0].rating)
                ratingList.append(temp)
            if evList[1].rating == None:
                temp=0
                ratingList.append(temp)
            else:
                temp=int(evList[1].rating)
                ratingList.append(temp)
       
        if len(evList) >= 2:
            evcompare_data={
            'compareev1':evList[0],
            'compareev2':evList[1],
            'ratingstar1':ratingList[0],
            'ratingstar2':ratingList[1]
            }
            path = os.path.join(os.path.dirname(__file__), 'templates/compareselectedev.html')
            self.response.out.write(template.render(path, evcompare_data))
        else:
            evcompare_data={
                'comparemessgae':'Invalid IDs Selected, Please Check EV Ids!'
            }
            path = os.path.join(os.path.dirname(__file__), 'templates/compareev.html')
            self.response.out.write(template.render(path, evcompare_data))
class RateEV(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates/rateev.html')
        self.response.out.write(template.render(path, []))
class RateEVFind (webapp2.RequestHandler):
    def get(self):
        evId=int(self.request.get('ev1'))
        evQuery=EV.query()
        evs=evQuery.fetch()
        for ev in evs:
            if ev.ev_id == evId:
                path = os.path.join(os.path.dirname(__file__), 'templates/evratingpage.html')
                self.response.out.write(template.render(path, {'ev':ev}))
                return

        path = os.path.join(os.path.dirname(__file__), 'templates/rateev.html')
        self.response.out.write(template.render(path, {'ratemessgae':'EV With ID #'+str(evId)+' not Found!'}))   
class SubmitEVRating(webapp2.RequestHandler):
    def get(self):
        evId=int(self.request.get('ev_id'))
        rating=int(self.request.get('rating'))
        evQuery=EV.query()
        evs=evQuery.fetch()
        for ev in evs:
            if ev.ev_id == evId:
                evToUpdate=ev
                evToUpdate.rating=rating
                evToUpdate.put()
                logging.info("EV Updated!")
        path = os.path.join(os.path.dirname(__file__), 'templates/rateev.html')
        self.response.out.write(template.render(path, []))


class ScoreEV(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'templates/scoreev.html')
        self.response.out.write(template.render(path, []))

class ScoreEVFind(webapp2.RequestHandler):
    def get(self):
        evId=int(self.request.get('ev1'))
        evQuery=EV.query()
        evs=evQuery.fetch()
        for ev in evs:
            if ev.ev_id == evId:
                path = os.path.join(os.path.dirname(__file__), 'templates/evscorepage.html')
                self.response.out.write(template.render(path, {'ev':ev}))
                return

        path = os.path.join(os.path.dirname(__file__), 'templates/scoreev.html')
        self.response.out.write(template.render(path, {'ratemessgae':'EV With ID #'+str(evId)+' not Found!'}))


class ReviewEV(webapp2.RequestHandler):
    def get(self):
        evQuery=EV.query()
        if len(evQuery.fetch()) == 0 :
            print "No EV Data"
            template_values = {
            'evs': []
            }

        else :
            evs=evQuery.fetch()
            template_values = {
            'evs': evs
            }
        path = os.path.join(os.path.dirname(__file__), 'templates/reviewev.html')
        self.response.out.write(template.render(path, template_values))

class ReviewEVDevice(webapp2.RequestHandler):
    def get(self):
        evId=int(self.request.get('ev_id'))
        evQuery=EV.query()
        reviews=Review.query() 
        evs=evQuery.fetch()
        for ev in evs:
            if ev.ev_id == evId:
                evToUpdate=ev
                evToUpdate.put()
                logging.info("EV Updated!")
        path = os.path.join(os.path.dirname(__file__), 'templates/reviewevdevice.html')
        self.response.out.write(template.render(path, {'ev':evToUpdate,"reviews":reviews}))


class ReviewEVDeviceSubmit(webapp2.RequestHandler):
    def updateEVScore(self,evId):
        rating =0
        total=0
        reviews=Review.query().fetch()
        for rev in reviews:
            rev.ev_id == evId
            rating+=rev.rating
            total+=1
        return rating/total

    def get(self):
        evId=int(self.request.get('ev_id'))
        review_text=self.request.get('reviewtext')
        rating=int(self.request.get('rating'))
        newRev=Review()
        newRev.ev_id=evId
        newRev.review_text=review_text
        newRev.rating=rating
        newRev.put()
        updateRating=self.updateEVScore(evId)
        #Update rating of the EV
        evs=EV.query().fetch()
        for ev in evs:
            if ev.ev_id == evId:
                ev.rating=updateRating
                ev.put()
        evQuery=EV.query()
        evs=evQuery.fetch()
        reviews=[]
        allreviews=Review.query().fetch()
        for rev in allreviews:
            if rev.ev_id == evId:
                reviews.append(rev)
        for ev in evs:
            if ev.ev_id == evId:
                evToUpdate=ev
                evToUpdate.put()
                logging.info("EV Updated!")
        path = os.path.join(os.path.dirname(__file__), 'templates/reviewevdevice.html')
        self.response.out.write(template.render(path, {"ev":evToUpdate,"reviews":reviews}))

# Entry Point Of the Application
app = webapp2.WSGIApplication([("/", HomePage), ("/login", Login), ("/about", About), ("/login-verify", LoginVerify),
                               ("/userdashboard", UserDashboard),("/viewev",ViewEV),("/addev",AddEV),("/addevsubmit",AddEVSubmit),("/deleteev",DeleteEV),
                               ("/deleteevdata",DeleteEVData),("/compareev",CompareEV),("/compareevsubmit",CompareEVSubmit),("/rateev",RateEV),("/rateevfind",RateEVFind)
                               ,("/submitevrating",SubmitEVRating),("/scoreev",ScoreEV)
                               ,("/scoreevfind",ScoreEVFind),("/reviewev",ReviewEV),("/reviewevdevice",ReviewEVDevice),("/adddevicereview",ReviewEVDeviceSubmit)],
                              debug=True)
