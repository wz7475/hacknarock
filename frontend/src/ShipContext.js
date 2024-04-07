import React, { useState } from 'react'

export const ShipContext = React.createContext(null)

export function ShipContextProvider(props) {
    const [type, setType] = useState('main')
    const [params, setParams] = useState({ instability: 3 })
    return (
        <ShipContext.Provider value={{ type, setType, params, setParams }}>
            {props.children}
        </ShipContext.Provider>
    )
}
