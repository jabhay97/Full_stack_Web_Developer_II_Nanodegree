from flask import (Flask, 
                   render_template, 
                   request, 
                   redirect, 
                   jsonify, 
                   url_for, 
                   flash)
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Company, Product
from flask import session as login_session
import random, string

# IMPORTS FOR THIS STEP
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)


CLIENT_ID = json.loads(
    open('/var/www/catalog/catalog/client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Company Products Application"


# Connect to Database and create database session
python engine = create_engine('postgresql://catalog:catalog@localhost/catalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('/var/www/catalog/catalog/client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    
    # looks for an error.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id
    output=""
    output+="Hey! Login Successful."
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# User Helper Functions


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def fetchUser(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user
    
# DISCONNECT - Revoke a current user's token and reset their login_session


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

#JSON Code To show all comapanys info.
@app.route('/company/JSON')
def companysJSON():
    companys = session.query(Company).all()
    return jsonify(companys=[r.serialize for r in companys])

#JSON Code To Show all products of a specific Company
@app.route('/company/<int:company_id>/products/JSON')
def companylistJSON(company_id):
    company = session.query(Company).filter_by(id=company_id).one()
    prods = session.query(Product).filter_by(company_id=company_id).all()
    return jsonify(Products=[i.serialize for i in prods])

#JSON Code To Show specific product of specific company
@app.route('/company/<int:company_id>/products/<int:product_id>/JSON')
def productsJSON(company_id, product_id):
    Product = session.query(Product).filter_by(id=product_id).one()
    return jsonify(Product=Product.serialize)

# Following Code is to show all company

@app.route('/')
@app.route('/company/')
def showCompany():
    company = session.query(Company).order_by(asc(Company.name))
    return render_template('companys.html', companys=company)

# Following Code is for creation of company

@app.route('/company/new/', methods=['GET', 'POST'])
def newCompany():
    if 'username' not in login_session:
        flash("You need to login first")
        return redirect('/login')
    if request.method == 'POST':
        newCompany = Company(name=request.form['Name'],
                             user_id=login_session['user_id'])
        session.add(newCompany)
        flash('New Company %s Created' % newCompany.name)
        session.commit()
        return redirect(url_for('showCompany'))
    else:
        return render_template('newCompany.html')

# Following Code is for editing of company

@app.route('/company/<int:company_id>/edit/', methods=['GET', 'POST'])
def editCompany(company_id):
    if 'username' not in login_session:
        flash("You need to login first")
        return redirect('/login')
    editedCompany = session.query(Company).filter_by(id=company_id).one()
    if editedCompany.user_id != login_session['user_id']:
        flash('You are not authorised to make this change')
        return redirect(url_for('showCompany'))
    if request.method == 'POST':
        if request.form['name']:
            editedCompany.name = request.form['name']
            flash('Company %s Edited Successfully!' % editedCompany.name)
            return redirect(url_for('showCompany'))
    else:
        return render_template('editCompany.html', company=editedCompany)


# Following Code is for deletion of company


@app.route('/company/<int:company_id>/delete/', methods=['GET', 'POST'])
def deleteCompany(company_id):
    if 'username' not in login_session:
        flash("You need to login first")
        return redirect('/login')
    companyToDelete = session.query(Company).filter_by(id=company_id).one()
    if companyToDelete.user_id != login_session['user_id']:
        flash('You are not allowed to delete %s' % companyToDelete.name)
        return redirect(url_for('showCompany'))
    if request.method != 'POST':
        return render_template('deleteCompany.html', company=companyToDelete)
    else:
        session.delete(companyToDelete)
        flash('Company %s Deleted Successfully' % companyToDelete.name)
        session.commit()
        return redirect(url_for('showCompany', company_id=company_id))

# Following Code is to show products of a company

@app.route('/company/<int:company_id>/')
@app.route('/company/<int:company_id>/products/')
def showProduct(company_id):
    company = session.query(Company).filter_by(id=company_id).one()
    products = session.query(Product).filter_by(company_id=company_id).all()
    return render_template('product.html', items=products, company=company)


# Following Code is to create new products of a company

@app.route('/company/<int:company_id>/products/new/', methods=['GET', 'POST'])
def newProduct(company_id):
    if 'username' not in login_session:
        flash("You need to login first before making this change")
        return redirect(url_for('/login'))
    company = session.query(Company).filter_by(id=company_id).one()
    if request.method == 'POST':
        newProduct = Product(name=request.form['name'],
                             description=request.form['description'],
                             price=request.form['price'],
                             categary=request.form['categary'],
                             company_id=company_id,
                             user_id=company.user_id)
        session.add(newProduct)
        session.commit()
        flash('New Product %s Added Successfully' % (newProduct.name))
        return redirect(url_for('showProduct', company_id=company_id))
    else:
        return render_template('newProduct.html', company_id=company_id)

# Following Code is to edit product of a company


@app.route('/company/<int:company_id>/products/<int:product_id>/edit', methods=['GET', 'POST'])
def editProduct(company_id, product_id):
    if 'username' not in login_session:
        flash("You need to login first before making this change")
        return redirect(url_for('/login'))
    editedProduct = session.query(Product).filter_by(id=product_id).one()
    company = session.query(Company).filter_by(id=company_id).one()
    if editedProduct.user_id != login_session['user_id']:
        flash('You are not allowed to edit')
        return redirect(url_for('showProduct'))
    if request.method == 'POST':
        if request.form['name']:
            editedProduct.name = request.form['name']
        if request.form['description']:
            editedProduct.description = request.form['description']
        if request.form['price']:
            editedProduct.price = request.form['price']
        if request.form['categary']:
            editedProduct.categary = request.form['categary']
        session.add(editedProduct)
        session.commit()
        flash('Menu Item Successfully Edited')
        return redirect(url_for('showProduct', company_id=company_id))
    else:
        return render_template('editProduct.html', company_id=company_id,
                               product_id=product_id, prod=editedProduct)


# Following Code is to delete product of a company

@app.route('/company/<int:company_id>/products/<int:product_id>/delete', methods=['GET', 'POST'])
def deleteProduct(company_id, product_id):
    if 'username' not in login_session:
        flash("You need to login before making a change")
        return redirect(url_for('/login'))
    company = session.query(Company).filter_by(id=company_id).one()
    toDeleteProduct = session.query(Product).filter_by(id=product_id).one()
    if toDeleteProduct.user_id != login_session['user_id']:
        flash("You are not allowed to make change!")
        return redirect(url_for('showProduct'))
    if request.method == 'POST':
        session.delete(toDeleteProduct)
        session.commit()
        flash('Menu Item Successfully Deleted')
        return redirect(url_for('showProduct', company_id=company_id))
    else:
        return render_template('deleteProduct.html', prod=toDeleteProduct)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
