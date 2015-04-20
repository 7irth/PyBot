__author__ = 'Tirth Patel <complaints@tirthpatel.com>'


class Clue:
    def __init__(self, number, coords, orientation, clue, length, answer=''):
        self.number = number
        self.orientation = orientation
        self.coords = coords
        self.clue = clue
        self.answer = answer
        self.length = length

    def __repr__(self):
        return '{0} {1} {2} - {3} ({4}): {5}' \
            .format(str(self.number), self.orientation, str(self.coords),
                    self.clue, str(self.length), self.answer)


class Crossword:
    def __init__(self):
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
                               'Amphibian (lodged in the throat?)', 4, 'frog')

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


if __name__ == '__main__':
    crossword = Crossword()
    for thing in crossword.across:
        print(crossword.across[thing])