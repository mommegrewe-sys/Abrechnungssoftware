import React, { useEffect, useState } from "react";
import {
  getCustomers,
  createCustomer,
  updateCustomer,
  deleteCustomer,
} from "../api/customers";
import CustomerTable from "../components/CustomerTable";
import CustomerForm from "../components/CustomerForm";

const CustomersPage: React.FC = () => {
  const [customers, setCustomers] = useState<any[]>([]);
  const [editing, setEditing] = useState<any | null>(null);
  const [showForm, setShowForm] = useState(false);
  const [filterActive, setFilterActive] = useState(false);

  const loadCustomers = async () => {
    const res = await getCustomers();
    setCustomers(res.data);
  };

  useEffect(() => {
    loadCustomers();
  }, []);

  const handleSave = async (data: any) => {
    if (editing) {
      await updateCustomer(editing.id, data);
    } else {
      await createCustomer(data);
    }
    setEditing(null);
    setShowForm(false);
    loadCustomers();
  };

  const handleDelete = async (id: number) => {
    await deleteCustomer(id);
    loadCustomers();
  };

  const filtered = filterActive
    ? customers.filter((c) => c.active)
    : customers;

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-200 py-10 px-4">
      {/* Header */}
      <header className="max-w-5xl mx-auto mb-8 text-center">
        <h1 className="text-4xl font-bold text-gray-800 mb-2">
          Kundenverwaltung
        </h1>
        <p className="text-gray-600">
          Erstellen, bearbeiten und verwalten Sie Ihre Kunden einfach.
        </p>
      </header>

      {/* Hauptbereich */}
      <main className="max-w-5xl mx-auto bg-white rounded-2xl shadow-lg p-8">
        <div className="flex justify-between items-center mb-6">
          {!showForm && (
            <button
              onClick={() => setShowForm(true)}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg shadow hover:bg-blue-700 transition"
            >
              + Neuer Kunde
            </button>
          )}
          <label className="flex items-center space-x-2 text-sm text-gray-700">
            <input
              type="checkbox"
              checked={filterActive}
              onChange={(e) => setFilterActive(e.target.checked)}
              className="accent-blue-600"
            />
            <span>Nur aktive Kunden anzeigen</span>
          </label>
        </div>

        {showForm && (
          <CustomerForm
            initialData={editing}
            onSubmit={handleSave}
            onCancel={() => {
              setEditing(null);
              setShowForm(false);
            }}
          />
        )}

        <CustomerTable
          customers={filtered}
          onEdit={(c) => {
            setEditing(c);
            setShowForm(true);
          }}
          onDelete={handleDelete}
        />
      </main>
    </div>
  );
};

export default CustomersPage;
