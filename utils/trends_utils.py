from pytrends.request import TrendReq

def get_trends(keyword):

    try:

        pytrends = TrendReq()

        pytrends.build_payload(
            [keyword]
        )

        data = pytrends.interest_over_time()

        return data

    except:

        return None
