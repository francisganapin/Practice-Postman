import requests


data ={
    'name':'Francis',
    'age':25,
    'city':'Manila'
}


respose = requests.post('http://localhost:5000/api/person',json=data)


print(respose.status_code)
print(respose.json())