__author__ = 'Tirth Patel <complaints@tirthpatel.com>'

from requests import get
from re import findall
from time import sleep

delimiter = ' '


class Clue:
    def __init__(self, number, coords, orientation, clue, length, answer=None):
        self.number = number
        self.orientation = orientation
        self.row, self.col = coords[0], coords[1]
        self.clue = clue + ' ({0})'.format(str(length))
        self.answers = [answer] if answer else None
        self.length = length

    def __repr__(self):
        return '{0} {1} {2} - {3} ({4}): {5}' \
            .format(str(self.number), self.orientation, (self.row, self.col),
                    self.clue, str(self.length), self.answers)


class Crossword:
    def __init__(self, size=13):
        self.size = size
        self.puzzle = [[delimiter for _ in range(size)] for _ in range(size)]
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
            'Herb used in cooking - a Mr Major (anag) (8)': [(4, 'marjoram'),
                                                             (3, 'rosemary'),
                                                             (3, 'snapbean'),
                                                             (2, 'beefcake')],
            'Colour between red and green? (5)': [(5, 'amber'), (2, 'green'),
                                                  (2, 'omani')],
            'Sharp tug (4)': [(5, 'jerk'), (4, 'yank'), (1, 'boat')],
            'European country (7)': [(5, 'ukraine'), (5, 'albania'),
                                     (5, 'finland'), (4, 'austria'),
                                     (4, 'andorra'), (2, 'germany'),
                                     (2, 'denmark'), (2, 'turkish'),
                                     (2, 'estonia'), (2, 'romania'),
                                     (2, 'georgia'), (2, 'croatia')],
            'Amphibian (lodged in the throat?) (4)': [(5, 'frog'), (3, 'rasp'),
                                                      (2, 'ahem'),
                                                      (1, 'fell')],
            'Ballroom dance in triple time (5)': [(5, 'waltz'), (3, 'samba'),
                                                  (3, 'valse'), (3, 'rumba'),
                                                  (2, 'bossa'), (2, 'polka')],
            'Cocktail crustacean? (5)': [(5, 'prawn'), (1, 'palps'),
                                         (1, 'eliot'),
                                         (1, 'crust'), (1, 'cosmo')],
            'Sandglass that runs for three (or four?) minutes (8)': [
                (4, 'eggtimer'), (2, 'csimiami'), (2, 'goeslong')],
            'Fishing harbour in northeast Scotland (4)': [(5, 'wick'),
                                                          (2, 'said'),
                                                          (2, 'tema'),
                                                          (2, 'hull'),
                                                          (1, 'suez'),
                                                          (1, 'iasi')],
            'Transmission in a motor vehicle (7)': [(5, 'gearbox'),
                                                    (2, 'renault'),
                                                    (2, 'peugeot')],
            'Loire or California grape - NBC Channel I (anag) (11)': [
                (4, 'cheninblanc')],
            'Regardless (11)': [(4, 'approbative'), (4, 'deferential'),
                                (4, 'appreciated'), (4, 'influential'),
                                (4, 'categorized'), (4, 'opinionated'),
                                (4, 'comewhatmay'), (4, 'appreciable'),
                                (4, 'prestigious'), (4, 'applaudable'),
                                (4, 'insensitive'), (4, 'thoughtless'),
                                (4, 'approbatory'), (4, 'calculating'),
                                (4, 'awestricken'), (4, 'inadvertent'),
                                (4, 'indifferent'), (4, 'inattentive'),
                                (4, 'overlooking'), (4, 'interesting'),
                                (4, 'affectional'), (4, 'consecrated'),
                                (4, 'unconcerned'), (4, 'nonetheless'),
                                (4, 'considerate')],
            'Beef, venison or lamb, for example (7)': [(4, 'redmeat'),
                                                       (2, 'navarin'),
                                                       (2, 'persian'),
                                                       (1, 'marsala'),
                                                       (1, 'gamiest'),
                                                       (1, 'reddeer')],
            'Hard, black wood (5)': [(5, 'ebony'), (2, 'emery'), (1, 'hoeft'),
                                     (1, 'maori')],
            'Something sensational, daring or erotic (8)': [(4, 'hotstuff'),
                                                            (1, 'ferocity')],
            'Massage to relieve tension by finger pressure (11)': [
                (5, 'reflexology'), (2, 'rockthebaby'), (2, 'breaktheice')],
            'Olympic field event in which Greg Rutherford won gold in 2012 ('
            '8)': [
                (4, 'longjump'), (3, 'roadtrip'), (2, 'sarajevo'),
                (2, 'grenoble')],
            'Brusque (7)': [(5, 'offhand'), (4, 'laconic'), (4, 'rushing'),
                            (4, 'raucous')],
            'Contest with the outcome in doubt right to the end (11)': [
                (5, 'cliffhanger'), (3, 'bloodvessel'), (1, 'goldenbrown')],
            'Seethe (4)': [(5, 'fume'), (4, 'foam'), (4, 'soak'), (4, 'heat'),
                           (4, 'boil'), (4, 'warm'), (4, 'buzz'), (4, 'rage'),
                           (4, 'fizz'), (4, 'fill'), (4, 'flip'), (4, 'stew'),
                           (4, 'cook'), (4, 'burn'), (4, 'brew'), (4, 'hiss')]}

        self.clues = []
        across_keys = sorted(self.across.keys())
        down_keys = sorted(self.down.keys())

        a_at, d_at = 0, 0
        for i in range((max(len(self.across), len(self.down)))):
            if a_at < len(self.across):
                self.clues.append(self.across[across_keys[a_at]])
                a_at += 1

            if d_at < len(self.down):
                self.clues.append(self.down[down_keys[d_at]])
                d_at += 1

        self.fill_answers()

    def fill_answers(self):
        counter = 0
        for clue in self.clues:
            counter += 1
            # print(str(counter * 100 // len(self.clues)) + '%')

            # clue.answers = get_answers(clue)
            clue.answers = self.test_ans[clue.clue]

            if len(clue.answers) == 0:
                print(clue, 'no answers found :(')
                continue

            collision = False

            for answer in clue.answers:

                current_word = ''
                for i in range(clue.length):
                    current_word += (self.puzzle[clue.row][clue.col + i]
                                     if clue.orientation == 'across'
                                     else self.puzzle[clue.row + i][clue.col])

                    if current_word[i] != delimiter and answer[1][i] != current_word[i]:
                        collision = True
                        break

                if collision:
                    if clue.answers.index(answer) == len(clue.answers) - 1:
                        print('bummer', clue)
                    collision = False
                    continue

                for i in range(clue.length):
                    if clue.orientation == 'across':
                        self.puzzle[clue.row][clue.col + i] = answer[1][i]
                    elif clue.orientation == 'down':
                        self.puzzle[clue.row + i][clue.col] = answer[1][i]
                break

    def __str__(self):
        s = ''
        for i in range(self.size):
            for j in range(self.size):
                s += str(self.puzzle[i][j]) + '  '
            s += '\n'  # + '-' * self.size * 2 + '\n'

        return s


def get_answers(clue_in):
    if clue_in.answers is None:
        url = 'http://www.wordplays.com/crossword-solver/'

        # encode URL
        for c in clue_in.clue:
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
        for clue in scraped:
            stars = len(findall(r'<div></div>', clue))
            answer = findall(r'crossword-clues/(.*?)"', clue)[
                0].strip().lower()
            if len(answer) == clue_in.length:
                answers.append((stars, answer))

        return answers
    else:
        return clue_in.answers


if __name__ == '__main__':
    crossword = Crossword()
    print(crossword)

    for thing in crossword.clues:
        print(thing)
