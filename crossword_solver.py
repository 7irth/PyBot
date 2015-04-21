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
        self.answers = answer
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
            'Amphibian (lodged in the throat?)': ['frog', 'rasp', 'ahem',
                                                  'laid'],
            'Olympic field event in which Greg Rutherford won gold in 2012': [
                'longjump', 'roadtrip', 'sarajevo'],
            'Ballroom dance in triple time': ['waltz', 'samba', 'valse',
                                              'rumba',
                                              'bossa', 'polka'],
            'Loire or California grape - NBC Channel I (anag)': [
                'cheninblanc'],
            'Brusque': ['rushing', 'raucous', 'laconic', 'offhand'],
            'Transmission in a motor vehicle': ['gearbox', 'renault',
                                                'peugeot'],
            'Sandglass that runs for three (or four?) minutes': ['eggtimer',
                                                                 'csimiami',
                                                                 'goeslong'],
            'Contest with the outcome in doubt right to the end': [
                'cliffhanger',
                'bloodvessel'],
            'Massage to relieve tension by finger pressure': ['reflexology',
                                                              'rockthebaby',
                                                              'breaktheice'],
            'Regardless': ['overlooking', 'interesting', 'opinionated',
                           'affectional', 'comewhatmay', 'appreciable',
                           'prestigious', 'consecrated', 'unconcerned',
                           'nonetheless', 'applaudable', 'considerate',
                           'approbative', 'insensitive', 'deferential',
                           'thoughtless', 'appreciated', 'approbatory',
                           'calculating', 'inadvertent', 'influential',
                           'indifferent'],
            'Cocktail crustacean?': ['prawn', 'palps', 'eliot'],
            'Beef, venison or lamb, for example': ['redmeat', 'navarin',
                                                   'persian',
                                                   'marsala', 'gamiest',
                                                   'reddeer'],
            'Colour between red and green?': ['amber', 'green', 'omani'],
            'Sharp tug': ['yank', 'jerk', 'boat', 'atwo', 'noon', 'edge'],
            'Seethe': ['boil', 'warm', 'cook', 'buzz', 'rage', 'burn', 'fume',
                       'brew', 'fizz', 'hiss', 'foam', 'soak', 'heat', 'fill',
                       'flip', 'stew'],
            'European country': ['andorra', 'austria', 'finland', 'albania',
                                 'ukraine', 'germany', 'denmark', 'turkish',
                                 'estonia'],
            'Something sensational, daring or erotic': ['hotstuff',
                                                        'ferocity'],
            'Herb used in cooking - a Mr Major (anag)': ['marjoram',
                                                         'rosemary',
                                                         'snapbean',
                                                         'beefcake'],
            'Hard, black wood': ['ebony', 'emery', 'hoeft', 'maori'],
            'Fishing harbour in northeast Scotland': ['wick', 'said', 'tema',
                                                      'hull', 'suez', 'iasi']}

        self.clues = ([clue for clue in self.across.values()] +
                      [clue for clue in self.down.values()])

        self.fill_answers()

    def fill_answers(self):
        for clue in self.clues:
            clue.answers = get_answers(clue)
            # clue.answers = self.test_ans[clue.clue]

            if len(clue.answers) == 0:
                print(clue, 'no answers found :(')
                continue

            for answer in clue.answers:
                for i in range(clue.length):

                    if clue.orientation == 'across':
                        curr = self.puzzle[clue.row][clue.col + i]
                        if curr == '*':
                            self.puzzle[clue.row][clue.col + i] = answer[i]
                            # elif curr != answer[i]:
                            #     print('mismatch!', answer)
                            #     break

                    elif clue.orientation == 'down':
                        curr = self.puzzle[clue.row + i][clue.col]
                        if curr == '*':
                            self.puzzle[clue.row + i][clue.col] = answer[i]
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
    # answers = re.findall(r'class=stars>(.*?)<td class=clue', r.text)

    # just the possible answers
    answers = []
    for c in findall(r'crossword-clues/(.*?)"', r.text):
        if len(c.strip()) == clue_in.length:
            answers.append(c.strip().lower())

    return answers


if __name__ == '__main__':
    crossword = Crossword()
    print(crossword)

    for thing in crossword.clues:
        print(thing)
