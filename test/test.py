import logging
from src.calculation import calc
from test.test_data import test_data


async def test(collection):

    for input_data, expected_result in test_data:
        actual_result = await calc(collection, input_data)
        try:
            assert actual_result == expected_result
            logging.info('=== SUCCESS !!! ===')
        except AssertionError:
            logging.info(expected_result)
            logging.info(actual_result)
