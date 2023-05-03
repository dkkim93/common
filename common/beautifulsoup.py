import copy


# define list of interactable tags
interactable_tags = [
    "a",
    "button",
    "details",
    "embed",
    "input",
    "label",
    "select",
    "textarea",
    "yt-formatted-string"
]


# define list of extractable tags
extractable_tags = [
    "div",
    "ytd-transcript-segment-renderer"
]


def remove_children(element):
    _element = copy.deepcopy(element)
    for sub_element in _element.findChildren():
        sub_element.clear()
    return _element
