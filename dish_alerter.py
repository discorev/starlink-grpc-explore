import asyncio
import time
from datetime import datetime

from alerts import check_for_alerts

start_time = time.time()

ALERTS = dict()


async def check_alerts():
    global ALERTS
    next_alerts = check_for_alerts()
    for key in ALERTS.keys():
        if key not in next_alerts:
            print(datetime.now(), key, "recovered")
    diff_set = {
        k: next_alerts[k] for k, _ in set(next_alerts.items()) - set(ALERTS.items())
    }
    for item in diff_set.keys():
        if isinstance(diff_set[item], float):
            print(datetime.now(), item, f"{diff_set[item]:.3f}")
        else:
            print(datetime.now(), item, diff_set[item])
    ALERTS = dict(next_alerts)


async def do_stuff_periodically(interval, periodic_function, *args):
    async def run_with_catch():
        try:
            await periodic_function(*args)
        except Exception:
            pass

    while True:
        # print(round(time.time() - start_time, 1), "Starting periodic function")
        await asyncio.gather(
            asyncio.sleep(interval),
            run_with_catch(),
        )

if __name__ == "__main__":
    print('\033c')
    alerts = {}
    asyncio.run(do_stuff_periodically(1, check_alerts))
