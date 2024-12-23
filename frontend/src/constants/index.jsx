import Badge from "@mui/material/Badge";
import AccountIcon from "@mui/icons-material/AccountCircle";
import ContainerIcon from "@mui/icons-material/ViewInAr";
import DashboardIcon from "@mui/icons-material/SpaceDashboard";
import FederatedJobIcon from "@mui/icons-material/Assignment";
import ImageIcon from "@mui/icons-material/Cloud";
import MetadataIcon from "@mui/icons-material/IntegrationInstructionsRounded";
import VaultIcon from "@mui/icons-material/VpnKey";
import ErrorIcon from "@mui/icons-material/ErrorRounded";
import SuccessIcon from "@mui/icons-material/CheckCircleRounded";
import TrainIcon from "@mui/icons-material/Train";
import StationIcon from "@mui/icons-material/Warehouse";
import JobsIcon from "@mui/icons-material/WorkHistory";


export const drawerWidth = 210;

export const navLinks = () => {
  // const { federatedJobs } = store.getState().federated;
  // const { trains, containers, images, vault } = store.getState().station;

  // const renderIcon = (contentLength, icon, { color = "primary" } = {}) => (
  //   <Badge badgeContent={contentLength} color={color}>
  //     {icon}
  //   </Badge>
  // );

  return [
    {
      title: "Dashboard",
      index: 0,
      to: "/",
      exact: true,
      icon: <DashboardIcon />,
    },
    {
      title: "Trains",
      index: 1,
      to: "/trains",
      icon: <TrainIcon />,
    },
    {
      title: "Stations",
      index: 2,
      to: "/stations",
      icon: <StationIcon />,
    },
  ];
};

export const navLinksNew = [
  {
    title: "Dashboard",
    index: 0,
    to: "/",
    icon: <DashboardIcon />,
  },
  {
    title: "Dashboard",
    index: 1,
    to: "/",
    icon: <DashboardIcon />,
  },
  {
    title: "Dashboard",
    index: 2,
    to: "/",
    icon: <DashboardIcon />,
  },
  {
    title: "Dashboard",
    index: 3,
    to: "/",
    icon: <DashboardIcon />,
  },
];
