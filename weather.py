import json
import urllib.error
import urllib.request


def fetch_bangalore_weather() -> str:
    url = "https://wttr.in/Bangalore?format=j1"

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.load(response)
    except (urllib.error.URLError, urllib.error.HTTPError) as exc:
        return f"Could not fetch weather data: {exc}"
    except Exception as exc:  # noqa: BLE001
        return f"Unexpected error while fetching weather data: {exc}"

    try:
        current = data["current_condition"][0]
        temp_c = current["temp_C"]
        feels_like_c = current["FeelsLikeC"]
        description = current["weatherDesc"][0]["value"]
    except (KeyError, IndexError, TypeError) as exc:
        return f"Received unexpected data format: {exc}"

    return (
        f"Current weather in Bangalore: {description}, "
        f"{temp_c}°C (feels like {feels_like_c}°C)."
    )


def main() -> None:
    message = fetch_bangalore_weather()
    print(message)


if __name__ == "__main__":
    main()

