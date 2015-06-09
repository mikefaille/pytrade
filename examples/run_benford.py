from util.edgar import Edgar

import util.pybenford as pyb

edgar = Edgar()
stock = 'GOGO'

data = edgar.get_financial_docs(stock)
values = []

for item in data['result']['rows'][0]['values']:
    try:
	if item['value'] is not None:
            values.append(int(item['value']))
    except ValueError:
        pass

benford_law   = pyb.benford_law()
benford_stock = pyb.calc_firstdigit(values[12:])

pyb.plot_comparative(benford_stock, benford_law, str(stock) + " Financial Statement Numbers ")

