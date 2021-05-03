from ..common_exceptions import DebugException

FRAG_KEY_CHARS = (
    "abcdefghijklmnopqrstuvwxyz"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "0123456789"
    "_"
)

# TODO: UNIT TEST THIS PLEASE (some at the bottom, not unittest code though)

# TODO: BEFORE PRODUCTION UNIT TEST FOR SECURITY

# TODO: Add frag_where and other abstraction helpers

# Might need to remove nested iteratables due to security situation but useful for VALUES

# Note that SQL evaluates IN ((3)) to IN (3), so IN ((3, 2)) doesn't seem to work


def safe_sql_value(value):
    """Checks if a value is safe to be passed to mysql connector.

    Params:
        value: The value to check

    Returns:
        True if safe, False if not
    """
    return (
        isinstance(value, (str, int, float))
        or value is None or value is True or value is False
    )


def frag_insert_into(table_name, values):
    """Generates a full insert_into.

    DO NOT pass dictionaries directly to values, always generate the dictionary
        right at the frag_insert_into or you risk injections!

    Returns:
        frag return value
    """
    if len(values) == 0:
        raise DebugException("Expected at least 1 value.")

    column_order = [col for col in values[0]]

    for value in values:
        if len(column_order) != len(value):
            raise DebugException("Expected all values to have the same number of columns.")

    return frag(
        "INSERT INTO " + table_name,
        frag(
            "(",
            ','.join(column_order),
            ")"
        ),
        frag(
            "VALUES",
            _frag_values([
                tuple(value[col] for col in column_order)
                for value in values
            ])
        )
    )


def frag_insert_ignore(table_name, row):
    """Generates a full INSERT INTO with a discard on duplicates.

    DO NOT pass dictionaries directly to values, always generate the dictionary
        right at the frag_insert_ignore or you risk injections!

    Params:
        table_name: The table name to insert into
        row: A dictionary definining the format of the insert

    Returns:
        frag return value
    """
    if not isinstance(row, dict):
        raise DebugException("Row should be a dict")

    columns = [col for col in row]
    values = [row[col] for col in columns]

    if len(values) == 0:
        raise DebugException("Row must be significant")

    return frag(
        "INSERT INTO",
        table_name,
        frag(
            "(",
            ','.join(columns),
            ")"
        ),
        frag(
            "SELECT",
            (','.join(('%s' for _ in values)), values)
        ),
        frag(
            "ON DUPLICATE KEY UPDATE " + columns[0] + "=" + columns[0]
        )
    )


def frag_insert_single_where(table_name, row, where_frag):
    """Generates a full insert_into with a WHERE clause.

    DO NOT pass dictionaries directly to values, always generate the dictionary
        right at the frag_insert_single_where or you risk injections!

    Params:
        table_name: The table name to insert into
        row: A dictionary definining the format of the insert
        where_frag: The result from a frag appended at the end (do not include 'WHERE')

    Returns:
        frag return value
    """
    if not isinstance(row, dict):
        raise DebugException("Row should be a dict")

    columns = [col for col in row]
    values = [row[col] for col in columns]

    if len(values) == 0:
        raise DebugException("Row must be significant")

    return frag(
        "INSERT INTO",
        table_name,
        frag(
            "(",
            ','.join(columns),
            ")"
        ),
        frag(
            "SELECT",
            (','.join(('%s' for _ in values)), values)
        ),
        frag(
            "WHERE",
            where_frag
        )
    )


def _frag_values(values):
    """Helper for the part after VALUES.

    Params:
        values: each of the values as tuples or lists
    """
    if not isinstance(values, (tuple, list)):
        raise DebugException("Expected values to be a tuple or list")
    if len(values) == 0:
        raise DebugException("Expected at least 1 value.")

    build_sqls = []
    build_values = []

    for value in values:
        if not isinstance(value, (tuple, list)):
            raise DebugException("All values should be tuples or lists.")
        if len(value) == 0:
            raise DebugException("All values should have some col values in them.")

        for v in value:
            if not safe_sql_value(v):
                raise DebugException("One of the values is not safe")

        build_sqls += ['(' + ','.join(['%s' for v in value]) + ')']
        build_values += value

    if len(build_values) == 0:
        raise DebugException("Expected at least 1 value.")
    if len(values) * len(values[0]) != len(build_values):
        raise DebugException("Expected each value to be the exact same size.")

    return ','.join(build_sqls), build_values


