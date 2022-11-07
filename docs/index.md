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
