#!/usr/bin/env python
# -_- coding: utf-8 -_-

import json
import datetime

NOW = datetime.datetime.now()
UTCNOW = datetime.datetime.utcnow()



class NextF1Race(object):

    def __init__(self, calendar_file='../data/%d.json' % NOW.year, 
                 next_year_calendar_file = '../data/%d.json' % (NOW.year + 1), 
                 circuit_file='../data/circuits.json'):
        super(NextF1Race, self).__init__()
        with open(calendar_file) as fnow,\
             open(next_year_calendar_file) as fnext,\
             open(circuit_file) as fcircuit:
            self.this_year = json.load(fnow)
            self.next_year = json.load(fnext)
            self.circuits = json.load(fcircuit)
        self.calendar = self.this_year + self.next_year[:1]


    def next_race(self):
        NOW = datetime.datetime.utcnow()
        for race in self.calendar:
            race_date = datetime.datetime(NOW.year, race['date'][0], 
                                          race['date'][1])
            if race_date > NOW:
                next_race = race
                next_race['gap'] = race_date - NOW
                break
        else:
            next = self.calendar[-1]
        next['gap'] = datetime.datetime(NOW.year+1, 
            race['date'][0], race['date'][1]) - NOW
        return next




def main():
    n = NextF1Race()
    next_race = n.next_race()

    print('Next race: %s Grand Prix' % next_race['country'])


if __name__ == '__main__':
    main()

