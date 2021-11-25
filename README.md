# car_price_model

Итоговый проект курса "Машинное обучение в бизнесе"

Стек:
ML: sklearn, pandas, numpy API: flask

Модель основана на датасете: 100,000 UK Used Car Data set
https://www.kaggle.com/kukuroo3/used-car-price-dataset-competition-format

Задача: Предсказать стоимость авто, по его параметрам

Модель: RandomForest

Клонируем репозиторий и создаем образ
$ git clone https://github.com/DaniilMelnik/car_price_model.git
$ cd GB_docker_flask_example
$ docker build -t daniil/carprice .
Запускаем контейнер
Здесь Вам нужно создать каталог локально и сохранить туда предобученную модель (<your_local_path_to_pretrained_models> нужно заменить на полный путь к этому каталогу)

$ docker run -d -p 8180:8180 -p 8181:8181 -v 
<your_home_path>/car_price_model/app/models:/app/models -v 
<your_home_path>/car_price_model/app/front/data:/app/front/data 
daniil/carprice
