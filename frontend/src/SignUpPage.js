import { Box } from "@mui/material";
import SignUp from "./SignUp";
import { ToolBar } from "./components/Toolbar";

export default function SignUpPage(props) {
  return (
    <div>
      <Box
        maxWidth
        sx={{
          bgcolor: "lightblue",
          minHeight: "100vh",
          zIndex: 0,
        }}
      />
      <Box
        position="absolute"
        top="0px"
        width="100%"
        display="flex"
        flexDirection="column"
      >
        <ToolBar isLogged={props.isLogged} />
        <SignUp />
      </Box>
    </div>
  );
}
