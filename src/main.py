from textnode import TextNode

def main():
    tn = TextNode("", "bold")
    print(tn)
    tn = TextNode("This is a text node", "bold", "https://www.boot.dev")
    print(tn)

main()

