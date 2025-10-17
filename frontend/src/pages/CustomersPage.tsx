import { useEffect, useState } from "react";
import { fetchCustomers, createCustomer, deleteCustomer } from "../api/customers";
import type { Customer, NewCustomer } from "../types/customer";

export default function CustomersPage() {
  const [items, setItems] = useState<Customer[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    fetchCustomers()
      .then(setItems)
      .catch((e: unknown) => setError(e instanceof Error ? e.message : "Unknown error"))
      .finally(() => setLoading(false));
  }, []);

  async function handleAdd(input: NewCustomer) {
    const created = await createCustomer(input);
    setItems((prev) => [created, ...prev]);
  }

  async function handleDelete(id: number) {
    await deleteCustomer(id);
    setItems((prev) => prev.filter((c) => c.id !== id));
  }

  if (loading) return <div>Loading…</div>;
  if (error) return <div>Failed: {error}</div>;

  return (
    <div className="p-4">
      <h1 className="text-xl font-semibold mb-4">Customers</h1>
      <ul className="space-y-2">
        {items.map((c) => (
          <li key={c.id} className="border rounded p-3 flex justify-between">
            <div>
              <div className="font-medium">{c.name}</div>
              {c.email_contact && <div className="text-sm opacity-70">{c.email_contact}</div>}
            </div>
            <button className="text-red-600" onClick={() => handleDelete(c.id)}>
              Delete
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
