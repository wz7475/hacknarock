import logo from "./logo.svg";
import { ToolBar } from "./components/Toolbar";
import { Background } from "./Backgrounnd";
import { Box, Button, Typography } from "@mui/material";

function Profile(props) {
  return (
    <div>
      <Box
        position="absolute"
        top="0px"
        height="100vh"
        width="100%"
        display="flex"
        flexDirection="column"
      >
        <ToolBar isLogged={props.isLogged} />
        <Box
          sx={{
            p: 3,
            bgcolor: "white",
            borderRadius: 8,
            width: "50%",
            mt: 7,
            mx: "auto",
          }}
        >
          <Typography>Here will be displayed data about profile</Typography>
          <Button sx={{ mt: 3 }}>Connect with Google Calendar</Button>
        </Box>
      </Box>
    </div>
  );
}

export default Profile;
