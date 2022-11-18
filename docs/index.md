# index

jsl = json + s expression + xml

- json is a first value.
- Nodes can be expressed like xml or s-expressions.

## example

These codes are roughly equivalent.
Not fully compatible, but can convert structures to each other.

=== "jsl"

    ``` jsl
    @values(
        "text1"
        @values("text2")
        "text3"
    )
    ```

=== "xml"

    ``` xml
    <values>
        text1
        <values>text2</values>
        text3
    </values>
    ```

=== "SXML"

    ``` sxml
    (values
        (value "text1")
        (values (value "text2"))
        (value "text3")
    )
    ```

=== "jsonlogic"

    ```
    {"values": [
        "text1,
        {"values": "text2"},
        "text3"
    ]}
    ```

=== "JSONML"

    ```
    ["values",
        ["value", "text1"],
        ["values", ["value", "text2"]],
        ["value", "text3"]
    ]
    ```

## node chain

supports chaining of nodes, Supports node chaining and achieves beautiful node representation.
Binary tree representation will be cleaner.

=== "jsl(use chain)"

    ``` jsl
        1
        :@add(2)
        :@add(3)
    ```

=== "jsl(no use chain)"

    ``` jsl
        @add(
            @add(
                1
                2
            )
            3
        )
    ```

``` jsl
# 型にするか/キーバリューにするか
@node(
    name: aaa
    asdf: asd
)

# 構文を分ける
@node(
    elem_type = 1
    @shape(
        @dim(
            dim_value = 1
        )
    )
)
```

```
@type(
    name: str  # def
    age: int  # def
    height: int = 1  # alias
    weights: int = $weights  # alias/param
)
```


```
t1 <- @task(5)
t2 <- @task(5)
t3 <- @task(5)
t4 <- @task(5)

all = @task{"name": "tasks1"}(
    t1
    t2
    t3
):@task{"name": "tasks2"}(
    t4
    t5
    t6
)
```


## Create a simple DSL.

```
def add(a, b):
    return Value(a.value + b.value)

transformer = Transformer({"add": add})

tree = parser.parse("1:@add(2):@add(3)")
result = transformer.evalute(tree[0])
assert result == 6

```


```

statements = {
    "from": From,
    "join": Join,
    "where": Where,
    "groupby": GroupBy,
    "having": Having,
    "orderby": OrderBy,
    "select": Select
}

expressions = {
    "+": add,
    "-": minus
}

identifiers = {

}

functions = {

}

parser = Schema(
    name="myschema",
    nodes=statements,
    expressions=expressions,
    identifiers=identifiers,
    functions=functions,
    case_sensitive=True,
    allow_unkown_identifiers=True,
    allow_unkown_functions=True,
    allow_param=True,
    allow_type={None, int, str, float, bool, list, dict}
)

parser.parse("""
@from(u = users)
:@join(g = groups, @(u.id == g.id))
:@where(@(u.id == g.id))
""")

parser.parse("""
@from(u = users)
:@join(g = groups, @(id))
:@where(@(u.id == g.id))
""")

```