from itertools import chain
from random import choices
import pandas as pd
import click

from .db import Sentence

@click.command()
@click.option("--size", type=click.INT)
@click.option("--output", type=click.STRING)
def main(size, output, input):
    sentence = Sentence()
    sentences = []
    for i in range(1, 10):
        data = [i[1] for i in sentence.list(page=i)]
        sentences.extend(data)
    with open(output, 'w') as f:
        for sent in sentences:
            f.write(sent + "\n")
            


if __name__ == "__main__":
    main()

