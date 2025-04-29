from defoe.query_utils import georesolve_cmd, georesolved_xml_tojson
from defoe import get_root_path
from tqdm import tqdm
import pandas as pd
import string
import regex

defoe_path = get_root_path() + "/"
gazetteer = "geonames"
bounding_box = ""

def normalize_name(name):
    name = regex.sub(r'[^\p{L}\s\-\'\,\.\’]', '', name)
    name = regex.sub(r'\n', '', name)
    name = string.capwords(name)
    return name

def construct_places_xml(tagged_tokens):
    xml_doc = '<placenames> '
    for index, token in enumerate(tagged_tokens):
        id = index + 1
        toponym = normalize_name(token['name'])
        start_index = token['start']
        end_index = token['end']
        child = f'<placename id="{str(id)}" start="{start_index}" end="{end_index}" name="{toponym}"/> '
        xml_doc = xml_doc + child
    xml_doc = xml_doc + '</placenames>'
    return xml_doc

def geo_resolve(geotagged_xml, defoe_path, gazetteer, bounding_box):
    resolved_xml = georesolve_cmd(geotagged_xml, defoe_path, gazetteer, bounding_box)
    geo_list = georesolved_xml_tojson(resolved_xml)
    return geo_list

def geoparse(target_article):
    # add name back to the text
    article_name = normalize_name(target_article["name"])
    tagged_tokens = []
    if target_article["is_location"]:
        tagged_tokens.append({
            "name": article_name,
            "start": 0,
            "end": 0,
        })
    tagged_tokens.extend(target_article["locations"])
    #print(text_with_article_name)

    resolve_locations = []
    # batch georesolve
    batch_size = 3
    current_chunk_start = 0
    current_chunk_end = batch_size
    if current_chunk_end > len(tagged_tokens):
        current_chunk_end = len(tagged_tokens)
    while current_chunk_end <= len(tagged_tokens):
        tagged_tokens_batched = tagged_tokens[current_chunk_start:current_chunk_end]
        # construct xml
        places_xml = construct_places_xml(tagged_tokens_batched)
        # georesolving
        current_batch_locations = geo_resolve(places_xml, defoe_path, gazetteer, bounding_box)
        if len(current_batch_locations) > 0:
            resolve_locations.extend(current_batch_locations)

        if current_chunk_end == len(tagged_tokens):
            break
        current_chunk_start = current_chunk_end
        if current_chunk_start + batch_size > len(tagged_tokens):
            current_chunk_end = len(tagged_tokens)
        else:
            current_chunk_end = current_chunk_start + batch_size

    print(resolve_locations)

    # check if this article is a location
    target_article_location = None
    if len(resolve_locations) > 0 and resolve_locations[0]['name'] == article_name and resolve_locations[0]['end'] == 0:
        target_article_location = resolve_locations[0]
        resolve_locations.pop(0)
    return target_article_location, resolve_locations


if __name__ == "__main__":
    # load samples
    print("Loading geotagged eb geo samples....")
    eb_geo_samples_df = pd.read_json('geotagged_articles_stanza_df.json', orient='records', lines=True)
    print(f"{len(eb_geo_samples_df)} samples loaded")

    # geoparse all samples
    sample_articles = eb_geo_samples_df.to_dict(orient='records')
    print("Geoparsing articles....")
    for index, article in enumerate(tqdm(sample_articles[:100])):
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
    result_path = "eb7_georesolved_df.json"
    articles_df.to_json(result_path, orient='records', lines=True)
    print(f"result saved to {result_path}")


