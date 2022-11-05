def get_sql_spec_matrix():
    from xml_json.compilers.sql import common, postgresql
    from xml_json.compilers.sql.common import unsupported
    from collections import defaultdict

    types_matrix = defaultdict(dict)  # type: ignore
    operators_matrix = defaultdict(dict)  # type: ignore
    identifiers_matrix = defaultdict(dict)  # type: ignore

    def update_matrix(matrix, name, items):
        for k, v in items:
            matrix[k][name] = v is not unsupported

    update_matrix(types_matrix, "common", common.types.items())
    update_matrix(types_matrix, "postgresql", postgresql.types.items())

    update_matrix(operators_matrix, "common", common.operators.items())
    update_matrix(operators_matrix, "postgresql", postgresql.operators.items())

    update_matrix(identifiers_matrix, "common", common.identifiers.items())
    update_matrix(identifiers_matrix, "postgresql", postgresql.identifiers.items())

    return {
        "types": types_matrix,
        "operators": operators_matrix,
        "identifiers": identifiers_matrix,
    }