def frag(*args, **kwargs):
    """Computes a fragment of SQL and values.

    Each argument passed into it is evaluated and then concatenated into a
    massive SQL query, except for the last one, which defines the (optional)
    values.

    Note that list types are expanded to comma separated, not space separated.
    Parentheses are required to be provided by frag() to prevent injections.
        (Example, a developer checks that only 5 things have been added to an array,
        but that array could be nested. That's why flattening of arrays in %s notation is
        not used.)

    Namespaces for keys are maintained only within the individual frag().
    SQL injection handling is still performed by mysql_connector.

    Params:
        *args: A list of strings or tuples of (string sql, iterable values) and
            None, which is ignored
        **kwargs: Key values to be subbed in at :key
            Keys should only contain charactesr in FRAG_KEY_CHARS and must be used once.
            Values should be in
                float, int, string, None, False, True or list/tuple of these types

    Raises:
        A bunch of DebugExceptions

    Returns:
        A string (the SQL) and a tuple of the values to be substituted in.
    """
    result_sqls = []
    result_values = []

    for arg in args:
        if isinstance(arg, str):
            build_sql = ""
            temp_symbol = None

            for c in arg:
                if temp_symbol is not None:
                    # In symbol evaluation
                    if c in FRAG_KEY_CHARS:
                        temp_symbol += c
                    else:
                        if c == ":":
                            raise DebugException("Can't start a kv after ending one")
                        build_sql += run_symbol(temp_symbol, kwargs, result_values)
                        build_sql += c
                        temp_symbol = None
                elif c == ":":
                    temp_symbol = ""
                else:
                    build_sql += c
            if temp_symbol is not None:
                build_sql += run_symbol(temp_symbol, kwargs, result_values)
            result_sqls += [build_sql]

        elif isinstance(arg, (tuple, list)):
            if len(arg) != 2:
                raise DebugException("tuple/lists should be of size 2")
            if not isinstance(arg[0], str):
                raise DebugException("first value should be a string")
            result_sqls += [arg[0]]
            result_values += arg[1]
        elif arg is None:
            pass
        else:
            raise DebugException("invalid argument type in *args")

    if len(kwargs) != 0:
        raise DebugException("Kwargs not exhausted: " + ', '.join(k for k in kwargs))

    return ' '.join(result_sqls), result_values


def run_symbol(symbol, source_keys, result_values):
    """Evaluates what to do with a single symbol.

    Params:
        symbol: The symbol, string
        source_keys: Dictionary to look up keys in (automatically removes the key when used)
        result_values: Outputs flattened values to here (list)

    Returns:
        The %s-notation SQL
    """

    if symbol == "":
        raise DebugException("Unfinished symbol")

    if not isinstance(symbol, str):
        raise DebugException("not isinstance(symbol, str)")

    if symbol not in source_keys:
        raise DebugException(
            "Missing key (or already used) " + symbol
        )

    values_to_add, built_sql = build_values(source_keys[symbol])

    if len(values_to_add) == 0 or not isinstance(values_to_add, list):
        # important to stop SQL injections
        raise DebugException("Empty values or other error")

    result_values += values_to_add

    del source_keys[symbol]

    return built_sql


def build_values(value):
    """Builds the values.

    Takes nested iterables (or just a plain value), verifies it can be passed
        to SQL, and then flattens it into a single array of variables and builds
        the %s syntax.

    Params:
        value: The value(s) to build %s strings for

    Returns:
        flattened values, built sql
    """
    if safe_sql_value(value):
        return [value], "%s"
    elif isinstance(value, (tuple, list)):
        build_sqls = []
        values = []
        for v in value:
            temp_values, built_sql = build_values(v)
            values += temp_values
            build_sqls += [built_sql]
        return values, "(" + ','.join(build_sqls) + ")"
    else:
        raise DebugException("Not recognizable value in frag key expansion")
