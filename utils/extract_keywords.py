import jieba
import jieba.analyse

def extract_keywords_CH(logger, text, topk, idf_path = "data/default_IDF.txt"):
    tfidf = jieba.analyse.extract_tags
    jieba.analyse.set_idf_path(idf_path)
    keywords_jieba = tfidf(text, topK=topk, withWeight=True)
    
    keywords = {"keywords" : []}
    for keyword, weight in keywords_jieba:
        keywords["keywords"].append(keyword)
    keywords_str = '、'.join(keywords["keywords"])

    logger.info(f"Keywords:{keywords_str}")
    return keywords
