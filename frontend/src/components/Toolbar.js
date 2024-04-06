import React, { useState } from "react";
import AppBar from "@mui/material/AppBar";
import Button from "@mui/material/Button";
import Box from "@mui/material/Box";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import IconButton from "@mui/material/IconButton";
import { MenuItem } from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import Menu from "@mui/material/Menu";
export function ToolBar(props) {
  const [anchorElNav, setAnchorElNav] = useState(null);

  const handleOpenNavMenu = (event) => {
    setAnchorElNav(event.currentTarget);
  };

  const handleCloseNavMenu = () => {
    setAnchorElNav(null);
  };

  const SUBPAGES = [
    {
      name: "profile",
      path: "/path",
    },
    {
      name: "friends",
      path: "/path",
    },
  ];

  // const navigate = useNavigate();

  return (
    <div>
      <AppBar
        sx={{
          mb: 0,
          opacity: 0.5,
          position: "static",
        }}
      >
        <Toolbar>
          <Box>
            <IconButton
              size="large"
              aria-label="account of current user"
              aria-controls="menu-appbar"
              aria-haspopup="true"
              onClick={handleOpenNavMenu}
              color="inherit"
            >
              <MenuIcon />
            </IconButton>
            <Menu
              id="menu-appbar"
              anchorEl={anchorElNav}
              anchorOrigin={{
                vertical: "bottom",
                horizontal: "left",
              }}
              keepMounted
              transformOrigin={{
                vertical: "top",
                horizontal: "left",
              }}
              open={Boolean(anchorElNav)}
              onClose={handleCloseNavMenu}
            >
              {SUBPAGES.map((data) => (
                <MenuItem
                  key={data.name}
                  // onClick={() => {
                  //   // navigate("/historia");
                  //   window.scrollTo(0, 0);
                  //   handleCloseNavMenu();
                  // }}
                >
                  <Typography textAlign="center">{data.name}</Typography>
                </MenuItem>
              ))}
            </Menu>
          </Box>
        </Toolbar>
      </AppBar>
    </div>
  );
}
