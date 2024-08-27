from glob import glob
import pandas as pd
import re

def join_eol_hyphen(text):
    """Joins all lines that are ended by a a end-of-line hyphen in the given text.

    This removes the hyphen (-) and joins the word broken by the eol.
    """
    text = re.sub(r'-\n', '', text)
    return text

def join_until_final_period(text):
    """Joins all lines until a final period is found.
    """
    lines = text.split('\n')
    acc = []
    current_line = ""
    for n, line in enumerate(lines):
        line = line.strip()
        if not line.endswith('.'):
            current_line += " " + line
        else:
            current_line += line
            acc.append(current_line)
            current_line = ""
    return '\n'.join(acc)



def main():
    txt_files = glob("extractions/*txt")
    df = pd.DataFrame({
        "file": txt_files,
        "text": [open(f).read() for f in txt_files]
    })
    print("Applying cleanup.")
    df["text"] = df["text"].apply(join_eol_hyphen)
    df["text"] = df["text"].apply(join_until_final_period)
    df["sentences"] = df['text'].str.split("\n")
    df.to_csv("clean_data.csv")


if __name__ == "__main__":
    main()
