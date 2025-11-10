import os
from block_markdown import extract_title, markdown_to_html_node


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    try:
        with open(from_path, "r") as f:
            markdown = f.read()

        with open(template_path, "r") as f:
            template = f.read()

        title = extract_title(markdown)
        html = markdown_to_html_node(markdown).to_html()

        new_file_content = template.replace("{{ Title }}", title).replace(
            "{{ Content }}", html
        )

        file_directory = os.path.dirname(dest_path)
        os.makedirs(file_directory, exist_ok=True)
        with open(dest_path, "w") as f:
            f.write(new_file_content)

    except Exception as e:
        return f"Error: {e}"
