import React, { useState } from 'react'

export const ShipContext = React.createContext(null)

export function ShipContextProvider(props) {
    const [type, setType] = useState('main')
    const [params, setParams] = useState({})

    const cameraPosition = {
        main: [0, 0, 0],
        port: [40, 0, 40],
        ocean: [40, 0, 0],
    }[type] || [0, 0, 0]

    const [cameraZoom, setCameraZoom] = useState(80)

    const [boats, setBoats] = useState([[5, 15]])

    return (
        <ShipContext.Provider
            value={{
                type,
                setType,
                params,
                setParams,
                cameraPosition,
                cameraZoom,
                setCameraZoom,
                boats,
            }}
        >
            {props.children}
        </ShipContext.Provider>
    )
}
