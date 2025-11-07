def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    sanitized_blocks = []
    for block in blocks:
        sanitized_block = block.strip("\n")
        sanitized_block = sanitized_block.strip()
        if sanitized_block != "":
            sanitized_blocks.append(sanitized_block)

    return sanitized_blocks
