import os
from block_markdown import extract_title, markdown_to_html_node


def generate_page(from_path: str, template_path: str, dest_path: str, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    try:
        with open(from_path, "r") as f:
            markdown = f.read()

        with open(template_path, "r") as f:
            template = f.read()

        title = extract_title(markdown)
        html = markdown_to_html_node(markdown).to_html()

        new_file_content = (
            template.replace("{{ Title }}", title)
            .replace("{{ Content }}", html)
            .replace('href="/', f'href="{basepath}')
            .replace('src="/', f'src="{basepath}')
        )

        file_directory = os.path.dirname(dest_path)
        os.makedirs(file_directory, exist_ok=True)
        with open(dest_path, "w") as f:
            f.write(new_file_content)

    except Exception as e:
        return f"Error: {e}"


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str, basepath: str
) -> None:
    dir_elements = os.listdir(dir_path_content)

    for element in dir_elements:
        path_from = os.path.join(dir_path_content, element)
        path_to = os.path.join(dest_dir_path, element)
        if os.path.isfile(path_from):
            path_to = path_to.replace(".md", ".html")
            print(f"generate html file from {path_from} to {path_to}")
            generate_page(path_from, template_path, path_to, basepath)
        else:
            print(f"create folder with name {element} at {path_to}")
            os.mkdir(path_to)
            generate_pages_recursive(path_from, template_path, path_to, basepath)
