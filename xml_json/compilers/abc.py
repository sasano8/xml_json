"""
main = @func.async{
}(
    @return(@(1 + 1))
)

await main()
"""

"""
1. 構文解析
2. パラム設定
3. リゾルバ設定
4. 意味解析（コンパイラ/インタプリタ: 実行可能な形式にする。解析不可な文脈は解析が保留される）
    未設定パラム判定
    リゾルバ設定
5. 実行（未設定パラム・リゾルバ次第で実行不可）
"""


class Undefined:
    def __str__(self):
        return "undefined"


undefined = Undefined()


from inspect import Parameter


class Param(Parameter):
    def __init__(self, name: str, *, default=..., annotation=object):
        super().__init__(
            name, Parameter.KEYWORD_ONLY, default=default, annotation=annotation
        )


class BaseCompiler:
    def __init__(self):
        self._executor = object()

    def __init_subclass__(cls, schema=None, sort=False):
        ...

    def prepare(self, __resolver, /, *args, **kwargs):
        ...

    def compile(self, __resolver, /, *args, **kwargs):
        ...

    def bind(self, *args, **kwargs):
        ...

    def resolver(self, resolver):
        ...

    def get_missing_args(self):
        ...

    def params(self):
        return {"a": undefined}

    def execute(self, *args, **kwargs):
        compiled = self.compile(*args, **kwargs)
        return compiled()
