tracks = [
    'http://www.formula1.com/en/championship/races/2016/Australia.html',
    'http://www.formula1.com/en/championship/races/2016/Bahrain.html',
    'http://www.formula1.com/en/championship/races/2016/China.html',
    'http://www.formula1.com/en/championship/races/2016/Russia.html',
    'http://www.formula1.com/en/championship/races/2016/Spain.html',
    'http://www.formula1.com/en/championship/races/2016/Monaco.html',
    'http://www.formula1.com/en/championship/races/2016/Canada.html',
    'http://www.formula1.com/en/championship/races/2016/Europe.html',
    'http://www.formula1.com/en/championship/races/2016/Austria.html',
    'http://www.formula1.com/en/championship/races/2016/Great_Britain.html',
    'http://www.formula1.com/en/championship/races/2016/Hungary.html',
    'http://www.formula1.com/en/championship/races/2016/Germany.html',
    'http://www.formula1.com/en/championship/races/2016/Belgium.html',
    'http://www.formula1.com/en/championship/races/2016/Italy.html',
    'http://www.formula1.com/en/championship/races/2016/Singapore.html',
    'http://www.formula1.com/en/championship/races/2016/Malaysia.html',
    'http://www.formula1.com/en/championship/races/2016/Japan.html',
    'http://www.formula1.com/en/championship/races/2016/United_States.html',
    'http://www.formula1.com/en/championship/races/2016/Mexico.html',
    'http://www.formula1.com/en/championship/races/2016/Brazil.html',
    'http://www.formula1.com/en/championship/races/2016/Abu_Dhabi.html'
]


import json
import requests 
from bs4 import BeautifulSoup

def get_info(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    raw_info = soup.find_all('div', {'class': 'circuit-info-container'})
    raw_time = soup.find('dl', {'class': 'race-data-dl desktop'}) 
    name = soup.find('div', {'class': 'parbase text'}).text.strip()
    info = {i: j for i, j in map(lambda x: (x.h5.text.strip().replace('\n', ' '),\
                                            x.p.text.strip()), raw_info)}
    info['time'] = {x[0].text.strip(): x[1].text.strip()[:5]\
                    for x in zip(raw_time.find_all('dt'), 
                                 raw_time.find_all('dd', {'class': 'bold time'}))}
    info['description'] = soup.find_all('div', {'class': 'parbase text'})[1].p.text.strip()
    return name, info


def main():
    ans = input('WARNING: Using this script will overwrite current circuit information \
        and cause chaos of timezone. You must change race time to UTC MANUALLY later! Continue? (yes/no)')
    if ans != 'yes': return
    with open('circuits_temp.json', 'w') as f:
        circuits = {}
        for t in tracks:
            name, info = get_info(t)
            circuits[name] = info
        json.dump(circuits, f)



if __name__ == '__main__':
    # print(get_info(tracks[0]))
    main()
