import fitz
import re
import sys

# open pdf & extract text
pdf = fitz.open(sys.argv[1])
text = "\n".join(page.get_text() for page in pdf)

# remove tabs
text = text.replace("\t", "")

# preserve capitalized words for character names
text = re.sub(r"\n(?=[A-Z][A-Z])", "\n\n\n", text)

# rejoin wrapped lines, but not after ALL-CAPS lines (character names, panels)
def rejoin(match):
    before = match.string[:match.start()].split("\n")[-1]
    if before == before.upper() and before.strip():
        return match.group(0) 
    return " "

text = re.sub(r"(?<![.!?:])\n(?=[a-z\"])", rejoin, text)
text = re.sub(r"(?<![.!?:])\n(?=[A-Z][a-z])", rejoin, text)

# collapse double spaces to single
text = re.sub(r"  +", " ", text)

# collapse 3+ newlines down to 2 (keeps intentional blank lines)
text = re.sub(r"\n{3,}", "\n\n", text)

# ensure PAGE headers are breaks
text = re.sub(r"(PAGE \d+)", r"\n---\n\n\1", text)

# write .txt file
output = sys.argv[1].replace(".pdf", "-clean.txt")
with open(output, "w") as f:
    f.write(text.strip() + "\n")

print(f"Done -> {output}")
