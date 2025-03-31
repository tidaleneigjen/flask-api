# flask-api README

To Run:

1. Create a virtualenv and activate it.
2. Run `pip install -r requirements.txt`
3. Run 'python app.py`


CREATE
curl -X POST http://127.0.0.1:5000/tasks -H "Content-Type: application/json" -d '{"title": "Buy groceries", "description": "Milk, Bread, Eggs"}'

GET ALL
curl -X GET http://127.0.0.1:5000/tasks

GET ONE
curl -X GET http://127.0.0.1:5000/tasks/1

UPDATE
curl -X PUT http://127.0.0.1:5000/tasks/1 -H "Content-Type: application/json" -d '{"done": true}'


DELETE
curl -X DELETE http://127.0.0.1:5000/tasks/1



