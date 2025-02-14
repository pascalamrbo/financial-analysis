from flask import Flask, request
import os

from readers.single_tb_reader import read_single_tb_excel_dynamic
from readers.monthly_tb_reader import read_monthly_tb_excel_dynamic
from readers.gl_reader import read_gl_excel_dynamic

from validators.trial_balance_validator import validate_trial_balance
from validators.gl_validator import validate_gl
from report import generate_html_report

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return """
    <html>
    <body>
    <h1>Financial Validation Web App</h1>
    <form method="POST" action="/upload" enctype="multipart/form-data">
      <h3>Upload Single TB Files (Excel):</h3>
      <input type="file" name="single_tb_files" multiple><br/><br/>
      <h3>Upload Monthly TB Files (Excel):</h3>
      <input type="file" name="monthly_tb_files" multiple><br/><br/>
      <h3>Upload General Ledger Files (Excel):</h3>
      <input type="file" name="gl_files" multiple><br/><br/>
      <input type="submit" value="Validate">
    </form>
    </body>
    </html>
    """

@app.route("/upload", methods=["POST"])
def upload():
    single_tb_files = request.files.getlist("single_tb_files")
    monthly_tb_files = request.files.getlist("monthly_tb_files")
    gl_files = request.files.getlist("gl_files")

    if not any([single_tb_files, monthly_tb_files, gl_files]):
        return "<h3>No files uploaded. Please go back and select a file.</h3>", 400

    results = {}

    for file_storage in single_tb_files:
        fname = file_storage.filename
        errors, warnings = [], []
        if fname:
            try:
                df_tb = read_single_tb_excel_dynamic(file_storage)
                e, w = validate_trial_balance(df_tb)
                errors.extend(e)
                warnings.extend(w)
            except Exception as ex:
                errors.append(str(ex))
            results[fname] = {"errors": errors, "warnings": warnings}

    for file_storage in monthly_tb_files:
        fname = file_storage.filename
        errors, warnings = [], []
        if fname:
            try:
                df_monthly = read_monthly_tb_excel_dynamic(file_storage)
                for month_val, group_df in df_monthly.groupby("Month"):
                    e, w = validate_trial_balance(group_df)
                    errors.extend(e)
                    warnings.extend(w)
            except Exception as ex:
                errors.append(str(ex))
            results[fname] = {"errors": errors, "warnings": warnings}

    for file_storage in gl_files:
        fname = file_storage.filename
        errors, warnings = [], []
        if fname:
            try:
                df_gl, parse_info = read_gl_excel_dynamic(file_storage)
                e, w = validate_gl(df_gl, parse_info=parse_info)
                errors.extend(e)
                warnings.extend(w)
            except Exception as ex:
                errors.append(str(ex))
            results[fname] = {"errors": errors, "warnings": warnings}

    report_html = generate_html_report(results)
    return report_html

if __name__ == "__main__":
    app.run(debug=True, port=5000)
