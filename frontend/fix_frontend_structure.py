import os
from pathlib import Path

base = Path(__file__).parent
src = base / "src"

folders = ["api", "components", "pages"]
for folder in folders:
    os.makedirs(src / folder, exist_ok=True)

files = {
    "src/api/customers.ts": '''import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/partners",
});

export const getCustomers = () => api.get("/");
export const createCustomer = (data: any) => api.post("/", data);
export const updateCustomer = (id: number, data: any) => api.put(`/${id}`, data);
export const deleteCustomer = (id: number) => api.delete(`/${id}`);
''',

    "src/components/CustomerTable.tsx": '''import React from "react";

interface Customer {
  id: number;
  name: string;
  email_contact?: string;
  city?: string;
  active?: boolean;
}

interface Props {
  customers: Customer[];
  onEdit: (customer: Customer) => void;
  onDelete: (id: number) => void;
}

const CustomerTable: React.FC<Props> = ({ customers, onEdit, onDelete }) => {
  return (
    <table className="min-w-full border border-gray-300 rounded-md mt-6 bg-white shadow">
      <thead className="bg-gray-100">
        <tr>
          <th className="px-4 py-2 text-left">Name</th>
          <th className="px-4 py-2 text-left">Email</th>
          <th className="px-4 py-2 text-left">City</th>
          <th className="px-4 py-2 text-left">Active</th>
          <th className="px-4 py-2 text-left">Actions</th>
        </tr>
      </thead>
      <tbody>
        {customers.map((c) => (
          <tr key={c.id} className="border-t hover:bg-gray-50">
            <td className="px-4 py-2">{c.name}</td>
            <td className="px-4 py-2">{c.email_contact}</td>
            <td className="px-4 py-2">{c.city}</td>
            <td className="px-4 py-2">{c.active ? "✅" : "❌"}</td>
            <td className="px-4 py-2 space-x-2">
              <button
                onClick={() => onEdit(c)}
                className="bg-blue-500 text-white px-2 py-1 rounded hover:bg-blue-600"
              >
                Edit
              </button>
              <button
                onClick={() => onDelete(c.id)}
                className="bg-red-500 text-white px-2 py-1 rounded hover:bg-red-600"
              >
                Delete
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default CustomerTable;
''',

    "src/components/CustomerForm.tsx": '''import React, { useState, useEffect } from "react";

interface Customer {
  id?: number;
  name: string;
  email_contact?: string;
  city?: string;
  active?: boolean;
}

interface Props {
  initialData?: Customer | null;
  onSubmit: (data: Customer) => void;
  onCancel: () => void;
}

const CustomerForm: React.FC<Props> = ({ initialData, onSubmit, onCancel }) => {
  const [form, setForm] = useState<Customer>({
    name: "",
    email_contact: "",
    city: "",
    active: true,
  });

  useEffect(() => {
    if (initialData) setForm(initialData);
  }, [initialData]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    setForm({ ...form, [name]: type === "checkbox" ? checked : value });
  };

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        onSubmit(form);
      }}
      className="bg-white p-4 border rounded shadow mt-4"
    >
      <div className="space-y-3">
        <input
          name="name"
          value={form.name}
          onChange={handleChange}
          placeholder="Name"
          className="border p-2 w-full rounded"
          required
        />
        <input
          name="email_contact"
          value={form.email_contact}
          onChange={handleChange}
          placeholder="Email"
          className="border p-2 w-full rounded"
        />
        <input
          name="city"
          value={form.city}
          onChange={handleChange}
          placeholder="City"
          className="border p-2 w-full rounded"
        />
        <label className="flex items-center space-x-2">
          <input
            type="checkbox"
            name="active"
            checked={form.active}
            onChange={handleChange}
          />
          <span>Active</span>
        </label>
      </div>

      <div className="flex space-x-2 mt-4">
        <button type="submit" className="bg-green-600 text-white px-3 py-1 rounded">
          Save
        </button>
        <button
          type="button"
          onClick={onCancel}
          className="bg-gray-400 text-white px-3 py-1 rounded"
        >
          Cancel
        </button>
      </div>
    </form>
  );
};

export default CustomerForm;
''',

    "src/pages/CustomersPage.tsx": '''import React, { useEffect, useState } from "react";
import { getCustomers, createCustomer, updateCustomer, deleteCustomer } from "../api/customers";
import CustomerTable from "../components/CustomerTable";
import CustomerForm from "../components/CustomerForm";

const CustomersPage: React.FC = () => {
  const [customers, setCustomers] = useState<any[]>([]);
  const [editing, setEditing] = useState<any | null>(null);
  const [showForm, setShowForm] = useState(false);

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

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Customer Management</h1>

      {!showForm && (
        <button
          onClick={() => setShowForm(true)}
          className="bg-blue-600 text-white px-3 py-1 rounded"
        >
          + Add Customer
        </button>
      )}

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
        customers={customers}
        onEdit={(c) => {
          setEditing(c);
          setShowForm(true);
        }}
        onDelete={handleDelete}
      />
    </div>
  );
};

export default CustomersPage;
''',

    "src/App.tsx": '''import CustomersPage from "./pages/CustomersPage";

function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <CustomersPage />
    </div>
  );
}

export default App;
'''
}

for path, content in files.items():
    file_path = base / path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content)

print("✅ Frontend structure fixed! You can now run:")
print("npm run dev")
