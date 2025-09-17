import json

from lambda_functions.products.getAll import lambda_handler as get_all_handler
from lambda_functions.products.getById import lambda_handler as get_by_id_handler

def test_get_all_products_success(mock_db):
    mock_conn, mock_cursor = mock_db
    mock_data = [
        {"id": 1, "name": "Product A"},
        {"id": 2, "name": "Product B"},
    ]
    mock_cursor.fetchall.return_value = mock_data

    result = get_all_handler({}, {})

    assert result["statusCode"] == 200
    body = json.loads(result["body"])
    assert body["success"] is True
    assert body["data"] == mock_data
    

def test_get_product_by_id_success(mock_db):
    mock_conn, mock_cursor = mock_db
    mock_data = {"id": 1, "name": "Product A"}
    mock_cursor.fetchone.return_value = mock_data
    
    event = {
        "pathParameters": {"id": "1"}
    }
    result = get_by_id_handler(event, {})

    assert result["statusCode"] == 200
    body = json.loads(result["body"])
    assert body["success"] is True
    assert body["data"] == mock_data