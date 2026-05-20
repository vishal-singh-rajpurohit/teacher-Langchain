const ANSWER_KEYS = ["answer", "response", "content"] as const

function unescapeAnswerFragment(value: string) {
  return value
    .replace(/\\n/g, "\n")
    .replace(/\\"/g, '"')
    .replace(/\\\\/g, "\\")
}

export function cleanAssistantResponse(message: string) {
  const text = message.trim()
  if (!text) return message

  try {
    const parsed = JSON.parse(text) as unknown

    if (parsed && typeof parsed === "object" && !Array.isArray(parsed)) {
      const record = parsed as Partial<Record<(typeof ANSWER_KEYS)[number], unknown>>

      for (const key of ANSWER_KEYS) {
        const value = record[key]
        if (typeof value === "string") return value.trim()
      }
    }
  } catch {
    // Older streamed responses may be an unfinished JSON object while tokens arrive.
  }

  const match = text.match(/^\{\s*"?(answer|response|content)"?\s*:\s*"/i)
  if (!match || match.index !== 0) return message

  const answerStart = match[0].length
  const answer = text.slice(answerStart).replace(/"\s*\}\s*$/, "")
  return unescapeAnswerFragment(answer).trim()
}
