from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, make_response # noqa
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Catalog, Investment, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id'] # noqa

# Connect to Database and create database session
engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Show login
@app.route('/login')
def showLogin():
	state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
	login_session['state'] = state
	return render_template('login.html', STATE=state)


# Connect to google server for authentication & authorization
@app.route('/gconnect', methods=['POST'])
def gconnect():
	if request.args.get('state') != login_session['state']:
		response = make_response(json.dumps('Invalid state parameter'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	code = request.data
	print "code is %s" % code
	try:
		# Pass the authorization code to credentials object
		oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
		oauth_flow.redirect_uri = 'postmessage'
		credentials = oauth_flow.step2_exchange(code)
		print "credentials is %s" % credentials
	except FlowExchangeError:
		response = make_response(json.dumps('Failed to upgrade the authorization code.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	# Check if the access token is valid
	access_token = credentials.access_token
	url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'% access_token)
	h = httplib2.Http()
	result = json.loads(h.request(url, 'GET')[1])
	# Abort if there's an error in the access token info
	if result.get('error') is not None:
		response = make_response(json.dumps(result.get('error')), 500)
		response.headers['Content-Type'] = 'application/json'
		return response
	# Authenticate the access token
	gplus_id = credentials.id_token['sub']
	print "gplus_id is %s" % gplus_id
	if result['user_id'] != gplus_id:
		response = make_response(json.dumps("Token cannot be authenticated"), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	# Verify the access token is valid for this app.
	if result['issued_to'] != CLIENT_ID:
		response = make_response(json.dumps("Token's client ID does not match the app's"), 401)
		print "Token's client ID does not match the app's"
		response.headers['Content-Type'] = 'application/json'
		return response
	# Check if the user is already logged in
	stored_credentials = login_session.get('credentials')
	stored_gplus_id = login_session.get('gplus_id')
	if stored_credentials is not None and gplus_id == stored_gplus_id:
		response = make_response(json.dumps("Current user is already logged in."), 200)
		response.headers['Content-Type'] = 'application/json'
		return response

	# Store the access token in the session
	login_session['access_token'] = credentials.access_token
	print "login_session['access_token'] is %s" % login_session['access_token']
	login_session['gplus_id'] = gplus_id

	# Get user info
	userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
	params = {'access_token': credentials.access_token, 'alt': 'json'}
	answer = requests.get(userinfo_url, params=params)
	print "answer is %s" % answer
	data = answer.json()

	print "Data is %s" % data

	print ("data['name'] is %s" % data['name'])

	login_session['username'] = data['name']
	login_session['picture'] = data['picture']
	login_session['email'] = data['email']

	print ('user name: ' + login_session['username'])

	# Check if user exists, or create a new user
	user_id = getUserID(login_session['email'])
	if not user_id:
		user_id = createUser(login_session)
	login_session['user_id'] = user_id

	output = ''
	output += '<h1>Welcome '
	output += login_session['username']
	output += '!</h1>'
	output += '<img src="'
	output += login_session['picture']
	output += '"style = "width: 50px; height: 50px; border-radius: 25px; -webkit-border-radius: 25px; -moz-border-radius: 25px;">'
	flash("You are now logged in as %s" % login_session['username'])
	print "Done!!!!"
	return output


# Disconnect the current user
@app.route('/gdisconnect')
def gdisconnect():
	access_token = login_session.get('access_token')
	if access_token is None:
		response = make_response(json.dumps('Current user not connected.'), 401)
		response.headers['Content-Type'] = 'application/json'
		return response
	url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
	h = httplib2.Http()
	result = h.request(url, 'GET')[0]

	if result['status'] == '200' or result['status'] == '400':
		# End the current user's session
		del login_session['access_token']
		del login_session['gplus_id']
		del login_session['username']
		del login_session['email']
		del login_session['picture']
		response = make_response(json.dumps('Successfullu disconnected.'), 200)
		response.headers['Content-Type'] = 'application/json'
		return redirect(url_for('showCatalog'))
	else:
		response = make_response(json.dumps('Failed to revoke token for current user.'), 400)
		response.headers['Content-Type'] = 'application/json'
		return response


# Show logout
@app.route('/logout')
def showLogout():
	return render_template('logout.html')


# Show the catalog
@app.route('/')
@app.route('/catalog')
def showCatalog():
	catalog = session.query(Catalog).order_by(asc(Catalog.name))
	investments = session.query(Investment).order_by(Investment.createDate.desc())
	if 'username' not in login_session:
		return render_template('publiccatalog.html', catalog=catalog, investments=investments)
	else:
		return render_template('catalog.html', catalog=catalog, investments=investments)


# Show the investments
@app.route('/catalog/<int:catalog_id>/')
@app.route('/catalog/<int:catalog_id>/investment/')
def showInvestments(catalog_id):
	catalog = session.query(Catalog).order_by(asc(Catalog.name))
	thisCatalog = session.query(Catalog).filter_by(id=catalog_id).one()
	creator = getUserInfo(thisCatalog.user_id)
	investments = session.query(Investment).filter_by(catalog_id=catalog_id).all()
	if 'username' not in login_session or creator.id != login_session['user_id']:
		return render_template('publicinvestment.html', investments=investments, catalog=catalog, thisCatalog=thisCatalog, creator=creator)
	else:
		return render_template('investment.html', investments=investments, catalog=catalog, thisCatalog=thisCatalog, creator=creator)


# Show the investment details
@app.route('/catalog/<int:catalog_id>/<int:investment_id>/')
def showInvestmentDetails(catalog_id, investment_id):
	catalog = session.query(Catalog).filter_by(id=catalog_id).one()
	creator = getUserInfo(catalog.user_id)
	investment = session.query(Investment).filter_by(id=investment_id).one()
	if 'username' not in login_session or creator.id != login_session['user_id']:
		return render_template('publicInvestmentDetails.html', investment=investment, catalog=catalog, creator=creator)
	else:
		return render_template('investmentDetails.html', investment=investment, catalog=catalog, creator=creator)


# Create a new catalog
@app.route('/catalog/new', methods=['GET', 'POST'])
def newCatalog():
	if 'username' not in login_session:
		return redirect('/login')
	if request.method == 'POST':
		newCatalog = Catalog(user_id = login_session['user_id'], name = request.form['name'])
		session.add(newCatalog)
		session.commit()
		return redirect(url_for('showCatalog'))
	else:
		return render_template('newCatalog.html')


# Create a new investment
@app.route('/catalog/<int:catalog_id>/new/', methods=['GET', 'POST'])
def newInvestment(catalog_id):
	if 'username' not in login_session:
		return redirect('/login')
	if request.method == 'POST':
		newInvestment = Investment(name=request.form['name'], description=request.form['description'], price=request.form['price'], catalog_id=catalog_id, user_id = login_session['user_id'])
		session.add(newInvestment)
		session.commit()
		return redirect(url_for('showInvestments', catalog_id=catalog_id))
	else:
		return render_template('newInvestment.html', catalog_id=catalog_id)


# Edit a catalog
@app.route('/catalog/<int:catalog_id>/edit/', methods = ['GET', 'POST'])
def editCatalog(catalog_id):
	editedCatalog = session.query(Catalog).filter_by(id = catalog_id).one()
	if 'username' not in login_session:
		return redirect('/login')
	if editedCatalog.user_id != login_session['user_id']:
		return alertUnauthAmendment()
	if request.method == 'POST':
		editedCatalog.name = request.form['name']
		session.add(editedCatalog)
		session.commit()
		return redirect(url_for('showCatalog'))
	else:
		return render_template('editCatalog.html', catalog_id=catalog_id, i = editedCatalog)


# Edit an investment
@app.route('/catalog/<int:catalog_id>/<int:investment_id>/edit/', methods = ['GET', 'POST'])
def editInvestment(catalog_id, investment_id):
	catalog = session.query(Catalog).order_by(asc(Catalog.name))
	editedInvestment = session.query(Investment).filter_by(id = investment_id).one()
	if 'username' not in login_session:
		return redirect('/login')
	if editedInvestment.user_id != login_session['user_id']:
		return alertUnauthAmendment()
	if request.method == 'POST':
		editedInvestment.name = request.form['name']
		editedInvestment.description = request.form['description']
		editedInvestment.price = request.form['price']
		editedInvestment.catalog_id = request.form['catalog_id']
		session.add(editedInvestment)
		session.commit()
		return redirect(url_for('showInvestments', catalog_id = catalog_id))
	else:
		return render_template('editInvestment.html', catalog_id=catalog_id, investment_id=investment_id, catalog=catalog, i = editedInvestment)


# Delete a catalog
@app.route('/catalog/<int:catalog_id>/delete/', methods= ['GET', 'POST'])
def deleteCatalog(catalog_id):
	catalogToDelete = session.query(Catalog).filter_by(id=catalog_id).one()
	investmentToDelete = session.query(Investment).filter_by(catalog_id = catalog_id).all()
	print login_session['user_id']
	print catalogToDelete.user_id
	if 'username' not in login_session:
		return redirect('/login')
	if catalogToDelete.user_id != login_session['user_id']:
		return alertUnauthAmendment()
	if request.method == 'POST':
		for i in investmentToDelete:
			session.delete(i)
		session.delete(catalogToDelete)
		flash('%s Successfully Deleted' % catalogToDelete.name)
		session.commit()
		return redirect(url_for('showCatalog'))
	else:
		return render_template('deleteCatalog.html', catalog_id=catalog_id, i = catalogToDelete)


# Delete an investment
@app.route('/catalog/<int:catalog_id>/<int:investment_id>/delete/', methods= ['GET', 'POST'])
def deleteInvestment(catalog_id, investment_id):
	investmentToDelete = session.query(Investment).filter_by(id = investment_id).one()
	if 'username' not in login_session:
		return redirect('/login')
	if investmentToDelete.user_id != login_session['user_id']:
		return alertUnauthAmendment()
	if request.method == 'POST':
		session.delete(investmentToDelete)
		session.commit()
		return redirect(url_for('showInvestments', catalog_id = catalog_id))
	else:
		return render_template('deleteInvestment.html', i = investmentToDelete)


# JSON endpoint for the entire catalog
@app.route('/json/catalog', methods = ['GET'])
def catalogJsonEndpoint():
	if request.method == 'GET':
		catalog = session.query(Catalog).all()
		return jsonify(catalog = [i.serialize for i in catalog])


# JSON endpoint for investments
@app.route('/json/catalog/<int:id>', methods = ['GET'])
def investmentsJsonEndpoint(id):
	if request.method == 'GET':
		investments = session.query(Investment).filter_by(catalog_id = id).all()
		return jsonify(investments = [i.serialize for i in investments])


# Get user ID
def getUserID(email):
	try:
		user = session.query(User).filter_by(email = email).one()
		return user.id
	except:
		return None


# Get user information
def getUserInfo(user_id):
	user = session.query(User).filter_by(id = user_id).one()
	return user


# Create a new sser
def createUser(login_session):
	newUser = User(name = login_session['username'], email = login_session['email'], picture = login_session['picture'])
	session.add(newUser)
	session.commit()
	user = session.query(User).filter_by(email = login_session['email']).one()
	return user.id


# Alert for unauthorized amendment
def alertUnauthAmendment():
	print 'in the method'
	return "<script>function myFunction() {alert('You are not authorized to modify this.');}</script><body onload='myFunction()''>" 


if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host='0.0.0.0', port = 8000)