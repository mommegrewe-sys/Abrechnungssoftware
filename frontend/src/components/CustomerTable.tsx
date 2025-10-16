import React from "react";
import { Pencil, Trash2 } from "lucide-react";

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
    <div className="overflow-x-auto rounded-lg border border-gray-200 shadow-sm">
      <table className="w-full text-left border-collapse">
        <thead className="bg-gray-100">
          <tr>
            <th className="px-4 py-2 font-semibold text-gray-600">Name</th>
            <th className="px-4 py-2 font-semibold text-gray-600">E-Mail</th>
            <th className="px-4 py-2 font-semibold text-gray-600">Stadt</th>
            <th className="px-4 py-2 font-semibold text-gray-600">Status</th>
            <th className="px-4 py-2 text-right font-semibold text-gray-600">
              Aktionen
            </th>
          </tr>
        </thead>
        <tbody>
          {customers.map((c) => (
            <tr
              key={c.id}
              className="border-t hover:bg-gray-50 transition-colors"
            >
              <td className="px-4 py-2">{c.name}</td>
              <td className="px-4 py-2">{c.email_contact}</td>
              <td className="px-4 py-2">{c.city}</td>
              <td className="px-4 py-2">
                {c.active ? (
                  <span className="text-green-600 font-medium">Aktiv</span>
                ) : (
                  <span className="text-red-500 font-medium">Inaktiv</span>
                )}
              </td>
              <td className="px-4 py-2 text-right space-x-2">
                <button
                  onClick={() => onEdit(c)}
                  className="p-1 text-blue-600 hover:text-blue-800"
                  title="Bearbeiten"
                >
                  <Pencil size={18} />
                </button>
                <button
                  onClick={() => onDelete(c.id)}
                  className="p-1 text-red-500 hover:text-red-700"
                  title="Löschen"
                >
                  <Trash2 size={18} />
                </button>
              </td>
            </tr>
          ))}
          {customers.length === 0 && (
            <tr>
              <td
                colSpan={5}
                className="px-4 py-6 text-center text-gray-500 italic"
              >
                Keine Kunden vorhanden.
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
};

export default CustomerTable;
