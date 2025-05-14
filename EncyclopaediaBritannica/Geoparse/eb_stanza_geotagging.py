import regex
from tqdm import tqdm
import pandas as pd
import string
import stanza
stanza.download('en') # download English model
nlp = stanza.Pipeline('en') # initialize English neural pipeline

def normalize_name(name):
    name = regex.sub(r'[^\p{L}\s\-\'\,\.\’]', '', name)
    name = regex.sub(r'\n', '', name)
    name = string.capwords(name)
    return name

def geo_tagging(text):
    doc = nlp(text)
    tagged_tokens = []
    for ent in doc.ents:
        #print(ent.text, ent.type)
        if ent.type == "LOC" or ent.type == "GPE" or ent.type == "FAC":
            toponym = ent.text
            start_index = ent.start_char
            end_index = ent.end_char
            tagged_tokens.append({
                "start": start_index,
                "end": end_index,
                "name": toponym,
            })

    return tagged_tokens


if __name__ == "__main__":
    # load samples
    print("Loading eb geo samples....")
    eb_geo_samples_df = pd.read_json('eb7th_geo_input.json', orient='records', lines=True)
    print(f"{len(eb_geo_samples_df)} samples loaded")

    # geoparse all samples
    sample_articles = eb_geo_samples_df.to_dict(orient='records')
    print("Geotagging articles....")
    for index, article in enumerate(tqdm(sample_articles)):
        # add name back to the text
        article_name = normalize_name(article["name"])
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

        # remove the all locations with negative index
        negative_locations_count = 0
        for location_token in location_tokens:
            if location_tokens[0]['start'] < 0:
                negative_locations_count += 1
        for _ in range(negative_locations_count):
            location_tokens.pop(0)

        article["locations"] = location_tokens

        #print(locations)
        if article_location:
            article["is_location"] = True
        else:
            article["is_location"] = False

    # store articles
    print("Saving geotagged articles....")
    articles_df = pd.DataFrame(sample_articles)
    result_path = "eb7_geotagged_articles_stanza_df.json"
    articles_df.to_json(result_path, orient='records', lines=True)
    print(f"result saved to {result_path}")


