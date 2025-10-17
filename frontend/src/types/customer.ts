export interface Customer {
  id: number;
  name: string;
  email_contact?: string;
  city?: string;
  postal_code?: string;
  street?: string;
  house_number?: string;
  active?: boolean;
  created_at?: string;
  updated_at?: string;
}

export type NewCustomer = Omit<Customer, "id" | "created_at" | "updated_at">;

export type UpdateCustomer = Partial<NewCustomer> & { id: number };
