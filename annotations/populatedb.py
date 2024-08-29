import click
import pandas as pd
from loguru import logger
from .db import Sentence


@click.command()
@click.option("--csvfile", type=click.STRING)
def main(csvfile):
    sent = Sentence()
    sent.create_table()
    logger.info("Loading data")
    df = pd.read_csv(csvfile)
    logger.info("Finished loading data")
    df['sentences'] = df['sentences'].apply(eval)
    sentences = [sent for sentences in df["sentences"] for sent in sentences]
    logger.info("Populating database")
    sent.insert_many([{
        "original_sentence": i, 
        "revised_sentence": None, 
        "commentary": None} for i in sentences])
    logger.info("Finished populating database")
