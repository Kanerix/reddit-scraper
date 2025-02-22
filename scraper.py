from swiftshadow import QuickProxy
from yars.yars import YARS
from yars.utils import export_to_json

SEARCH_TERMS = ["Udlændinge"]

proxy = QuickProxy()
if proxy is None:
    exit(1)

yars = YARS(proxy=proxy.as_requests_dict())
search_result = yars.search_reddit(SEARCH_TERMS[0], limit=100, after="t3_t85h9k")
export_to_json(search_result)
