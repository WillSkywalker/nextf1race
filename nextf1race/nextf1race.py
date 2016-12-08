#!/usr/bin/env python
# -_- coding: utf-8 -_-

import os.path
import sys
import json
import datetime
import argparse

NOW = datetime.datetime.utcnow()
TIMELAG = datetime.datetime.now() - NOW
# UTCNOW = datetime.datetime.utcnow()
MONTHS = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec')
DATAPATH = os.path.abspath(os.path.join(os.path.realpath(__file__), '../../data/'))


class NextF1Race(object):

    def __init__(self, calendar_file=DATAPATH+'/%d.json' % NOW.year, 
                 next_year_calendar_file = DATAPATH+'/%d.json' % (NOW.year + 1), 
                 circuit_file=DATAPATH+'/circuits.json'):
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
            circuit = self.circuits[next['circuit']]
            race_time = list(map(int, circuit['time']['Race'].split(':')))
        next['gap'] = datetime.datetime(NOW.year+1, race['date'][0], 
            race['date'][1], race_time[0], race_time[1]) - NOW
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


def print_time(times, lag=TIMELAG, is_monaco=False):
    for i in times:
        t = datetime.datetime.strptime(times[i], '%H:%M') + lag
        times[i] = datetime.datetime.strftime(t, '%H:%M')
    if is_monaco:
        print("Practice 1: " + times['Practice 1'] + ' Thursday')
        print("Practice 2: " + times['Practice 2'] + ' Thursday')
    else:
        print("Practice 1: " + times['Practice 1'] + ' Friday')
        print("Practice 2: " + times['Practice 2'] + ' Friday')
    print("Practice 3: " + times['Practice 3'] + ' Saturday')
    print("Qualifying: " + times['Qualifying'] + ' Saturday')
    print("      Race: " + times['Race'] + ' Sunday')


def main():
    parser = argparse.ArgumentParser(description='What\'s the next Formula 1 race?')
    parser.add_argument('-d', '--detailed', action='store_true')
    parser.add_argument('-s', '--simplified', action='store_true')
    args = vars(parser.parse_args())

    n = NextF1Race()
    next_race = n.next_race()
    timestr = format_timedelta(next_race['gap'])


    print('Next race: %s Grand Prix, on %s %2d' % (next_race['country'], 
        MONTHS[next_race['date'][0]-1], next_race['date'][1]))
    print(timestr)

    if not args['simplified']:
        print('')
        print_time(next_race['circuit']['time'])


    if args['detailed']:
        print('')
        c = next_race['circuit']
        print(c['description'].strip())
        print('')
        print('First Grand Prix: %s' % c['First Grand Prix'])
        print('Circuit Length: %s' % c['Circuit Length'])
        print('Race Distance: %s' % c['Race Distance'])
        print('Lap Record: %s' % c['Lap Record'])
        print('Number of Laps: %s' % c['Number of Laps'])



if __name__ == '__main__':
    main()

