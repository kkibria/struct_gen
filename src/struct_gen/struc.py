from os import makedirs, mkdir
import sys
from pathlib import Path
from .translate import strip_tag, translate_doc, get_pairs
import tomllib

def songstrct(secno, struct):
    s_secno = {}
    for i in struct:
        n = 0
        if i in s_secno:
            n = s_secno[i]+1
        s_secno[i] = n
    return secno == s_secno

def parse_skelation_file(input_path):
    song = {}
    cursection = None
    secno = {}
    sectname = {}
    text = input_path.read_text(encoding="utf-8")
    for l in text.split("\n"):
        line = l.strip()
        if line:
            if line[0] == "[" and line[-1] == "]":
                section = line[1].lower()
                
                if section in sectname:
                    if sectname[section] != line[1:-1]:
                        raise SystemExit(f'"{sectname[section]}" and "{line[1:-1]}" starting with "{section}" not allowed')
                else:
                    sectname[section] = line[1:-1]

                n = 0
                if section in secno:
                    n = secno[section]+1
                secno[section] = n
                cursection = f'{section}{n+1}'
                # print(cursection)
                continue

        if cursection:
            if cursection not in song:
                song[cursection] = []
            song[cursection].append(line)

    for i in song:
        lines = song[i]
        # Remove leading empty strings
        while lines and not lines[0]:
            lines.pop(0)
        # Remove trailing empty strings
        while lines and not lines[-1]:
            lines.pop()
    return song,secno,sectname

def get_content(song, secno, sectname, song_pat):
    expanded = []
    for pat in song_pat:
        if songstrct(secno, pat):
            s_secno = {}
            for i in song_pat[pat]:
                n = 0
                if i in s_secno:
                    n = s_secno[i]+1
                s_secno[i] = min(n, secno[i]-1)

                cursection = sectname[i]
                # if secno[i] > 0:
                #     cursection += f' {n+1}'
                expanded.append(f'[{cursection}]')
                expanded.append("")
                # print(secno[i])
                key = f'{i}{n+1}'
                for sl in song[key]:
                    expanded.append(f'{sl}')
                expanded.append("")
                    
    content = "\n".join(expanded)
    return content


def gen_struct(input_path):
    if not input_path.exists():
        raise SystemExit(f"Input file not found: {input_path}")
 
    SKEL = "skeleton"
    skel = input_path.parent
    if skel.name != SKEL:
        raise SystemExit('The input file must be in a "skeleton" directory')
    
    root = skel.parent
    
    config = root / "struct.toml"
    with open(config, "rb") as f:
        config_data = tomllib.load(f)

    song_pat = config_data['song_pat']
    xlate = config_data['translate']
    tag = config_data['tag']

    song, secno, sectname = parse_skelation_file(input_path)
    content = get_content(song, secno, sectname, song_pat)

    for pairname in xlate:
        # Cant override source
        if pairname == SKEL:
            continue
        pairs = get_pairs(xlate[pairname])
        # print(pairs)

        folder = root / pairname
        makedirs (folder, exist_ok=True)
        outpath = folder / input_path.name

        text = content
        if pairname in tag:
            if not tag[pairname]:
                text = strip_tag(content)
        translate_doc(pairs, text, outpath, "forward")

def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python translate.py <input_file>")

    input_path = Path(sys.argv[1])
    gen_struct(input_path)

if __name__ == "__main__":
    main()
