import typing as t

import pydantic
import requests
from pydantic import BaseModel, ValidationError, Field, validator, constr
from pydantic_i18n import I18nConfig, set_i18n
from schema import Schema, SchemaError, SchemaMissingKeyError, And
from requests import Request

set_i18n(I18nConfig(locale='zh'))

# 在软件开发过程中，数据验证和序列化是非常重要的一环。
# Python的pydantic库为开发者提供了强大的工具，可以轻松实现数据验证、模型定义和序列化操作。
# 特性
#     数据验证：可以定义数据模型并对数据进行验证。
#     数据序列化：可以将数据序列化为JSON等格式。
#     数据转换：可以将数据转换为特定类型。
#     默认值和选项：可以设置字段的默认值和选项。
#     异常处理：可以处理数据验证过程中的异常情况。


class View:
    class CreateDetailInstance:
        class DetailModel(BaseModel):
            pass

        def __init__(self, source: "View", request: Request):
            self.source = source
            self.request = request

        def _validate_request_data_for_cdi(self):
            Schema({
                "id": And(lambda x: x is not None)
            }).validate(self.request.data)

        def create_detail_instance(self):
            self._validate_request_data_for_cdi()

        def apply(self):
            try:
                self.create_detail_instance()
            except SchemaMissingKeyError as e:
                print(f"SchemaMissingKeyError: {e}")
            except SchemaError as e:
                print(f"SchemaError: {e}")
            except Exception as e:
                print(f"Exception: {e}")

    def create_detail_instance(self, request):
        return self.CreateDetailInstance(self, request).apply()


# [pydantic，一个超强的 Python 库！](https://segmentfault.com/a/1190000044856508)

def test():
    class DetailModel(BaseModel):
        id: int
        username: t.List[str]
        email: str
        password: t.Optional[constr(max_length=3, min_length=3)]

        class Config:
            # 注意，还有全局设置的办法，继承 ValidationError 修改 __init__ 即可
            error_msg_templates = {
                'value_error.missing': '缺少字段',
                'value_error.any_str.min_length': '字符串长度不能小于 {limit_value}',
                # 添加更多自定义错误信息...
            }

        @validator("password")
        def validate_password(cls, value):
            print(f"validate_password: {value}")
            return value

    detail = DetailModel(**dict(
        id="1",  # 如果可以被强转为数字，这里并不会报错
        username=["123"],
        # email="123456",
        password="11",
        creator="zsh",  # 不在模型中定义的字段会忽略，detail.dict() 也不会有这个键值对
    ))
    # DetailModel.validate(detail.dict())
    print(detail)
    print(detail.dict())
    print(detail.json())
    # print(detail.validate())


if __name__ == '__main__':
    test()
