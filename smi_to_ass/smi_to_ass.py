from smi_to_ass.common import DEFAULT_FONT_NAME
import chardet
import os
import re
from bs4 import BeautifulSoup
import unicodedata
from glob import glob


SCRIPT_INFO = """
[Script Info]
; This is an Advanced SubStation Alpha v4+ script.
Title: Converted from SMI
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.601

[Aegisub Project Garbage]
...
"""

STYLES = f"""
[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,{DEFAULT_FONT_NAME},50,&H00FFFFFF,&H00B4FCFC,&H00000008,&H80000008,-1,0,0,0,100,100,0,0,1,2,3,2,10,10,10,1
"""

EVENTS = """
[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""



def smi_to_ass(smi_dir: str, save_dir: str, styles: list):
    """
    convert smi to ass
    """
    

    files = glob(f"{smi_dir}/*.smi")

    for file in files:
        scripts = []

        with open(file, "rb") as f:
            file_encoding = chardet.detect(f.read())
        
        with open(file, encoding=file_encoding.get("encoding")) as f:
            lines = f.read()
            first_index = lines.index("<SYNC")
            smi_content = lines[first_index:]

            
            
            for content in smi_content.split("\n"):
                pattern = re.compile(r"<SYNC Start=\d+>", re.DOTALL | re.IGNORECASE)
                sync_tag = pattern.findall(content)

                if len(sync_tag) == 0:
                    continue

                time = "".join(re.findall("\d", sync_tag[0]))

                script = content[content.find("<P Class="):]
                soup = BeautifulSoup(script, "html.parser")

                scripts.append({
                    "time": time,
                    "script": unicodedata.normalize("NFC", soup.get_text()),
                })

        ass_scripts = []
        ass_scripts.append(SCRIPT_INFO)
        ass_scripts.append(STYLES)

        if len(styles) > 0:
            for style in styles:
                ass_scripts.append(f"Style: {style},{DEFAULT_FONT_NAME},50,&H00FFFFFF,&H00B4FCFC,&H00000008,&H80000008,-1,0,0,0,100,100,0,0,1,2,3,2,10,10,10,1\n")

        ass_scripts.append(EVENTS)


        for index, script in enumerate(scripts):
            start_time = int(script.get("time")) / 1000
            
            if index + 1 < len(scripts):
                end_time = int(scripts[index + 1].get("time")) / 1000
            else:
                end_time = start_time + 100
            
            start_hour, remain = divmod(start_time, 3600)
            start_min, start_sec = divmod(remain, 60)

            end_hour, remain = divmod(end_time, 3600)
            end_min, end_sec = divmod(remain, 60)

            ass_scripts.append(f"Dialogue: 0,{int(start_hour):02}:{int(start_min):02}:{start_sec:05.2f},{int(end_hour):02}:{int(end_min):02}:{end_sec:05.2f},Default,,0,0,0,,{script.get('script')}\n")

        os.makedirs(save_dir, exist_ok=True)
        with open(f"{save_dir}/{os.path.splitext(os.path.basename(file))[-2]}.ass", "w", encoding="utf-8") as f:
            f.writelines(ass_scripts)


