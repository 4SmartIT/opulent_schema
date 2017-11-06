import unittest

import sqlalchemy
import sqlalchemy.dialects
import sqlalchemy.dialects.postgresql
from sqlalchemy.ext.declarative import declarative_base
from opulent_schema import schemalchemy, InLineField


Base = declarative_base()


class TestTableOrm(Base):
    __tablename__ = 'test_table'

    integer = sqlalchemy.Column(sqlalchemy.INTEGER, primary_key=True)
    uuid = sqlalchemy.Column(sqlalchemy.dialects.postgresql.UUID)
    timestamp = sqlalchemy.Column(sqlalchemy.TIMESTAMP)
    json = sqlalchemy.Column(sqlalchemy.dialects.postgresql.json.JSON)
    boolean = sqlalchemy.Column(sqlalchemy.BOOLEAN, nullable=False)
    time = sqlalchemy.Column(sqlalchemy.TIME, nullable=False)
    numeric = sqlalchemy.Column(sqlalchemy.Numeric(20, 6), nullable=False)
    date = sqlalchemy.Column(sqlalchemy.DATE, nullable=False)
    varchar = sqlalchemy.Column(sqlalchemy.VARCHAR(), nullable=False)
    varchar_len = sqlalchemy.Column(sqlalchemy.VARCHAR(67), nullable=False)


metadata = sqlalchemy.MetaData()

TestTable = sqlalchemy.Table(
    'test_table', sqlalchemy.MetaData(),
    sqlalchemy.Column('integer', sqlalchemy.INTEGER, primary_key=True),
    sqlalchemy.Column('uuid', sqlalchemy.dialects.postgresql.UUID),
    sqlalchemy.Column('timestamp', sqlalchemy.TIMESTAMP),
    sqlalchemy.Column('json', sqlalchemy.dialects.postgresql.json.JSON),
    sqlalchemy.Column('boolean', sqlalchemy.BOOLEAN, nullable=False),
    sqlalchemy.Column('time', sqlalchemy.TIME, nullable=False),
    sqlalchemy.Column('numeric', sqlalchemy.Numeric(20, 6), nullable=False),
    sqlalchemy.Column('date', sqlalchemy.DATE, nullable=False),
    sqlalchemy.Column('varchar', sqlalchemy.VARCHAR(), nullable=False),
    sqlalchemy.Column('varchar_len', sqlalchemy.VARCHAR(67), nullable=False),
)


class SetListComparator:
    def __init__(self, iterable):
        self._set = set(iterable)

    def __eq__(self, other):
        try:
            set_other = set(other)
        except TypeError:
            return False
        return self._set == set_other

    def __repr__(self):
        return repr(self._set)

    __str__ = __repr__


