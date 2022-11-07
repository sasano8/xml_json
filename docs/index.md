# index

jsl = json + s expression + xml

- json is a first value.
- Nodes can be expressed like xml or s-expressions.

## example

These codes are roughly equivalent.
Not fully compatible, but can convert structures to each other.

=== "jsl"

    <div class="termy">

    ``` jsl
    @values(
        "text1"
        @values("text2")
        "text3"
    )
    ```

    </div>

=== "xml"

    <div class="termy">

    ``` xml
    <values>
        text1
        <values>text2</values>
        text3
    </values>
    ```

    </div>

=== "SXML"

    <div class="termy">

    ``` sxml
    (values
        (value "text1")
        (values (value "text2"))
        (value "text3")
    )
    ```

    </div>

## node chain

supports chaining of nodes, Supports node chaining and achieves beautiful node representation.
Binary tree representation will be cleaner.

=== "jsl(use chain)"

    <div class="termy">

    ``` jsl
        1
        :@add(2)
        :@add(3)
    ```

    </div>

=== "jsl(no use chain)"

    <div class="termy">

    ``` jsl
        @add(
            @add(
                1
                2
            )
            3
        )
    ```

    </div>
