const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

type RequestOptions = {
  method?: string;
  body?: unknown;
  token?: string;
};

async function request<T>(endpoint: string, options: RequestOptions = {}): Promise<T> {
  const { method = "GET", body, token } = options;
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_URL}/api/v1${endpoint}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });

  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: "Something went wrong" }));
    throw new Error(error.detail || `HTTP ${res.status}`);
  }

  return res.json();
}

export const api = {
  register(data: { email: string; password: string; full_name: string }) {
    return request<import("@/types/api").UserResponse>("/user/register", {
      method: "POST",
      body: data,
    });
  },

  login(email: string, password: string) {
    const formData = new URLSearchParams();
    formData.append("username", email);
    formData.append("password", password);

    return fetch(`${API_URL}/api/v1/user/login`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body: formData,
    }).then(async (res) => {
      if (!res.ok) {
        const error = await res.json().catch(() => ({ detail: "Login failed" }));
        throw new Error(error.detail || `HTTP ${res.status}`);
      }
      return res.json() as Promise<import("@/types/api").Token>;
    });
  },

  getMe(token: string) {
    return request<import("@/types/api").UserResponse>("/user/me", { token });
  },

  healthCheck() {
    return request<{ status: string }>("/health");
  },
};
