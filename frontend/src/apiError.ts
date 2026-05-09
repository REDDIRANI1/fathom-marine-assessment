import axios from "axios";

export function getApiErrorMessage(error: unknown, fallback: string) {
  if (!axios.isAxiosError(error)) return fallback;

  const detail = error.response?.data?.detail;
  if (typeof detail === "string") return detail;

  if (Array.isArray(detail)) {
    const messages = detail
      .map((item) => (typeof item?.msg === "string" ? item.msg : null))
      .filter((message): message is string => Boolean(message));
    if (messages.length > 0) return messages.join(", ");
  }

  return fallback;
}
