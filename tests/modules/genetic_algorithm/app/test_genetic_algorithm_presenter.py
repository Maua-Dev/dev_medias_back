import json
from src.modules.genetic_algorithm.app.genetic_algorithm_presenter import lambda_handler


class Test_GeneticAlgorithmPresenter:
    
    def test_genetic_algorithm_presenter_only_tests(self):
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path",
            "rawQueryString": "",
            "headers": {
                "header1": "value1"
            },
            "requestContext": {
                "accountId": "123456789012",
                "apiId": "<urlid>",
                "domainName": "<url-id>.lambda-url.us-west-2.on.aws",
                "requestId": "id",
                "routeKey": "$default",
                "stage": "$default",
                "time": "12/Mar/2020:19:03:58 +0000",
                "timeEpoch": 1583348638390
            },
            "body": {
                'current_tests': [5.0],
                'current_assignments': [],
                'num_remaining_tests': 3,
                'num_remaining_assignments': 0,
                'test_weight': 1.0,
                'assignment_weight': 0.0,
                'target_average': 7.0
            }
        }

        response = lambda_handler(event=event, context=None)
        assert response["statusCode"] == 200

    def test_genetic_algorithm_presenter_only_assignments(self):
        event = {
            "version": "2.0",
            "routeKey": "$default",
            "rawPath": "/my/path",
            "body": {
                'current_tests': [],
                'current_assignments': [8.0, 9.0],
                'num_remaining_tests': 0,
                'num_remaining_assignments': 2,
                'test_weight': 0.0,
                'assignment_weight': 1.0,
                'target_average': 6.0
            }
        }

        response = lambda_handler(event=event, context=None)
        assert response["statusCode"] == 200

    def test_genetic_algorithm_presenter_with_custom_params(self):
        event = {
            "body": {
                'current_tests': [6.0],
                'current_assignments': [7.0],
                'num_remaining_tests': 2,
                'num_remaining_assignments': 1,
                'test_weight': 0.6,
                'assignment_weight': 0.4,
                'target_average': 7.0,
                'max_grade': 10.0,
                'population_size': 200,
                'generations': 300
            }
        }

        response = lambda_handler(event=event, context=None)
        assert response["statusCode"] == 200

    def test_genetic_algorithm_presenter_with_spec_weights(self):
        event = {
            "body": {
                'current_tests': [6.0],
                'current_assignments': [7.0],
                'num_remaining_tests': 2,
                'num_remaining_assignments': 2,
                'test_weight': 0.6,
                'assignment_weight': 0.4,
                'target_average': 7.0,
                'spec_test_weight': [0.2, 0.4, 0.4],
                'spec_assingment_weight': [0.3, 0.3, 0.4]
            }
        }

        response = lambda_handler(event=event, context=None)
        assert response["statusCode"] == 200

    def test_genetic_algorithm_presenter_api_gateway_format(self):
        event = {
            'resource': '/mss-medias/genetic-algorithm',
            'path': '/mss-medias/genetic-algorithm',
            'httpMethod': 'POST',
            'headers': {
                'Accept': 'application/json, text/plain, */*',
                'content-type': 'application/json',
                'Host': 'api.example.com'
            },
            'requestContext': {
                'resourcePath': '/mss-medias/genetic-algorithm',
                'httpMethod': 'POST',
                'requestTime': '15/Sep/2023:18:13:45 +0000',
                'path': '/prod/mss-medias/genetic-algorithm',
                'accountId': '264055331071',
                'stage': 'prod'
            },
            'body': '{"current_tests":[6.0,8.0],"current_assignments":[7.0],"num_remaining_tests":2,"num_remaining_assignments":1,"test_weight":0.6,"assignment_weight":0.4,"target_average":7.0}',
            'isBase64Encoded': False
        }

        response = lambda_handler(event=event, context=None)
        assert response["statusCode"] == 200

    def test_genetic_algorithm_presenter_multiple_calls(self):
        event = {
            "body": {
                'current_tests': [6.0, 7.0],
                'current_assignments': [8.0],
                'num_remaining_tests': 2,
                'num_remaining_assignments': 1,
                'test_weight': 0.6,
                'assignment_weight': 0.4,
                'target_average': 7.5
            }
        }

        for _ in range(10):
            response = lambda_handler(event=event, context=None)
            assert response["statusCode"] == 200

    def test_genetic_algorithm_presenter_missing_current_tests(self):
        event = {
            "body": {
                'current_assignments': [7.0],
                'num_remaining_tests': 2,
                'num_remaining_assignments': 1,
                'test_weight': 0.6,
                'assignment_weight': 0.4,
                'target_average': 7.0
            }
        }

        response = lambda_handler(event=event, context=None)
        assert response["statusCode"] == 400
        assert 'current_tests' in json.loads(response["body"])

    def test_genetic_algorithm_presenter_missing_current_assignments(self):
        event = {
            "body": {
                'current_tests': [6.0],
                'num_remaining_tests': 2,
                'num_remaining_assignments': 1,
                'test_weight': 0.6,
                'assignment_weight': 0.4,
                'target_average': 7.0
            }
        }

        response = lambda_handler(event=event, context=None)
        assert response["statusCode"] == 400
        assert 'current_assignments' in json.loads(response["body"])

    def test_genetic_algorithm_presenter_missing_num_remaining_tests(self):
        event = {
            "body": {
                'current_tests': [6.0],
                'current_assignments': [7.0],
                'num_remaining_assignments': 1,
                'test_weight': 0.6,
                'assignment_weight': 0.4,
                'target_average': 7.0
            }
        }

        response = lambda_handler(event=event, context=None)
        assert response["statusCode"] == 400
        assert 'num_remaining_tests' in json.loads(response["body"])

    def test_genetic_algorithm_presenter_missing_test_weight(self):
        event = {
            "body": {
                'current_tests': [6.0],
                'current_assignments': [7.0],
                'num_remaining_tests': 2,
                'num_remaining_assignments': 1,
                'assignment_weight': 0.4,
                'target_average': 7.0
            }
        }

        response = lambda_handler(event=event, context=None)
        assert response["statusCode"] == 400
        assert 'test_weight' in json.loads(response["body"])

    def test_genetic_algorithm_presenter_missing_target_average(self):
        event = {
            "body": {
                'current_tests': [6.0],
                'current_assignments': [7.0],
                'num_remaining_tests': 2,
                'num_remaining_assignments': 1,
                'test_weight': 0.6,
                'assignment_weight': 0.4
            }
        }

        response = lambda_handler(event=event, context=None)
        assert response["statusCode"] == 400
        assert 'target_average' in json.loads(response["body"])

    def test_genetic_algorithm_presenter_wrong_type_current_tests(self):
        event = {
            "body": {
                'current_tests': 6.0,
                'current_assignments': [7.0],
                'num_remaining_tests': 2,
                'num_remaining_assignments': 1,
                'test_weight': 0.6,
                'assignment_weight': 0.4,
                'target_average': 7.0
            }
        }

        response = lambda_handler(event=event, context=None)
        assert response["statusCode"] == 400
        assert 'current_tests' in json.loads(response["body"])

    def test_genetic_algorithm_presenter_wrong_type_test_weight(self):
        event = {
            "body": {
                'current_tests': [6.0],
                'current_assignments': [7.0],
                'num_remaining_tests': 2,
                'num_remaining_assignments': 1,
                'test_weight': '0.6',
                'assignment_weight': 0.4,
                'target_average': 7.0
            }
        }

        response = lambda_handler(event=event, context=None)
        assert response["statusCode"] == 400
        assert 'test_weight' in json.loads(response["body"])

    def test_genetic_algorithm_presenter_wrong_type_target_average(self):
        event = {
            "body": {
                'current_tests': [6.0],
                'current_assignments': [7.0],
                'num_remaining_tests': 2,
                'num_remaining_assignments': 1,
                'test_weight': 0.6,
                'assignment_weight': 0.4,
                'target_average': '7.0'
            }
        }

        response = lambda_handler(event=event, context=None)
        assert response["statusCode"] == 400
        assert 'target_average' in json.loads(response["body"])

    def test_genetic_algorithm_presenter_negative_num_remaining(self):
        event = {
            "body": {
                'current_tests': [6.0],
                'current_assignments': [7.0],
                'num_remaining_tests': -1,
                'num_remaining_assignments': 1,
                'test_weight': 0.6,
                'assignment_weight': 0.4,
                'target_average': 7.0
            }
        }

        response = lambda_handler(event=event, context=None)
        assert response["statusCode"] == 400
        assert 'non-negative' in json.loads(response["body"]).lower()

    def test_genetic_algorithm_presenter_test_weight_out_of_range(self):
        event = {
            "body": {
                'current_tests': [6.0],
                'current_assignments': [7.0],
                'num_remaining_tests': 2,
                'num_remaining_assignments': 1,
                'test_weight': 1.5,
                'assignment_weight': 0.4,
                'target_average': 7.0
            }
        }

        response = lambda_handler(event=event, context=None)
        assert response["statusCode"] == 400
        assert 'between 0 and 1' in json.loads(response["body"]).lower()

    def test_genetic_algorithm_presenter_target_average_out_of_range(self):
        event = {
            "body": {
                'current_tests': [6.0],
                'current_assignments': [7.0],
                'num_remaining_tests': 2,
                'num_remaining_assignments': 1,
                'test_weight': 0.6,
                'assignment_weight': 0.4,
                'target_average': 15.0
            }
        }

        response = lambda_handler(event=event, context=None)
        assert response["statusCode"] == 400
        assert 'between 0 and 10' in json.loads(response["body"]).lower()

    def test_genetic_algorithm_presenter_invalid_max_grade(self):
        event = {
            "body": {
                'current_tests': [6.0],
                'current_assignments': [7.0],
                'num_remaining_tests': 2,
                'num_remaining_assignments': 1,
                'test_weight': 0.6,
                'assignment_weight': 0.4,
                'target_average': 7.0,
                'max_grade': -5.0
            }
        }

        response = lambda_handler(event=event, context=None)
        assert response["statusCode"] == 400
        assert 'greater than 0' in json.loads(response["body"]).lower()

    def test_genetic_algorithm_presenter_invalid_population_size(self):
        event = {
            "body": {
                'current_tests': [6.0],
                'current_assignments': [7.0],
                'num_remaining_tests': 2,
                'num_remaining_assignments': 1,
                'test_weight': 0.6,
                'assignment_weight': 0.4,
                'target_average': 7.0,
                'population_size': 0
            }
        }

        response = lambda_handler(event=event, context=None)
        assert response["statusCode"] == 400
        assert 'greater than 0' in json.loads(response["body"]).lower()

    def test_genetic_algorithm_presenter_invalid_generations(self):
        event = {
            "body": {
                'current_tests': [6.0],
                'current_assignments': [7.0],
                'num_remaining_tests': 2,
                'num_remaining_assignments': 1,
                'test_weight': 0.6,
                'assignment_weight': 0.4,
                'target_average': 7.0,
                'generations': -10
            }
        }

        response = lambda_handler(event=event, context=None)
        assert response["statusCode"] == 400
        assert 'greater than 0' in json.loads(response["body"]).lower()

    def test_genetic_algorithm_presenter_spec_test_weight_wrong_length(self):
        event = {
            "body": {
                'current_tests': [6.0],
                'current_assignments': [7.0],
                'num_remaining_tests': 2,
                'num_remaining_assignments': 1,
                'test_weight': 0.6,
                'assignment_weight': 0.4,
                'target_average': 7.0,
                'spec_test_weight': [0.5, 0.5]
            }
        }

        response = lambda_handler(event=event, context=None)
        assert response["statusCode"] == 400
        assert 'same length' in json.loads(response["body"]).lower()

    def test_genetic_algorithm_presenter_spec_test_weight_sum_not_one(self):
        event = {
            "body": {
                'current_tests': [6.0],
                'current_assignments': [7.0],
                'num_remaining_tests': 2,
                'num_remaining_assignments': 1,
                'test_weight': 0.6,
                'assignment_weight': 0.4,
                'target_average': 7.0,
                'spec_test_weight': [0.3, 0.3, 0.3]
            }
        }

        response = lambda_handler(event=event, context=None)
        assert response["statusCode"] == 400
        assert 'sum' in json.loads(response["body"]).lower()

    def test_genetic_algorithm_presenter_high_target(self):
        event = {
            "body": {
                'current_tests': [10.0, 10.0],
                'current_assignments': [10.0],
                'num_remaining_tests': 2,
                'num_remaining_assignments': 1,
                'test_weight': 0.6,
                'assignment_weight': 0.4,
                'target_average': 10.0
            }
        }

        response = lambda_handler(event=event, context=None)
        assert response["statusCode"] == 200

    def test_genetic_algorithm_presenter_low_target(self):
        event = {
            "body": {
                'current_tests': [3.0],
                'current_assignments': [4.0],
                'num_remaining_tests': 1,
                'num_remaining_assignments': 1,
                'test_weight': 0.5,
                'assignment_weight': 0.5,
                'target_average': 5.0
            }
        }

        response = lambda_handler(event=event, context=None)
        assert response["statusCode"] == 200