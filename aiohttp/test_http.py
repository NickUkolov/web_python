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






    # response = requests.post('http://0.0.0.0:8080/users/',
    #                          json={'name': 'testuser', 'password': 'testpassword', 'email': 'nick@mail.ru'},
    #                          )
    # print(response.status_code)
    # print(response.json())
    #
    # response = requests.get('http://0.0.0.0:8080/users/1/',
    #                          )
    # print(response.status_code)
    # print(response.json())

    response = requests.post('http://0.0.0.0:8080/login/',
                             json={'name': 'testuser', 'password': 'testpassword'},
                             )
    print(response.status_code)
    print(response.json())


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
    # response = requests.get('http://0.0.0.0:8080/users/1/',
    #                          )
    # print(response.status_code)
    # print(response.json())
