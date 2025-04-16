import jieba
import jieba.analyse

def extract_keywords(text, topk, idf_path = "data/default_IDF.txt"):
    tfidf = jieba.analyse.extract_tags
    jieba.analyse.set_idf_path(idf_path)
    keywords_jieba = tfidf(text, topK=topk, withWeight=True)
    
    keywords = []
    for keyword, weight in keywords_jieba:
        keywords.append(keyword)

    return keywords
