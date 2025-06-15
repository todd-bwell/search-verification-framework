import tempfile
import os
import csv
import pytest
from search_verification.services.csv_writer import CsvWriter

def test_csv_writer_e2e():
    json_string = '''{
        "searchTerm": "Dr. Smith",
        "inferredIntent": "Find a healthcare provider",
        "searchResults": [
            {
              "rank": "1",
              "content": "Dr. John Smith",
              "relevanceScore": 9,
              "relevanceRationale": "Direct match"
            },
            {
              "rank": "2",
              "content": "Cardiac Care Center",
              "relevanceScore": 6,
              "relevanceRationale": "Tangentially related"
            }
        ]
    }'''

    with tempfile.TemporaryDirectory() as tmpdir:
        csv_path = os.path.join(tmpdir, "results.csv")
        pss_envt = "TEST"
        converter = CsvWriter(json_string, pss_envt=pss_envt)
        converter.convert(csv_path)

        assert os.path.exists(csv_path)

        with open(csv_path, newline='', encoding='utf-8') as f:
            rows = list(csv.DictReader(f))
            assert len(rows) == 2
            assert rows[0]['searchTerm'] == "Dr. Smith"
            assert rows[0]['inferredIntent'] == "Find a healthcare provider"
            assert rows[0]['content'] == "Dr. John Smith"
            assert rows[0]['relevanceScore'] == "9"
            assert rows[0]['relevanceRationale'] == "Direct match"
            assert rows[1]['content'] == "Cardiac Care Center"
            assert rows[1]['relevanceScore'] == "6"
            assert rows[1]['relevanceRationale'] == "Tangentially related"