"""
tasks.__init__.py
Support long-running distributed tasks
"""

from celery import Celery

celery = Celery("spinneret")

def __init_app(app):
  celery.config_from_object(app.config)
  TaskBase = celery.Task
  class ContextTask(TaskBase):
    """ContextTask from Flask Documentation"""
    abstract = True
    def __call__(self, *args, **kwargs):
      with app.app_context():
        return TaskBase.__call__(self, *args, **kwargs)
  celery.Task = ContextTask

celery.init_app = __init_app

def batch_iter(iterable, batch_items):
  """
  batch iterables, trying to return the same type as passed in
  works best on types that extend the builtin collections, but will work on
  any iterable type that accepts lists as a solitary constructor parameter
  """
  in_type = type(iterable)
  try:
    if isinstance(iterable, dict):
      iterable = iter(iterable.items())
    while True:
      batched = []
      while len(batched) < batch_items:
        batched.append(next(iterable))
      yield in_type(batched)
  except StopIteration:
    pass
