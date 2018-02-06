from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Catalog, Investment, User

engine = create_engine('sqlite:///itemcatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Warren Buffett", email="wb@gmail.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')

session.add(User1)
session.commit()

# Investments for Stocks
catalog1 = Catalog(user_id=1, name="Stocks")

session.add(catalog1)
session.commit()

investment1 = Investment(user_id=1, name="Alibaba Group Holding Ltd", description="A Chinese multinational e-commerce, retail, Internet and technology conglomerate founded in 1999 that provides consumer-to-consumer, business-to-consumer and business-to-business sales services via web portals, as well as electronic payment services, shopping search engines and data-centric cloud computing services. It also owns and operates a diverse array of businesses around the world in numerous sectors.", price="$189", catalog=catalog1)

session.add(investment1)
session.commit()

investment2 = Investment(user_id=1, name="The Phillips 66 Company", description="An American multinational energy company headquartered in Westchase, Houston, Texas. It debuted as an independent energy company when ConocoPhillips executed a spin-off of its downstream and midstream assets. The company is engaged in producing natural gas liquids (NGL) and petrochemicals. The company has approximately 14,000 employees worldwide and is active in more than 65 countries.", price="$102", catalog=catalog1)

session.add(investment2)
session.commit()

investment3 = Investment(user_id=1, name="The Coca-Cola Company", description="Coca-Cola, or Coke, is a carbonated soft drink produced by The Coca-Cola Company. Originally intended as a patent medicine, it was invented in the late 19th century by John Pemberton and was bought out by businessman Asa Griggs Candler, whose marketing tactics led Coca-Cola to its dominance of the world soft-drink market throughout the 20th century. The drink's name refers to two of its original ingredients, which were kola nuts (a source of caffeine) and coca leaves. The current formula of Coca-Cola remains a trade secret, although a variety of reported recipes and experimental recreations have been published.", price="$46", catalog=catalog1)

session.add(investment3)
session.commit()

# Investments for Bonds
catalog2 = Catalog(user_id=1, name="Bonds")

session.add(catalog2)
session.commit()

investment1 = Investment(user_id=1, name="US Treasuries", description="Marketable securities from the U.S. government - known collectively as 'Treasuries' - follow this guideline and are issued as Treasury bonds, Treasury notes and Treasury bills (T-bills). All debt issued by the U.S. government is regarded as extremely safe, often referred to as 'risk-free' securities, as is the debt of many stable countries.", price="N/A", catalog=catalog2)

session.add(investment1)
session.commit()

investment2 = Investment(user_id=1, name="Corporate Bonds", description="Large corporations have a great deal of flexibility as to how much debt they can issue: the limit is generally whatever the market will bear. A corporate bond is considered short-term corporate when the maturity is less than five years; intermediate is five to 12 years, and long-term is over 12 years. Corporate bonds are characterized by higher yields than government securities because there is a higher risk of a company defaulting than a government. The upside is that they can also be the most rewarding fixed-income investments because of the risk the investor must take on, where higher credit companies that are more likely to pay back their obligations will carry a relatively lower interest rate than riskier borrowers. Companies can issue bonds with fixed or variable interest rates and of varying maturity. Bonds issued by highly rated companies are referred to as investment grade while those below investment grade are junk or high-yield.", price="N/A", catalog=catalog2)

session.add(investment2)
session.commit()

investment3 = Investment(user_id=1, name="Asset-Backed Securities", description="Issued by banks or other financial sector participants and are referred to as asset-backed securities or ABS. These bonds are created by packaging up the cash flows generated by a number of similar assets and offering them to investors. If such a bond is backed by a number of mortgages, they are known as mortgage-backed securities or MBS. These bonds are typically reserved for sophisticated or institutional investors and not individuals.", price="N/A", catalog=catalog2)

session.add(investment3)
session.commit()

# Investments for Funds
catalog3 = Catalog(user_id=1, name="Funds")

session.add(catalog3)
session.commit()

investment1 = Investment(user_id=1, name="Exchange-Traded Fund (ETF)", description="An ETF, or exchange-traded fund, is a marketable security that tracks an index, a commodity, bonds, or a basket of assets like an index fund. Unlike mutual funds, an ETF trades like a common stock on a stock exchange. ETFs experience price changes throughout the day as they are bought and sold. ETFs typically have higher daily liquidity and lower fees than mutual fund shares, making them an attractive alternative for individual investors.", price="N/A", catalog=catalog3)

session.add(investment1)
session.commit()

investment2 = Investment(user_id=1, name="Real Estate Investment Trust (REIT)", description="A real estate investment trust, or REIT, is a company that owns, operates or finances income-producing real estate. For a company to qualify as a REIT, it must meet certain regulatory guidelines. REITs often trades on major exchanges like other securities and provide investors with a liquid stake in real estate. ", price="N/A", catalog=catalog3)

session.add(investment2)
session.commit()

investment3 = Investment(user_id=1, name="Hedge Fund", description="Hedge funds are alternative investments using pooled funds that employ numerous different strategies to earn active return, or alpha, for their investors. Hedge funds may be aggressively managed or make use of derivatives and leverage in both domestic and international markets with the goal of generating high returns (either in an absolute sense or over a specified market benchmark). It is important to note that hedge funds are generally only accessible to accredited investors as they require less SEC regulations than other funds. One aspect that has set the hedge fund industry apart is the fact that hedge funds face less regulation than mutual funds and other investment vehicles.", price="N/A", catalog=catalog3)

session.add(investment3)
session.commit()

# Investments for Real Estate
catalog4 = Catalog(user_id=1, name="Real Estate")

session.add(catalog4)
session.commit()

investment1 = Investment(user_id=1, name="Apartment", description="An Apartment", price="N/A", catalog=catalog4)

session.add(investment1)
session.commit()

investment2 = Investment(user_id=1, name="Parking lot", description="A parking lot", price="N/A", catalog=catalog4)

session.add(investment2)
session.commit()

print "added menu items!"

