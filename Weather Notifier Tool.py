import requests
import time

API_KEY = "your_openweathermap_api_key"  # 替换为你的OpenWeatherMap API密钥
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    try:
        params = {"q": city, "appid": API_KEY, "units": "metric", "lang": "zh_cn"}
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"获取天气数据失败：{e}")
        return None

def check_weather_condition(weather_data, condition):
    if weather_data:
        weather_desc = weather_data["weather"][0]["description"]
        return condition.lower() in weather_desc.lower()
    return False

def weather_notifier(city, condition, interval=60):
    print(f"正在监控 {city} 的天气情况，当满足条件“{condition}”时将通知您。")
    while True:
        weather_data = get_weather(city)
        if weather_data:
            temp = weather_data["main"]["temp"]
            desc = weather_data["weather"][0]["description"]
            print(f"当前温度：{temp}°C，天气：{desc}")
            if check_weather_condition(weather_data, condition):
                print(f"提醒：当前天气符合条件“{condition}”！")
                break
        else:
            print("无法获取天气数据，请检查网络或API配置。")
        time.sleep(interval)

if __name__ == "__main__":
    print("欢迎使用天气通知工具！")

    city = input("请输入城市名称：")
    condition = input("请输入天气条件（例如：雨、晴、雪）：")
    try:
        interval = int(input("请输入检查天气的间隔时间（秒）："))
    except ValueError:
        interval = 60
        print("输入无效，使用默认间隔时间 60 秒。")

    weather_notifier(city, condition, interval)
