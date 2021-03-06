# stock-table.py
from urllib.request import urlopen
from bs4 import BeautifulSoup
import plotly
import plotly.graph_objects as go


def HistoralStock(CODE, days=180):
    url = 'https://www.settrade.com/C04_02_stock_historical_p1.jsp?txtSymbol={}&selectPage=2&max={}&offset=0'.format(
        CODE, days)

    webopen = urlopen(url)
    pagehtml = webopen.read()
    webopen.close()

    data = BeautifulSoup(pagehtml, 'html.parser')

    # print(data.get_text())

    table = data.find('table', {'class': 'table table-info table-hover'})
    # ຖ້າມີ table ທີ່ມີຊື່ຄລາສນີ້ພຽງຄລາສດຽວ ສາມາດໃຊ້ .find ໄດ້ ທີ່ຈະອອກມາພຽງແຕ່ 1 ລາຍການ ບໍ່ຕ້ອງຣັນລູປ

    table = table.find_all('tr')[1:]
    # print(table)

    result = []

    for row in table:
        column = row.find_all('td')
        # print(column)
        column_list = []
        for i, c in enumerate(column):
            if i != 0:
                column_list.append(float(c.text.replace(',', '')))
            else:
                column_list.append(c.text)
        # print(column_list)
        result.append(column_list)
        # print('-------')

    return result


result = HistoralStock('FORTH', 20)
print(result)

price = []
day = []

for rs in result:
    price.append(rs[5])
    day.append(rs[0])

print(price)

x = range(len(price))

price.reverse()
day.reverse()

plotly.offline.plot(
    {
        "data": [go.Scatter(x=day, y=price)],
        "layout": go.Layout(title="Stock : FORTH")
    }, auto_open=True)
