from typing import Union

import pandas as pd
import regex

def dms_to_dd(degrees: int, minutes: int, seconds: float, direction: str) -> float:
    """
    Convert coordinates from degrees, minutes, seconds (DMS) format to decimal degrees (DD).

    :param degrees: Degrees component of the coordinate.
    :type degrees: int
    :param minutes: Minutes component of the coordinate.
    :type minutes: int
    :param seconds: Seconds component of the coordinate.
    :type seconds: float
    :param direction: Direction character ('N', 'S', 'E', 'W') that determines the sign.
    :type direction: str
    :return: The coordinate in decimal degrees.
    :rtype: float

    :raises ValueError: If an invalid direction is provided.
    """
    if direction.upper() not in ['N', 'S', 'E', 'W', '']:
        raise ValueError("Direction must be one of 'N', 'S', 'E', 'W', or empty")

    dd = degrees + minutes / 60 + seconds / 3600
    if direction.upper() in ['S', 'W']:
        dd = -dd
    return dd


def extract_coordinates(text: str) -> Union[tuple[float, float], None]:
    """
    This function extract coordinates from the given text, it will return the longitude and latitude coordinates if exists, otherwise it will return None.
    :param text: the text to extract coordinates from.
    :return: (latitude, longitude) if exists, None otherwise.
    """
    # fix simple OCR errors
    text = text.replace("O", "0")
    text = text.replace("Ò", "0")
    text = text.replace("Ε", "E")
    text = text.replace("Ë", "E")
    text = text.replace("Ľ", "E")
    text = text.replace("z", "'")
    text = text.replace(" L ", " 1. ")
    text = text.replace("I.", "1.")
    text = regex.sub(r'(?<=\d)L', '1.', text)
    text = text.replace("T", "1")
    text = text.replace("G", "6")
    text = text.replace("&", "S")
    text = text.replace("ĵ", ";")
    # print(text)

    coordinates_pattern = regex.search(
        r"(?P<first>(?P<first_type>[Ll](ong|at))[\.\,\s]*(?P<first_vals>(\d+[\.,∙\s’°\'\"]*)+)\s*(?P<first_dir>[NSEWnsew]?)[\.,;\'\‘∙»«\s\-]*)"
        r"(and\s+)?"
        r"(?P<second>(?P<second_type>[Ll](ong|at))[\.\,\s]*(?P<second_vals>(\d+[\.,∙\s’°'\"]*)+)\s*(?P<second_dir>[NSEWnsew]?)[\.,;\'\‘∙\s»«\∣\-]*)$",
        text
    )
    if coordinates_pattern:
        coord1_type = coordinates_pattern.group("first_type").lower()
        coord1_vals = regex.sub(r"[\.,∙\s’°\'\"]", " ", coordinates_pattern.group("first_vals").strip()).split()
        coord1_dir = coordinates_pattern.group("first_dir").upper()
        coord1_dms_values = [0, 0, 0]
        for index, val in enumerate(coord1_vals):
            coord1_dms_values[index] =int(val)
        coord1_dd = dms_to_dd(coord1_dms_values[0], coord1_dms_values[1], coord1_dms_values[2], coord1_dir)
        #print(coord1_dd)
        coord2_type = coordinates_pattern.group("second_type").lower()
        coord2_vals = regex.sub(r"[\.,∙\s’°\'\"]", " ", coordinates_pattern.group("second_vals").strip()).split()
        coord2_dir = coordinates_pattern.group("second_dir").upper()
        coord2_dms_values = [0, 0, 0]
        for index, val in enumerate(coord2_vals):
            coord2_dms_values[index] =int(val)
        coord2_dd = dms_to_dd(coord2_dms_values[0], coord2_dms_values[1], coord2_dms_values[2], coord2_dir)
        #print(coord2_dd)
        #print(coord1_type, coord1_vals, coord1_dir)
        #print(coord2_type, coord2_vals, coord2_dir)
        #print(coord1_dms_values, coord2_dms_values)
        longitude = coord1_dd
        latitude = coord2_dd
        if "long" == coord2_type:
            longitude = coord2_dd
            latitude = coord1_dd
        return latitude, longitude

    return None

def is_location(article):
    if "coordinates" in article and article["coordinates"] and pd.notna(article["coordinates"]):
        return True
    return article["is_location"]


if __name__ == "__main__":
    # load input dataframe
    eb_df = pd.read_json('eb1_1771_geotagged_articles_stanza_df.json', orient='records', lines=True)
    eb_df['coordinates'] = eb_df['hq_text'].apply(extract_coordinates)
    eb_df['is_location'] = eb_df.apply(is_location, axis=1)
    eb_df.to_json('eb1_1771_refined_geotagged_articles_stanza_df.json', orient='records', lines=True)