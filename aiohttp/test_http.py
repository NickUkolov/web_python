import requests

if __name__ == '__main__':
    response = requests.post('http://0.0.0.0:8081/api/posts/',
                             json={'title': 'test_title', 'description': 'test_descr', 'owner': 'testuser_1'},
                             headers={'token': 'cbc11fd6-7f29-48f9-bc9b-89c638e8b254'},
                             )
    print(response.status_code)
    print(response.json())
    #
    # response = requests.get('http://0.0.0.0:8081/api/posts/7/')
    # print(response.status_code)
    # print(response.json())
    #
    # response = requests.patch('http://0.0.0.0:8081/api/posts/3/',
    #                          json={'title': 'test_title', 'description': 'interesting', 'owner': 'krasavchik'},
    #                          headers={'token': 'cbc11fd6-7f29-48f9-bc9b-89c638e8b254'},
    #                          )
    # print(response.status_code)
    # print(response.json())

    #
    # response = requests.delete('http://0.0.0.0:8081/api/posts/1/',
    #                             headers={'token': '9e22a7dd-252e-4f09-b6eb-42e705f46f79'},
    #                            )
    # print(response.status_code)
    # print(response.json())
    #
    # response = requests.get('http://0.0.0.0:8080/posts/1/')
    # print(response.status_code)
    # print(response.json())






    # response = requests.post('http://0.0.0.0:8081/api/register/',
    #                          json={'name': 'testuser', 'password': 'testpassword', 'email': 'nick@mail.ru'},
    #                          )
    # print(response.status_code)
    # print(response.json())
    #
    # response = requests.post('http://0.0.0.0:8081/api/register/',
    #                          json={'name': 'testuser_1', 'password': 'testpassword_1', 'email': 'nic1k@mail.ru'},
    #                          )
    # print(response.status_code)
    # print(response.json())

    #



    # response = requests.post('http://0.0.0.0:8081/api/login/',
    #                          json={'name': 'testuser', 'password': 'testpassword',}, headers={'token': '9e22a7dd-252e-4f09-b6eb-42e705f46f79'},
    #                          )
    # print(response.status_code)
    # print(response.json())
    #
    # response = requests.post('http://0.0.0.0:8081/api/login/',
    #                          json={'name': 'testuser_1', 'password': 'testpassword_1',}, headers={'token': 'cbc11fd6-7f29-48f9-bc9b-89c638e8b254'},
    #                          )
    # print(response.status_code)
    # print(response.json())



    # response = requests.patch('http://0.0.0.0:8080/users/1/',
    #                          json={'name': 'nice user'},
    #                          )
    # print(response.status_code)
    # print(response.json())
    #
    # response = requests.delete('http://0.0.0.0:8080/users/1/',
    #                          )
    # print(response.status_code)
    # print(response.json())
    #
    # response = requests.get('http://0.0.0.0:8081/api/users/1/', headers={'token': '9e22a7dd-252e-4f09-b6eb-42e705f46f79'},
    #                          )
    # print(response.status_code)
    # print(response.json())

    # response = requests.get('http://0.0.0.0:8081/api/posts/1/'
    #                          )
    # print(response.status_code)
    # print(response.json())

