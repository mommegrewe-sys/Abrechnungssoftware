import type { Customer, NewCustomer, UpdateCustomer } from "../types/customer";

const API_BASE = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

async function http<T>(url: string, init?: RequestInit): Promise<T> {
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!res.ok) {
    const text = await res.text().catch(() => "");
    throw new Error(`HTTP ${res.status}: ${text || res.statusText}`);
  }
  return (await res.json()) as T;
}

export function fetchCustomers(): Promise<Customer[]> {
  return http<Customer[]>(`${API_BASE}/partners`);
}
export function createCustomer(payload: NewCustomer): Promise<Customer> {
  return http<Customer>(`${API_BASE}/partners`, { method: "POST", body: JSON.stringify(payload) });
}
export function updateCustomer(payload: UpdateCustomer): Promise<Customer> {
  const { id, ...data } = payload;
  return http<Customer>(`${API_BASE}/partners/${id}`, { method: "PUT", body: JSON.stringify(data) });
}
export async function deleteCustomer(id: number): Promise<{ success: boolean }> {
  await http<void>(`${API_BASE}/partners/${id}`, { method: "DELETE" });
  return { success: true };
}
