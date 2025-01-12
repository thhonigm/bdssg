import unittest

from parentnode import ParentNode
from leafnode import LeafNode

leafs = [
    LeafNode("b", "Bold text"),
    LeafNode(None, "Normal text"),   
    LeafNode("i", "Italic text"),
    LeafNode(None, "More normal text"),   
]
html_leafs = "<b>Bold text</b>Normal text<i>Italic text</i>More normal text"

class TestParentNode(unittest.TestCase):

    def test_empty(self):
        with self.assertRaises(TypeError):
            node = ParentNode()

    def test_without_children(self):
        with self.assertRaises(TypeError):
            node = ParentNode("p")

    def test_without_tag(self):
        with self.assertRaises(ValueError):
            node = ParentNode(None, None)
            node.to_html()

    def test_with_none_children(self):
        with self.assertRaises(ValueError):
            node = ParentNode("p", None)
            node.to_html()

    def test_simple(self):
        node = ParentNode("p", leafs)
        self.assertEqual(node.to_html(), "<p>" + html_leafs + "</p>")

    def test_no_children(self):
        node = ParentNode("p", [])
        self.assertEqual(node.to_html(), "<p></p>")

    def test_one_child(self):
        node = ParentNode("p", [LeafNode(None, "normal text")])
        self.assertEqual(node.to_html(), "<p>normal text</p>")

    def test_complex(self):
        node = ParentNode("div", [
            ParentNode("p", leafs), 
            ParentNode("p", leafs), 
            ParentNode("p", leafs), 
            ParentNode("p", leafs),
        ])
        self.assertEqual(node.to_html(),
            "<div>" + ("<p>" + html_leafs + "</p>") * 4 + "</div>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )

if __name__ == "__main__":
    unittest.main()

