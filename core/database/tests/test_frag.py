from ..frag import (
    frag, build_values, _frag_values, frag_insert_into,
    frag_insert_single_where
)


def test_frag():
    def a(a, b):
        assert a == b

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

    a(
        _frag_values([
            (3, 5, '3'),
            (2, 7, 'a')
        ]),
        (
            "(%s,%s,%s),(%s,%s,%s)",
            [3, 5, '3', 2, 7, 'a']
        )
    )

    a(
        frag_insert_into("a", [
            {
                'a': 3,
                'b': 4
            },
            {
                'b': 6,
                'a': 6
            }
        ]),
        ('INSERT INTO a ( a,b ) VALUES (%s,%s),(%s,%s)', [3, 4, 6, 6])
    )

    assert (
        frag_insert_single_where(
            "testing_unique",
            {"v1": 1, "v2": 3345},
            frag(
                (
                    "(SELECT COUNT(*)"
                    " FROM testing_unique AS t2 WHERE t2.v1=:v1 AND t2.v2=:v2) = 0"
                ),
                v1=1,
                v2=3345
            )
        )
        ==
        (
            "INSERT INTO testing_unique ( v1,v2 ) SELECT %s,%s WHERE (SELECT COUNT(*)"
            " FROM testing_unique AS t2 WHERE t2.v1=%s AND t2.v2=%s) = 0",
            [1, 3345, 1, 3345]
        )
    )
