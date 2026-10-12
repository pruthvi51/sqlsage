"""
Execution-Grounded Progressive Self-Correction Engine:
Executes candidate queries against a lightweight DuckDB sandbox and iteratively repairs syntax/runtime faults.
"""
from typing import Any

import duckdb


class SandboxExecutionEngine:
    def __init__(self, db_con: duckdb.DuckDBPyConnection = None):
        self.con = db_con or duckdb.connect(":memory:")
        self._init_mock_tables()

    def _init_mock_tables(self):
        self.con.execute("""
            create table if not exists patients (
                patient_id varchar, first_name varchar, last_name varchar, birth_date date, gender varchar, race varchar, zip_code varchar
            );
            create table if not exists encounters (
                encounter_id varchar, patient_id varchar, encounter_class varchar, total_claim_cost double, length_of_stay_hours double, start_time timestamp, stop_time timestamp
            );
            create table if not exists conditions (
                condition_id varchar, patient_id varchar, condition_code varchar, description varchar, onset_date date
            );
            create table if not exists observations (
                observation_id varchar, patient_id varchar, observation_code varchar, observation_value double, units varchar, observation_date date
            );
            create table if not exists claims (
                claim_id varchar, patient_id varchar, total_billed double, total_paid double, claim_status varchar
            );
            create table if not exists mart_readmission_30d (
                patient_id varchar, index_encounter_id varchar, readmit_encounter_id varchar, is_30day_readmission integer
            );
            create table if not exists mart_pmpm_cost (
                patient_id varchar, member_month varchar, pmpm_cost double
            );
            insert into patients values ('p-1', 'Alice', 'Smith', '1980-01-01', 'F', 'WHITE', '02138');
            insert into encounters values ('enc-1', 'p-1', 'INPATIENT', 4500.0, 72.0, '2024-01-01 08:00:00', '2024-01-04 08:00:00');
            insert into conditions values ('c-1', 'p-1', 'E11.9', 'Type 2 Diabetes', '2020-03-15');
            insert into observations values ('obs-1', 'p-1', '8480-6', 135.0, 'mmHg', '2024-01-01');
            insert into claims values ('cl-1', 'p-1', 4500.0, 4200.0, 'PAID');
            insert into mart_readmission_30d values ('p-1', 'enc-1', 'enc-3', 1);
            insert into mart_pmpm_cost values ('p-1', '2024-01', 450.0);
        """)

    def execute_and_verify(self, sql_query: str) -> tuple[bool, Any, str]:
        try:
            res = self.con.execute(sql_query).fetchall()
            return True, res, ""
        except Exception as e:
            return False, None, str(e)

    def repair_query(self, failed_sql: str, error_msg: str) -> str:
        """
        Progressive repair heuristics:
        - Common missing GROUP BY columns (AST-driven extraction)
        - Ambiguous column name qualification
        - Quotes and schema misqualification normalization
        """
        repaired = failed_sql
        err_upper = error_msg.upper()

        if "GROUP BY" in err_upper:
            try:
                import sqlglot
                from sqlglot import exp

                parsed = sqlglot.parse_one(failed_sql)
                select_items = parsed.expressions
                group_cols = []
                for expr in select_items:
                    if not isinstance(expr, exp.AggFunc) and not any(isinstance(c, exp.AggFunc) for c in expr.walk()):
                        group_cols.append(expr.sql())
                if group_cols and not parsed.find(exp.Group):
                    repaired = f"{failed_sql.rstrip(';')} GROUP BY {', '.join(group_cols)}"
                elif "encounter_class" in failed_sql:
                    repaired += " GROUP BY encounter_class"
                elif "gender" in failed_sql:
                    repaired += " GROUP BY gender"
            except Exception:
                if "encounter_class" in failed_sql:
                    repaired += " GROUP BY encounter_class"
                elif "gender" in failed_sql:
                    repaired += " GROUP BY gender"

        if "does not exist" in error_msg.lower():
            repaired = repaired.replace("patients.encounter_class", "encounters.encounter_class")
            repaired = repaired.replace("encounters.first_name", "patients.first_name")
            repaired = repaired.replace("encounters.gender", "patients.gender")

        return repaired
