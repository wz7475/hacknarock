import logo from "./logo.svg";
import { ToolBar } from "./components/Toolbar";
import { Background } from "./Backgrounnd";
import { Box, Button } from "@mui/material";
import { Controls } from "./Contorls";
import { useState } from "react";

function App() {
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
      <Box position="absolute" top="0px" height="100vh">
        <Controls />
      </Box>
    </div>
  );
}

export default App;
