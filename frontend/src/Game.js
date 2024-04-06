import logo from './logo.svg'
import { ToolBar } from './components/Toolbar'
import { Background } from './Backgrounnd'
import { Box, Button } from '@mui/material'
import { Controls } from './Contorls'
import { useContext, useEffect, useState } from 'react'
import { ShipContext } from './ShipContext'

function Game(props) {
    return (
        <div>
            <Box
                position="absolute"
                top="0px"
                height="100vh"
            >
                <Controls isLogged={props.isLogged} />
            </Box>
        </div>
    )
}

export default Game
