import React, { useState, useEffect } from "react";

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
