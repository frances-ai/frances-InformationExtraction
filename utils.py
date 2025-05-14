from typing import Dict
import re

# chunk text
import re
def ends_with(options, text):
    for option in options:
        if text.endswith(option):
            return True
    return False

def chunk(text, max_sequence_length=1120):
    sentences = re.split(r'(?<=\.)\s+', text)
    # remove the last empty sentence if exists
    if len(sentences[-1]) == 0:
        sentences.pop(-1)
    offsets = []
    previous_end = 0
    for index, sentence in enumerate(sentences):
        if len(sentence) == 0:
            print(previous_end)
            raise Exception('Empty sentence')
        sent_start = text.find(sentence, previous_end, previous_end + len(sentence) + 2)
        sent_end = sent_start + len(sentence)
        if sent_start < 0:
            raise Exception("Cannot find start index of the sentence")
        previous_end = sent_end
        offsets.append({'start': sent_start, 'end': sent_end})
    #print(len(offsets))
    # if sentence ends with specified chars, then the next sentence will be added
    ignores = ["Mr.", "Mrs.", "Ms.", "Miss", "Dr.", "Prof.", "Rev.", "Gen.", "Col.", "Maj.", "Lt.", "Sgt.", "Capt.",
    "Gov.", "Sen.", "Rep.", "Pres.", "Amb.", "Hon.", "Atty.", "Fr.", "Br.", "Sr.", "Fig."]
    s_size = len(sentences)
    s_index = 0
    while (s_index < s_size):
        if ends_with(ignores, sentences[s_index]):
          if s_index + 1 < s_size:
            sentences[s_index] += " " + sentences[s_index + 1]
            sentences.pop(s_index + 1)
            offsets[s_index]['end'] = offsets[s_index + 1]['end']
            offsets.pop(s_index + 1)
            #print("-----specified chars")
            #print(sentences[s_index])
            s_size -= 1
            continue
        s_index += 1

    # if the next sentence starts with lowercase char, then it will be added
    s_size = len(sentences)
    s_index = 1
    while (s_index < s_size):
        if sentences[s_index][0].islower():
            sentences[s_index - 1] += " " + sentences[s_index]
            sentences.pop(s_index)
            offsets[s_index - 1]['end'] = offsets[s_index]['end']
            offsets.pop(s_index)
            #print("-----lowercase chars")
            #print(sentences[s_index-1])
            s_size -= 1
            continue
        s_index += 1
    #print(len(offsets))

    # if sentence has less than max_sequence_length words, then it will be added to previous sentence
    s_size = len(sentences)
    s_index = 0
    while (s_index < s_size):
        len_current_sequence = len(sentences[s_index].split())
        if len_current_sequence < max_sequence_length:
          if s_index + 1 < s_size and len(sentences[s_index + 1].split()) + len_current_sequence < max_sequence_length:
            sentences[s_index] += " " + sentences[s_index + 1]
            sentences.pop(s_index + 1)
            offsets[s_index]['end'] = offsets[s_index + 1]['end']
            offsets.pop(s_index + 1)
            s_size -= 1
            continue
        s_index += 1
    sentences = [text[offset['start']:offset['end']] for offset in offsets]
    return sentences, offsets



def get_normalised_snippet(source_text, target_str, target_start_index, max_prefix_size=10, max_suffix_size=10):
    prefix_start_index = target_start_index - max_prefix_size * 2
    if prefix_start_index > 0:
        prefix = source_text[prefix_start_index:target_start_index]
    else:
        prefix = source_text[:target_start_index]

    # print(prefix)
    prefix_without_white_space = re.sub(r"\s", "", prefix)
    prefix_size = len(prefix_without_white_space)
    if prefix_size > max_prefix_size:
        prefix_size = max_prefix_size
    prefix = prefix_without_white_space[-prefix_size:]
    # print(prefix)

    target_end_index = target_start_index + len(target_str)
    suffix_end_index = target_end_index + max_suffix_size * 2
    if suffix_end_index < len(source_text):
        suffix = source_text[target_end_index:suffix_end_index]
    else:
        suffix = source_text[target_end_index:]

    # print(suffix)
    suffix_without_white_space = re.sub(r"\s", "", suffix)
    suffix_size = len(suffix_without_white_space)
    if suffix_size > max_suffix_size:
        suffix_size = max_suffix_size
    suffix = suffix_without_white_space[:suffix_size]
    # print(suffix)
    snippet = prefix + target_str + suffix

    return snippet, prefix_size, suffix_size


def add_position_to_geo_obj(geo_obj: Dict, source_text: str, from_source_index: int,
                            location_start_index_in_geo_snippet) -> Dict:
    """
    This function aims to find the start index and end index of a location from geo_obj within the source text.
    :param geo_obj: dict result of geoparser_xml_tojson function.
    :param source_text: text where location is recognised.
    :param from_source_index: find position from this index in the source text.
    :param location_start_index_in_geo_snippet: the start index of the location from  the geo_obj snippet.
    :return:
    """
    location_name = geo_obj["name"]
    location_start_index = source_text.find(location_name, from_source_index)
    geo_obj_snippet = geo_obj["snippet"]
    match = False
    # Keep checking if current located location matches the one in geo_obj,
    # Match should be true when they have same snippet.
    while not match and location_start_index != -1:
        # compare snippets with no whitespaces, the lengths of the snippets are same,
        # the prefix and suffix are no more than the defined max value.
        geo_obj_snippet, geo_prefix_size, geo_suffix_size = get_normalised_snippet(geo_obj_snippet, location_name,
                                                                                   location_start_index_in_geo_snippet)
        print(location_start_index)
        current_snippet, prefix_size, suffix_size = get_normalised_snippet(source_text, location_name,
                                                                           location_start_index, geo_prefix_size,
                                                                           geo_suffix_size)
        print(f"geo_obj_snippet: {geo_obj_snippet}, current_snippet: {current_snippet}")
        if current_snippet == geo_obj_snippet:
            match = True
        else:
            location_start_index = source_text.find(location_name, location_start_index + len(location_name) + 1)

    if match:
        start_index = location_start_index
        end_index = location_start_index + len(location_name)
        geo_obj["start_index"] = start_index
        geo_obj["end_index"] = end_index
        return geo_obj