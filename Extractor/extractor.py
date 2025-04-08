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


def extra_see_references(text:str) -> list[str]:
    """
    This function extracts see references after the word "See". If there are same reference name occurs multiple times, this function will only return one.
    :param text: text to extract references from.
    :return: a list of reference names
    """
    pass