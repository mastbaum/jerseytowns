'''A program that generates random New Jersey town names.'''

import sys
import random
import itertools
import urllib2
import json

words = ['spring', 'lake', 'river', 'brook', 'ridge', 'wood', 'hill',
    'saddle', 'glen', 'ROCK', 'branch', 'valley']

words_that_only_go_first = ['north', 'south', 'east', 'west', 'upper', 'lower',
    'green', 'hills']

words_that_only_go_second = ['heights', 'beach', 'city', 'hook', 'field',
    'dale']

class BadCityException(Exception):
    pass


class NotInJerseyException(BadCityException):
    pass


def get_weather(name):
    '''gets current weather using google's undocumented weather api'''
    import settings
    weather_url = 'http://api.wunderground.com/api/%s/conditions/q/NJ/%s.json'
    name = name.replace(' ', '_')

    p = urllib2.urlopen(weather_url % (settings.api_key, name))
    d = json.load(p)

    if 'current_observation' not in d:
        raise BadCityException(name)

    state = d['current_observation']['display_location']['state']
    if state != 'NJ':
        raise NotInJerseyException(state)

    temp = d['current_observation']['temp_f']
    weather = d['current_observation']['weather']

    return temp, weather


def make_name():
    '''Creates a random city name.

    If it is a real city, the weather is also returned.

    :returns: (name, weather) tuple
    '''
    word1 = random.choice(words + words_that_only_go_first)
    word2 = random.choice(words)

    while word1 == word2:
        word2 = random.choice(words)

    name = '%s %s' % (word1.title(), word2.title())

    weather = None

    try:
        weather = get_weather(name)
    except BadCityException:
        try:
            s = '%s%s' % (word1.title(), word2.lower())
            weather = get_weather(s)
        except BadCityException:
            pass
    
    return name, weather


def list_all():
    '''Generates a list of all possible New Jersey town names.

    :returns: list of names
    '''
    titlefy = lambda x: x.title()

    pretty_words = map(titlefy, words)
    pretty_firsts = map(titlefy, words_that_only_go_first)
    pretty_seconds = map(titlefy, words_that_only_go_second)

    perms = list(itertools.permutations(pretty_words, 2))
    firsts = list(itertools.product(pretty_firsts, pretty_words))
    seconds = list(itertools.product(pretty_words, pretty_seconds))

    all_cities = perms + firsts + seconds

    return map(lambda x: '%s %s' % (x[0], x[1]), all_cities)


def check_real(cities):
    '''Check if cities really exist, and if they do, get the weather!

    :param cities: List of city names
    :returns: {name: weather} dict
    '''
    real_cities = {}

    for city in cities:
        try:
            weather = get_weather(name)
            real_cities[city] = weather
        except BadCityException:
            try:
                s = '%s%s' % (word1.title(), word2.lower())
                weather = get_weather(s)
                real_cities[city] = weather
            except BadCityException:
                pass

    return real_cities


if __name__ == '__main__':
    if len(sys.argv) < 2:
        count = 1
    else:
        count = int(sys.argv[1])

    for i in range(count):
        print make_name()

