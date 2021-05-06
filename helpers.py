def seconds_to_human_friendly(seconds: int) -> str:
    output = []
    if seconds >= 86400:
        days = seconds // 86400
        output.append(f"{days} days" if days > 1 else "1 day")
        seconds = seconds - (days * 86400) 
    if seconds >= 3600:
        hours = seconds // 3600
        output.append(f"{hours} hours" if hours > 1 else "1 hour")
        seconds = seconds - (hours * 3600)
    if seconds >= 60:
        minutes = seconds // 60
        output.append(f"{minutes} minutes" if minutes > 1 else "1 minute")
        seconds = seconds - (minutes * 60)
    with_s = "s" if seconds != 1 else ""
    output.append(f"{seconds} second{with_s}")
    return ', '.join(output)


def bitrate_to_human_friendly(bitrate: float) -> str:
    units = ['bps', 'Kbps', 'Mbps', 'Gbps', 'Tbps']
    i = 0
    while bitrate > 1000:
        bitrate = bitrate / 1024
        i = i + 1
    return f"{bitrate:.2f} {units[i]}"
