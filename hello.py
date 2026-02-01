import json
from pathlib import Path
import urllib.error
import urllib.request
from datetime import datetime
from sys import version


WEATHER_CODE_MAP = {
    0: "晴朗",
    1: "大部晴朗",
    2: "局部多云",
    3: "阴",
    45: "有雾",
    48: "霜雾",
    51: "小毛毛雨",
    53: "中等毛毛雨",
    55: "密集毛毛雨",
    56: "轻度冻毛毛雨",
    57: "密集冻毛毛雨",
    61: "小雨",
    63: "中雨",
    65: "大雨",
    66: "轻度冻雨",
    67: "大冻雨",
    71: "小雪",
    73: "中雪",
    75: "大雪",
    77: "雪粒",
    80: "小阵雨",
    81: "中阵雨",
    82: "强阵雨",
    85: "小阵雪",
    86: "大阵雪",
    95: "雷暴",
    96: "轻度冰雹雷暴",
    99: "强冰雹雷暴",
}


def _build_weather_result(current):
    temperature = current.get("temperature_2m")
    weather_code = current.get("weathercode")
    time_value = current.get("time")

    if temperature is None or weather_code is None:
        return {"error": "天气数据不完整"}

    description = WEATHER_CODE_MAP.get(weather_code, "未知天气")
    return {
        "temperature": temperature,
        "description": description,
        "time": time_value,
    }


def load_sample_weather(error_message=None):
    """加载示例天气数据作为回退。"""
    sample_path = Path(__file__).with_name("tokyo_weather_sample.json")
    try:
        payload = json.loads(sample_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        message = f"获取天气失败: {error_message or exc}"
        return {"error": message}

    current = payload.get("current", {})
    result = _build_weather_result(current)
    if "error" in result:
        return result

    result["source"] = "sample"
    if error_message:
        result["note"] = f"使用示例数据（原因: {error_message}）"
    return result


def fetch_tokyo_weather():
    """获取东京当前天气信息。"""
    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=35.6762"
        "&longitude=139.6503"
        "&current=temperature_2m,weathercode"
        "&timezone=Asia%2FTokyo"
    )
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, json.JSONDecodeError) as exc:
        return load_sample_weather(str(exc))

    current = payload.get("current", {})
    result = _build_weather_result(current)
    if "error" in result:
        return result

    result["source"] = "live"
    return result


def main():
    """打印Hello World"""
    print("Hello World!")

    # 可选：添加一些额外信息
    print(f"当前时间: {datetime.now()}")
    print(f"Python版本: {version}")

    weather = fetch_tokyo_weather()
    if "error" in weather:
        print(weather["error"])
    else:
        time_label = weather.get("time", "未知时间")
        note = f" {weather['note']}" if weather.get("note") else ""
        source_label = "（实时）" if weather.get("source") == "live" else "（示例）"
        print(
            f"东京天气{source_label}（{time_label}）：{weather['description']}，"
            f"{weather['temperature']}°C{note}"
        )

    return 0

if __name__ == "__main__":
    main()
