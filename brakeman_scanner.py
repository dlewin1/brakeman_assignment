from flask import Flask, request, jsonify
import git
import os
import json

api = Flask(__name__)

# Ruby source code scanner (POST)
@api.route('/scan', methods=['POST'])
def scan():

  # Define variables from params
  source_code_url = request.args.get('source_code_url')
  lang = request.args.get('lang')
  scanner_name = request.args.get('scanner_name')

  # Define location to temporarily store source code
  source_code_location = '/tmp/source_to_scan_temp'

  # Git clone from source_code_url
  git.Repo.clone_from(source_code_url, source_code_location)

  # Run brakeman against source code and return report in json format
  os.system(scanner_name + ' -o /tmp/report.json ' + source_code_location)

  response = jsonify(message="success")
  return response

# Return results of the ruby source code scan performed above (GET)
@api.route('/scan_report', methods=['GET'])

# Open and return the report generated from brakeman scan
def get_report():
  with open('/tmp/report.json') as report:
    open_report = json.load(report)

  return open_report


if __name__ == '__main__':
    api.run(debug=True, host="0.0.0.0", port=5000)