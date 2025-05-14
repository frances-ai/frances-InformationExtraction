from typing import Union

import regex
def extract_names(head: str) -> tuple[str, list[str]]:
    """
    This function extracts primary name (first name appears) and alternative names from a head (first few words with article names in dictionary like text).
    :param head: first few words with article names in dictionary like text.
    :return: primary name and a list of alternative names.
    """
    pre_or, sep, post_or = head.partition(" OR ")
    #print(f"pre_or: {pre_or}, sep: {sep}, post_or: {post_or}")
    alternative_names = []
    primary_name = head
    words_pattern_str = "(([\p{L}\p{N}\-\'\.]+\s*)+)"
    if sep:
        # handle head with "OR"
        # if "OR" is embedded within parentheses
        paren_match = regex.search(r'' + words_pattern_str + '\(([^)]+)\sOR\s([^)]+)\)', head)
        if paren_match:
            #print(f"group 1: {paren_match.group(1)}, group 3: {paren_match.group(3)}, group4: {paren_match.group(4)}")
            pre_name = paren_match.group(1).strip()
            first_post_name = paren_match.group(3).strip()
            # remove the last comma if exists
            first_post_name = first_post_name.split(',', 1)[0]
            second_post_name = paren_match.group(4).strip()
            primary_name = f"{pre_name} {first_post_name}"
            alter_name = f"{pre_name} {second_post_name}"
            alternative_names.append(alter_name)
            #print(head)
            return primary_name, alternative_names

        names = pre_or.split(",")
        names = [name.strip() for name in names if len(name) > 0]
        primary_name = names[0]
        alternative_names = names[1:]
        last_alter_match = regex.search(r'\s+(PROPERLY|CALLED)\s+', post_or)
        if last_alter_match:
            last_name_start_index = last_alter_match.end(1)
            last_name = post_or[last_name_start_index:].strip()
            alternative_names.append(last_name)
        else:
            alternative_names.append(post_or)

        return primary_name, alternative_names

    # other rules
    indicator_match = regex.search(r'\s+(OTHERWISE\s+CALLED|CALLED|NAMED|PROPERLY|OTHERWISE)\s+' + words_pattern_str, head)
    if indicator_match:
        #print(head)
        pre_indicator_end_index = indicator_match.start(0)
        primary_name_end_index = head.rfind(",", 0, pre_indicator_end_index)
        if primary_name_end_index < 0:
            primary_name_end_index = head.rfind("(", 0, pre_indicator_end_index)
            if primary_name_end_index < 0:
                primary_name_end_index = pre_indicator_end_index
        primary_name = head[:primary_name_end_index].strip()
        last_name = indicator_match.group(2).strip()
        alternative_names.append(last_name)
        return primary_name, alternative_names
    return primary_name, alternative_names


def extract_see_references(text:str) -> list[str]:
    """
    This function extracts see references after the word "See" at the end of the text. If there are same reference name occurs multiple times, this function will only return one.
    :param text: text to extract references from.
    :return: a list of reference names
    """
    references = []
    indicator_match = regex.search(r"(See|Vide)\s+((\(?\p{Lu}[\p{Lu\p{L}\-\'\.\)]+\s*)+(and\s+(\(?\p{Lu}[\p{Lu\p{L}\-\'\.\)]+\s*)+)?)$", text)

    if indicator_match:
        post_indicator_text = indicator_match.group(2).strip()
        if post_indicator_text[-1] == '.':
            post_indicator_text = post_indicator_text[:-1]
        pre_and, sep, post_and = post_indicator_text.partition(" and ")
        #print(post_indicator_text)
        if sep:
            references.append(pre_and.strip())
            references.append(post_and.strip())
        else:
            references.append(post_indicator_text.strip())

    return references


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
