import axios, { AxiosError, type AxiosRequestConfig } from "axios";
import { QueryClient } from "@tanstack/react-query";
import { BASE_URL } from "@/constants/api";

export const api = axios.create({
  baseURL: BASE_URL,
  headers: { "Content-Type": "application/json" },
});

api.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    // eslint-disable-next-line no-console
    console.error(
      "[API ERROR]",
      error.config?.method?.toUpperCase(),
      error.config?.url,
      error.response?.status,
      error.response?.data ?? error.message,
    );
    return Promise.reject(error);
  },
);

export async function get<T>(url: string, config?: AxiosRequestConfig): Promise<T> {
  const res = await api.get<T>(url, config);
  return res.data;
}

export async function post<T>(
  url: string,
  body?: unknown,
  config?: AxiosRequestConfig,
): Promise<T> {
  const res = await api.post<T>(url, body, config);
  return res.data;
}

export async function postForm<T>(
  url: string,
  formData: FormData,
  config?: AxiosRequestConfig,
): Promise<T> {
  const res = await api.post<T>(url, formData, {
    ...config,
    headers: {
      ...(config?.headers ?? {}),
      "Content-Type": "multipart/form-data",
    },
  });
  return res.data;
}

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
      staleTime: 30_000,
    },
  },
});
