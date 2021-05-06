import grpc

from spacex.api.device import device_pb2
from spacex.api.device import device_pb2_grpc
from spacex.api.device import dish_pb2

import helpers


def check_for_alerts():
    try:
        with grpc.insecure_channel("192.168.100.1:9200") as channel:
            stub = device_pb2_grpc.DeviceStub(channel)
            response = stub.Handle(device_pb2.Request(get_status={}))
    except Exception:
        return {"GRPC Error": True}

    alerts = {}

    for field in dish_pb2._DISHALERTS.fields_by_name:
        if getattr(response.dish_get_status.alerts, field):
            if "general" not in alerts:
                alerts["general"] = [field]
            else:
                alerts["general"].append(field)

    if response.dish_get_status.state != dish_pb2.DishState.CONNECTED:
        state = dish_pb2.DishState.Name(response.dish_get_status.state)
        alerts["state"] = state

    if response.dish_get_status.snr < 9.0:
        alerts["SNR low"] = response.dish_get_status.snr

    if response.dish_get_status.pop_ping_drop_rate >= 0.5:
        alerts["POP ping drop rate"] = response.dish_get_status.pop_ping_drop_rate

    if response.dish_get_status.seconds_to_first_nonempty_slot > 0.0:
        alerts[
            "Seconds to first non-empty slot"
        ] = response.dish_get_status.seconds_to_first_nonempty_slot

    if response.dish_get_status.obstruction_stats.currently_obstructed:
        alerts["Currently obstructed"] = True

    return alerts
