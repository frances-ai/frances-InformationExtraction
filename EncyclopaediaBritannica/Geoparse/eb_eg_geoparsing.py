from defoe.query_utils import get_geoparser_xml, geoparser_xml_tojson
from defoe import get_root_path, get_geo_supported_os_type
from tqdm import tqdm
import pandas as pd

defoe_path = get_root_path() + "/"
os_type = get_geo_supported_os_type()
gazetteer = "geonames-local"
bounding_box = ""

def geoparse(article):
    # add name back to the text
    article_name = article["name"].capitalize()
    text_with_article_name = article_name + ", " + article["hq_text"]

    # geoparsering
    test_geo_xml = get_geoparser_xml(text_with_article_name, defoe_path, os_type, gazetteer, bounding_box)
    locations = geoparser_xml_tojson(test_geo_xml, text_with_article_name)

    # check if this article is a location
    article_location = None
    if len(locations) > 0 and locations[0]['name'] == article_name:
        article_location = locations[0]
        locations.pop(0)

    # forward all the indices by the length of <article_name, >
    forward_len = len(article_name + ", ")
    for location in locations:
        location["start"] -= forward_len
        location["end"] -= forward_len

    return article_location, locations


if __name__ == "__main__":
    # load samples
    print("Loading eb geo samples....")
    eb_geo_samples_df = pd.read_json('eb_geo_samples.json', orient='records', lines=True)
    print(f"{len(eb_geo_samples_df)} samples loaded")

    # geoparse all samples
    sample_articles = eb_geo_samples_df.to_dict(orient='records')
    print("Geoparsing articles....")
    for index, article in enumerate(tqdm(sample_articles)):
        article_location, locations = geoparse(article)
        article["locations"] = locations
        #print(locations)
        if article_location:
            article["is_location"] = True
            article["latitude"] = article_location["latitude"]
            article["longitude"] = article_location["longitude"]
            article["gazetteer_ref"] = article_location["gazetteer_ref"]
            article["population"] = article_location["population"]
            article["in_country"] = article_location["in_country"]
            article["feature_type"] = article_location["feature_type"]
        else:
            article["is_location"] = False
            article["latitude"] = ""
            article["longitude"] = ""
            article["gazetteer_ref"] = ""
            article["population"] = ""
            article["in_country"] = ""
            article["feature_type"] = ""

    # store articles
    print("Saving geoparsed articles....")
    articles_df = pd.DataFrame(sample_articles)
    result_path = "articles_with_locations_eg_df.json"
    articles_df.to_json(result_path, orient='records', lines=True)
    print(f"result saved to {result_path}")


