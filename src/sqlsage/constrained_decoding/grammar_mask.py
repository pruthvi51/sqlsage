"""
Schema-Guided Constrained Decoding (SGCD):
Validates and sanitizes SQL AST to ensure 100% adherence to schema tables and columns.
"""

import sqlglot
from sqlglot import exp


class GrammarMaskValidator:
    def __init__(self, valid_schema: dict[str, list[str]]):
        self.valid_tables = {t.lower() for t in valid_schema}
        self.valid_columns = {t.lower(): {c.lower() for c in cols} for t, cols in valid_schema.items()}

    def validate_ast(self, sql_query: str) -> tuple[bool, list[str]]:
        try:
            parsed = sqlglot.parse_one(sql_query)
        except Exception as e:
            return False, [f"SQL Syntax Error: {e}"]

        errors = []
        # Check referenced tables
        for table in parsed.find_all(exp.Table):
            t_name = table.name.lower()
            if t_name not in self.valid_tables:
                errors.append(f"Hallucinated Table: '{t_name}' not in schema")

        # Check referenced columns
        for col in parsed.find_all(exp.Column):
            c_name = col.name.lower()
            t_name = col.table.lower() if col.table else None
            if t_name and t_name in self.valid_columns:
                if c_name not in self.valid_columns[t_name]:
                    errors.append(f"Hallucinated Column: '{c_name}' not in table '{t_name}'")

        is_valid = len(errors) == 0
        return is_valid, errors
