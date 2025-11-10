import os
import shutil
import sys

from generate_content import generate_page, generate_pages_recursive

def main() -> None:
    basepath = "/"
    if len(sys.argv) > 1:
        basepath = sys.argv[1] 

    if os.path.exists("./docs"):
        shutil.rmtree("./docs")

    os.mkdir("./docs")
    deep_copy_from_to("./docs", "./static")

    generate_pages_recursive("./content", "./template.html", "./docs", basepath)

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
