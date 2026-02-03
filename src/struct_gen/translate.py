import sys
from pathlib import Path


DICT_FILE = "dict.txt"
# MODE = "forward"   # change to "backward" if needed
MODE = "backrward"   # change to "backward" if needed

def load_dict(path):
    pairs = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            left, right = line.split("=", 1)
            pairs.append((left.strip(), right.strip()))
    return pairs

def unescape (text):
    if not text:
        text = " "
    return text.encode('utf-8').decode('unicode_escape')

def get_pairs(pattern:str):
    pairs = []
    for line in pattern.split('\n'):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        left, right = line.split("=", 1)
        pairs.append((unescape(left.strip()), unescape(right.strip())))
    return pairs

def translate_doc(pairs, text, output_path, mode):
    if mode == "backward":
        pairs = [(b, a) for a, b in pairs]

    # longest-first replacement
    repl = []
    for line in text.split("\n"):
        if line:
            if line[0] == "[" and line[-1] == "]":
                pass
            else:
                for src, dst in sorted(pairs, key=lambda x: len(x[0]), reverse=True):
                    line = line.replace(src, dst)
        repl.append(line)
    text = "\n".join(repl)

    # collapse multiple spaces into one
    clean = [" ".join(i.split()) for i in text.split("\n")]
    text = "\n".join(clean)

    output_path.write_text(text, encoding="utf-8")

def strip_tag(text):
    empty = True
    lines = []
    for line in text.split("\n"):
        if line:
            if line[0] == "[" and line[-1] == "]":
                continue
            empty = False
        else:
            if empty:
                continue
            empty = True

        lines.append(line)

    return "\n".join(lines)
        
def main():
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python translate.py <input_file>")

    input_path = Path(sys.argv[1])
    if not input_path.exists():
        raise SystemExit(f"Input file not found: {input_path}")

    # derive output filename
    output_path = input_path.with_name(
        f"{input_path.stem}.translated{input_path.suffix}"
    )

    pairs = load_dict(DICT_FILE)
    text = input_path.read_text(encoding="utf-8")

    translate_doc(pairs, text, output_path, MODE)

if __name__ == "__main__":
    main()
