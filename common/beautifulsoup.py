import copy
import itertools
import bs4
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


# define list of irrelevant tags
irrelevant_tags = [
    "svg",
    "style",
    "script",
    "img"
]

# define list of irrelevant attributes
irrelevant_attributes = [
    "href",
    "ping",
    "jsname",
    "jsaction",
    "jscontroller",
    "tabindex",
    "autocapitalize",
    "autocorrect",
    "autocomplete",
    "autofocus",
    "style",
    "data-ved",
]


# define list of extractable tags
extractable_tags = [
    "div",
    "ytd-transcript-segment-renderer"
]


def to_xpath(element):
    components = []
    child = element if element.name else element.parent
    for parent in child.parents:
        previous = itertools.islice(parent.children, 0, parent.contents.index(child))
        xpath_tag = child.name
        xpath_index = sum(1 for i in previous if i.name == xpath_tag) + 1
        components.append(xpath_tag if xpath_index == 1 else '%s[%d]' % (xpath_tag, xpath_index))
        child = parent
    components.reverse()
    return '/%s' % '/'.join(components)


def remove_children(element, copy):
    _element = copy.deepcopy(element) if copy else element
    if not isinstance(_element, bs4.element.NavigableString):
        for sub_element in _element.findChildren():
            sub_element.decompose()
    return _element


def find_extractable_elements(driver):
    # initialize beautifulsoup object
    soup = BeautifulSoup(driver.page_source, features="html.parser")

    # find all elements that are interactable
    elements, elements_str = [], []
    for tag in extractable_tags:
        for element in soup.find_all(tag):
            elements.append(element)
            elements_str.append(str(element).strip())

    return elements, elements_str


def format_element(soup, element):
    """Foramt element to get surroundings of a target element
        1. Get a parent element (1-depth)
        2. For sibling element, print only its children (1-depth)
        3. For sibling element, remove href and ping attributes
        4. For target element, do nothing
    """
    parent_element = copy.deepcopy(element.parent)
    cleanup_element(parent_element)

    for sibling_element in parent_element.children:
        if not isinstance(sibling_element, bs4.element.NavigableString):
            # remove irrelevant attributes
            cleanup_element(sibling_element)

            # print only sibling's children (1-depth)
            if sibling_element.get("target_element") is None:
                for sibling_element_child in sibling_element.children:
                    cleanup_element(sibling_element_child)
                    remove_children(sibling_element_child, copy=False)
    return parent_element


def cleanup_html(soup):
    for tag in irrelevant_tags:
        for element in soup.findAll(tag):
            element.extract()


def cleanup_element(element):
    if not isinstance(element, bs4.element.NavigableString):
        for attribute in irrelevant_attributes:
            if element.get(attribute) is not None:
                del element[attribute]


def find_interactable_elements(driver, is_format):
    # initialize beautifulsoup object
    soup = BeautifulSoup(driver.page_source, features="html.parser")

    # cleanup html by removing irrelevant tags (svg, style)
    cleanup_html(soup)

    # find all elements that are interactable
    elements, elements_str = [], []
    for tag in interactable_tags:
        for element in soup.find_all(tag):
            element["target_element"] = True
            elements.append(element)
            element_str = format_element(soup, element) if is_format else element
            elements_str.append(str(element_str).replace("\n", ""))
            del element["target_element"]

    return elements, elements_str
