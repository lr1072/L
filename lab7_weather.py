import requests
import json
from datetime import datetime

# ===================== OpenWeatherMap配置 =====================
API_KEY = "40aec05522b09f45ddeab4c0111edcc9"  
CITY = "Beijing"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
# ==============================================================

def get_weather():
    """获取北京天气数据"""
    params = {
        "q": CITY,
        "appid": API_KEY,
        "units": "metric",      
        "lang": "zh_cn"         
    }
    
    try:
        print(f"🌐 正在查询 {CITY} 的天气...")
        print(f"请求地址: {BASE_URL}")
        print(f"参数: {params}")
        
        response = requests.get(BASE_URL, params=params, timeout=10)
        print(f"状态码: {response.status_code}")
        
        response.raise_for_status()  
        data = response.json()
        
        print("✅ 数据获取成功！")
        return data
        
    except requests.exceptions.Timeout:
        print("❌ 连接超时：服务器响应太慢")
        return None
    except requests.exceptions.ConnectionError:
        print("❌ 连接错误：无法访问网络")
        return None
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            print("❌ API密钥无效，请检查密钥是否正确")
        elif response.status_code == 404:
            print(f"❌ 找不到城市：{CITY}")
        else:
            print(f"❌ HTTP错误: {e}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ 网络请求失败: {e}")
        return None
    except json.JSONDecodeError:
        print("❌ 数据解析失败")
        return None

def show_weather(data):
    """显示北京天气信息（7个字段）"""
    if not data:
        print("没有获取到天气数据")
        return
    
    try:
        print("\n" + "=" * 65)
        print(f"🌍 北京天气查询 - {datetime.now().strftime('%Y年%m月%d日 %H:%M')}")
        print("=" * 65)
        
        # 1. 城市名称
        city_name = data.get('name', '北京')
        country = data.get('sys', {}).get('country', 'CN')
        print(f"📍 城市：{city_name}, {country}")
        
        # 2. 天气状况
        weather = data.get("weather", [{}])[0]
        weather_main = weather.get('main', '未知')
        weather_desc = weather.get('description', '未知')
        print(f"☁️  天气状况：{weather_desc} ({weather_main})")
        
        # 3. 温度（作业要求）
        main = data.get("main", {})
        temp = main.get('temp', '未知')
        feels_like = main.get('feels_like', '未知')
        temp_min = main.get('temp_min', '未知')
        temp_max = main.get('temp_max', '未知')
        print(f"🌡️  当前温度：{temp}°C")
        print(f"   体感温度：{feels_like}°C")
        print(f"   最低温度：{temp_min}°C")
        print(f"   最高温度：{temp_max}°C")
        
        # 4. 湿度（作业要求 - 必须）
        humidity = main.get('humidity', '未知')
        print(f"💧 相对湿度：{humidity}%")
        
        # 5. 气压（作业要求 - 必须）
        pressure = main.get('pressure', '未知')
        print(f"📊 大气压强：{pressure} hPa")
        
        # 6. 风速
        wind = data.get("wind", {})
        wind_speed = wind.get('speed', '未知')
        wind_deg = wind.get('deg', 0)
        
        # 将风向度数转换为方向
        directions = ['北', '东北', '东', '东南', '南', '西南', '西', '西北']
        if wind_deg != '未知' and wind_deg is not None:
            idx = round(wind_deg / 45) % 8
            wind_dir = directions[idx]
        else:
            wind_dir = '未知'
        
        print(f"💨 风速：{wind_speed} m/s")
        print(f"   风向：{wind_dir} ({wind_deg}°)")
        
        # 7. 能见度
        visibility = data.get('visibility')
        if visibility:
            print(f"👁️  能见度：{visibility/1000} km")
        
        # 8. 云量（额外信息）
        clouds = data.get("clouds", {})
        cloudiness = clouds.get('all', '未知')
        print(f"☁️  云量：{cloudiness}%")
        
        # 9. 日出日落（额外信息）
        sys = data.get("sys", {})
        if sys.get("sunrise") and sys.get("sunset"):
            sunrise = datetime.fromtimestamp(sys.get("sunrise")).strftime("%H:%M:%S")
            sunset = datetime.fromtimestamp(sys.get("sunset")).strftime("%H:%M:%S")
            print(f"🌅 日出时间：{sunrise}")
            print(f"🌇 日落时间：{sunset}")
        
        print("=" * 65)
        print(f"📝 数据来源：OpenWeatherMap")
        
    except KeyError as e:
        print(f"❌ 数据格式错误: {e}")
    except Exception as e:
        print(f"❌ 显示数据时出错: {e}")

def main():
    print("=" * 65)
    print("  实验室工作 №7 — OpenWeatherMap 北京天气查询")
    print("=" * 65)
    
    # 检查API密钥
    if API_KEY == "你的OpenWeatherMap密钥" or len(API_KEY) < 10:
        print("❌ API密钥无效！")
        print("   请确认密钥是否正确: 40aec05522b09f45ddeab4c0111edcc9")
        return
    
    weather_data = get_weather()
    show_weather(weather_data)
    
    print("\n" + "=" * 65)
    print("✅ 程序运行完毕")

if __name__ == "__main__":
    main()