import json
import boto3
import pytest

from translate import app


@pytest.fixture()
def apigw_event(mocker):
    translate = boto3.client("translate")
    mock_client = mocker.Mock(wraps=translate)
    mock_client.translate_text.return_value = { 
        "TranslatedText": "Bonjour"
    } 
    mocker.patch.object(app, "translate", mock_client)

    return {
        "body": '{ "text": "Good morning" }'
    }


def test_lambda_handler(apigw_event):
    ret = app.lambda_handler(apigw_event, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 200
    assert "text" in ret["body"]
    assert data["text"] == "Good morning"
    assert data["translated_text"] == "Bonjour"
