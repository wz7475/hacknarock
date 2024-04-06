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

export default function App() {
    const [isLogged, setIsLogged] = useState(true)

    const router = createBrowserRouter([
        // {
        //   path: "/",
        //   element: <App />,
        // },
        {
            path: '/app',
            element: <Game isLogged={isLogged} />,
        },
        {
            path: '/profile',
            element: <Profile isLogged={isLogged} />,
        },
        {
            path: '/friends',
            element: <Friends isLogged={isLogged} />,
        },
        {
            path: '/sign-in',
            element: <SignInPage isLogged={isLogged} />,
        },
        {
            path: '/sign-up',
            element: <SignUpPage isLogged={isLogged} />,
        },
    ])

    return (
        <div>
            <Box
                maxWidth
                sx={{
                    minHeight: '100vh',
                    zIndex: 0,
                }}
            >
                <ShipBackground />
            </Box>
            <RouterProvider router={router} />{' '}
        </div>
    )
}
