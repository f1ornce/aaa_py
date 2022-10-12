class CountVectorizer:
    def __init__(self, lowercase=True, vocabulary=None):
        self.lowercase = lowercase
        self.vocabulary = vocabulary

    def text_to_sequence(self, texts):
        sent_list = texts
        vocabulary = []
        sent_length = []
        for sent in range(len(sent_list)):
            words = sent_list[sent].split(' ')
            if self.lowercase:
                words = [x.lower() for x in words]
            sent_length.append(len(words))
            for i in range(sent_length[sent]):
                if words[i] not in vocabulary:
                    vocabulary.append(words[i])
        self.vocabulary = vocabulary
        return vocabulary

    def fit_transform(self, texts):
        if self.vocabulary is None:
            tokens = self.text_to_sequence(texts)
        else:
            tokens = self.vocabulary
        matrix = []
        count_dict = {i: 0 for i in tokens}
        for sent in range(len(texts)):
            words = texts[sent].split(' ')
            if self.lowercase:
                words = [x.lower() for x in words]
            temp_dict = dict(count_dict)
            for i in range(len(words)):
                temp_dict[words[i]] += 1
            matrix.append(list(temp_dict.values()))
        return matrix

    def get_feature_names(self):
        if self.vocabulary is not None:
            return self.vocabulary
        else:
            raise AttributeError('vocabulary is empty - fit the vectorizer first')
