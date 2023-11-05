from datetime import datetime as dt, timedelta
from motor.core import AgnosticCollection


def _get_stage_group_by(format: str) -> dict:
    return {
        '$group': {
            '_id': {'$dateToString': {'format': format, 'date': '$dt'}},
            'total': {'$sum': '$value'},
        }
    }


def _get_data(start_date: dt, end_date: dt, group_type: str):

    def get_date(time_unit_plural: str, time_unit: int, coef: int = 1):
        return [(
            start_date + timedelta(**{time_unit_plural: i * coef})).strftime(format)
            for i in range(int(interval/time_unit) + 1)]

    interval = (end_date - start_date).total_seconds()
    hour = 60 * 60
    day = hour * 24
    month = day * 30.5
    match group_type:
        case 'hour':
            format = '%Y-%m-%dT%H'
            extra = ':00:00'
            time_sequence = get_date('hours', hour)
        case 'day':
            format = '%Y-%m-%d'
            extra = 'T00:00:00'
            time_sequence = get_date('days', day)
        case 'month':
            format = '%Y-%m'
            extra = '-01T00:00:00'
            time_sequence = get_date('days', month, 28)
    return (_get_stage_group_by(format),
            {time: 0 for time in time_sequence},
            extra)


async def calc(collection: AgnosticCollection, data: dict[str, str]):
    dt_from = dt.fromisoformat(data['dt_from'])
    dt_upto = dt.fromisoformat(data['dt_upto'])
    group_type = data['group_type']
    dataset, labels = [], []

    (stage_group_and_sum,
     initial_data,
     extra) = _get_data(dt_from, dt_upto, group_type)
    stage_match_dates = {'$match': {'dt': {'$gte': dt_from, '$lte': dt_upto}}}
    pipeline = [stage_match_dates, stage_group_and_sum]

    async for item in collection.aggregate(pipeline):
        initial_data[item['_id']] = item['total']

    for date, value in initial_data.items():
        dataset.append(value)
        labels.append(date + extra)

    return {'dataset': dataset, 'labels': labels}
