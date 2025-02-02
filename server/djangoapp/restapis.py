import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"],
                                    city=dealer_doc["city"],
                                    full_name=dealer_doc["full_name"],
                                    id=dealer_doc["id"],
                                    lat=dealer_doc["lat"],
                                    long=dealer_doc["long"],
                                    short_name=dealer_doc["short_name"],
                                    st=dealer_doc["st"],
                                    zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)

def post_request(url, json_payload, **kwargs):
    #untested
    try:
        response = requests.post(url, params=kwargs, headers={'Content-Type': 'application/json'}, 
                                 json=json_payload)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    json_data = json.loads(response.text)
    
    return json_data


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealer_reviews_from_cf(url, dealerId):
    results = []

    json_result = get_request(url)
    if json_result:

        for data in json_result:
            analyzed_sentiment = analyze_review_sentiments(data["review"])            
            dealer_obj = DealerReview(dealership=data["dealership"],
                                    name=data["name"],
                                    purchase=data["purchase"],
                                    review=data["review"],
                                    purchase_date=data["purchase_date"],
                                    car_make=data["car_make"],
                                    car_model=data["car_model"],
                                    car_year=data["car_year"],
                                    sentiment=analyzed_sentiment,
                                    id=data["id"])
            results.append(dealer_obj)

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text): 

        url = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/5744b0c5-c384-4a45-95c4-2bd0b822c42b"
        api_key = "v2-lSOGOc2Py8PtIn0hHvQG6aXPAfNSAnaKdYwl48poB"

        authenticator = IAMAuthenticator(api_key)
        natural_language_understanding = NaturalLanguageUnderstandingV1(version='2021-08-01',authenticator=authenticator)
        natural_language_understanding.set_service_url(url)

        response = natural_language_understanding.analyze( text=text ,features=Features(sentiment=SentimentOptions(targets=[text])), language="en").get_result()

        sentiment=json.dumps(response, indent=2)
        sentiment = response['sentiment']['document']['label']

        return(sentiment)
