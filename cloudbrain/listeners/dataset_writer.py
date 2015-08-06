import csv
import json

class DatasetWriter(object):
  
  def __init__(self, headers, file_path='training_set.csv'):
    self.file_path = file_path
    self.headers = headers
    self.csv_writer = None
    self.file = None
    
  def open(self):
    self.file = open(self.file_path, 'wb')
    self.csv_writer = csv.writer(self.file)
    self.csv_writer.writerow(self.headers)
    

  def write(self, ch, method, properties, body):
    buffer_content = json.loads(body)
    for record in buffer_content:
      self.csv_writer.writerow([record[column_name] for column_name in self.headers])
    
  def close(self):
    self.file.close()