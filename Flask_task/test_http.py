import requests

if __name__ == '__main__':
    response = requests.post('http://127.0.0.1:5000/posts',
                             json={'title': 'test_title', 'description': 'test_descr', 'owner': 'mr_kent_paul'},
                             )
    print(response.status_code)
    print(response.json())

    response = requests.get('http://127.0.0.1:5000/posts/1')
    print(response.status_code)
    print(response.json())

    response = requests.delete('http://127.0.0.1:5000/posts/1')
    print(response.status_code)
    print(response.json())
