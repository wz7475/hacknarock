import { Box } from '@mui/material'
import SignIn from './SignIn'
import { ToolBar } from './components/Toolbar'

export default function SignInPage(props) {
    return (
        <div>
            <Box
                position="absolute"
                top="0px"
                width="100%"
                display="flex"
                flexDirection="column"
            >
                <ToolBar isLogged={props.isLogged} />
                <SignIn />
            </Box>
        </div>
    )
}
