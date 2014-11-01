"""schemas_test.py"""

import os
import glob

from standard.dictfuncs import generate_data_from_json
from standard.dictfuncs import ensure_schema_exception_is_raised

def test_schemas():
    """Test schemas"""

    paths = [
        os.path.dirname(__file__)+'/*_test.json'
    ]

    for path in paths:

        files = glob.glob(path)
        if not files:
            raise IOError('Nothing found in %s' % path)

        for filename in files:
            for test_description, schema_filename, instance, expected_errors \
                    in generate_data_from_json(filename):
                ensure_schema_exception_is_raised.description = test_description
                yield ensure_schema_exception_is_raised, schema_filename, \
                    instance, expected_errors
