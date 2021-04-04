import json, uuid, random
from flask import Flask, request

items = [
    {
        "id": str(uuid.uuid4()),
        "name": "Wooden Sword",
        "description": "A simple sword made of wood",
        "price": 100
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Wooden Mail",
        "description": "A simple mail made of wood",
        "price": 500
    },
    {
        "id": str(uuid.uuid4()),
        "name": "Life Potion",
        "description": "A red drink that recovers health",
        "price": 20
    }
]

character = {
    "health": 100,
    "attack": 1,
    "defense": 1,
    "level": 1,
    "exp": 0,
    "money": 0
}

app = Flask(__name__)

@app.route('/character')
def characterProfile():
    return json.dumps(character)

@app.route('/character/inventory')
def inventory():
    return json.dumps([])

@app.route('/character/new', methods = ['POST'])
def newCharacter():
    character["health"] = 100
    character["attack"] = 1
    character["defense"] = 1
    character["level"] = 1
    character["exp"] = 0
    character["money"] = 0
    return json.dumps({
        "message": "Character successfully reset!"
    })

@app.route('/hunt', methods = ['POST'])
def hunt():
    if character['health'] < 0:
        return {
            'message': 'You can\'t hunt when you are dead',
            'character': character
        }
    character['health'] -= random.randint(5, 10)
    character['exp'] += random.randint(10, 30)
    character['money'] += random.randint(0, 5)
    if character['health'] > 0:
        result = {
            'message': 'You successfully killed something!',
            'character': character
        }
    else:
        result = {
            'message': 'You died! :(',
            'character': character
        }
    return result

@app.route('/items', methods = ['GET', 'POST'])
def itemList():
    if request.method == 'POST':
        body = request.json
        newItem = {
            'id': str(uuid.uuid4()),
            'name': body['name'],
            'description': body['description'],
            'price': body['price']
        }
        items.append(newItem)
        return newItem
    return json.dumps(items)

@app.route('/items/<id>')
def getItem(id):
    result = next(item for item in items if item["id"] == id)
    return json.dumps(result)

if __name__ == '__main__':
    app.run()