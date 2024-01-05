import chardet

def remove_empty_script(ass_file_path: str):
    
    with open(ass_file_path, "rb") as f:
        file_encoding = chardet.detect(f.read())
    
    with open(ass_file_path, "r", encoding=file_encoding.get("encoding")) as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            if "Dialogue:" in line:
                script = line.split(",")[-1].strip()
                if script == "":
                    lines.pop(index)

    with open(ass_file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

