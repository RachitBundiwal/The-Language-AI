import type { ReactNode } from "react";
import { Sidebar } from "./Sidebar";
import { TopBar } from "./TopBar";

interface Props {
  children: ReactNode;
}

export function Layout({ children }: Props) {
  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-950 dark:text-gray-100">
      <Sidebar />
      <div className="md:pl-60">
        <TopBar />
        <main className="px-4 pb-20 pt-6 md:px-8 md:pb-8">{children}</main>
      </div>
    </div>
  );
}
