import os, shutil
from block_markdown import markdown_to_html_node

CONTENT = "content"
TEMPLATE = "template.html"
DESTINATION = "public"


def main():
    if os.path.exists(DESTINATION): shutil.rmtree(DESTINATION)
    copy_files("static", DESTINATION)
    dir_content = list(map(lambda file: os.path.join(CONTENT, file), os.listdir(CONTENT)))
    generate_pages_recursive(dir_content, TEMPLATE, DESTINATION)


def copy_files(copypath, dst_path):
    if not os.path.exists(dst_path): os.mkdir(dst_path)
    diritems = os.listdir(copypath)
    if not diritems: raise Exception("Directory is empty")
    for item in diritems:
        current_path = os.path.join(copypath, item)
        if os.path.isfile(current_path):
            shutil.copy(current_path, dst_path)
        else: 
            new_dst_path = os.path.join(dst_path, item)
            os.mkdir(new_dst_path)
            copy_files(current_path, new_dst_path)
    

def extract_title(markdown):
    lines = markdown.split('\n')
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise Exception("No h1 header found")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}.")    
    with open(from_path) as f: markdown = f.read()
    title, html = extract_title(markdown), markdown_to_html_node(markdown).to_html()
    with open(template_path) as f: template_file = f.read()
    page = template_file.replace("{{ Title }}", title).replace("{{ Content }}", html)
    dir_path = os.path.dirname(dest_path)
    if not os.path.exists(dir_path): os.makedirs(dir_path)
    with open(dest_path, "w") as f: f.write(page)
    

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for path in dir_path_content:
        if os.path.isfile(path): 
            page_dest = dest_dir_path + '/' + path.split('/', 1)[1][:-3] + ".html"
            generate_page(path, template_path, page_dest)
        else:
            new_dir_path_content = list(map(lambda file: os.path.join(path, file),
                                   os.listdir(path)))
            print("content:", new_dir_path_content, "for:", path)
            generate_pages_recursive(new_dir_path_content, template_path, dest_dir_path)


if __name__ == "__main__":
    main()

