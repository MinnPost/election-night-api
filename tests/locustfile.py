"""
Locust.io file for load testing.

Install Locust:
http://docs.locust.io/en/latest/installation.html

Run from this directory with host changing depending on where
the API server is:
locust --host=http://50.19.100.197

Web interface:
http://localhost:8089/
"""

from random import randrange
from locust import HttpLocust, TaskSet, task


class UserBehavior(TaskSet):
  """
  Locust task class.
  """

  query_call = '/?box=ubuntu&method=sql&q=%s'


  def on_start(self):
    """
    on_start is called when a Locust start before any task is scheduled
    """
    # nothing


  @task(10)
  def results_query(self):
    query = 'SELECT * FROM results LIMIT %s' % (randrange(20) + 10)
    self.client.get(self.query_call % (query))


class WebsiteUser(HttpLocust):
  task_set = UserBehavior
  min_wait = 1000
  max_wait = 5000
