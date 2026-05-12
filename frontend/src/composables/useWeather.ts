import { ref } from 'vue'

export type WeatherCondition = 'clear' | 'clouds' | 'rain' | 'drizzle' | 'thunderstorm' | 'snow' | 'mist'

export interface Weather {
  condition: WeatherCondition
  temp: number
  description: string
  icon: string
  city: string
  dateTime: string
  isDay: boolean
}

const weather = ref<Weather | null>(null)

export function useWeather() {
  async function fetchWeather(lat: number, lng: number) {
    const key = import.meta.env.VITE_OPENWEATHER_KEY
    const url = `https://api.openweathermap.org/data/2.5/weather?lat=${lat}&lon=${lng}&appid=${key}&units=metric&lang=es`
    const res = await fetch(url)
    const data = await res.json()
    const main = data.weather[0].main.toLowerCase() as WeatherCondition
    const now = new Date()
    const dateTime = new Intl.DateTimeFormat('es-ES', {
      weekday: 'short', month: 'short', day: 'numeric',
      hour: 'numeric', minute: '2-digit', hour12: false,
    }).format(now)
    weather.value = {
      condition: main,
      temp: Math.round(data.main.temp),
      description: data.weather[0].description,
      icon: data.weather[0].icon,
      city: data.name,
      dateTime,
      isDay: data.weather[0].icon.includes('d'),
    }
  }

  return { weather, fetchWeather }
}
