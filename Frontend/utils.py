import requests
from .models import ApiData


def get_reader_data():
    api_url = "https://example.com/api"
    response = requests.get(api_url)
    api_data = response.json()

    # Assuming the API response is a JSON object with keys: 'number1', 'number2', 'number3', 'number4'
    ApiData.objects.create(
        number1=api_data['number1'],
        number2=api_data['number2'],
        number3=api_data['number3'],
        number4=api_data['number4'],
    )