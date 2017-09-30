from django_cron import CronJobBase, Schedule


class UpdateScoresJob(CronJobBase):
    RUN_EVERY_MINS = 120 # every 2 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'ffooty.cron.UpdateScoresJob'

    def do(self):
        pass    # do your thing here
