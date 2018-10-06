from jsonrpcclient.response import (
    NOID,
    ErrorResponse,
    NotificationResponse,
    Response,
    SuccessResponse,
    total_results,
)


def test_success_response():
    response = SuccessResponse(**{"jsonrpc": "2.0", "result": 5, "id": 1})
    assert response.ok == True
    assert response.id == 1
    assert response.result == 5
    assert repr(response) == "<SuccessResponse(id=1, result=5)>"
    assert str(response) == '{"jsonrpc": "2.0", "result": 5, "id": 1}'


def test_success_response_null_id():
    # Acceptable.
    response = SuccessResponse(**{"jsonrpc": "2.0", "result": "foo", "id": None})
    assert response.ok == True
    assert response.id == None
    assert repr(response) == "<SuccessResponse(id=None, result=foo)>"
    assert str(response) == '{"jsonrpc": "2.0", "result": "foo", "id": null}'


def test_notification_response():
    response = NotificationResponse()
    assert response.ok == True
    assert response.id == NOID
    assert response.result == None
    assert repr(response) == "<NotificationResponse()>"
    assert str(response) == ""


def test_error_response():
    deserialized = {
        "jsonrpc": "2.0",
        "error": {"code": -32000, "message": "Not Found", "data": "foo"},
        "id": 1,
    }
    response = ErrorResponse(**deserialized)
    assert response.ok == False
    assert response.id == 1
    assert response.code == -32000
    assert response.message == "Not Found"
    assert response.data == "foo"
    assert repr(response) == '<ErrorResponse(id=1, message="Not Found")>'
    assert (
        str(response)
        == '{"jsonrpc": "2.0", "error": {"code": -32000, "message": "Not Found", "data": "foo"}, "id": 1}'
    )


def test_error_response_no_id():
    deserialized = {"jsonrpc": "2.0", "error": {"code": -32000, "message": "Not Found"}}
    response = ErrorResponse(**deserialized)
    assert repr(response) == '<ErrorResponse(message="Not Found")>'
    assert (
        str(response)
        == '{"jsonrpc": "2.0", "error": {"code": -32000, "message": "Not Found"}}'
    )


def test_error_with_data():
    response = {
        "jsonrpc": "2.0",
        "error": {
            "code": -32000,
            "message": "Not Found",
            "data": "Lorem ipsum dolor sit amet, consectetur adipiscing elit",
        },
        "id": None,
    }
    response = ErrorResponse(**response)
    assert response.code == -32000
    assert response.message == "Not Found"
    assert response.data == "Lorem ipsum dolor sit amet, consectetur adipiscing elit"


def test_error_with_nonstring_data():
    """Reported in issue #56"""
    response = {
        "jsonrpc": "2.0",
        "error": {"code": -32000, "message": "Not Found", "data": {}},
        "id": None,
    }
    response = ErrorResponse(**response)
    assert response.code == -32000
    assert response.message == "Not Found"
    assert response.data == {}


def test_total_responses_unparsed():
    assert total_results(None) == 0


def test_total_responses_one():
    response = SuccessResponse(**{"jsonrpc": "2.0", "result": "foo", "id": 1})
    assert total_results(response) == 1


def test_total_responses_list():
    response = SuccessResponse(**{"jsonrpc": "2.0", "result": "foo", "id": 1})
    assert total_results([response, response]) == 2


def test_response():
    response = Response("foo")
    assert response.text == "foo"


def test_response_repr():
    response = Response("foo")
    assert repr(response) == "<Response[0]>"


def test_response_repr_with_results():
    response = Response("foo")
    response.data = ErrorResponse(
        **{"jsonrpc": "2.0", "error": {"message": "foo"}, "id": 1}
    )
    assert repr(response) == "<Response[0 ok, 1 errors]>"
