from defoe.query_utils import georesolve_cmd, georesolved_xml_tojson
from defoe import get_root_path
from tqdm import tqdm
import pandas as pd

defoe_path = get_root_path() + "/"
gazetteer = "geonames-local"
bounding_box = ""


def geo_resolve(geotagged_xml, defoe_path, gazetteer, bounding_box):
    resolved_xml = georesolve_cmd(geotagged_xml, defoe_path, gazetteer, bounding_box)
    geo_list = georesolved_xml_tojson(resolved_xml)
    return geo_list

def geoparse(article):
    article_name = article["name"].capitalize()
    geotagged_xml = article['tagged_xml']
    locations = geo_resolve(geotagged_xml, defoe_path, gazetteer, bounding_box)
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
    eb_geo_samples_df = pd.read_json('geotagged_xml_articles_flair_df.json', orient='records', lines=True)
    print(f"{len(eb_geo_samples_df)} samples loaded")

    # georesolving all samples
    sample_articles = eb_geo_samples_df.to_dict(orient='records')
    print("Georesolving articles....")
    for index, article in enumerate(tqdm(sample_articles)):
        article_location, locations = geoparse(article)
        article["locations"] = locations
        article.pop('tagged_xml')
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
    result_path = "articles_with_locations_flair_df.json"
    articles_df.to_json(result_path, orient='records', lines=True)
    print(f"result saved to {result_path}")