class Test(unittest.TestCase):
    def test(self):
        self.maxDiff=None
        in_schema = {
            'type': 'object',
            'properties': {
                schemalchemy.Required('abc'): {'type': 'integer'},
                schemalchemy.Optional('def'): {'type': 'integer'},
                'ghi': {'type': 'integer'},
                'string_list': {
                    'type': 'array',
                    'items': {'type': 'string'}
                },
                'object_list': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            schemalchemy.Required('1abc'): {'type': 'integer'},
                            schemalchemy.Optional('1def'): {'type': 'integer'},
                            '1ghi': {'type': 'integer'},
                        },
                    }
                },
                'mixed_list': {
                    'type': 'array',
                    'items': [
                        {
                            'type': 'object',
                            'properties': {
                                schemalchemy.Required('2abc'): {'type': 'integer'},
                                schemalchemy.Optional('2def'): {'type': 'integer'},
                                '2ghi': {'type': 'integer'},
                            },
                        },
                        {
                            'type': 'object',
                            'properties': {
                                schemalchemy.Required('3abc'): {'type': 'integer'},
                                schemalchemy.Optional('3def'): {'type': 'integer'},
                                '3ghi': {'type': 'integer'},
                            },
                        },
                        {
                            'type': 'string',
                        },
                    ]
                },
                'ored_property': {
                    'anyOf': [
                        {
                            'type': 'object',
                            'properties': {
                                schemalchemy.Required('4abc'): {'type': 'integer'},
                                schemalchemy.Optional('4def'): {'type': 'integer'},
                                '4ghi': {'type': 'integer'},
                            }
                        },
                        {
                            'type': 'object',
                        },
                        {
                            'type': 'string',
                        },
                    ]
                },
                'complex_object': {
                    'type': 'object',
                    'properties': {
                        schemalchemy.Required('5abc'): {'type': 'integer'},
                        schemalchemy.Optional('5def'): {'type': 'integer'},
                        '5ghi': {'type': 'integer'},
                        '5jkl': {
                            'type': 'object',
                            'properties': {
                                schemalchemy.Required('6abc'): {'type': 'integer'},
                                schemalchemy.Optional('6def'): {'type': 'integer'},
                                '6ghi': {'type': 'integer'},
                            }
                        },
                        '5mno': {
                            'allOf': [
                                {
                                    'type': 'object',
                                    'properties': {
                                        schemalchemy.Required('7abc'): {'type': 'integer'},
                                        schemalchemy.Optional('7def'): {'type': 'integer'},
                                        '7ghi': {'type': 'integer'},
                                    }
                                },
                                {
                                    'type': 'object',
                                    'properties': {
                                        schemalchemy.Required('8abc'): {'type': 'integer'},
                                        schemalchemy.Optional('8def'): {'type': 'integer'},
                                        '8ghi': {'type': 'integer'},
                                    }
                                },
                                {'type': 'integer'}
                            ]
                        },
                        '5pqr': {
                            'oneOf': [
                                {
                                    'type': 'object',
                                    'properties': {
                                        schemalchemy.Required('9abc'): {'type': 'integer'},
                                        schemalchemy.Optional('9def'): {'type': 'integer'},
                                        '9ghi': {'type': 'integer'},
                                    }
                                },
                                {
                                    'type': 'object',
                                    'properties': {
                                        schemalchemy.Required('10abc'): {'type': 'integer'},
                                        schemalchemy.Optional('10def'): {'type': 'integer'},
                                        '10ghi': {'type': 'integer'},
                                    }
                                },
                                {'type': 'integer'}
                            ]
                        },
                    }
                }
            },
        }
        schemalchemy.calculate_reqs(in_schema)
        self.assertEqual(
            in_schema,
            {
                'type': 'object',
                'required': SetListComparator(['abc', 'ghi', 'string_list', 'object_list', 'mixed_list',
                                               'ored_property', 'complex_object']),
                'properties': {
                    'abc': {'type': 'integer'},
                    'def': {'type': 'integer'},
                    'ghi': {'type': 'integer'},
                    'string_list': {
                        'type': 'array',
                        'items': {'type': 'string'}
                    },
                    'object_list': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                '1abc': {'type': 'integer'},
                                '1def': {'type': 'integer'},
                                '1ghi': {'type': 'integer'},
                            },
                            'required': SetListComparator(['1abc', '1ghi']),
                        }
                    },
                    'mixed_list': {
                        'type': 'array',
                        'items': [
                            {
                                'type': 'object',
                                'properties': {
                                    '2abc': {'type': 'integer'},
                                    '2def': {'type': 'integer'},
                                    '2ghi': {'type': 'integer'},
                                },
                                'required': SetListComparator(['2abc', '2ghi']),
                            },
                            {
                                'type': 'object',
                                'properties': {
                                    '3abc': {'type': 'integer'},
                                    '3def': {'type': 'integer'},
                                    '3ghi': {'type': 'integer'},
                                },
                                'required': SetListComparator(['3abc', '3ghi']),
                            },
                            {
                                'type': 'string',
                            },
                        ]
                    },
                    'ored_property': {
                        'anyOf': [
                            {
                                'type': 'object',
                                'properties': {
                                    '4abc': {'type': 'integer'},
                                    '4def': {'type': 'integer'},
                                    '4ghi': {'type': 'integer'},
                                },
                                'required': SetListComparator(['4abc', '4ghi']),
                            },
                            {
                                'type': 'object',
                            },
                            {
                                'type': 'string',
                            },
                        ]
                    },
                    'complex_object': {
                        'type': 'object',
                        'required': SetListComparator(['5abc', '5ghi', '5jkl', '5mno', '5pqr']),
                        'properties': {
                            '5abc': {'type': 'integer'},
                            '5def': {'type': 'integer'},
                            '5ghi': {'type': 'integer'},
                            '5jkl': {
                                'type': 'object',
                                'properties': {
                                    '6abc': {'type': 'integer'},
                                    '6def': {'type': 'integer'},
                                    '6ghi': {'type': 'integer'},
                                },
                                'required': SetListComparator(['6abc', '6ghi']),
                            },
                            '5mno': {
                                'allOf': [
                                    {
                                        'type': 'object',
                                        'properties': {
                                            '7abc': {'type': 'integer'},
                                            '7def': {'type': 'integer'},
                                            '7ghi': {'type': 'integer'},
                                        },
                                        'required': SetListComparator(['7abc', '7ghi']),
                                    },
                                    {
                                        'type': 'object',
                                        'properties': {
                                            '8abc': {'type': 'integer'},
                                            '8def': {'type': 'integer'},
                                            '8ghi': {'type': 'integer'},
                                        },
                                        'required': SetListComparator(['8abc', '8ghi']),
                                    },
                                    {'type': 'integer'}
                                ]
                            },
                            '5pqr': {
                                'oneOf': [
                                    {
                                        'type': 'object',
                                        'properties': {
                                            '9abc': {'type': 'integer'},
                                            '9def': {'type': 'integer'},
                                            '9ghi': {'type': 'integer'},
                                        },
                                        'required': SetListComparator(['9abc', '9ghi']),
                                    },
                                    {
                                        'type': 'object',
                                        'properties': {
                                            '10abc': {'type': 'integer'},
                                            '10def': {'type': 'integer'},
                                            '10ghi': {'type': 'integer'},
                                        },
                                        'required': SetListComparator(['10abc', '10ghi']),
                                    },
                                    {'type': 'integer'}
                                ]
                            },
                        }
                    }
                },
            }
        )

    def test_get_validator_integer(self):
        expected = {'type': 'integer'}
        val = schemalchemy.get_validator(TestTable.columns['integer'])
        self.assertEqual(expected, val)

        val = schemalchemy.get_validator(TestTableOrm.integer)
        self.assertEqual(expected, val)

    def test_get_validator_uuid(self):
        expected = {'type': ['null', 'string'],
                    'pattern': '^[0-9,a-f]{8}-[0-9,a-f]{4}-[0-9,a-f]{4}-[0-9,a-f]{4}-[0-9,a-f]{12}$'}
        val = schemalchemy.get_validator(TestTable.columns['uuid'])
        self.assertEqual(expected, val)

        val = schemalchemy.get_validator(TestTableOrm.uuid)
        self.assertEqual(expected, val)

    def test_get_validator_timestamp(self):
        expected = {'type': ['null', 'string', 'number']}
        val = schemalchemy.get_validator(TestTable.columns['timestamp'])
        self.assertIsInstance(val, InLineField)
        self.assertEqual(val.transformation, schemalchemy.any_time_stamp)
        self.assertEqual(expected, val)

        val = schemalchemy.get_validator(TestTableOrm.timestamp)
        self.assertIsInstance(val, InLineField)
        self.assertEqual(val.transformation, schemalchemy.any_time_stamp)
        self.assertEqual(expected, val)

    def test_get_validator_json(self):
        expected = {'anyOf': [{'type': 'null'}, {}]}
        val = schemalchemy.get_validator(TestTable.columns['json'])
        self.assertEqual(expected, val)

        val = schemalchemy.get_validator(TestTableOrm.json)
        self.assertEqual(expected, val)

    def test_get_validator_bool(self):
        expected = {'type': 'boolean'}
        val = schemalchemy.get_validator(TestTable.columns['boolean'])
        self.assertEqual(expected, val)

        val = schemalchemy.get_validator(TestTableOrm.boolean)
        self.assertEqual(expected, val)

    def test_get_validator_time(self):
        expected = {'type': 'string',
                    'pattern': '^[0-2]?\\d:[0-5]\\d:[0-5]\\d(.\\d+)?$'}
        val = schemalchemy.get_validator(TestTable.columns['time'])
        self.assertEqual(expected, val)

        val = schemalchemy.get_validator(TestTableOrm.time)
        self.assertEqual(expected, val)

    def test_get_validator_numeric(self):
        expected = {'type': 'number'}
        val = schemalchemy.get_validator(TestTable.columns['numeric'])
        self.assertIsInstance(val, InLineField)
        self.assertEqual(val.transformation, schemalchemy.any_decimal)
        self.assertEqual(expected, val)

        val = schemalchemy.get_validator(TestTableOrm.numeric)
        self.assertIsInstance(val, InLineField)
        self.assertEqual(val.transformation, schemalchemy.any_decimal)
        self.assertEqual(expected, val)

    def test_get_validator_date(self):
        expected = {'type': ['string', 'number']}
        val = schemalchemy.get_validator(TestTable.columns['date'])
        self.assertIsInstance(val, InLineField)
        self.assertEqual(val.transformation, schemalchemy.any_date)
        self.assertEqual(expected, val)

        val = schemalchemy.get_validator(TestTableOrm.date)
        self.assertIsInstance(val, InLineField)
        self.assertEqual(val.transformation, schemalchemy.any_date)
        self.assertEqual(expected, val)

    def test_get_validator_varchar(self):
        expected = {'type': 'string'}
        val = schemalchemy.get_validator(TestTable.columns['varchar'])
        self.assertEqual(expected, val)

        val = schemalchemy.get_validator(TestTableOrm.varchar)
        self.assertEqual(expected, val)

    def test_get_validator_varchar_len(self):
        expected = {'type': 'string', 'maxLength': 67}
        val = schemalchemy.get_validator(TestTable.columns['varchar_len'])
        self.assertEqual(expected, val)

        val = schemalchemy.get_validator(TestTableOrm.varchar_len)
        self.assertEqual(expected, val)

    def test_get_validator_bool_properties(self):
        expected = {'type': 'boolean', 'title': 'title', 'examples': [True, False]}
        val = schemalchemy.get_validator(schemalchemy.RequiredP(TestTable.columns['boolean'], title='title',
                                                                examples=[True, False]))
        self.assertEqual(expected, val)

        val = schemalchemy.get_validator(schemalchemy.RequiredP(TestTableOrm.boolean, title='title',
                                                                examples=[True, False]))
        self.assertEqual(expected, val)

    def test_get_validator_bool_properties_nullable(self):
        expected = {'type': ['null', 'boolean'], 'title': 'title', 'examples': [True, False]}
        val = schemalchemy.get_validator(schemalchemy.RequiredP(TestTable.columns['boolean'], title='title',
                                                                examples=[True, False], nullable=True))
        self.assertEqual(expected, val)

        val = schemalchemy.get_validator(schemalchemy.RequiredP(TestTableOrm.boolean, title='title',
                                                                examples=[True, False], nullable=True))
        self.assertEqual(expected, val)

    def test_get_validator_bool_properties_not_nullable(self):
        expected = {'type': 'boolean', 'title': 'title', 'examples': [True, False]}
        val = schemalchemy.get_validator(schemalchemy.RequiredP(TestTable.columns['boolean'], title='title',
                                                                examples=[True, False], nullable=False))
        self.assertEqual(expected, val)

        val = schemalchemy.get_validator(schemalchemy.RequiredP(TestTableOrm.boolean, title='title',
                                                                examples=[True, False], nullable=False))
        self.assertEqual(expected, val)

    def test_get_validator_json_properties(self):
        expected = {'anyOf': [{'type': 'null'}, {}], 'title': 'title', 'examples': [True, False]}
        val = schemalchemy.get_validator(schemalchemy.RequiredP(TestTable.columns['json'], title='title',
                                                                examples=[True, False]))
        self.assertEqual(expected, val)

        val = schemalchemy.get_validator(schemalchemy.RequiredP(TestTableOrm.json, title='title',
                                                                examples=[True, False]))
        self.assertEqual(expected, val)

    def test_get_validator_json_properties_nullable(self):
        expected = {'anyOf': [{'type': 'null'}, {}], 'title': 'title', 'examples': [True, False]}
        val = schemalchemy.get_validator(schemalchemy.RequiredP(TestTable.columns['json'], title='title',
                                                                examples=[True, False], nullable=True))
        self.assertEqual(expected, val)

        val = schemalchemy.get_validator(schemalchemy.RequiredP(TestTableOrm.json, title='title',
                                                                examples=[True, False], nullable=True))
        self.assertEqual(expected, val)

    def test_get_validator_json_properties_notnullable(self):
        expected = {'title': 'title', 'examples': [True, False]}
        val = schemalchemy.get_validator(schemalchemy.RequiredP(TestTable.columns['json'], title='title',
                                                                examples=[True, False], nullable=False))
        self.assertEqual(expected, val)

        val = schemalchemy.get_validator(schemalchemy.RequiredP(TestTableOrm.json, title='title',
                                                                examples=[True, False], nullable=False))
        self.assertEqual(expected, val)

    def test_make_contract_orm(self):
        self.maxDiff = None
        expected = {
            'title': 'hey ho!',
            'type': 'object',
            'properties': {
                'integer': {'type': 'integer'},
                'uuid': {'type': ['null', 'string'],
                         'pattern': '^[0-9,a-f]{8}-[0-9,a-f]{4}-[0-9,a-f]{4}-[0-9,a-f]{4}-[0-9,a-f]{12}$',
                         'title': 'nah',
                         },
                'timestamp': {'type': ['string', 'number'], 'title': 'meh'},
                'json': {'anyOf': [{'type': 'null'}, {}]},
                'boolean': {'type': ['null', 'boolean'], 'title': 'yay'},
                'time': {'type': 'string',
                         'pattern': '^[0-2]?\\d:[0-5]\\d:[0-5]\\d(.\\d+)?$',
                         'title': 'hey'
                         },
                'numeric': {'type': 'number'},
                'date': {'type': ['string', 'number']},
                'varchar': {'type': 'string'},
                'varchar_len': {'type': 'string', 'maxLength': 67},
            },
            'required': SetListComparator([
                'integer',
                'json',
                'boolean',
                'time',
                'numeric',
                'date',
                'varchar',
                'varchar_len',
            ]),
        }
        res = schemalchemy.make_contract(
            TestTableOrm.integer,
            schemalchemy.OptionalP(TestTableOrm.uuid, title='nah', nullable=True),
            schemalchemy.OptionalP(TestTableOrm.timestamp, title='meh', nullable=False),
            TestTableOrm.json,
            schemalchemy.RequiredP(TestTableOrm.boolean, title='yay', nullable=True),
            schemalchemy.RequiredP(TestTableOrm.time, title='hey', nullable=False),
            TestTableOrm.numeric,
            TestTableOrm.date,
            TestTableOrm.varchar,
            TestTableOrm.varchar_len,
            title='hey ho!',
        )
        self.assertDictEqual(expected, res)

        res = schemalchemy.make_contract(
            TestTable.columns['integer'],
            schemalchemy.OptionalP(TestTableOrm.uuid, title='nah', nullable=True),
            schemalchemy.OptionalP(TestTableOrm.timestamp, title='meh', nullable=False),
            TestTable.columns['json'],
            schemalchemy.RequiredP(TestTable.columns['boolean'], title='yay', nullable=True),
            schemalchemy.RequiredP(TestTable.columns['time'], title='hey', nullable=False),
            TestTable.columns['numeric'],
            TestTable.columns['date'],
            TestTable.columns['varchar'],
            TestTable.columns['varchar_len'],
            title='hey ho!',
        )
        self.assertDictEqual(expected, res)
