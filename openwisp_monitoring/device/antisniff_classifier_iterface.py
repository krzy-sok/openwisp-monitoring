import requests

def get_prediction(device_id, host_ip, avg, median):
    try:
        res = requests.get("http://antisniff:8001/predict")
        return float(res.text)
    except Exception:
        return -1.0