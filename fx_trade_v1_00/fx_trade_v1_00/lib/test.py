from .get_ma import GetMA


def test():

    request = dict()
    test = GetMA()

    request['instruments'] = "USD_JPY"
    request['alignmentTimezone'] = "Japan"
    request['count'] = 50
    request['granularity'] = "M5"

    print(test.get_MA(request))
