import {
  Box,
  Button,
  Fab,
  Grow,
  Slide,
  TextField,
  Typography,
} from "@mui/material";
import { ToolBar } from "./components/Toolbar";
import { DataGrid } from "@mui/x-data-grid";
import { useState } from "react";

const columns = [
  {
    field: "name",
    headerName: "Name",
    width: 150,
    editable: false,
    hideable: false,
  },
  {
    field: "experience",
    headerName: "Ex",
    width: 90,
    editable: false,
    hideable: false,
  },
  {
    width: 70,
    editable: false,
    sortable: false,
    hideable: false,
    filterable: false,
    renderCell: (params) => {
      return <Button>Visit</Button>;
    },
  },
];

const friendList = [
  {
    id: 1,
    name: "janek232",
    experience: 1231,
  },
  {
    id: 2,
    name: "malogosia2007",
    experience: 453,
  },
  {
    id: 3,
    name: "o1122lek",
    experience: 654,
  },
];

export function Friends(props) {
  const [isAddingFriend, setIsAddingFriend] = useState(false);
  const [isUserNotFound, setIsUserNotFound] = useState(false);
  const [isUserAddedSuccessfully, setIsUserAddedSuccessfully] = useState(false);

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
        <Slide in={!isAddingFriend}>
          <Button
            sx={{ mt: 5, mb: 5, width: "50%", mx: "auto" }}
            variant="contained"
            onClick={() => setIsAddingFriend(true)}
          >
            Add new friend
          </Button>
        </Slide>
        {!isAddingFriend && (
          <Grow in={!isAddingFriend}>
            <Box
              display="flex"
              flexDirection="column"
              bgcolor="white"
              borderRadius="20px"
              sx={{ mx: "auto", mt: 2, width: "30hw" }}
            >
              <Typography variant="h5" sx={{ mb: 2, mt: 3, mb: 2, ml: 4 }}>
                Your Friends:{" "}
              </Typography>
              <DataGrid
                sx={{ ml: 2, mr: 2, mb: 3 }}
                disableColumnMenu
                bulkActionButtons={false}
                rows={friendList}
                columns={columns}
                initialState={{
                  pagination: {
                    paginationModel: {
                      pageSize: 5,
                    },
                  },
                }}
                pageSizeOptions={[5]}
                disableRowSelectionOnClick
              />
            </Box>
          </Grow>
        )}
        <Grow in={isAddingFriend}>
          <Box
            sx={{
              bgcolor: "white",
              mx: "auto",
              mt: 2,
              p: 2,
              borderRadius: "20px",
              width: "30hw",
              display: "flex",
              flexDirection: "column",
            }}
          >
            <TextField></TextField>
            <Box
              marginTop={2}
              flexDirection="row"
              display="flex"
              justifyItems="center"
              justifyContent="center"
            >
              <Button
                onClick={() => {
                  if (Math.random() > 0.5) setIsUserNotFound(true);
                  else setIsAddingFriend(false);
                }}
              >
                Add Friend
              </Button>
              <Button
                onClick={() => {
                  setIsUserNotFound(false);
                  setIsAddingFriend(false);
                }}
              >
                Cancel
              </Button>
            </Box>
            {isUserNotFound && <Typography>User not found</Typography>}
          </Box>
        </Grow>
        {isUserAddedSuccessfully && (
          <Typography>Friend added successfully</Typography>
        )}
      </Box>
    </div>
  );
}
