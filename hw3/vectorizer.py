class CountVectorizer:
    """creates vectorized form of a text """
    def __init__(self, lowercase=True, vocabulary=None):
        self.lowercase = lowercase
        self.vocabulary = vocabulary

    def text_to_sequence(self, texts):
        """splits given texts into unique tokens=words and writes it
            in vocabulary"""
        vocabulary = []
        sent_length = []
        for sent in range(len(texts)):
            words = texts[sent].split(' ')
            if self.lowercase:
                words = [x.lower() for x in words]
            sent_length.append(len(words))
            for i in range(sent_length[sent]):
                if words[i] not in vocabulary:
                    vocabulary.append(words[i])
        self.vocabulary = vocabulary
        return vocabulary

    def fit_transform(self, texts):
        """learns the vocabulary, forms and returns
            term-document matrix of texts based
            on words from vocabulary"""
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
        """prints out vocabulary if it's not empty"""
        if self.vocabulary is not None:
            return self.vocabulary
        else:
            raise AttributeError('vocabulary is empty - fit the vectorizer first')
