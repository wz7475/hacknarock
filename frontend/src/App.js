import React, { useState } from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import Game from "./Game";
import reportWebVitals from "./reportWebVitals";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import { Friends } from "./Friends";
import { Box } from "@mui/material";
import SignIn from "./SignIn";
import SignInPage from "./SignInPage";
import SignUpPage from "./SignUpPage";

export default function App() {
  const [isLogged, setIsLogged] = useState(false);

  const router = createBrowserRouter([
    // {
    //   path: "/",
    //   element: <App />,
    // },
    {
      path: "/app",
      element: <Game isLogged={isLogged} />,
    },
    //   {
    //     path: "/profile",
    //     element: <App isLogged={isLogged} />,
    //   },
    {
      path: "/friends",
      element: <Friends isLogged={isLogged} />,
    },
    {
      path: "/sign-in",
      element: <SignInPage isLogged={isLogged} />,
    },
    {
      path: "/sign-up",
      element: <SignUpPage isLogged={isLogged} />,
    },
  ]);

  return <RouterProvider router={router} />;
}
