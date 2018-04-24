from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Company, Base, Product, User

python engine = create_engine('postgresql://catalog:catalog@localhost/catalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#Create Dummy User
User1 = User(name="Abhay Jain", email="abhayj97@gmail.com",picture='''https://plus.google.com/u/0/photos/110581984025459992644/albums/profile/6417914292639670386?iso=false''')
session.add(User1)
session.commit()

# Products of Orient
company1 = Company(user_id=1, name="Orient")

session.add(company1)
session.commit()

prod2 = Product(user_id=1, name="Valeria", description="Premium 1500 mm 5 Blade fan with light",
                     price="Rs. 4750",categary="Decorative", company=company1)

session.add(prod2)
session.commit()


prod1 = Product(user_id=1, name="Adelia", description="Premium 1300 mm 5 Blade fan with light",
                     price="Rs. 4250",categary="Decorative", company=company1)

session.add(prod1)
session.commit()

prod2 = Product(user_id=1, name="Quasar Ornamental", description="Premium 1200 mm 3 Blade Decoratiive fan",
                     price="Rs. 2000",categary="Decorative", company=company1)

session.add(prod2)
session.commit()

prod3 = Product(user_id=1, name="Summer Crown", description="Premium 1200 mm 3 Blade Energy Saver Decorative fan",
                     price="Rs. 1600",categary="Decorative", company=company1)

session.add(prod3)
session.commit()

prod4 = Product(user_id=1, name="Summer Cool", description="Basic 1200mm Fan",
                     price="Rs. 1400",categary="Basic", company=company1)

session.add(prod4)
session.commit()


# Products for Usha
company2 = Company(name="Usha")

session.add(company2)
session.commit()


prod1 = Product(user_id=1, name="Subaris", description="Premium 1300 mm 5 Blade fan with light",
                     price="Rs 4799",categary="Decorative", company=company2)

session.add(prod1)
session.commit()

prod2 = Product(user_id=1, name="New Trump", description="New Trump Decorative Fan 48", price="Rs. 1520",categary="Decorative", company=company2)

session.add(prod2)
session.commit()

prod3 = Product(user_id=1, name="Spin", description="Basic 1200mm fan with aluminium blades ",
                     price="Rs. 1250",categary="Basic", company=company2)

session.add(prod3)
session.commit()

prod4 = Product(user_id=1, name="Swift", description="Basic 1200mm fan with iron blades",
                     price="Rs. 1200",categary="Basic", company=company2)

session.add(prod4)
session.commit()


# Products of Bajaj
company3 = Company(user_id=1, name="Bajaj")

session.add(company1)
session.commit()


prod1 = Product(user_id=1, name="Winstrim", description="a premium 1200mm fan",price="Rs. 2799",categary="Decorative", company=company3)

session.add(prod1)
session.commit()

prod2 = Product(user_id=1, name="Hextrim", description="a Premium High speed energy saver fan",
                     price="Rs. 3199",categary="Decorative", company=company3)

session.add(prod2)
session.commit()

prod3 = Product(user_id=1, name="Bahar Deco", description="A 1200mm decorative fan",
                     price="Rs. 1450",categary="Decorative", company=company3)

session.add(prod3)
session.commit()

prod4 = Product(user_id=1, name="Edge", description="Basic Energy saver 1200mm fan",
                     price="Rs 1299",categary="Basic", company=company3)

session.add(prod4)
session.commit()

prod5 = Product(user_id=1, name="Bahar", description="A 1200mm basic fan",
                     price="Rs. 1450",categary="Basic", company=company3)

session.add(prod5)
session.commit()


# Products of Crompton
company4 = Company(user_id=1, name="Crompton Greaves ")

session.add(company4)
session.commit()


prod1 = Product(user_id=1, name="Flyleaf", description="Premium High speed decorative fan",
                     price="Rs. 2399",categary="Decorative", company=company4)

session.add(prod1)
session.commit()

prod2 = Product(user_id=1, name="Aura", description="Premium Energy Saver Fan",
                     price="Rs. 2199",categary="Decorative", company=company4)

session.add(prod2)
session.commit()

prod3 = Product(user_id=1, name="Highbreeze", description="Basic High Speed Fan",
                     price="Rs. 1450",categary="Basic", company=company4)

session.add(prod3)
session.commit()

prod4 = Product(user_id=1, name="Twister", description="Basic High Speed Fan",
                     price="Rs. 1250",categary="Basic", company=company4)

session.add(prod4)
session.commit()

print "added Product items!"
