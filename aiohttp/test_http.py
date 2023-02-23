import requests

if __name__ == '__main__':
    response = requests.post('http://0.0.0.0:8080/posts/',
                             json={'title': 'test_title', 'description': 'test_descr', 'owner': 'mr_kent_paul'},
                             )
    print(response.status_code)
    print(response.json())

    response = requests.get('http://0.0.0.0:8080/posts/1/')
    print(response.status_code)
    print(response.json())

    response = requests.patch('http://0.0.0.0:8080/posts/1/',
                             json={'title': 'test_title', 'description': 'interesting', 'owner': 'krasavchik'},
                             )
    print(response.status_code)
    print(response.json())


    response = requests.delete('http://0.0.0.0:8080/posts/1/')
    print(response.status_code)
    print(response.json())

    response = requests.get('http://0.0.0.0:8080/posts/1/')
    print(response.status_code)
    print(response.json())

