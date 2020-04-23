# encoding: utf-8

from bs4 import BeautifulSoup
import requests
import urllib3
urllib3.disable_warnings()

url_source = 'https://ncov.moh.gov.vn'

class ncov:
    def get():
        try:
            response = requests.get(url = url_source, verify = False).text
            soup = BeautifulSoup(response, 'html.parser')
            section_data= soup.find('section', {'class': 'bg-xanh123'})
            data = section_data.findAll('div', {'class': 'row fivecolumns'})
            vn_data = data[0].findAll('span')
            qt_data = data[1].findAll('span')

            res_vn = []
            res_qt = []
            icount = 1
            for item in vn_data:
                icount = icount + 1
                if icount > 2:
                    res_vn.append(item.text)
            icount = 1     
            for item in qt_data:
                icount = icount + 1
                if icount > 2:
                    res_qt.append(item.text)
        except:
            None
            
        return (res_vn, res_qt)

