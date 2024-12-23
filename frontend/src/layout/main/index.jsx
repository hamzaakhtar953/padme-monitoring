import * as React from "react";
import Box from "@mui/material/Box";
import CssBaseline from "@mui/material/CssBaseline";
import { Outlet } from "react-router-dom";

import Header from "./Header";
import Sidebar from "./Sidebar";
import SidebarHeader from "./SidebarHeader";

export default function RootLayout() {
  const [open, setOpen] = React.useState(false);

  const handleSidebarOpen = () => {
    setOpen(true);
  };

  const handleSidebarClose = () => {
    setOpen(false);
  };

  return (
    <Box sx={{ display: "flex" }}>
      <CssBaseline />
      <Header open={open} onSidebarOpen={handleSidebarOpen} />
      <Sidebar open={open} onSidebarClose={handleSidebarClose} />
      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        <SidebarHeader />
        <Outlet />
      </Box>
    </Box>
  );
}
