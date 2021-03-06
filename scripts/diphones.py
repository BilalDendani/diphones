import sys

vocabulary = dict()

for dictionary_filename in ['data/librispeech-lexicon.txt', 'data/TEDLIUM.152k.dic']:
    with open(dictionary_filename) as dictionary_file:
        for string in dictionary_file:
            if string[0] != '#':
                if '\t' in string:
                    [word, transcription] = string.strip().split('\t')
                else:
                    parts = [x for x in string.strip().split(' ') if x != '']

                    if len(parts) == 2:
                        parts.append(parts[1])

                    [word, transcription] = [parts[0], ' '.join(parts[1:])]

                word = word.upper()

                if word in vocabulary:
                    next

                transcription = transcription \
                    .replace('AW', 'AA UH') \
                    .replace('AY', 'AA IY') \
                    .replace('ER', 'UH R') \
                    .replace('EY', 'EH IY') \
                    .replace('OW', 'AO UH') \
                    .replace('OY', 'AO IY')
                vocabulary[word] = transcription

vocabulary['_SIL_'] = 'SIL'

words_filename = sys.argv[1]

with open(words_filename) as words_file, open(words_filename[:-4] + '_diphones.txt', 'w') as words_diphones_file:
    for string in words_file:
        [count, phrase] = string.strip().split(':')

        found = True
        transcription = list()

        for word in phrase.split(' '):
            if word in vocabulary:
                for phone in vocabulary[word].split(' '):
                    transcription.append(phone.rstrip('0123456789'))
            else:
                print('Missing lexicon entry: ' + word)
                found = False

        if found:
            words_diphones_file.write(count + '\t' + phrase + '\t' + ' '.join(['_'.join(x) for x in zip(transcription, transcription[1:])]) + '\n')

