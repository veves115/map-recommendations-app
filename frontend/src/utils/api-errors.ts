const typeMessages: Record<string, string> = {
  string_pattern_mismatch: 'Solo se permiten letras, números, guiones bajos y guiones medios.',
  string_too_short: 'Demasiado corto.',
  string_too_long: 'Demasiado largo.',
  value_error: 'Valor no válido.',
  missing: 'Campo obligatorio.',
}

export function formatApiError(e: unknown, fallback: string): string {
  const err = e as { response?: { data?: { detail?: string | Array<{ type: string; msg: string }> } } }
  const detail = err?.response?.data?.detail
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail)) {
    return detail.map((d) => typeMessages[d.type] ?? d.msg).join(', ')
  }
  return fallback
}
