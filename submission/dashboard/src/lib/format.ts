export const number = (value: number) => new Intl.NumberFormat("en-US").format(value);
export const currency = (value: number) => new Intl.NumberFormat("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 }).format(value);
export const percent = (value: number) => `${value.toFixed(0)}%`;
export const delta = (value: number, unit = "") => `${value > 0 ? "+" : ""}${value}${unit}`;
