import pytest
import sqlite3
from annotations.db import Sentence

@pytest.fixture
def temp_db(tmp_path):
    db_file = tmp_path / "test_sentences.db"
    return str(db_file)

@pytest.fixture
def sentence(temp_db):
    return Sentence(temp_db)

def test_create_table(sentence):
    sentence.create_table()
    conn = sqlite3.connect(sentence.database_file)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='sentences'")
    assert cursor.fetchone() is not None
    conn.close()

def test_insert(sentence):
    sentence.create_table()
    sentence.insert("Original", "Revised", "Commentary")
    conn = sqlite3.connect(sentence.database_file)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sentences")
    result = cursor.fetchone()
    assert result == (1, "Original", "Revised", "Commentary")
    conn.close()

def test_insert_many(sentence):
    sentence.create_table()
    data = [
        {"original_sentence": "Original1", "revised_sentence": "Revised1", "commentary": "Commentary1"},
        {"original_sentence": "Original2", "revised_sentence": "Revised2", "commentary": "Commentary2"}
    ]
    sentence.insert_many(data)
    conn = sqlite3.connect(sentence.database_file)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM sentences")
    count = cursor.fetchone()[0]
    assert count == 2
    conn.close()

def test_fetch(sentence):
    sentence.create_table()
    sentence.insert("Original", "Revised", "Commentary")
    result = sentence.fetch(1)
    assert result[0] == 1  # The _fetch method returns only the id

def test_list(sentence):
    sentence.create_table()
    for i in range(15):
        sentence.insert(f"Original{i}", f"Revised{i}", f"Commentary{i}")
    
    page1 = sentence.list(1)
    assert len(page1) == 10
    assert page1[0][1] == "Original0"
    
    page2 = sentence.list(2)
    assert len(page2) == 5
    assert page2[0][1] == "Original10"

def test_empty_list(sentence):
    sentence.create_table()
    result = sentence.list()
    assert len(result) == 0

def test_list_ordering(sentence):
    sentence.create_table()
    for i in range(5):
        sentence.insert(f"Original{i}", f"Revised{i}", f"Commentary{i}")
    
    result = sentence.list()
    assert len(result) == 5
    for i, row in enumerate(result):
        assert row[1] == f"Original{i}"

