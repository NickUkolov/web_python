### Инструкция

- ```docker build . -t hw_1_2:docker```
- ```docker run --name django_cont -d -p 8000:8000 hw_1_2:docker```
- Далее проверить командами из ```requests-examples.http```