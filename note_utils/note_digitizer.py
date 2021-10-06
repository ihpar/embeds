class NoteDigitizer:
    def __init__(self):
        self.__alphabet = ['do', 're', 'mi', 'fa', 'sol', 'la', 'si']
        self.__flat_alphabet = ['re', 'mi', 'fa', 'sol', 'la', 'si', 'do']
        self.__intervals = [9, 9, 4, 9, 9, 9, 4]
        self.__comma_alp = [
            ['', 'b9'],
            ['#1', 'b8'],
            ['#2', 'b7'],
            ['#3', 'b6'],
            ['#4', 'b5'],
            ['#5', 'b4'],
            ['#6', 'b3'],
            ['#7', 'b2'],
            ['#8', 'b1'],
            ['#9', '']
        ]
        self.__sharp_comma_alp = self.__comma_alp[1:]
        self.__flat_comma_alp = self.__comma_alp[:-1]
        self.__sharp_dictionary = {}
        self.__flat_dictionary = {}
        self.__natural_dictionary = {}

        self.__r_sharp_dictionary = {}
        self.__r_flat_dictionary = {}
        self.__r_natural_dictionary = {}

        self.__build_self()

    def __build_self(self):
        idx = 2
        idy = 1
        idn = 1
        self.__sharp_dictionary[0] = self.Note('rest', '', '')
        self.__sharp_dictionary[1] = self.Note('do', 0, '')

        self.__flat_dictionary[0] = self.Note('rest', '', '')
        self.__natural_dictionary[0] = self.Note('rest', '', '')

        for octave_no in range(0, 9):
            # sharps
            for note_no in range(0, len(self.__alphabet)):
                k_idx = 0

                for koma_no in range(0, len(self.__sharp_comma_alp)):
                    if k_idx == self.__intervals[note_no]:
                        break
                    root = self.__alphabet[note_no]
                    self.__sharp_dictionary[idx] = self.Note(
                        root, octave_no, self.__sharp_comma_alp[koma_no][0])
                    idx += 1
                    k_idx += 1

            # flats
            for note_no in range(0, len(self.__flat_alphabet)):
                for koma_no in reversed(range(0, self.__intervals[note_no])):
                    root = self.__alphabet[(note_no + 1) %
                                           len(self.__alphabet)]
                    octave = octave_no
                    if (note_no + 1) == len(self.__alphabet):
                        octave += 1
                    self.__flat_dictionary[idy] = self.Note(
                        root, octave, 'b' + str(koma_no + 1))
                    idy += 1

            # naturals
            for note_no in range(0, len(self.__alphabet)):
                self.__natural_dictionary[idn] = self.Note(
                    self.__alphabet[note_no], octave_no, '')
                idn += self.__intervals[note_no]

        self.__flat_dictionary[idy] = self.Note('re', 9, 'b9')

        # build reverse dicts
        for k, v in self.__sharp_dictionary.items():
            if k in self.__natural_dictionary:
                self.__r_natural_dictionary[self.__natural_dictionary[k].name] = k

            self.__r_sharp_dictionary[v.name] = k
            self.__r_flat_dictionary[self.__flat_dictionary[k].name] = k

    def __str__(self):
        str_rep = []

        for k, v in self.__sharp_dictionary.items():
            if k in self.__natural_dictionary:
                str_rep.append(str(k) + '\t' + v.name + '\t' +
                               self.__flat_dictionary[k].name + '\t' +
                               self.__natural_dictionary[k].name)
            else:
                str_rep.append(str(k) + '\t' + v.name + '\t' +
                               self.__flat_dictionary[k].name)

        return "\n".join(str_rep)

    def get_num_by_name(self, note_name):
        res = [-1, -1, -1, False]
        if note_name in self.__r_flat_dictionary:
            res[0] = self.__r_flat_dictionary[note_name]
            res[3] = True
        if note_name in self.__r_sharp_dictionary:
            res[1] = self.__r_sharp_dictionary[note_name]
            res[3] = True
        if note_name in self.__r_natural_dictionary:
            res[2] = self.__r_natural_dictionary[note_name]
            res[3] = True

        return res

    def get_note_by_num(self, num):
        res = [False, False, False, False]
        if num in self.__flat_dictionary:
            res[0] = self.__flat_dictionary[num]
            res[3] = True
        if num in self.__sharp_dictionary:
            res[1] = self.__sharp_dictionary[num]
            res[3] = True
        if num in self.__natural_dictionary:
            res[2] = self.__natural_dictionary[num]
            res[3] = True

        return res

    class Note:
        def __init__(self, root, octave, accidental):
            self.root_note = root
            self.octave = octave
            self.accidental = accidental
            self.name = root + str(octave) + accidental
