import urllib

class Filter(object):
   
    def get_all_categories(self):
	return self.filter_dict.keys()

    # Endpoint
    def __init__(self):
        self.url = 'https://screener.finance.yahoo.com/b?'
    
        # List of filters and values
        self.filter_dict = {
            'sc': {
                    '431': 'Accident & Health Insurance (Financial)',
                    '720': 'Advertising Agencies (Services)',
                    '610': 'Aerospace/Defense - Major Diversified (Industrial Goods)',
                    '611': 'Aerospace/Defense Products & Services (Industrial Goods)',
                    '112': 'Agricultural Chemicals (Basic Materials)',
                    '773': 'Air Delivery & Freight Services (Services)',
                    '772': 'Air Services, Other (Services)',
                    '132': 'Aluminum (Basic Materials)',
                    '730': 'Apparel Stores (Services)',
                    '310': 'Appliances (Consumer Goods)',
                    '821': 'Application Software (Technology)',
                    '422': 'Asset Management (Financial)',
                    '744': 'Auto Dealerships (Services)',
                    '330': 'Auto Manufacturers - Major (Consumer Goods)',
                    '333': 'Auto Parts (Consumer Goods)',
                    '738': 'Auto Parts Stores (Services)',
                    '750': 'Auto Parts Wholesale (Services)',
                    '758': 'Basic Materials Wholesale (Services)',
                    '346': 'Beverages - Brewers (Consumer Goods)',
                    '348': 'Beverages - Soft Drinks (Consumer Goods)',
                    '347': 'Beverages - Wineries & Distillers (Consumer Goods)',
                    '515': 'Biotechnology (Healthcare)',
                    '724': 'Broadcasting - Radio (Services)',
                    '723': 'Broadcasting - TV (Services)',
                    '751': 'Building Materials Wholesale (Services)',
                    '313': 'Business Equipment (Consumer Goods)',
                    '760': 'Business Services (Services)',
                    '826': 'Business Software & Services (Technology)',
                    '725': 'CATV Systems (Services)',
                    '739': 'Catalog & Mail Order Houses (Services)',
                    '633': 'Cement (Industrial Goods)',
                    '110': 'Chemicals - Major Diversified (Basic Materials)',
                    '350': 'Cigarettes (Consumer Goods)',
                    '326': 'Cleaning Products (Consumer Goods)',
                    '841': 'Communication Equipment (Technology)',
                    '812': 'Computer Based Systems (Technology)',
                    '815': 'Computer Peripherals (Technology)',
                    '755': 'Computers Wholesale (Services)',
                    '345': 'Confectioners (Consumer Goods)',
                    '210': 'Conglomerates (Conglomerates)',
                    '763': 'Consumer Services (Services)',
                    '131': 'Copper (Basic Materials)',
                    '424': 'Credit Services (Financial)',
                    '344': 'Dairy Products (Consumer Goods)',
                    '813': 'Data Storage Devices (Technology)',
                    '731': 'Department Stores (Services)',
                    '516': 'Diagnostic Substances (Healthcare)',
                    '732': 'Discount, Variety Stores (Services)',
                    '846': 'Diversified Communication Services (Technology)',
                    '810': 'Diversified Computer Systems (Technology)',
                    '836': 'Diversified Electronics (Technology)',
                    '423': 'Diversified Investments (Financial)',
                    '622': 'Diversified Machinery (Industrial Goods)',
                    '913': 'Diversified Utilities (Utilities)',
                    '513': 'Drug Delivery (Healthcare)',
                    '510': 'Drug Manufacturers - Major (Healthcare)',
                    '511': 'Drug Manufacturers - Other (Healthcare)',
                    '514': 'Drug Related Products (Healthcare)',
                    '733': 'Drug Stores (Services)',
                    '512': 'Drugs - Generic (Healthcare)',
                    '756': 'Drugs Wholesale (Services)',
                    '766': 'Education & Training Services (Services)',
                    '911': 'Electric Utilities (Utilities)',
                    '314': 'Electronic Equipment (Consumer Goods)',
                    '735': 'Electronics Stores (Services)',
                    '753': 'Electronics Wholesale (Services)',
                    '722': 'Entertainment - Diversified (Services)',
                    '620': 'Farm & Construction Machinery (Industrial Goods)',
                    '341': 'Farm Products (Consumer Goods)',
                    '340': 'Food - Major Diversified (Consumer Goods)',
                    '757': 'Food Wholesale (Services)',
                    '417': 'Foreign Money Center Banks (Financial)',
                    '418': 'Foreign Regional Banks (Financial)',
                    '910': 'Foreign Utilities (Utilities)',
                    '714': 'Gaming Activities (Services)',
                    '912': 'Gas Utilities (Utilities)',
                    '634': 'General Building Materials (Industrial Goods)',
                    '636': 'General Contractors (Industrial Goods)',
                    '716': 'General Entertainment (Services)',
                    '134': 'Gold (Basic Materials)',
                    '734': 'Grocery Stores (Services)',
                    '522': 'Health Care Plans (Healthcare)',
                    '825': 'Healthcare Information Services (Technology)',
                    '635': 'Heavy Construction (Industrial Goods)',
                    '737': 'Home Furnishing Stores (Services)',
                    '311': 'Home Furnishings & Fixtures (Consumer Goods)',
                    '526': 'Home Health Care (Healthcare)',
                    '736': 'Home Improvement Stores (Services)',
                    '524': 'Hospitals (Healthcare)',
                    '312': 'Housewares & Accessories (Consumer Goods)',
                    '121': 'Independent Oil & Gas (Basic Materials)',
                    '627': 'Industrial Electrical Equipment (Industrial Goods)',
                    '621': 'Industrial Equipment & Components (Industrial Goods)',
                    '752': 'Industrial Equipment Wholesale (Services)',
                    '133': 'Industrial Metals & Minerals (Basic Materials)',
                    '827': 'Information & Delivery Services (Technology)',
                    '824': 'Information Technology Services (Technology)',
                    '434': 'Insurance Brokers (Financial)',
                    '851': 'Internet Information Providers (Technology)',
                    '850': 'Internet Service Providers (Technology)',
                    '852': 'Internet Software & Services (Technology)',
                    '420': 'Investment Brokerage - National (Financial)',
                    '421': 'Investment Brokerage - Regional (Financial)',
                    '742': 'Jewelry Stores (Services)',
                    '430': 'Life Insurance (Financial)',
                    '710': 'Lodging (Services)',
                    '843': 'Long Distance Carriers (Technology)',
                    '523': 'Long-Term Care Facilities (Healthcare)',
                    '632': 'Lumber, Wood Production (Industrial Goods)',
                    '624': 'Machine Tools & Accessories (Industrial Goods)',
                    '770': 'Major Airlines (Services)',
                    '120': 'Major Integrated Oil & Gas (Basic Materials)',
                    '769': 'Management Services (Services)',
                    '631': 'Manufactured Housing (Industrial Goods)',
                    '721': 'Marketing Services (Services)',
                    '343': 'Meat Products (Consumer Goods)',
                    '521': 'Medical Appliances & Equipment (Healthcare)',
                    '754': 'Medical Equipment Wholesale (Services)',
                    '520': 'Medical Instruments & Supplies (Healthcare)',
                    '525': 'Medical Laboratories & Research (Healthcare)',
                    '527': 'Medical Practitioners (Healthcare)',
                    '626': 'Metal Fabrication (Industrial Goods)',
                    '410': 'Money Center Banks (Financial)',
                    '447': 'Mortgage Investment (Financial)',
                    '726': 'Movie Production, Theaters (Services)',
                    '820': 'Multimedia & Graphics Software (Technology)',
                    '743': 'Music & Video Stores (Services)',
                    '814': 'Networking & Communication Devices (Technology)',
                    '136': 'Nonmetallic Mineral Mining (Basic Materials)',
                    '327': 'Office Supplies (Consumer Goods)',
                    '123': 'Oil & Gas Drilling & Exploration (Basic Materials)',
                    '124': 'Oil & Gas Equipment & Services (Basic Materials)',
                    '125': 'Oil & Gas Pipelines (Basic Materials)',
                    '122': 'Oil & Gas Refining & Marketing (Basic Materials)',
                    '325': 'Packaging & Containers (Consumer Goods)',
                    '324': 'Paper & Paper Products (Consumer Goods)',
                    '811': 'Personal Computers (Technology)',
                    '323': 'Personal Products (Consumer Goods)',
                    '762': 'Personal Services (Services)',
                    '318': 'Photographic Equipment & Supplies (Consumer Goods)',
                    '623': 'Pollution & Treatment Controls (Industrial Goods)',
                    '835': 'Printed Circuit Boards (Technology)',
                    '342': 'Processed & Packaged Goods (Consumer Goods)',
                    '842': 'Processing Systems & Products (Technology)',
                    '432': 'Property & Casualty Insurance (Financial)',
                    '448': 'Property Management (Financial)',
                    '729': 'Publishing - Books (Services)',
                    '727': 'Publishing - Newspapers (Services)',
                    '728': 'Publishing - Periodicals (Services)',
                    '440': 'REIT - Diversified (Financial)',
                    '442': 'REIT - Healthcare Facilities (Financial)',
                    '443': 'REIT - Hotel/Motel (Financial)',
                    '444': 'REIT - Industrial (Financial)',
                    '441': 'REIT - Office (Financial)',
                    '445': 'REIT - Residential (Financial)',
                    '446': 'REIT - Retail (Financial)',
                    '776': 'Railroads (Services)',
                    '449': 'Real Estate Development (Financial)',
                    '317': 'Recreational Goods, Other (Consumer Goods)',
                    '332': 'Recreational Vehicles (Consumer Goods)',
                    '412': 'Regional - Mid-Atlantic Banks (Financial)',
                    '414': 'Regional - Midwest Banks (Financial)',
                    '411': 'Regional - Northeast Banks (Financial)',
                    '416': 'Regional - Pacific Banks (Financial)',
                    '413': 'Regional - Southeast Banks (Financial)',
                    '415': 'Regional - Southwest Banks (Financial)',
                    '771': 'Regional Airlines (Services)',
                    '761': 'Rental & Leasing Services (Services)',
                    '768': 'Research Services (Services)',
                    '630': 'Residential Construction (Industrial Goods)',
                    '711': 'Resorts & Casinos (Services)',
                    '712': 'Restaurants (Services)',
                    '322': 'Rubber & Plastics (Consumer Goods)',
                    '419': 'Savings & Loans (Financial)',
                    '837': 'Scientific & Technical Instruments (Technology)',
                    '765': 'Security & Protection Services (Services)',
                    '823': 'Security Software & Services (Technology)',
                    '830': 'Semiconductor - Broad Line (Technology)',
                    '833': 'Semiconductor - Integrated Circuits (Technology)',
                    '832': 'Semiconductor - Specialized (Technology)',
                    '834': 'Semiconductor Equipment & Materials (Technology)', 
                    '831': 'Semiconductor- Memory Chips (Technology)',
                    '775': 'Shipping (Services)',
                    '135': 'Silver (Basic Materials)',
                    '625': 'Small Tools & Accessories (Industrial Goods)',
                    '528': 'Specialized Health Services (Healthcare)',
                    '113': 'Specialty Chemicals (Basic Materials)',
                    '713': 'Specialty Eateries (Services)',
                    '745': 'Specialty Retail, Other (Services)',
                    '715': 'Sporting Activities (Services)',
                    '316': 'Sporting Goods (Consumer Goods)',
                    '740': 'Sporting Goods Stores (Services)',
                    '764': 'Staffing & Outsourcing Services (Services)',
                    '130': 'Steel & Iron (Basic Materials)',
                    '433': 'Surety & Title Insurance (Financial)',
                    '111': 'Synthetics (Basic Materials)',
                    '822': 'Technical & System Software (Technology)',
                    '767': 'Technical Services (Services)',
                    '844': 'Telecom Services - Domestic (Technology)',
                    '845': 'Telecom Services - Foreign (Technology)',
                    '320': 'Textile - Apparel Clothing (Consumer Goods)',
                    '321': 'Textile - Apparel Footwear & Accessories (Consumer Goods)',
                    '628': 'Textile Industrial (Industrial Goods)',
                    '351': 'Tobacco Products, Other (Consumer Goods)',
                    '741': 'Toy & Hobby Stores (Services)',
                    '315': 'Toys & Games (Consumer Goods)',
                    '774': 'Trucking (Services)',
                    '331': 'Trucks & Other Vehicles (Consumer Goods)',
                    '637': 'Waste Management (Industrial Goods)',
                    '914': 'Water Utilities (Utilities)',
                    '759': 'Wholesale, Other (Services)',
                    '840': 'Wireless Communications (Technology)'
            },
             'im' : {
                '^DJI': 'Dow Jones Industrials',
                '^DJT': 'Dow Jones Transportation',
                '^DJU': 'Dow Jones Utilities',
                '^SPC': 'S&P 500',
                '^MID': 'S&P 400 MidCap',
                '^SML': 'S&P 600 SmallCap'     
            },
            'prmin': 'int',
            'prmax': 'int',
            'mcmin': 'int',
            'mxmax': 'int',
            'dvymin': 'pct',
            'dvymax': 'pct',
            'betamin': 'float',
            'betamax': 'float',              
            'remin': 'int',
            'remax': 'int',
            'pmmin': 'pct',
            'pmmax': 'pct',
            'pemin': 'int',
            'pemax': 'int',
            'pbmin': 'int',
            'pbmax': 'int',
            'psmin': 'int',
            'psmax': 'int',
            'pegmin': 'float',
            'pegmax': 'float',
            'gr': {
                '250/': 'Up more than 100%',
                '200/': 'Up more than 50%',
                '180/': 'Up more than 30%',
                '175/': 'Up more than 25%',
                '170/': 'Up more than 20%',
                '165/': 'Up more than 15%',
                '160/': 'Up more than 10%',
                '155/': 'Up more than 5%',
                '150/': 'Up more than 0%',
                '50/150': 'Down more than 0%',
                '50/140': 'Down more than 10%',
                '50/125': 'Down more than 25%',
                '50/100': 'Down more than 50%',       
            },
            'grfy': {
                '250/': 'Up more than 100%',
                '200/': 'Up more than 50%',
                '180/': 'Up more than 30%',
                '175/': 'Up more than 25%',
                '170/': 'Up more than 20%',
                '165/': 'Up more than 15%',
                '160/': 'Up more than 10%',
                '155/': 'Up more than 5%',
                '150/': 'Up more than 0%',
                '50/150': 'Down more than 0%',
                '50/140': 'Down more than 10%',
                '50/125': 'Down more than 25%',
                '50/100': 'Down more than 50%',         
            },
            'ar': {
                '1': 'Buy Rating (1)',
                '1/2': 'Buy/Hold rating (2) or better',
                '1/3': 'Hold Rating (3) or better',
                '4/5': 'Hold/Sell Rating (4) or worse',
                '5': 'Sell Rating (5)',       
            },
            'vw' : {
                '1': 'Actively Screened',
                '2': 'Share',
                '4': 'Sales & Profitablility',
                '5': 'Valuation Ratios',
                '6': 'Analyst Estimates',
            },
        }
        
        # Description of filters
        self.filter_desc = {
            'sc': 'Industry',
            'im': 'Index Membership',
            'prmin': 'Share Price (min)',
            'prmax': 'Share Price (max)',
            'mcmin': 'Market Cap (min)',
            'mxmax': 'Market Cap (max)',
            'dvymin': 'Dividend Yield (min)',
            'dvymax': 'Dividend Yield (max)',
            'betamin': 'Beta (min)',
            'remin': 'Sales Revenue (min)',
            'remax': 'Sales Revenue (max)',
            'pmmin': 'Profit Margin (min)',
            'pmmax': 'Profit Margin (max)',
            'pemin': 'Price / Earnings (min)',
            'pemax': 'Price / Earnings (max)',
            'pbmin': 'Price / Book (min)',
            'pbmax': 'Price / Book (max)',
            'psmin': 'Price / Sales (min)',
            'psmax': 'Price / Sales (max)',
            'pegmin': 'PEG Ratio (min)',
            'pegmax': 'PEG Ratio (max)',
            'gr': 'Est. 1 Yr EPS Growth',
            'grfy': 'Est. 5 Yr EPS Growth',
            'ar': 'Avg. Analyst Rec:',
            'vw': 'Display info for...',
        }
    
    # Returns the list of filters
    def get_filters(self):
        return self.filter_list
    
    # Prints a list of filters
    def list_filters(self):
        print'Filter List:'
        for key in self.filter_desc:
            print key, 'is the', self.filter_exp[key]
        
    # Explains a filter
    def explain_filter(self, filter):
        try:
            print self.filter_desc[filter]
        except KeyError:
            print 'Filter ', filter,' not found'

    # Return values for a given filter
    def get_values(self, filter):
        try:
            dct = self.filter_dict[filter]
            if isinstance(dct, dict):
                for key in dct:
                    print key, ': ', dct[key]
            else:
                if dct == 'int':
                    print 'Integer values'
                elif dct == 'float':
                    print 'Floating point values'
                elif dct == 'pct':
                    print 'Percentage'
        except KeyError:
            print 'Filter ', filter,' not found'
            
    # Build a query string
    # Accepts a list of tuples
    def build_query_string(self, params):
        url = self.url + 'db=stocks'
        for tpl in params:
            try:
                if tpl[0] not in self.filter_dict:
                    raise KeyError(tpl[0] + ' is not a valid filter')
                # @TODO implement value check
                elem = '&' + str(tpl[0]) + '=' + str(tpl[1])
                #elem = urllib.quote(elem)
                url += elem
            except KeyError:
                print tpl, 'is not a valid tuple'
                
        return url
