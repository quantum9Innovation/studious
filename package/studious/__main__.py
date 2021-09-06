
import os, time, random
from copy import deepcopy
import matplotlib as mpl
from matplotlib import pyplot as plt
from termcolor import cprint
import fire
from . import metadata

def setup():
    os.chdir(os.path.expanduser('~/.config/'))
    
    if not os.path.exists(os.path.expanduser('~/.config/studious/')):
        os.mkdir('studious/')
        with open('studious/events.csv', 'w') as f:
            f.write('name,abbr,duration,percent\n')
        with open('studious/logs.csv', 'w') as f:
            f.write('abbr,minutes\n')
    
    os.chdir(os.path.expanduser('~/.config/studious/'))

class Shell(object):
    """A time manager for people without time"""

    def __init__(self, version=False):

        self.metadata = metadata
        setup()

        if version:
            cprint('studious @' + self.metadata['version'], 'green', 
                   attrs=['bold'])

    def _find(self, abbr):
        """Find event by abbreviation"""
        with open('events.csv', 'r') as f:
            for no, line in enumerate(f):
                if no == 0:
                    continue
                if line.split(',')[1] == abbr:
                    return no, line

    def _validate(self, duration, percent):
        """Validate duration and percent formats"""

        if len(duration) != 4:
            raise ValueError('Duration must be in format h:mm')
        if duration[1] != ':':
            raise ValueError('Duration must be in format h:mm')

        if float(percent) > 100 or float(percent) < 0:
            raise ValueError('Percent must be between 0 and 100')

    def _rescale(self):
        """Rescale all percentage values so that their sum is 100"""

        outlines = []
        with open('events.csv', 'r') as f:
            outlines = f.readlines()
            lines = deepcopy(outlines)

            total = sum([float(line.split(',')[3]) for line in lines[1:]])

            for no, line in enumerate(lines):

                if no == 0:
                    continue

                name, abbr, duration, percent = line[:-1].split(',')
                percent = float(percent)
                percent = percent * 100 / total
                outlines[no] = name + ',' + abbr + ',' + duration + ',' + \
                               str(percent) + '\n'
        
        with open('events.csv', 'w') as f:
            f.writelines(outlines)

        cprint('Values were rescaled successfully!', 'grey')

    def schedule(self):
        """Create a pie chart of all the events"""

        cprint('Trigerring an auto-rescale ...')
        cprint('(Press Ctrl+C to cancel)', 'grey')
        time.sleep(3)
        self._rescale()

        labels = []
        sizes = []

        with open('events.csv', 'r') as f:
            for no, line in enumerate(f):
                if no == 0:
                    continue
                _, abbr, _, percent = line[:-1].split(',')
                labels.append(abbr)
                sizes.append(float(percent))

        plt.pie(sizes, labels=labels, startangle=90)
        plt.legend(labels, loc='best')
        plt.show()

    def pick(self):
        """
        Pick an event.

        Events are picked by totaling the time spent on each event using
        the logs. Then, these times are taken together and transformed 
        into percentages. The event that has the greatest difference 
        between the log percentage and actual percentage is selected.
        
        """
        # Total time spent on each event from logs
        totals = {}

        with open('logs.csv', 'r') as f:
            for no, line in enumerate(f):
                if no == 0:
                    continue
                abbr, minutes = line[:-1].split(',')
                try: 
                    totals[abbr] += int(minutes)
                except KeyError:
                    totals[abbr] = int(minutes)
        
        total = sum(totals.values())
        percentages = {}
        for abbr, minutes in totals.items():
            percentages[abbr] = 100 * minutes / total
        
        # Find the event with the greatest difference from the log
        # percentage and the actual percentage
        max_diff = 0
        max_abbr = None

        with open('events.csv', 'r') as f:
            lines = f.readlines()[1:]
            for line in lines:
                _, abbr, _, percent_log = line[:-1].split(',')
                try:
                    percent = percentages[abbr]
                except KeyError:
                    percent = 0
                
                diff = float(percent_log) - percent
                
                if diff >= max_diff:
                    max_diff = diff
                    max_abbr = abbr

        colors = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan']
        random.shuffle(colors)
        cprint('\n' + 'Work on ' + max_abbr + ' ...\n', colors[0], 
              attrs=['bold'])
        self.view(max_abbr)

    def add(self, name, abbr, duration, percent):
        """Add a new event to the list"""

        self._validate(duration, percent)

        if self._find(abbr):
            cprint('Event with the same abbreviation already exists!\n'
                  'Please choose a different abbreviation to continue.', 
                  'red', 'on_white')
            return

        with open('events.csv', 'a') as f:
            f.write(name + ',' + abbr + ',' + duration + ',' + 
                    str(percent) + '\n')

    def delete(self, abbr):
        """Delete an event by abbreviation"""
        if self._find(abbr):
            no, _ = self._find(abbr)
        else:
            cprint('Abbreviation not found!', 'red', 'on_white')
            return
        
        with open('events.csv', 'r') as f:
            lines = f.readlines()
            lines.pop(no)

        with open('events.csv', 'w') as f:
            f.writelines(lines)

    def modify(self, abbr, property, value):
        """
        Modify an existing event.
        
        abbr: Abbreviation of event to be modified
        property: The property of the event to modify;
                  one of:
                    - name
                    - abbr
                    - duration
                    - percent
        value: New value for the property

        """
        if self._find(abbr):
            no, line = self._find(abbr)
            name, abbrev, duration, percent = line[:-1].split(',')
            if property == 'name':
                name = value
            elif property == 'abbr':
                abbrev = value
            elif property == 'duration':
                self._validate(value, percent)
                duration = value
            elif property == 'percent':
                self._validate(duration, value)
                percent = value
            else:
                raise ValueError('Invalid property!')

            with open('events.csv', 'r') as f:
                lines = f.readlines()
                lines[no] = name + ',' + abbrev + ',' + duration + ',' \
                            + percent + '\n'

            with open('events.csv', 'w') as f:
                f.writelines(lines)
        else:
            cprint('Event not found!', 'red', 'on_white')

    def log(self, abbr):
        """Logs an activity after completion"""
        if self._find(abbr):
            _, line = self._find(abbr)
            name, _, duration, _ = line[:-1].split(',')

            hours = int(duration[0])
            minutes = int(duration[2:])
            time = 60 * hours + minutes

            with open('logs.csv', 'a') as f:
                f.write(abbr + ',' + str(time) + '\n')
            
            cprint('Logged ' + name + ' successfully', 'green')
        else:
            cprint('Event not found!', 'red', 'on_white')

    def logs(self):
        """View total event time from logs in a pie chart"""
        
        labels = []
        sizes = []

        with open('logs.csv', 'r') as f:
            for no, line in enumerate(f):
                if no == 0:
                    continue
                
                abbr, minutes = line[:-1].split(',')
                found = False

                for label in labels:
                    if label == abbr:
                        found = True
                        sizes[labels.index(label)] += int(minutes)
                        break

                if not found:
                    labels.append(abbr)
                    sizes.append(int(minutes))

        plt.pie(sizes, labels=labels, startangle=90)
        plt.legend(labels, loc='best')
        plt.show()

    def view(self, abbr):
        """View an event by abbreviation"""
        if self._find(abbr):
            _, line = self._find(abbr)
            name, abbrev, duration, percent = line[:-1].split(',')
            percent = str(round(float(percent), 2))
            colors = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan']
            random.shuffle(colors)
            cprint('Event: {0} ({1})\nDuration: {2}\nPercent: {3}%'.format(
                name, abbrev, duration, percent
            ), colors[0], attrs=['bold'])
        else:
            cprint('Event not found!', 'red', 'on_white')

    def list(self):
        """List all events"""
        with open('events.csv', 'r') as f:
            for no, line in enumerate(f):
                if no == 0:
                    continue
                name, abbrev, _, _ = line[:-1].split(',')
                cprint('{0} ({1})'.format(name, abbrev), attrs=['bold'])

    def about(self):
        """Print useful package information"""
        cprint(self.metadata['copyright'], attrs=['bold', 'underline'])
        cprint('Version: ' + self.metadata['version'], attrs=['bold'])
        print('---')
        cprint('Principal author: ' + self.metadata['author'], attrs=['bold'])
        print('This software is distributed under the ' + \
              self.metadata['license'])
        print('---')
        print('Credits to: ')
        print(', '.join( self.metadata['credits'] ))

def go():
    fire.Fire(Shell)
