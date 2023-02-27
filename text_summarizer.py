import spacy
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.probability import FreqDist
from nltk import pos_tag
from math import log
from docx import Document

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

def summarize_text(file_name, max_sentences=1):
    if file_name.endswith('.txt'):
        with open(file_name, 'r', encoding='utf-8') as file:
            text = file.read()
    elif file_name.endswith('.docx'):
        doc = Document(file_name)
        paragraphs = [p.text for p in doc.paragraphs]
        text = '\n'.join(paragraphs)
    else:
        raise ValueError('Unsupported file format')

    # Tokenize text into sentences
    sentences = sent_tokenize(text)

    # Remove stop words and stem remaining words
    stop_words = set(stopwords.words('english'))
    ps = PorterStemmer()
    stemmed_sentences = []
    for sentence in sentences:
        words = word_tokenize(sentence)
        tagged_words = pos_tag(words)
        stemmed_words = [ps.stem(word.lower()) for word, pos in tagged_words
                         if word.lower() not in stop_words and pos.startswith('NN')]
        stemmed_sentences.append(' '.join(stemmed_words))

    # Use NER model to identify important entities
    nlp = spacy.load('en_core_web_sm')
    entity_scores = {}
    for i, sentence in enumerate(sentences):
        doc = nlp(sentence)
        entities = [ent.label_ for ent in doc.ents]
        entity_scores[i] = len(entities)

    # Calculate IDF scores for each word
    all_words = ' '.join(stemmed_sentences)
    num_docs = len(sentences)
    idf_scores = {}
    for word in set(all_words.split()):
        count = sum([1 for sent in stemmed_sentences if word in sent])
        idf_scores[word] = log(num_docs / count)

    # Calculate TF-IDF scores for each sentence, weighted by entity scores
    sentence_scores = {}
    for i, sentence in enumerate(sentences):
        words = word_tokenize(sentence)
        tagged_words = pos_tag(words)
        stemmed_words = [ps.stem(word.lower()) for word, pos in tagged_words
                         if word.lower() not in stop_words and pos.startswith('NN')]
        tf_scores = FreqDist(stemmed_words)
        tfidf_score = sum([tf_scores[word] * idf_scores[word] for word in tf_scores])
        if len(stemmed_words) > 0:
            sentence_scores[i] = (tfidf_score / len(stemmed_words)) * entity_scores[i]

    # Rank sentences by scores
    ranked_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)

    # Generate summary
    summary = ''
    for i in range(min(max_sentences, len(ranked_sentences))):
        summary += sentences[ranked_sentences[i]] + ' '

    return summary
