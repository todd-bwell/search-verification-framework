import os
import json
import csv
from typing import List, Dict, Any
from pathlib import Path


# Initialize the converter with a JSON string.
class CsvWriter:
  def __init__(self, json_string: str, pss_envt: str) -> None:
    self._json_string = json_string
    self._parsed_data: Dict[str, Any] = {}
    self._pss_envt = pss_envt

  # Parse the JSON string and store the result.
  def _parse_json(self) -> None:
    try:
      self._parsed_data = json.loads(self._json_string)
    except json.JSONDecodeError as e:
      raise ValueError(f"Invalid JSON: {e}")

  def write_to_csv(self, output_path: str | Path = 'search_results.csv') -> None:
      if not self._parsed_data:
          self._parse_json()

      headers = [
          'pssEnv',
          'dateTime',
          'searchTerm',
          'inferredIntent',
          'rank',
          'content',
          'relevanceScore',
          'relevanceRationale'
      ]

      output_path = str(output_path)
      file_exists = os.path.isfile(output_path)

      with open(output_path, 'a', newline='', encoding='utf-8') as csvfile:
          writer = csv.DictWriter(csvfile, fieldnames=headers)
          if not file_exists:
              writer.writeheader()

          base_row = {
            'pssEnv': self._pss_envt,
            'dateTime': self._parsed_data.get('dateTime', ''),
            'searchTerm': self._parsed_data.get('searchTerm', ''),
            'inferredIntent': self._parsed_data.get('inferredIntent', '')
          }

          for result in self._parsed_data.get('searchResults', []):
              row = base_row.copy()
              row.update({
                  'rank': result.get('rank', ''),
                  'content': result.get('content', ''),
                  'relevanceScore': result.get('relevanceScore', ''),
                  'relevanceRationale': result.get('relevanceRationale', '')
              })
              writer.writerow(row)

  def convert(self, output_path: str | Path = 'search_results.csv') -> None:
    """
    Convenience method to parse JSON and write to CSV in one step.

    Args:
        output_path (str | Path): Path to the output CSV file
    """
    self._parse_json()
    self.write_to_csv(output_path)


# # Example usage
# if __name__ == "__main__":
#   json_string = '''{
#     "searchTerm": "Dr. Smith",
#     "inferredIntent": "Find a healthcare provider or medical practice",
#     "searchResults": [
#         {
#           "rank": 1,
#           "content": "Dr. John Smith",
#           "relevanceScore": 9,
#           "relevanceRationale": "Direct match to the search term with a full name. Highly likely to be the specific provider being sought."
#         },
#         {
#           "rank": 2,
#           "content": "Cardiac Care Center",
#           "relevanceScore": 6,
#           "relevanceRationale": "Tangentially related to the search, representing a medical practice but not a direct provider match."
#         }
#     ]
# }'''
#
#   converter = CsvWriter(json_string)
#   converter.convert()  # Writes to default 'search_results.csv'