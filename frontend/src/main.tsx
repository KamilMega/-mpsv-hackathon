import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.scss";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { AppLayout } from "./components/common/AppLayout";
import ErrorPage from "./components/common/ErrorPage";
import { VolnaMista } from "./components/volnaMista";
import { VolneMistoDetail } from "./components/volnaMista/detail/VolneMistoDetail";

const queryClient = new QueryClient();

const router = createBrowserRouter([
  {
    element: <AppLayout />,
    errorElement: <ErrorPage />,
    children: [
      {
        path: "/volna-mista",
        element: <VolnaMista />,
        errorElement: <ErrorPage />,
      },
      {
        path: "/volna-mista/:id",
        element: <VolneMistoDetail />,
        errorElement: <ErrorPage />,
      },
    ],
  },
]);

// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
window.GOV_DS_CONFIG = {
  iconsLazyLoad: false,
  iconsPath: "/assets/icons",
};

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <RouterProvider router={router} />
    </QueryClientProvider>
  </StrictMode>
);
