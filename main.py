import argparse
import os

from readers.single_tb_reader import read_single_tb_excel_dynamic
from readers.monthly_tb_reader import read_monthly_tb_excel_dynamic
from readers.gl_reader import read_gl_excel_dynamic

from validators.trial_balance_validator import validate_trial_balance
from validators.general_ledger_validator import validate_gl
from report import generate_html_report

def main():
    parser = argparse.ArgumentParser(description="Financial Validation CLI")
    parser.add_argument("--single_tb", nargs="*", default=[], help="Paths to single TB Excel files")
    parser.add_argument("--monthly_tb", nargs="*", default=[], help="Paths to monthly TB Excel files")
    parser.add_argument("--gl", nargs="*", default=[], help="Paths to General Ledger Excel files")
    parser.add_argument("--out", default="validation_report.html", help="Output HTML report")

    args = parser.parse_args()
    results = {}

    # Single TB
    for path in args.single_tb:
        fname = os.path.basename(path)
        errors, warnings = [], []
        try:
            df_tb = read_single_tb_excel_dynamic(path)
            e, w = validate_trial_balance(df_tb)
            errors.extend(e)
            warnings.extend(w)
        except Exception as ex:
            errors.append(str(ex))
        results[fname] = {"errors": errors, "warnings": warnings}

    # Monthly TB
    for path in args.monthly_tb:
        fname = os.path.basename(path)
        errors, warnings = [], []
        try:
            df_monthly = read_monthly_tb_excel_dynamic(path)
            for month_val, group_df in df_monthly.groupby("Month"):
                e, w = validate_trial_balance(group_df)
                errors.extend(e)
                warnings.extend(w)
        except Exception as ex:
            errors.append(str(ex))
        results[fname] = {"errors": errors, "warnings": warnings}

    # GL
    for path in args.gl:
        fname = os.path.basename(path)
        errors, warnings = [], []
        try:
            df_gl, parse_info = read_gl_excel_dynamic(path)
            e, w = validate_gl(df_gl, parse_info=parse_info)
            errors.extend(e)
            warnings.extend(w)
        except Exception as ex:
            errors.append(str(ex))
        results[fname] = {"errors": errors, "warnings": warnings}

    # Generate HTML report
    html = generate_html_report(results)
    with open(args.out, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Validation complete. See '{args.out}' for results.")

if __name__ == "__main__":
    main()
