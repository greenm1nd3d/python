from locust import Locust, HttpLocust, TaskSet, task

class MyTaskSet(TaskSet):
    @task
    def getusers(self):
        self.client.get("/users")

    @task
    def createuser(self):
        self.client.post("/createuser", {"first_name":"John", "last_name":"Doe"})

class MyLocust(HttpLocust):
    task_set = MyTaskSet
    host = "http://localhost:8888"
    min_wait = 1000
    max_wait = 1000