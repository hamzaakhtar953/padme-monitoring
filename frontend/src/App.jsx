import {
  createTheme,
  ThemeProvider,
  responsiveFontSizes,
} from "@mui/material/styles";
import { createBrowserRouter, RouterProvider } from "react-router-dom";

import RootLayout from "./layout/main";
import DashboardPage from "./pages/dashboard";
import TrainsPage from "./pages/trains";
import TrainDetailsPage from "./pages/train-detail";
import StationsPage from "./pages/stations";
import StationDetailsPage from "./pages/station-detail";
import ErrorPage from "./pages/Error";
// import { ColorModeContext, useMode } from "./theme";
import theme from "./theme";

function App() {
  // const [theme, colorMode] = useMode();

  const router = createBrowserRouter([
    {
      path: "/",
      element: <RootLayout />,
      errorElement: <ErrorPage />,
      children: [
        { index: true, element: <DashboardPage /> },
        { path: "trains", element: <TrainsPage /> },
        { path: "trains/:trainId", element: <TrainDetailsPage /> },
        { path: "stations", element: <StationsPage /> },
        { path: "stations/:stationId", element: <StationDetailsPage /> },
      ],
    },
  ]);

  return (
    // <ColorModeContext.Provider value={colorMode}>
    <ThemeProvider theme={theme}>
      <RouterProvider router={router} />
    </ThemeProvider>
    // </ColorModeContext.Provider>
  );
}

export default App;
