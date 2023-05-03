import copy
from bs4 import BeautifulSoup


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
        sub_element.decompose()
    return _element


def find_interactable_elements(driver, is_format):
    # initialize beautifulsoup object
    soup = BeautifulSoup(driver.page_source, features="html.parser")

    # find all elements that are interactable
    elements, elements_str = [], []
    for tag in interactable_tags:
        for element in soup.find_all(tag):
            elements.append(element)
            element_str = remove_children(element) if is_format else element
            elements_str.append(str(element_str).replace("\n", ""))

    return elements, elements_str
