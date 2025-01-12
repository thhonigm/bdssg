import unittest

from textnode import TextNode, TextType
from leafnode import LeafNode
from conversion import (
     text_node_to_html_node,
     split_nodes_delimiter,
     extract_markdown_images,
     extract_markdown_links,
     split_nodes_image,
     split_nodes_link,
)

class TestTextNodeToHtmlNode(unittest.TestCase):

    def test_unknown_text_type(self):
        with self.assertRaises(ValueError):
            text = TextNode("some text", None)
            cv_text = text_node_to_html_node(text)
    
    def test_text(self):
        text = TextNode("This is a text node", "text")
        cv_text = text_node_to_html_node(text)
        leaf = LeafNode(None, "This is a text node")
        self.assertEqual(cv_text, leaf)

    def test_bold(self):
        text = TextNode("This is bold text", "bold")
        cv_text = text_node_to_html_node(text)
        leaf = LeafNode("b", "This is bold text")
        self.assertEqual(cv_text, leaf)

    def test_italic(self):
        text = TextNode("This is italic text", "italic")
        cv_text = text_node_to_html_node(text)
        leaf = LeafNode("i", "This is italic text")
        self.assertEqual(cv_text, leaf)

    def test_code(self):
        text = TextNode("This is code", "code")
        cv_text = text_node_to_html_node(text)
        leaf = LeafNode("code", "This is code")
        self.assertEqual(cv_text, leaf)

    def test_link(self):
        text = TextNode("This is a link", "link", "http://www.google.com")
        cv_text = text_node_to_html_node(text)
        leaf = LeafNode("a", "This is a link", {"href": "http://www.google.com"})
        self.assertEqual(cv_text, leaf)

    def test_image(self):
        text = TextNode("image description", "image", "http://www.google.com/icon.png")
        cv_text = text_node_to_html_node(text)
        leaf = LeafNode("img", "", {"src": "http://www.google.com/icon.png", "alt": "image description"})
        self.assertEqual(cv_text, leaf)

class TestSplitNodesDelimiter(unittest.TestCase):

    def test_empty(self):
        nodes = []
        new_nodes = split_nodes_delimiter(nodes, '*', "italic")
        self.assertEqual(new_nodes, [])

    def test_code(self):
        node = TextNode("This is text with a `code block` word", "text")
        new_nodes = split_nodes_delimiter([node], "`", "code")
        self.assertSequenceEqual(new_nodes,
            [
                TextNode("This is text with a ", "text"),
                TextNode("code block", "code"),
                TextNode(" word", "text"),
            ]
        )

    def test_bold(self):
        node = TextNode("This is text with a **bold** word", "text")
        new_nodes = split_nodes_delimiter([node], "**", "bold")
        self.assertSequenceEqual(new_nodes,
            [
                TextNode("This is text with a ", "text"),
                TextNode("bold", "bold"),
                TextNode(" word", "text"),
            ]
        )

    def test_italic(self):
        node = TextNode("This is text with an *italic* word", "text")
        new_nodes = split_nodes_delimiter([node], "*", "italic")
        self.assertSequenceEqual(new_nodes,
            [
                TextNode("This is text with an ", "text"),
                TextNode("italic", "italic"),
                TextNode(" word", "text"),
            ]
        )

    def test_complex(self):
        node_bold = TextNode("This is text with a **bold** word.", "text")
        node_italic = TextNode("This is text with an *italic* word.", "text")
        node_code = TextNode("This is text with a `code block` word.", "text")
        node_all = TextNode("This is text with a **bold** word, an *italic* word, and some `code`.", "text")
        new_nodes = [node_bold, node_italic, node_code, node_all]
        new_nodes = split_nodes_delimiter(new_nodes, "**", "bold")
        new_nodes = split_nodes_delimiter(new_nodes, "*", "italic")
        new_nodes = split_nodes_delimiter(new_nodes, "`", "code")
        self.assertSequenceEqual(new_nodes,
            [
                TextNode("This is text with a ", "text"),
                TextNode("bold", "bold"),
                TextNode(" word.", "text"),
                TextNode("This is text with an ", "text"),
                TextNode("italic", "italic"),
                TextNode(" word.", "text"),
                TextNode("This is text with a ", "text"),
                TextNode("code block", "code"),
                TextNode(" word.", "text"),
                TextNode("This is text with a ", "text"),
                TextNode("bold", "bold"),
                TextNode(" word, an ", "text"),
                TextNode("italic", "italic"),
                TextNode(" word, and some ", "text"),
                TextNode("code", "code"),
                TextNode(".", "text"),
            ]
        )


