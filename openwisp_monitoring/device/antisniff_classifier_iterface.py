import requests

def get_prediction(device_id, host_ip, avg, median, flood_flag, max_diff):
    try:
        res = requests.post(
            "http://antisniff:8001/predict",
            json={
                "rtt_avg": avg,
                "rtt_median": median,
                "flood_flag": flood_flag,
                "max_diff": max_diff,
                "device": device_id,
                "ip": host_ip
            })
        data = res.json()
        return (data["sniffing"], data['computer_type'])
        # return float(res.text)
    except Exception as ex:
        print(ex)
        return (-0.1, "exception")