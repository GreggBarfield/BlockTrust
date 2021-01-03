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
    if (
        isinstance(value, (str, int, float))
        or value is None or value is True or value is False
    ):
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


if __name__ == "__main__":
    def a(a, b):
        if a != b:
            print(a)
            print(b)
            print("!=")

    a(
        build_values((4, 3, 2, (3, 2))),
        (
            [4, 3, 2, 3, 2],
            "(%s,%s,%s,(%s,%s))"
        )
    )

    a(frag(":test", test=3), ("%s", [3]))
    a(frag(":test ", test=3), ("%s ", [3]))
    a(frag(" :test", test=3), (" %s", [3]))
    a(frag(":test :tT2", test=3, tT2=4), ("%s %s", [3, 4]))
    a(frag(":test :tT2", test=3, tT2=(5, 6)), ("%s (%s,%s)", [3, 5, 6]))
    a(
        frag("SELECT * FROM accounts WHERE id=:id", id=4),
        ("SELECT * FROM accounts WHERE id=%s", [4])
    )

    a(
        frag(
            "SELECT * FROM accounts",
            frag(
                "LEFT JOIN account_links ON account_links.account=accounts.id AND account_links.f=:f",
                f=5
            ),
            "WHERE accounts.id=:id OR accounts.abc IN :abcs",
            id=4,
            abcs=('a', 'b', 'c')
        ),
        (
            "SELECT * FROM accounts LEFT JOIN account_links ON account_links.account="
            "accounts.id AND account_links.f=%s WHERE accounts.id=%s OR accounts.abc IN (%s,%s,%s)",
            [5, 4, 'a', 'b', 'c']
        )
    )
