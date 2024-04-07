import React, { useState } from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'
import Game from './Game'
import reportWebVitals from './reportWebVitals'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import { Friends } from './Friends'
import { Box } from '@mui/material'
import Profile from './Profile'
import SignInPage from './SignInPage'
import SignUpPage from './SignUpPage'
import ShipBackground from './Ships'
import { ShipContextProvider } from './ShipContext'

export default function App() {
    const [token, setToken] = useState(null)

    const router = createBrowserRouter([
        // {
        //   path: "/",
        //   element: <App />,
        // },
        {
            path: '/app',
            element: <Game isLogged={token !== null} />,
        },
        {
            path: '/profile',
            element: <Profile isLogged={token !== null} />,
        },
        {
            path: '/friends',
            element: <Friends isLogged={token !== null} />,
        },
        {
            path: '/sign-in',
            element: (
                <SignInPage
                    isLogged={token !== null}
                    setToken={setToken}
                />
            ),
        },
        {
            path: '/sign-up',
            element: <SignUpPage isLogged={token !== null} />,
        },
    ])

    return (
        <div>
            <ShipContextProvider>
                <Box
                    maxWidth
                    sx={{
                        minHeight: '100vh',
                        zIndex: 0,
                    }}
                >
                    <ShipBackground />
                </Box>
                <RouterProvider router={router} />
            </ShipContextProvider>
        </div>
    )
}
