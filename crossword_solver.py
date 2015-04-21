__author__ = 'Tirth Patel <complaints@tirthpatel.com>'

from requests import get
from re import findall
from time import sleep


class Clue:
    def __init__(self, number, coords, orientation, clue, length, answer=None):
        self.number = number
        self.orientation = orientation
        self.row, self.col = coords[0], coords[1]
        self.clue = clue
        self.answers = [answer] if answer else None
        self.length = length

    def __repr__(self):
        return '{0} {1} {2} - {3} ({4}): {5}' \
            .format(str(self.number), self.orientation, (self.row, self.col),
                    self.clue, str(self.length), self.answers)


class Crossword:
    def __init__(self, size=13):
        self.size = size
        self.puzzle = [['*' for _ in range(size)] for _ in range(size)]
        self.across, self.down = {}, {}

        # sample, Guardian #14,022
        self.across[5] = Clue(5, (1, 1), 'across',
                              'Contest with the outcome in doubt '
                              'right to the end', 11)

        self.across[7] = Clue(7, (3, 0), 'across', 'Sharp tug', 4)

        self.across[8] = Clue(8, (3, 5), 'across',
                              'Something sensational, daring or erotic', 8)

        self.across[9] = Clue(9, (5, 0), 'across', 'European country', 7)

        self.across[11] = Clue(11, (5, 8), 'across',
                               'Colour between red and green?', 5)

        self.across[13] = Clue(13, (7, 0), 'across', 'Hard, black wood', 5)

        self.across[14] = Clue(14, (7, 6), 'across',
                               'Transmission in a motor vehicle', 7)

        self.across[16] = Clue(16, (9, 0), 'across',
                               'Herb used in cooking - a Mr Major (anag)', 8)

        self.across[17] = Clue(17, (9, 9), 'across',
                               'Amphibian (lodged in the throat?)', 4)

        self.across[18] = Clue(18, (11, 1), 'across', 'Regardless', 11)

        self.down[1] = Clue(1, (0, 3), 'down',
                            'Fishing harbour in northeast Scotland', 4)

        self.down[2] = Clue(2, (0, 5), 'down', 'Brusque', 7)

        self.down[3] = Clue(3, (0, 7), 'down', 'Ballroom dance in triple time',
                            5)

        self.down[4] = Clue(4, (0, 9), 'down', 'Sandglass that runs for '
                                               'three (or four?) minutes', 8)

        self.down[5] = Clue(5, (1, 1), 'down', 'Loire or California grape - '
                                               'NBC Channel I (anag)', 11)

        self.down[6] = Clue(6, (1, 11), 'down',
                            'Massage to relieve tension by '
                            'finger pressure', 11)

        self.down[10] = Clue(10, (5, 3), 'down',
                             'Olympic field event in which '
                             'Greg Rutherford won gold in '
                             '2012', 8)

        self.down[12] = Clue(12, (6, 7), 'down',
                             'Beef, venison or lamb, for example', 7)

        self.down[15] = Clue(15, (8, 5), 'down', 'Cocktail crustacean?', 5)

        self.down[17] = Clue(17, (9, 9), 'down', 'Seethe', 4)

        self.test_ans = {
            'Colour between red and green?': [(4, 'amber'), (2, 'green'),
                                              (2, 'omani')],
            'Beef, venison or lamb, for example': [(4, 'redmeat'),
                                                   (2, 'navarin'),
                                                   (2, 'persian'),
                                                   (1, 'marsala'),
                                                   (1, 'gamiest'),
                                                   (1, 'reddeer')],
            'Sharp tug': [(5, 'yank'), (2, 'jerk'), (1, 'boat'), (1, 'atwo'),
                          (1, 'noon'), (1, 'edge')],
            'Contest with the outcome in doubt right to the end': [
                (4, 'cliffhanger'), (3, 'bloodvessel')],
            'Herb used in cooking - a Mr Major (anag)': [(4, 'marjoram'),
                                                         (3, 'rosemary'),
                                                         (3, 'snapbean'),
                                                         (2, 'beefcake')],
            'Sandglass that runs for three (or four?) minutes': [
                (4, 'eggtimer'),
                (2, 'csimiami'),
                (2, 'goeslong')],
            'European country': [(5, 'austria'), (5, 'andorra'),
                                 (2, 'finland'),
                                 (2, 'albania'), (2, 'ukraine'),
                                 (2, 'germany'),
                                 (2, 'denmark'), (2, 'turkish'),
                                 (2, 'estonia')],
            'Brusque': [(5, 'rushing'), (5, 'raucous'), (5, 'laconic'),
                        (5, 'offhand')],
            'Transmission in a motor vehicle': [(4, 'gearbox'), (2, 'renault'),
                                                (2, 'peugeot')],
            'Ballroom dance in triple time': [(4, 'waltz'), (3, 'samba'),
                                              (3, 'valse'), (3, 'rumba'),
                                              (2, 'bossa'), (2, 'polka')],
            'Cocktail crustacean?': [(2, 'prawn'), (1, 'palps'), (1, 'eliot')],
            'Something sensational, daring or erotic': [(4, 'hotstuff'),
                                                        (1, 'ferocity')],
            'Hard, black wood': [(3, 'ebony'), (2, 'emery'), (1, 'hoeft'),
                                 (1, 'maori')],
            'Regardless': [(5, 'inadvertent'), (5, 'influential'),
                           (5, 'indifferent'), (5, 'awestricken'),
                           (5, 'inattentive'), (5, 'categorized'),
                           (5, 'overlooking'), (5, 'interesting'),
                           (5, 'opinionated'), (5, 'affectional'),
                           (5, 'comewhatmay'), (5, 'appreciable'),
                           (5, 'prestigious'), (5, 'consecrated'),
                           (5, 'unconcerned'), (5, 'nonetheless'),
                           (5, 'applaudable'), (5, 'considerate'),
                           (5, 'approbative'), (5, 'insensitive'),
                           (5, 'deferential'), (5, 'thoughtless'),
                           (5, 'appreciated')],
            'Massage to relieve tension by finger pressure': [
                (4, 'reflexology'),
                (2, 'rockthebaby'),
                (2, 'breaktheice')],
            'Amphibian (lodged in the throat?)': [(4, 'frog'), (3, 'rasp'),
                                                  (2, 'ahem'), (1, 'fell')],
            'Seethe': [(5, 'fill'), (5, 'flip'), (5, 'stew'), (5, 'boil'),
                       (5, 'warm'), (5, 'cook'), (5, 'buzz'), (5, 'rage'),
                       (5, 'burn'), (5, 'fume'), (5, 'brew'), (5, 'fizz'),
                       (5, 'hiss'), (5, 'foam'), (5, 'soak'), (5, 'heat')],
            'Olympic field event in which Greg Rutherford won gold in 2012': [
                (4, 'longjump'), (3, 'roadtrip'), (2, 'sarajevo')],
            'Fishing harbour in northeast Scotland': [(4, 'wick'), (2, 'said'),
                                                      (2, 'tema'), (2, 'hull'),
                                                      (1, 'suez'),
                                                      (1, 'iasi')],
            'Loire or California grape - NBC Channel I (anag)': [
                (4, 'cheninblanc')]}

        self.clues = ([clue for clue in self.across.values()] +
                      [clue for clue in self.down.values()])

        self.fill_answers()

    def fill_answers(self):
        for clue in self.clues:
            # clue.answers = get_answers(clue)
            clue.answers = self.test_ans[clue.clue]

            if len(clue.answers) == 0:
                print(clue, 'no answers found :(')
                continue

            for answer in clue.answers:
                for i in range(clue.length):

                    if clue.orientation == 'across':
                        curr = self.puzzle[clue.row][clue.col + i]
                        if curr == '*':
                            self.puzzle[clue.row][clue.col + i] = answer[1][i]
                            # elif curr != answer[i]:
                            #     print('mismatch!', answer)
                            #     break

                    elif clue.orientation == 'down':
                        curr = self.puzzle[clue.row + i][clue.col]
                        if curr == '*':
                            self.puzzle[clue.row + i][clue.col] = answer[1][i]
                            # elif curr != answer[i]:
                            #     print('mismatch!', answer)
                            #     break

    def __str__(self):
        s = ''
        for i in range(self.size):
            for j in range(self.size):
                s += str(self.puzzle[i][j])
            s += '\n'

        return s


def get_answers(clue_in):
    clue = clue_in.clue
    url = 'http://www.wordplays.com/crossword-solver/'

    # encode URL
    for c in clue:
        if c == ' ':
            url += '-'
        elif c == ',':
            url += '%2C'
        elif c == ':':
            url += '%3A'
        elif c == '?':
            url += '%3F'
        elif c == '\'':
            url += '%27'
        elif c == '(':
            url += '%28'
        elif c == ')':
            url += '%29'
        else:
            url += c

    sleep(4)
    r = get(url)

    if r.status_code != 200:
        print('Nope', url)

    # get ranks and answers
    scraped = findall(r'class=stars>(.*?)<td class=clue', r.text)

    # clean up and put into list
    answers = []
    for a in scraped:
        stars = len(findall(r'<div></div>', a))
        answer = findall(r'crossword-clues/(.*?)"', a)[0].strip().lower()
        if len(answer) == clue_in.length:
            answers.append((stars, answer))

    return answers


if __name__ == '__main__':
    crossword = Crossword()
    print(crossword)

    for thing in crossword.clues:
        print(thing)
