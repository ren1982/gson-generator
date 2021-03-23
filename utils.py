def generate_lyric_segment(segment_name, segment_length, text_model):
    segment = [segment_name]
    for i in range(segment_length):
        segment.append(text_model.make_sentence(tries=100, max_words=20, max_overlap_ratio=0.6))
    return segment


def generate_chorus(text_model, chorus_length, title_line):
    chorus = ["CHORUS"]
    title = None
    for i in range(chorus_length):
        if i == title_line:
            title = text_model.make_sentence(tries=100, max_words=6)
            chorus.append(title)
        else:
            chorus.append(text_model.make_sentence(tries=100, max_words=10, max_overlap_ratio=0.6))
    return chorus, title
