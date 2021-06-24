# rabbitmq_study_project

Making education project using rabbitmq

In this project I create a 4 docker instances:
- rabbitmq server
- feature container that pushed to rabbit mq queue features and real price value
- model container that get features from rabbit and pushing predictions to queue
- metrics container that gets real price value and prediction and calculate RMSE values of model

This is simpe but interesting project, that helps me take basic knowledge of this techonoly!
