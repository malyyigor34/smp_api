from django.core.exceptions import ValidationError

from smp_api.utils.Exceptions import *
from smp_api.utils.common_modules.common import validate_url
from smp_api.utils.data_extractor import DataExtractor


class DataExtractorManager:
    def __init__(self, url):
        self._url = url
        self._data_extractor = DataExtractor()

    def get(self):
        response = {'error': False}
        data = None
        try:
            validate_url(self._url)
        except ValidationError as e:
            response['error'] = e.message
            return response
        try:
            data = self._data_extractor.extract(self._url)
        except InvalidUrl as e:
            response['error'] = e.message
        except WebSiteBlocked:
            response['error'] = f'{self._url} is blocked'
        response['data'] = data
        return response



    #def _add_cache(self, data):
    #    data = json.dumps(data)
    #    Cache.objects.create(data=data, domain=self._url, date=datetime.datetime.now().timestamp())

    #def _get_from_cache(self):
    #    try:
    #        try:
    #            response = Cache.objects.get(domain=self._url)
    #        except MultipleObjectsReturned:
    #            Cache.objects.all().delete()
    #            raise OldChache
    #        if datetime.datetime.now().timestamp() - response.date > float(os.environ.get('CACHE_LIFETIME')) * 60:
    #            response.delete()
    #            raise OldChache
    #        else:
    #            return json.loads(response.data)
    #    except ObjectDoesNotExist:
    #        raise OldChache
