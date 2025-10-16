import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000/partners",
});

export const getCustomers = () => api.get("/");
export const createCustomer = (data: any) => api.post("/", data);
export const updateCustomer = (id: number, data: any) => api.put(`/${id}`, data);
export const deleteCustomer = (id: number) => api.delete(`/${id}`);
