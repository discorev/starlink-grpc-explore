import grpc
import asyncio
import time

from spacex.api.device import device_pb2
from spacex.api.device import device_pb2_grpc
from spacex.api.device import dish_pb2

import helpers

start_time = time.time()


async def print_status():
    with grpc.insecure_channel("192.168.100.1:9200") as channel:
        stub = device_pb2_grpc.DeviceStub(channel)
        response = stub.Handle(device_pb2.Request(get_status={}))
        context_response = stub.Handle(device_pb2.Request(dish_get_context={}))


    uptime = helpers.seconds_to_human_friendly(
        response.dish_get_status.device_state.uptime_s
    )
    state = dish_pb2.DishState.Name(response.dish_get_status.state)

    pad = 32
    print('\033c')
    print(f"{'Uptime':<{pad}} {uptime}")
    print(f"{'Device id':<{pad}} {response.dish_get_status.device_info.id}")
    print(
        f"{'Hardware version':<{pad}} {response.dish_get_status.device_info.hardware_version}"
    )
    print(
        f"{'Software version':<{pad}} {response.dish_get_status.device_info.software_version}"
    )
    print(f"{'Country code':<{pad}} {response.dish_get_status.device_info.country_code}")
    print(f"{'Status':<{pad}} {state}")
    print(f"{'SNR':<{pad}} {response.dish_get_status.snr}")
    print(
        f"{'Downlink usage':<{pad}} {helpers.bitrate_to_human_friendly(response.dish_get_status.downlink_throughput_bps)}"
    )
    print(
        f"{'Upload usage':<{pad}} {helpers.bitrate_to_human_friendly(response.dish_get_status.uplink_throughput_bps)}"
    )

    print(f"{'POP rack id':<{pad}} {context_response.dish_get_context.pop_rack_id}")
    print(f"{'POP ping drop rate':<{pad}} {(response.dish_get_status.pop_ping_drop_rate * 100):.3f}")
    print(
        f"{'POP ping latency':<{pad}} {response.dish_get_status.pop_ping_latency_ms:.2f} ms"
    )

    print(f"{'Cell id':<{pad}} {context_response.dish_get_context.cell_id}")
    print(
        f"{'Seconds to slot end':<{pad}} {context_response.dish_get_context.seconds_to_slot_end:.3f}"
    )
    print(
        f"{'Seconds to first no-empty slot':<{pad}} {response.dish_get_status.seconds_to_first_nonempty_slot}"
    )

    print(
        f"{'Currently obstructed':<{pad}} {response.dish_get_status.obstruction_stats.currently_obstructed}"
    )
    # print(context_response)

async def do_stuff_periodically(interval, periodic_function, *args):
    async def run_with_catch():
        try:
            await periodic_function(*args)
        except Exception:
            pass
        
    while True:
        await asyncio.gather(
            asyncio.sleep(interval),
            run_with_catch()
        )

if __name__ == "__main__":
    asyncio.run(do_stuff_periodically(1, print_status))
