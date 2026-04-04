import requests

def get_prediction(device_id, host_ip, avg, median, flood_flag):
    try:
        res = requests.post("http://antisniff:8001/predict", json={"rtt_avg": avg, "rtt_median": median, "flood_flag": flood_flag})
        return float(res.text)
    except Exception:
        return -1.0