from textnode import TextNode, TextType


def main() -> None:
    text_node = TextNode("foo bar", TextType.PLAIN)
    print(text_node)


if __name__ == "__main__":
    main()
