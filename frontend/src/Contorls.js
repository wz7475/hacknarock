import { Box, Button, Fab, Grow, Slide, Typography } from '@mui/material'
import { ToolBar } from './components/Toolbar'
import { useEffect, useState } from 'react'
import ArrowUpwardIcon from '@mui/icons-material/ArrowUpward'
import KeyboardArrowLeftIcon from '@mui/icons-material/KeyboardArrowLeft'
import KeyboardArrowRightIcon from '@mui/icons-material/KeyboardArrowRight'
import Picker from 'react-mobile-picker'

const selections = {
    minutes: Array.from(Array(120).keys()),
    seconds: Array.from(Array(60).keys()),
}

export function Controls(props) {
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

        return () => clearInterval(interval)
    }, [])

    const [screen, setScreen] = useState('BasePage')
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
            {screen === 'BasePage' && (
                <Slide
                    direction="down"
                    in={screen === 'BasePage'}
                >
                    <Box>
                        <ToolBar isLogged={props.isLogged} />
                    </Box>
                </Slide>
            )}
            {screen === 'StartPage' && (
                <Slide
                    direction="down"
                    in={screen === 'StartPage'}
                >
                    <Fab
                        size="small"
                        color="primary"
                        onClick={() => setScreen('BasePage')}
                        sx={{ ml: 5, mt: 5 }}
                    >
                        <ArrowUpwardIcon fontSize="small" />
                    </Fab>
                </Slide>
            )}
            {screen === 'StartPage' && (
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
            {screen === 'CruisePage' && (
                <Grow in={screen === 'CruisePage'}>
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
            {screen === 'FailurePage' && (
                <Grow in={screen === 'FailurePage'}>
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
                {screen === 'StartPage' && (
                    <Slide
                        direction="right"
                        in={screen === 'StartPage'}
                    >
                        <Fab
                            color="primary"
                            size="small"
                            // onClick={() => setScreen("BasePage")}
                            sx={{ ml: 5 }}
                        >
                            <KeyboardArrowLeftIcon />
                        </Fab>
                    </Slide>
                )}

                {screen === 'StartPage' && (
                    <Slide
                        direction="left"
                        in={screen === 'StartPage'}
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
            {screen === 'BasePage' && (
                <Grow in={screen === 'BasePage'}>
                    <Button
                        variant="contained"
                        sx={{
                            mt: 5,
                            mx: 20,
                            mb: 5,
                        }}
                        onClick={() => setScreen('StartPage')}
                    >
                        START
                    </Button>
                </Grow>
            )}
            {screen === 'StartPage' && (
                <Grow in={screen === 'StartPage'}>
                    <Button
                        variant="contained"
                        sx={{
                            mt: 5,
                            mx: 20,
                            mb: 5,
                        }}
                        onClick={() => {
                            setScreen('CruisePage')
                            setTimeLeft(
                                pickerValue.minutes * 60 + pickerValue.seconds
                            )
                        }}
                    >
                        GO
                    </Button>
                </Grow>
            )}
            {screen === 'CruisePage' && (
                <Grow in={screen === 'CruisePage'}>
                    <Button
                        variant="contained"
                        sx={{
                            mt: 5,
                            mx: 20,
                            mb: 5,
                        }}
                        onClick={() => setScreen('FailurePage')}
                    >
                        SINK 💀
                    </Button>
                </Grow>
            )}
            {screen === 'FailurePage' && (
                <Grow in={screen === 'FailurePage'}>
                    <Button
                        variant="contained"
                        sx={{
                            mt: 5,
                            mx: 20,
                            mb: 5,
                        }}
                        onClick={() => setScreen('BasePage')}
                    >
                        BACK TO MAIN MENU
                    </Button>
                </Grow>
            )}
        </Box>
    )
}
