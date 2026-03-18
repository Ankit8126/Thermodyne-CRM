"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { api } from "@/lib/api";
import type { UserResponse } from "@/types/api";

export default function HomePage() {
  const router = useRouter();
  const [user, setUser] = useState<UserResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.push("/login");
      return;
    }
    api
      .getMe(token)
      .then(setUser)
      .catch(() => {
        localStorage.removeItem("token");
        router.push("/login");
      })
      .finally(() => setLoading(false));
  }, [router]);

  function handleLogout() {
    localStorage.removeItem("token");
    router.push("/login");
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-950">
        <div className="text-gray-500 dark:text-gray-400">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950">
      <nav className="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between h-16 items-center">
            <h1 className="text-xl font-bold text-gray-900 dark:text-white">
              Thermodyne CRM
            </h1>
            <div className="flex items-center gap-4">
              <span className="text-sm text-gray-600 dark:text-gray-400">
                {user?.full_name}
              </span>
              <button
                onClick={handleLogout}
                className="text-sm text-red-600 hover:text-red-500 font-medium cursor-pointer"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="bg-white dark:bg-gray-900 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-800 p-6">
            <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">
              Welcome
            </h3>
            <p className="mt-2 text-2xl font-semibold text-gray-900 dark:text-white">
              {user?.full_name}
            </p>
            <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
              {user?.email}
            </p>
          </div>

          <div className="bg-white dark:bg-gray-900 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-800 p-6">
            <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">
              Account Status
            </h3>
            <p className="mt-2 text-2xl font-semibold text-green-600">Active</p>
            <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
              Member since {user ? new Date(user.created_at).toLocaleDateString() : ""}
            </p>
          </div>

          <div className="bg-white dark:bg-gray-900 rounded-2xl shadow-sm border border-gray-200 dark:border-gray-800 p-6">
            <h3 className="text-sm font-medium text-gray-500 dark:text-gray-400">
              Quick Actions
            </h3>
            <div className="mt-3 space-y-2">
              <p className="text-sm text-gray-600 dark:text-gray-400">
                Dashboard modules coming soon...
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
