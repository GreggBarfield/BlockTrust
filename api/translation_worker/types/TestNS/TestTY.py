from ...abstract_type import AbstractType


class TestTYType(AbstractType):

    NAMESPACE = "TestNS"
    TYPE = "TestTY"

    def block_key(self):
        insert = self.insert
        if insert['account'] >= 0:
            raise RuntimeError("Not allowed to TestTY")
        if 'key' in insert['fields']:
            return insert['fields']['key']
        return None

    def handle(self):
        insert = self.insert
        if 'emit' in insert['fields'] and 'emit_key' in insert['fields']:
            self.emit_block(insert['fields']['emit_key'], insert['fields']['emit'])
