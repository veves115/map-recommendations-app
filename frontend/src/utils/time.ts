/**
 * Devuelve un string legible de tiempo transcurrido desde una fecha ISO.
 * Ej: "hace 5 segundos", "hace 2 minutos", "hace 1 hora".
 */
export function relativeTime(iso: string): string {
  const ms = Date.now() - new Date(iso).getTime()
  const seconds = Math.floor(ms / 1000)

  if (seconds < 5) return 'ahora'
  if (seconds < 60) return `hace ${seconds} segundos`

  const minutes = Math.floor(seconds / 60)
  if (minutes === 1) return 'hace 1 minuto'
  if (minutes < 60) return `hace ${minutes} minutos`

  const hours = Math.floor(minutes / 60)
  if (hours === 1) return 'hace 1 hora'
  return `hace ${hours} horas`
}
