import unittest

from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):

    def test_empty(self):
        with self.assertRaises(TypeError):
            node = LeafNode()

    def test_node_p(self):
        node = LeafNode("p", "This is a paragraph of text.")
        self.assertEqual(node.to_html(), '<p>This is a paragraph of text.</p>')
        
    def test_node2(self):
        node = LeafNode("a", "Google", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com" target="_blank">Google</a>')
        
    def test_node_children(self):
        with self.assertRaises(TypeError):
            google = LeafNode("a", "Google", None, {"href": "https://www.google.com"})
            facebook = LeafNode("a", "Facebook", None, {"href": "https://www.facebook.com"})
            par = LeafNode("p", "a paragraph", [facebook, google], None)

if __name__ == "__main__":
    unittest.main()