class TestExtract(unittest.TestCase):

    def test_empty(self):
        text = ""
        self.assertEqual(extract_markdown_images(text), [])
        self.assertEqual(extract_markdown_links(text), [])

    def test_no_markdown(self):
        text = "This is text."
        self.assertEqual(extract_markdown_images(text), [])
        self.assertEqual(extract_markdown_links(text), [])

    def test_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"), 
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ])
        self.assertEqual(extract_markdown_links(text), [])

    def test_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_images(text), [])
        self.assertEqual(extract_markdown_links(text), [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ])

    def test_markdown_all(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev), a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) and another link to [to youtube](https://www.youtube.com/@bootdotdev)."
        self.assertEqual(extract_markdown_images(text), [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"), 
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ])
        self.assertEqual(extract_markdown_links(text), [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ])


class TestSplit(unittest.TestCase):

    def test_empty(self):
        node = TextNode("", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [node])
        self.assertEqual(split_nodes_link([node]), [node])

    def test_no_markdown(self):
        nodes = [TextNode("", TextType.TEXT), TextNode("this is text.", TextType.TEXT)]
        self.assertEqual(split_nodes_image(nodes), nodes)
        self.assertEqual(split_nodes_link(nodes), nodes)

    def test_markdown_images(self):
        node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg).", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"), 
            TextNode(" and ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(".", TextType.TEXT),
        ])
        self.assertEqual(split_nodes_link([node]), [node])

    def test_markdown_images_empty_begin(self):
        node = TextNode("![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg).", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"), 
            TextNode(" and ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(".", TextType.TEXT),
        ])
        self.assertEqual(split_nodes_link([node]), [node])

    def test_markdown_images_empty_end(self):
        node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"), 
            TextNode(" and ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        ])
        self.assertEqual(split_nodes_link([node]), [node])

    def test_markdown_images_empty_middle(self):
        node = TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)![obi wan](https://i.imgur.com/fJRm4Vk.jpeg).", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"), 
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(".", TextType.TEXT),
        ])
        self.assertEqual(split_nodes_link([node]), [node])

    def test_markdown_links(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev).", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [node])
        self.assertEqual(split_nodes_link([node]), [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            TextNode(".", TextType.TEXT),
        ])

    def test_markdown_links_empty_begin(self):
        node = TextNode("[to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev).", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [node])
        self.assertEqual(split_nodes_link([node]), [
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            TextNode(".", TextType.TEXT),
        ])

    def test_markdown_links_empty_end(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [node])
        self.assertEqual(split_nodes_link([node]), [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ])

    def test_markdown_links_empty_middle(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev)[to youtube](https://www.youtube.com/@bootdotdev).", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [node])
        self.assertEqual(split_nodes_link([node]), [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            TextNode(".", TextType.TEXT),
        ])

    def test_markdown_all(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev), a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) and another link to [to youtube](https://www.youtube.com/@bootdotdev).", TextType.TEXT)
        self.assertEqual(split_nodes_link(split_nodes_image([node])), [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(", a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"), 
            TextNode(" and ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and another link to ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            TextNode(".", TextType.TEXT),
        ])
        self.assertEqual(split_nodes_image(split_nodes_link([node])), [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(", a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"), 
            TextNode(" and ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and another link to ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            TextNode(".", TextType.TEXT),
        ])




if __name__ == "__main__":
    unittest.main()

