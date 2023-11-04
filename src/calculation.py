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
    match group_type:
        case 'hour':
            format = '%Y-%m-%dT%H'
            extra = ':00:00'
            time_sequence = [(
                start_date + timedelta(hours=i)).strftime(format)
                for i in range((end_date - start_date).days*24 + 1)]
        case 'day':
            format = '%Y-%m-%d'
            extra = 'T00:00:00'
            time_sequence = [(
                start_date + timedelta(days=i)).strftime(format)
                for i in range((end_date - start_date).days + 1)]
        case 'month':
            format = '%Y-%m'
            extra = '-01T00:00:00'
            time_sequence = [(
                start_date + timedelta(days=i*30.5)).strftime(format)
                for i in range(int((end_date-start_date).days/30))]
    return _get_stage_group_by(format), time_sequence, extra


async def calc(collection: AgnosticCollection, data: dict[str, str]):
    dt_from = dt.fromisoformat(data['dt_from'])
    dt_upto = dt.fromisoformat(data['dt_upto'])
    group_type = data['group_type']
    dataset, labels = [], []

    (stage_group_and_sum,
     time_sequence,
     extra) = _get_data(dt_from, dt_upto, group_type)
    stage_match_dates = {'$match': {'dt': {'$gte': dt_from, '$lte': dt_upto}}}
    stage_sort = {'$sort': {'_id': 1}}
    pipeline = [stage_match_dates, stage_group_and_sum, stage_sort]
    initial_data = {time: 0 for time in time_sequence}

    async for item in collection.aggregate(pipeline):
        initial_data[item['_id']] = item['total']

    for date, value in initial_data.items():
        dataset.append(value)
        labels.append(date + extra)

    return {'dataset': dataset, 'labels': labels}
