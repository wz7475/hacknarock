import { Box, Button, Fab, Grow, Slide, Typography } from '@mui/material'
import { ToolBar } from './components/Toolbar'
import { createRef, useContext, useEffect, useRef, useState } from 'react'
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward'
import KeyboardArrowLeftIcon from '@mui/icons-material/KeyboardArrowLeft'
import KeyboardArrowRightIcon from '@mui/icons-material/KeyboardArrowRight'
import Picker from 'react-mobile-picker'
import { ShipContext } from './ShipContext'
import { startJourney } from './api/startJourney'

const selections = {
    minutes: Array.from(Array(120).keys()),
    seconds: Array.from(Array(60).keys()),
}

export function Controls(props) {
    const shipContext = useContext(ShipContext)
    const [lastLeftTime, setLastLeftTime] = useState(null)
    const intervalTimer = useRef(null)

    useEffect(() => {
        const interval = setInterval(
            () =>
                setTimeLeft((prevTimeLeft) => {
                    if (prevTimeLeft === 0) {
                        return prevTimeLeft
                    }
                    if (prevTimeLeft > 0) {
                        return prevTimeLeft - 1
                    }
                }),
            1000
        )
        shipContext.setType('main')

        return () => clearInterval(interval)
    }, [])

    window.onblur = function () {
        clearInterval(intervalTimer.current)
        intervalTimer.current = null
        if (shipContext.type === 'ocean') setLastLeftTime(Date.now())
    }

    window.onfocus = function () {
        if (shipContext.type === 'ocean') {
            const timeOutsideApp = Date.now() - lastLeftTime
            shipContext.setParams((oldParams) => ({
                ...oldParams,
                instability: Math.min(
                    oldParams.instability + timeOutsideApp / 10000,
                    10
                ),
            }))
        }

        intervalTimer.current = setInterval(
            () =>
                shipContext.setParams((prevParams) => ({
                    ...prevParams,
                    instability: Math.max(prevParams.instability - 0.5, 3),
                })),
            1000
        )
    }

    const [pickerValue, setPickerValue] = useState({
        minutes: 0,
        seconds: 0,
    })
    const [timeLeft, setTimeLeft] = useState(-1)

    return (
        <Box
            display="flex"
            flexDirection="column"
            height="100%"
        >
            {shipContext.type === 'main' && (
                <Slide
                    direction="down"
                    in={shipContext.type === 'main'}
                >
                    <Box>
                        <ToolBar isLogged={props.isLogged} />
                    </Box>
                </Slide>
            )}
            {shipContext.type === 'port' && (
                <Slide
                    direction="down"
                    in={shipContext.type === 'port'}
                >
                    <Fab
                        size="small"
                        color="primary"
                        onClick={() => shipContext.setType('main')}
                        sx={{ ml: 5, mt: 5 }}
                    >
                        <ArrowUpwardIcon fontSize="small" />
                    </Fab>
                </Slide>
            )}
            {shipContext.type === 'port' && (
                <Box
                    sx={{ width: '32%', ml: 'auto', mr: 'auto', p: 1, mt: 2 }}
                    bgcolor="white"
                    borderRadius="10px"
                >
                    <Typography>Minutes Seconds</Typography>
                    <Picker
                        value={pickerValue}
                        onChange={setPickerValue}
                        height="100"
                    >
                        {Object.keys(selections).map((name) => (
                            <Picker.Column
                                key={name}
                                name={name}
                            >
                                {selections[name].map((option) => (
                                    <Picker.Item
                                        key={option}
                                        value={option}
                                    >
                                        {({ selected }) => (
                                            /* Use the `selected` state ti conditionally style the selected item */
                                            <div
                                                style={{
                                                    fontWeight: selected
                                                        ? 'bold  '
                                                        : 'normal',
                                                    color: selected
                                                        ? 'black'
                                                        : 'grey',
                                                }}
                                            >
                                                {option}
                                            </div>
                                        )}
                                    </Picker.Item>
                                ))}
                            </Picker.Column>
                        ))}
                    </Picker>
                </Box>
            )}
            {shipContext.type === 'ocean' && (
                <Grow in={shipContext.type === 'ocean'}>
                    <Typography
                        sx={{ mt: 10, ml: 'auto', mr: 'auto' }}
                        variant="h1"
                    >
                        {Math.floor(timeLeft / 60)
                            .toString()
                            .padStart(2, '0')}
                        :{(timeLeft % 60).toString().padStart(2, '0')}
                    </Typography>
                </Grow>
            )}
            {shipContext.type === 'failure' && (
                <Grow in={shipContext.type === 'failure'}>
                    <Box sx={{ mt: 5, ml: 'auto', mr: 'auto' }}>
                        <Typography
                            variant="h4"
                            textAlign="center"
                        >
                            Ups.. Your boat sank
                        </Typography>
                        <Typography
                            sx={{ mt: 2 }}
                            variant="h5"
                            textAlign="center"
                        >
                            Don't give up, it will be better next time.
                        </Typography>
                    </Box>
                </Grow>
            )}
            <div
                style={{
                    width: '100vw',
                    flexGrow: 1,
                    display: 'flex',
                    alignItems: 'center',
                }}
            >
                {shipContext.type === 'port' && (
                    <Slide
                        direction="right"
                        in={shipContext.type === 'port'}
                    >
                        <Fab
                            color="primary"
                            size="small"
                            // onClick={() => setshipContext.type("main")}
                            sx={{ ml: 5 }}
                        >
                            <KeyboardArrowLeftIcon />
                        </Fab>
                    </Slide>
                )}

                {shipContext.type === 'port' && (
                    <Slide
                        direction="left"
                        in={shipContext.type === 'port'}
                    >
                        <Fab
                            color="primary"
                            size="small"
                            // onClick={() => pass}
                            sx={{ mr: 5, ml: 'auto' }}
                        >
                            <KeyboardArrowRightIcon />
                        </Fab>
                    </Slide>
                )}
            </div>
            {shipContext.type === 'main' && (
                <Grow in={shipContext.type === 'main'}>
                    <Button
                        variant="contained"
                        sx={{
                            mt: 5,
                            mx: 20,
                            mb: 5,
                        }}
                        onClick={() => shipContext.setType('port')}
                    >
                        START
                    </Button>
                </Grow>
            )}
            {shipContext.type === 'port' && (
                <Grow in={shipContext.type === 'port'}>
                    <Button
                        variant="contained"
                        sx={{
                            mt: 5,
                            mx: 20,
                            mb: 5,
                        }}
                        onClick={() => {
                            shipContext.setType('ocean')
                            startJourney(
                                pickerValue.minutes * 60 + pickerValue.seconds,
                                props.token
                            )
                            setTimeLeft(
                                pickerValue.minutes * 60 + pickerValue.seconds
                            )
                        }}
                    >
                        GO
                    </Button>
                </Grow>
            )}
            {shipContext.type === 'ocean' && (
                <Grow in={shipContext.type === 'ocean'}>
                    <Button
                        variant="contained"
                        sx={{
                            mt: 5,
                            mx: 20,
                            mb: 5,
                        }}
                        onClick={() => shipContext.setType('failure')}
                    >
                        SINK 💀
                    </Button>
                </Grow>
            )}
            {shipContext.type === 'failure' && (
                <Grow in={shipContext.type === 'failure'}>
                    <Button
                        variant="contained"
                        sx={{
                            mt: 5,
                            mx: 20,
                            mb: 5,
                        }}
                        onClick={() => shipContext.setType('main')}
                    >
                        BACK TO MAIN MENU
                    </Button>
                </Grow>
            )}
        </Box>
    )
}
