import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def test_empty(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_node(self):
        node = HTMLNode("a", "Google", None, {"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')
        
    def test_node2(self):
        node = HTMLNode("a", "Google", None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
        
    def test_node_pos(self):
        google = HTMLNode("a", "Google", None, {"href": "https://www.google.com"})
        facebook = HTMLNode("a", "Facebook", None, {"href": "https://www.facebook.com"})
        par = HTMLNode("p", "a paragraph", [facebook, google], None)
        self.assertEqual(par.props_to_html(), "")

    def test_node_key(self):
        google = HTMLNode(value = "Google", tag = "a", props = {"href": "https://www.google.com"})
        facebook = HTMLNode(tag = "a", value = "Facebook",  props = {"href": "https://www.facebook.com"})
        par = HTMLNode(tag = "p", value = "a paragraph", children = [facebook, google])
        self.assertEqual(par.props_to_html(), "")

if __name__ == "__main__":
    unittest.main()

