# User Service

### List all users

**Method**

`GET /users`

**Response**

`200` (ok) on success

```json
[
	{
		"user_id": 1,
		"first_name": "John",
		"last_name": "Doe"
	},
	{
		"user_id": 2,
		"first_name": "Mary",
		"last_name": "Poppins"
	}
]
```

### Creating a new user

**Method**

`POST /users`

**Arguments**

- `"first_name":string` user's first name
- `"last_name":string` user's last name

**Response**

`201` (created) on success

# Order Service

### Show order data

**Method**

`GET /order`

**Response**

`200` (ok) on success

```json
[
	{
		"order_id": 1,
		"order_name": "Amoxicillin 500mg",
		"user_first_name": "Albert",
		"user_last_name": "Einstein"
	},
	{
		"order_id": 2,
		"order_name": "Advil 250mg",
		"first_name": "Albert",
		"last_name": "Einstein"
	}
]
```

### Creating a new order

**Method**

`POST /order`

**Arguments**

- `"order_name":string` ordered item's name
- `"user_id":string` user's unique id

**Response**

`201` (created) on success