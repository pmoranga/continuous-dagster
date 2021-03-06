from dagster import RepositoryDefinition, pipeline, solid
from dagster import schedules, ScheduleDefinition, hourly_schedule
from dagster_cron import SystemCronScheduler
import datetime


@schedules
def define_scheduler():
    def create_hello_world_schedule(name):
        return ScheduleDefinition(
            name=name,
            cron_schedule="* * * * *",
            pipeline_name="hello_world_pipeline",
            environment_dict={},
        )

    hello_world_every_minute = ScheduleDefinition(
        name="hello_world_every_minute",
        cron_schedule="* * * * *",
        pipeline_name="hello_world_pipeline",
        environment_dict={},
    )

    goodbye_world_every_minute = ScheduleDefinition(
        name="goodbye_world_every_minute",
        cron_schedule="* * * * *",
        pipeline_name="goodbye_world_pipeline",
        environment_dict={},
    )

    long_running_every_hour = ScheduleDefinition(
        name="long_running_every_hour",
        cron_schedule="0 * * * *",
        pipeline_name="long_running_pipeline",
        environment_dict={},
    )

    s = [create_hello_world_schedule("hello_world_{i}".format(i=i)) for i in range(10)]
    s.extend([hello_world_every_minute, goodbye_world_every_minute, long_running_every_hour])
    return s


@solid
def hello_world(context):
    context.log.info('Hello, world!')


@pipeline
def hello_world_pipeline():
    hello_world()


@solid
def goodbye_world(context):
    context.log.info('Goodbye, world!')


@pipeline
def goodbye_world_pipeline():
    goodbye_world()


import time


@solid
def long_three(_):
    time.sleep(60 * 60)  # 1 hour
    return 1


@solid
def long_two(_, number):
    time.sleep(60 * 60)  # 1 hour
    return number + 1


@solid
def long_one(context, number):
    time.sleep(60 * 60)  # 1 hour
    context.log.info(str(number + 1))
    return number + 1


@pipeline
def long_running_pipeline():
    long_one(long_two(long_three()))


def define_repo():
    return RepositoryDefinition(
        name='scheduler_demo_repository',
        pipeline_defs=[hello_world_pipeline, goodbye_world_pipeline, long_running_pipeline],
    )
