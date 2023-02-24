import requests

if __name__ == '__main__':
    # response = requests.post('http://0.0.0.0:8080/posts/',
    #                          json={'title': 'test_title', 'description': 'test_descr', 'owner': 'mr_kent_paul'},
    #                          )
    # print(response.status_code)
    # print(response.json())
    #
    # response = requests.get('http://0.0.0.0:8080/posts/1/')
    # print(response.status_code)
    # print(response.json())
    #
    # response = requests.patch('http://0.0.0.0:8080/posts/1/',
    #                          json={'title': 'test_title', 'description': 'interesting', 'owner': 'krasavchik'},
    #                          )
    # print(response.status_code)
    # print(response.json())
    #
    #
    # response = requests.delete('http://0.0.0.0:8080/posts/1/')
    # print(response.status_code)
    # print(response.json())
    #
    # response = requests.get('http://0.0.0.0:8080/posts/1/')
    # print(response.status_code)
    # print(response.json())






    # response = requests.post('http://0.0.0.0:8081/users/',
    #                          json={'name': 'testuser', 'password': 'testpassword', 'email': 'nick@mail.ru'},
    #                          )
    # print(response.status_code)
    # print(response.json())
    #
    # response = requests.post('http://0.0.0.0:8081/users/',
    #                          json={'name': 'testuser_1', 'password': 'testpassword_1', 'email': 'nic1k@mail.ru'},
    #                          )
    # print(response.status_code)
    # print(response.json())

    #
    response = requests.get('http://0.0.0.0:8081/users/1/', headers={'token': '3242c402-78da-4b16-9561-2090b8a54466'},
                             )
    print(response.status_code)
    print(response.json())



    # response = requests.post('http://0.0.0.0:8081/login/',
    #                          json={'name': 'testuser', 'password': 'testpassword',}, headers={'token': '3242c402-78da-4b16-9561-2090b8a54466'},
    #                          )
    # print(response.status_code)
    # print(response.json())
    #
    # response = requests.post('http://0.0.0.0:8081/login/',
    #                          json={'name': 'testuser_1', 'password': 'testpassword_1',}, headers={'token': 'e23725b0-6fc7-4395-92f3-d99bea274144'},
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
    # response = requests.get('http://0.0.0.0:8080/users/1/', headers={'token': '93c8c792-402d-4ee2-a97f-b831f4401651'},
    #                          )
    # print(response.status_code)
    # print(response.json())
