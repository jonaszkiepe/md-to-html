import re

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,
)

delimiters = {
    text_type_bold: "**",
    text_type_italic: "*",
    text_type_code: "`",
}

def split_nodes_delimiter(old_nodes: list, delimiter, text_type) -> list:
    split_nodes = []
    for node in old_nodes:
        if node.text_type is text_type_text:
            texts = node.text.split(delimiter)
            if len(texts) == 2:
                raise Exception("Matching closing delimiter not found")
            for text in texts:
                if text:
                    split_type = text_type_text
                    if texts.index(text) % 2 == 1: split_type = text_type
                    split_nodes.append(TextNode(text, split_type))
        else: split_nodes.append(node)
    return split_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_url(old_nodes, extract_func) -> list:
    new_nodes = []
    for node in old_nodes:
        node_text = node.text
        if node_text:
            pairs = extract_func(node_text)
            if pairs:
                for pair in pairs:
                    splitter = f"[{pair[0]}]({pair[1]})"
                    if extract_func is extract_markdown_images: splitter = f"!{splitter}"
                    if pairs.index(pair) == 0:
                        texts = node_text.split(splitter, 1)
                    else: 
                        target_item = texts[-1]
                        texts.extend(target_item.split(splitter, 1))
                        texts.remove(target_item)
                for i in range(len(texts)):
                    if i != 0:
                        text, url, text_type = pairs[i - 1][0], pairs[i - 1][1], text_type_link
                        if extract_func is extract_markdown_images: text_type = text_type_image
                        new_nodes.append(TextNode(text, text_type, url))
                    if texts[i]: new_nodes.append(TextNode(texts[i], text_type_text))
            else: new_nodes.append(node)
    return new_nodes


def split_nodes_images(old_nodes: list) -> list:
    return split_nodes_url(old_nodes, extract_markdown_images)


def split_nodes_links(old_nodes: list) -> list:
    return split_nodes_url(old_nodes, extract_markdown_links)


def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    for text_type, delimiter in delimiters.items():
        nodes = (split_nodes_delimiter(nodes, delimiter, text_type))
    nodes = split_nodes_images(nodes)
    return split_nodes_links(nodes)
    
