from defoe.nlsArticles.setup import filename_to_object
from defoe.nlsArticles.query_utils import filter_terms_page


def get_content_edge_hpos(page_hpos_vpos_font):
    previous_vpos = -1
    max_width = 1030
    right_column = False
    left_hpos_list = []
    right_hpos_list = []
    top_edge = -1
    ln = 0
    while ln < len(page_hpos_vpos_font):
        line = page_hpos_vpos_font[ln]
        ln += 1
        if len(line) > 0:
            tmp_top_edge = int(line[0][1])
            hpos = int(line[0][0])
            print(hpos)
            if tmp_top_edge > 500 or hpos > 700:
                continue
            else:
                top_edge = tmp_top_edge - 40
                break

    while ln < len(page_hpos_vpos_font):
        line = page_hpos_vpos_font[ln]
        ln += 1
        if len(line) > 0:
            first_word_hpos = int(line[0][0])
            last_word_hpos = int(line[len(line)-1][0])
            vpos = int(line[0][1])
            if previous_vpos > 0 and vpos < previous_vpos:
                right_column = True
            previous_vpos = vpos
            if right_column:
                if first_word_hpos > max_width and vpos > top_edge:
                    right_hpos_list.append(first_word_hpos)
            else:
                left_hpos_list.append(last_word_hpos)
    print(f" left: {left_hpos_list} ")
    print(right_hpos_list)
    left_column_right_edge = max(left_hpos_list)
    right_column_left_edge = min(right_hpos_list)
    left_column_left_edge = left_column_right_edge - max_width
    right_column_right_edge = right_column_left_edge + max_width
    return [left_column_left_edge, left_column_right_edge, right_column_left_edge, right_column_right_edge, top_edge]


def remove_notes(page_hpos_vpos_font):
    removed_notes = []
    edges = get_content_edge_hpos(page_hpos_vpos_font)
    left_column_left_edge = edges[0]
    right_column_right_edge = edges[3]
    top_edge = edges[4]
    while True:
        line = page_hpos_vpos_font[0]
        if len(line) > 0:
            if int(line[0][1]) > 500:
                removed_notes.extend(line)
                del page_hpos_vpos_font[0]
            else:
                break

    for ln in range(0, len(page_hpos_vpos_font)):
        line = page_hpos_vpos_font[ln]
        wn = 0
        line_length = len(line)
        while wn < line_length:
            word = page_hpos_vpos_font[ln][wn]
            hpos = int(word[0])
            vpos = int(word[1])
            if hpos <= left_column_left_edge or hpos >= right_column_right_edge or vpos < top_edge:
                removed_notes.append(word)
                del page_hpos_vpos_font[ln][wn]
            else:
                wn += 1
            if wn == len(page_hpos_vpos_font[ln]):
                break
    return removed_notes


def page_to_paragraphs(page_hpos_vpos_font):
    edges = get_content_edge_hpos(page_hpos_vpos_font)
    print(remove_notes(page_hpos_vpos_font))
    print(edges)
    left_column_left_edge = edges[0]
    left_column_right_edge = edges[1]
    right_column_left_edge = edges[2]
    right_column_right_edge = edges[3]
    top_edge = edges[4]
    paragraphs = []
    paragraph = []
    previous_first_word_hpos = -1
    right_column_first_line = False
    previous_vpos = -1
    for ln in range(0, len(page_hpos_vpos_font)):
        line = page_hpos_vpos_font[ln]
        if len(line) == 0:
            continue

        vpos = int(line[0][1])
        if previous_vpos > 0 and vpos < previous_vpos:
            right_column_first_line = True
        else:
            right_column_first_line = False

        words = list(map(lambda w: w[3], line))
        if ln == 0:
            previous_first_word_hpos = int(line[0][0])
            paragraph = words
        else:
            first_word_hpos = int(line[0][0])
            print(line)
            #print(f"hpos: {first_word_hpos}, previous: {previous_first_word_hpos}")
            if abs(first_word_hpos - previous_first_word_hpos) < 20 or \
                    (not right_column_first_line and previous_first_word_hpos > first_word_hpos + 40) or \
                    (right_column_first_line and first_word_hpos < right_column_left_edge + 40):
                print("here")
                paragraph.extend(words)
            else:
                if (right_column_first_line and first_word_hpos > right_column_left_edge + 40) or \
                        (not right_column_first_line and previous_first_word_hpos < first_word_hpos + 40):
                    # new paragraph
                    paragraphs.append(paragraph)
                    paragraph = words
                else:
                    print("case")
            previous_first_word_hpos = first_word_hpos

        if ln == len(page_hpos_vpos_font) - 1:
            paragraphs.append(paragraph)
    for paragraph in paragraphs:
        print(paragraph)


if __name__ == "__main__":
    data_file = "./eb.txt"
    filenames = [filename.strip() for filename in list(open(data_file))]
    data = [filename_to_object(filename) for filename in filenames]
    document1 = data[0][0][0]
    # page1 = document1.page('alto/190338559.34.xml')
    # page1 = document1.page('alto/190334399.34.xml')
    page1 = document1.page('alto/190335088.34.xml')
    print(document1.code)
    #print(page1.words)
    print(page1.page_id)
    #print(page1.header_left_words)
    #print(page1.header_right_words)
    #print(page1.content)
    page_hpos_vpos_font = page1.hpos_vpos_font_words

    defoe_path = "/Users/ly40/Documents/PhD/InformationExtraction/EncyclopaediaBritannica/NLS/"
    os_type = "sys-x86-64-sierra"
    type_page, header, page_clean_term_dict, length = filter_terms_page(page1, defoe_path, os_type)
    for term in page_clean_term_dict:
        print(term)
        #print(page_clean_term_dict[term])

    print("-----")
    page_to_paragraphs(page_hpos_vpos_font)