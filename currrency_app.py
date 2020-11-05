import requests
import xml.etree.ElementTree as ET
from flask import Flask
from flask_restful import Api, Resource, reqparse


app = Flask(__name__)
api = Api(app)

@api.resource('/showcurrency')
class ListOfCurrency(Resource):
    def get(self):
        url = 'http://www.cbr.ru/scripts/XML_valFull.asp'
        response = requests.get(url)
        response = response.content
        answer = {}
        root = ET.fromstring(response)
        for child in root.findall('Item'):
            answer[child.find('ISO_Char_Code').text] = child.find('EngName').text
        return answer

@api.resource('/diff')
class DifferRates(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('char_code', type=str)
        parser.add_argument('date_first', type=str)
        parser.add_argument('date_second', type=str)
        args = parser.parse_args()

        char_code = args['char_code']
        date_first = args['date_first']
        date_second = args['date_second']

        def parser_date(date):
            date = date[8:] + '/' + date[5:7] + '/' + date[:4]
            return date

        if char_code is None or date_first is None or date_second is None:
            return {'Message': 'Incorrect input!'}
        
        url_id = 'http://www.cbr.ru/scripts/XML_valFull.asp'

        date_1 = parser_date(date_first)
        date_2 = parser_date(date_second)

        response_id = requests.get(url_id).content
        root = ET.fromstring(response_id)
        answer = None
        for child in root.findall('Item'):
            if child.find('ISO_Char_Code').text == char_code:
                answer = child.attrib['ID']
                break
        
        if answer is None:
            return {'Message': 'This char code is not found!'}
        
        url_rate = 'http://www.cbr.ru/scripts/XML_dynamic.asp'

        params = {'date_req1': date_1, 'date_req2': date_2, 'VAL_NM_RQ': answer}
        response_rate = requests.get(url_rate, params=params).content
        root = ET.fromstring(response_rate)
        rate_1 = None
        rate_2 = None
        date_1 = date_1.replace('/', '.')
        date_2 = date_2.replace('/', '.')
        for child in root.findall('Record'):
            if child.attrib['Date'] == date_1:
                rate_1 = child.find('Value').text.replace(',', '.')
            if child.attrib['Date'] == date_2:
                rate_2 = child.find('Value').text.replace(',', '.')

        if rate_1 is None:
            return {'Message': 'Rate for the first date is not found'}
        if rate_2 is None:
            return {'Message': 'Rate for the second date is not found'}

        diff = round(float(rate_2)-float(rate_1), 4)
        if diff >= 0:
            diff = '+' + str(diff)

        return {'The first date': date_first, 'The second date': date_second,
                'Differance rate': diff}


app.run(debug=False)

