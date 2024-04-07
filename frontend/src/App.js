import React, { useEffect, useState } from 'react'
import ReactDOM from 'react-dom/client'
import './index.css'
import Game from './Game'
import reportWebVitals from './reportWebVitals'
import {
    createBrowserRouter,
    Navigate,
    RouterProvider,
    useNavigate,
} from 'react-router-dom'
import { Friends } from './Friends'
import { Box } from '@mui/material'
import Profile from './Profile'
import SignInPage from './SignInPage'
import SignUpPage from './SignUpPage'
import ShipBackground from './Ships'
import { ShipContextProvider } from './ShipContext'
import { verifyUser } from './api/verifyUser'
import Cookie from 'js-cookie'
import { amber } from '@mui/material/colors'
import { ThemeProvider, createTheme } from '@mui/material/styles'

export default function App() {
    useEffect(() => {
        const fetchData = async () => {
            const userData = await verifyUser()
            if (userData.hasOwnProperty('nick')) {
                setToken('pla')
            } else {
                Cookie.remove('jwt_cookie', { path: '/' })
            }
            setisLoading(false)
        }
        fetchData()
    }, [])

    const [token, setToken] = useState(null)
    const [isLoading, setisLoading] = useState(true)
    const theme = createTheme({
        palette: {
            mode: 'light',
            primary: {
                main: amber[700],
            },
            secondary: {
                main: '#f50057',
            },
        },
    })

    const router = createBrowserRouter([
        // {
        //   path: "/",
        //   element: <App />,
        // },
        {
            path: '/app',
            element: (
                <Game
                    token={token}
                    isLogged={token !== null}
                />
            ),
        },
        {
            path: '/profile',
            element: (
                <Profile
                    isLogged={token !== null}
                    logOut={() => {
                        Cookie.remove('jwt_cookie', { path: '/' })
                        setToken(null)
                    }}
                />
            ),
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
            {!isLoading && (
                <ThemeProvider theme={theme}>
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
                </ThemeProvider>
            )}
        </div>
    )
}
