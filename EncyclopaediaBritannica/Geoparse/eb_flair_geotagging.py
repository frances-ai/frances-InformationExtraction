from tqdm.auto import tqdm
import pandas as pd
from flair.data import Sentence
from flair.models import SequenceTagger

# load tagger
tagger = SequenceTagger.load("flair/ner-english-ontonotes-large")


def geo_tagging(text):
    doc = Sentence(text)
    tagger.predict(doc)
    tagged_tokens = []
    for ent in doc.get_spans('ner'):
        label = ent.labels[0].value
        #print(ent.text, ent.type)
        if label == "LOC" or label == "GPE" or label == "FAC":
            toponym = ent.text
            start_index = ent.start_position
            end_index = ent.end_position
            tagged_tokens.append({
                "start": start_index,
                "end": end_index,
                "name": toponym,
            })

    return tagged_tokens


if __name__ == "__main__":
    # load samples
    print("Loading eb geo samples....")
    eb_geo_samples_df = pd.read_json('eb_geo_samples.json', orient='records', lines=True)
    print(f"{len(eb_geo_samples_df)} samples loaded")

    # geoparse all samples
    sample_articles = eb_geo_samples_df.to_dict(orient='records')
    print("Geotagging articles....")
    for index, article in enumerate(tqdm(sample_articles)):
        # add name back to the text
        article_name = article["name"].capitalize()
        text_with_article_name = article_name + ", " + article["hq_text"]
        # geotagging
        location_tokens = geo_tagging(text_with_article_name)
        # check if this article is a location
        article_location = None
        if len(location_tokens) > 0 and location_tokens[0]['name'] == article_name:
            article_location = location_tokens[0]
            location_tokens.pop(0)

        # forward all the indices by the length of <article_name, >
        forward_len = len(article_name + ", ")
        for location in location_tokens:
            location["start"] -= forward_len
            location["end"] -= forward_len
        article["locations"] = location_tokens
        #print(locations)
        if article_location:
            article["is_location"] = True
        else:
            article["is_location"] = False

    # store articles
    print("Saving geotagged articles....")
    articles_df = pd.DataFrame(sample_articles)
    result_path = "geotagged_articles_flair_df.json"
    articles_df.to_json(result_path, orient='records', lines=True)
    print(f"result saved to {result_path}")


