import re

from textnode import TextNode, TextType
from leafnode import LeafNode


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "",  {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"unknown text type '{text_node.text_type}'")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type == TextType.TEXT:
            if old_node.text.count(delimiter) % 2:
                raise ValueError("invalid Markdown syntax")
            for i, text in enumerate(old_node.text.split(delimiter)):
                if i % 2 == 0:
                    new_nodes.append(TextNode(text, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(text, text_type))
        else:
            new_nodes.append(old_node)
    return new_nodes

element_re = re.compile(r"(!?)\[([^]]*)\]\(([^)]*)\)")
_LINK    = 0x01
_IMAGE   = 0x02
_EXTRACT = 0x00
_SPLIT   = 0x10

def handle_markdown_elements(text, what = _LINK | _IMAGE):
    elements = []
    off = 0
    for m in element_re.finditer(text):
        if (
            m.group(1) == "" and (what & _LINK) == _LINK
            or
            m.group(1) == "!" and (what & _IMAGE) == _IMAGE
        ):
            if (what & _SPLIT) == _SPLIT:
                t0 = off
                t1, off = m.span()
                if t0 < t1:
                    elements.append(TextNode(text[t0:t1], TextType.TEXT))
                if (what & _LINK) == _LINK:
                    text_type = TextType.LINK
                elif (what & _IMAGE) == _IMAGE:
                    text_type = TextType.IMAGE
                else:
                    text_type = TextType.TEXT
                elements.append(TextNode(m.group(2), text_type, m.group(3)))
                off = m.span()[1]
            else:
                elements.append((m.group(2), m.group(3)))
    if (what & _SPLIT) == _SPLIT and (len(elements) == 0 or off < len(text)):
        elements.append(TextNode(text[off:], TextType.TEXT))
    return elements

def extract_markdown_images(text):
    return handle_markdown_elements(text, _IMAGE | _EXTRACT)

def extract_markdown_links(text):
    return handle_markdown_elements(text, _LINK | _EXTRACT)

def split_nodes_image(old_nodes):
    nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            nodes.extend(handle_markdown_elements(node.text, _IMAGE | _SPLIT))
        else:
            nodes.append(node)
    return nodes

def split_nodes_link(old_nodes):
    nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            nodes.extend(handle_markdown_elements(node.text, _LINK | _SPLIT))
        else:
            nodes.append(node)
    return nodes

