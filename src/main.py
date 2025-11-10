import os
import shutil

from generate_content import generate_page, generate_pages_recursive

def main() -> None:
    if os.path.exists("./public"):
        shutil.rmtree("./public")

    os.mkdir("./public")
    deep_copy_from_to("./public", "./static")

    generate_pages_recursive("./content", "./template.html", "./public")

    return None

def deep_copy_from_to(target: str, source: str)-> None:
    print(f"init fn with {target}, {source}")

    contents = os.listdir(source)
    for content in contents:
        if os.path.isfile(os.path.join(source, content)):
            print(f"copy file from {os.path.join(source, content)} to {os.path.join(target, content)}")
            shutil.copy(os.path.join(source, content), os.path.join(target, content))
        else:
            print(f"create folder with name {content} at {os.path.join(target, content)}")
            os.mkdir(os.path.join(target, content))
            deep_copy_from_to(os.path.join(target, content), os.path.join(source, content))

if __name__ == "__main__":
    main()
