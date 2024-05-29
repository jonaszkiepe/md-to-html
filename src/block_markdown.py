from htmlnode import LeafNode, ParentNode
from textnode import TextNode, text_nodes_to_html_nodes
from inline_markdown import text_to_textnodes

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"


def markdown_to_blocks(md):
    return [block.strip() for block in md.split('\n\n') if block]


def block_to_block_type(md_block):
    block_first_chars = md_block.split()[0]
    if (not [c for c in block_first_chars if c != '#'] and len(block_first_chars) <= 6):
        return block_type_heading
    if md_block[:3] == "```" and md_block[-3:] == "```":
        return block_type_code
    block_lines = md_block.split('\n')
    if not [line[0] for line in block_lines if line[0] != '>']:
        return block_type_quote
    lines_first_chars = [line.split()[0] for line in block_lines]
    if not [c for c in lines_first_chars if not (c == "*" or c == "-")]:
        return block_type_unordered_list
    line_nr = 1
    for chars in lines_first_chars:
        if chars != str(line_nr) + '.': return block_type_paragraph
        line_nr += 1
    return block_type_ordered_list


def block_to_html_paragraph(p_block):
    return ParentNode(
        text_nodes_to_html_nodes(text_to_textnodes(p_block)),
        'p',
    )


convert = lambda arg: text_nodes_to_html_nodes(text_to_textnodes(arg))


def block_to_html_heading(h_block):
    text = h_block.lstrip("#")[1:]
    return ParentNode(
        convert(text),
        f"h{len(h_block.split()[0])}",
    )



def block_to_html_code(c_block):
    return ParentNode([LeafNode(c_block[3:-3], "code")], "pre")


def block_to_html_quote(q_block):
    new_block = '\n'.join([line[2:] for line in q_block.split('\n')])
    return ParentNode(
        convert(new_block),
        "quoteblock"
    )


def block_to_html_unordered_list(ul_block):
    lines = ul_block.split('\n')
    return ParentNode([ParentNode(convert(l[2:]), "li") for l in lines], "ul")


def block_to_html_ordered_list(ol_block):
    lines = ol_block.split('\n')
    return ParentNode([ParentNode(convert(l[3:]), "li") for l in lines], "ol")


def markdown_to_html_node(markdown):
    node_blocks = []
    for block in markdown_to_blocks(markdown):
        block_type = block_to_block_type(block)
        if block_type == block_type_paragraph:
            node_blocks.append(block_to_html_paragraph(block))
        elif block_type == block_type_heading:
            node_blocks.append(block_to_html_heading(block))
        elif block_type == block_type_code:
            node_blocks.append(block_to_html_code(block))
        elif block_type == block_type_quote:
            node_blocks.append(block_to_html_quote(block))
        elif block_type == block_type_unordered_list:
            node_blocks.append(block_to_html_unordered_list(block))
        else:
            node_blocks.append(block_to_html_ordered_list(block))
    return ParentNode(node_blocks, "div")

