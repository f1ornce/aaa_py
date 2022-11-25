import math


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
            '''if self.lowercase:
                words = [x.lower() for x in words]'''
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
        '''if self.vocabulary is None:
            tokens = self.text_to_sequence(texts)
        else:
            tokens = self.vocabulary'''
        tokens = self.text_to_sequence(texts)
        matrix = []
        count_dict = {i: 0 for i in tokens}
        for sent in range(len(texts)):
            words = texts[sent].split(' ')
            '''if self.lowercase:
                    words = [x.lower() for x in words]'''
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
            raise AttributeError('vocabulary is empty '
                                 '- fit the vectorizer first')


class TfidfTransformer:
    def __init__(self):
        self.idf = None

    def tf_transform(self, matrix: list) -> list:
        ans = []
        for elem in matrix:
            temp = []
            m_sum = sum(elem)
            for x in elem:
                temp.append(x / m_sum)
            ans.append(temp)
        return ans

    def idf_transform(self, count_matrix):
        total = len(count_matrix) + 1
        transposed_m = list(map(list, zip(*count_matrix)))
        result = [1 + round(math.log(total / (sum(map(bool, document)) + 1)),
                            1) for document in transposed_m]
        return result

    def fit(self, count_matrix):
        self.idf = self.idf_transform(count_matrix)

    def transform(self, count_matrix):
        out_size = len(count_matrix)
        in_size = len(count_matrix[0])
        idf = self.idf
        tf = self.tf_transform(count_matrix)
        tf_idf_matrix = [[0] * in_size for _ in range(out_size)]
        for i in range(out_size):
            for j in range(in_size):
                tf_idf_matrix[i][j] = round(idf[j] * tf[i][j], 3)
        return tf_idf_matrix

    def fit_transform(self, count_matrix):
        self.fit(count_matrix)
        return self.transform(count_matrix)


class TfidfVectorizer(CountVectorizer):
    def __init__(self):
        super().__init__(self)
        self._transformer = TfidfTransformer()

    def fit_transform(self, texts):
        matrix = super().fit_transform(texts)
        return self._transformer.fit_transform(matrix)


if __name__ == '__main__':
    corpus = [
        'Crock Pot Pasta Never boil pasta again',
        'Pasta Pomodoro Fresh ingredients Parmesan to taste'
    ]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    print(vectorizer.get_feature_names())
    print(tfidf_matrix)
