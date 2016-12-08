#!/usr/bin/env python
# -_- coding: utf-8 -_-

import sys
import json
import datetime
import argparse

NOW = datetime.datetime.utcnow()
# UTCNOW = datetime.datetime.utcnow()



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
            circuit = self.circuits[race['circuit']]
            race_time = list(map(int, circuit['time']['Race'].split(':')))
            race_date = datetime.datetime(NOW.year, race['date'][0], race['date'][1], 
                                          race_time[0], race_time[1])
            if race_date > NOW:
                next = race
                next['gap'] = race_date - NOW
                break
        else:
            next = self.calendar[-1]
        next['gap'] = datetime.datetime(NOW.year+1, 
            race['date'][0], race['date'][1]) - NOW
        next['circuit'] = self.circuits[next['circuit']]
        return next


def format_timedelta(timedelta):
    hours, seconds = divmod(timedelta.seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    timestr = 'In '

    def add_part(name, num):
        s = ''
        if num:
            if num == 1:
                s += '1 %s ' % name
            else:
                s += '%d %ss ' % (num, name)
        return s

    timestr += add_part('day', timedelta.days)
    timestr += add_part('hour', hours)
    timestr += add_part('minute', minutes)
    timestr += add_part('second', seconds)

    return timestr.strip()


def main():
    parser = argparse.ArgumentParser(description='What\'s the next Formula 1 race?')
    parser.add_argument('-d', '--detailed', action='store_true')
    parser.add_argument('-s', '--simplified', action='store_true')
    args = vars(parser.parse_args())

    n = NextF1Race()
    next_race = n.next_race()
    timestr = format_timedelta(next_race['gap'])


    print('Next race: %s Grand Prix' % next_race['country'])
    print(timestr)

    if not args['simplified']:
        print(next_race['circuit']['time'])


    if args['detailed']:
        print('stay tuned...')



if __name__ == '__main__':
    main()

