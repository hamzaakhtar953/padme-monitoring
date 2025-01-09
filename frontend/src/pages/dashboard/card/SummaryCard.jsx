import Avatar from '@mui/material/Avatar';
import Paper from '@mui/material/Paper';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import CloseIcon from '@mui/icons-material/Close';
import ErrorIcon from '@mui/icons-material/ErrorOutline';
import JobsIcon from '@mui/icons-material/WorkHistoryOutlined';
import StationIcon from '@mui/icons-material/WarehouseOutlined';
import TrainIcon from '@mui/icons-material/TrainOutlined';
import CpuIcon from '@mui/icons-material/Memory';
import NetworkIcon from '@mui/icons-material/Wifi';
import { createSvgIcon } from '@mui/material/utils';

function SummaryCard({ title, value, type }) {
  return (
    <Paper className="flex h-full rounded-xl px-6 py-4" variant="outlined">
      <Stack direction="row" alignItems="center" spacing={3.5} py={1}>
        <Avatar
          className={`h-16 w-16 border-[3px] bg-white ${summaryProps[type].color}`}
        >
          {summaryProps[type].icon}
        </Avatar>
        <Stack className="sm:ml-2" direction="column" spacing={1}>
          <Typography className="text-sm font-bold uppercase text-gray-500">
            {title}
          </Typography>
          <Typography variant="h4" className="font-semibold">
            {value}
          </Typography>
        </Stack>
      </Stack>
    </Paper>
  );
}

// Credit: memory icon from https://fontawesome.com/v5/icons/memory?f=classic&s=solid
// const MemoryIcon = createSvgIcon(
//   <svg
//     xmlns="http://www.w3.org/2000/svg"
//     aria-hidden="true"
//     focusable="false"
//     viewBox="0 0 512 512"
//     aria-describedby="Memory icon from https://fontawesome.com/v5/icons/memory?f=classic&s=solid"
//   >
//     <path
//       fill="currentColor"
//       d="M640 130.9V96c0-17.7-14.3-32-32-32H32C14.3 64 0 78.3 0 96v34.9c18.6 6.6 32 24.2 32 45.1s-13.4 38.5-32 45.1V320h640v-98.9c-18.6-6.6-32-24.2-32-45.1s13.4-38.5 32-45.1zM224 256h-64V128h64v128zm128 0h-64V128h64v128zm128 0h-64V128h64v128zM0 448h64v-26.7c0-8.8 7.2-16 16-16s16 7.2 16 16V448h128v-26.7c0-8.8 7.2-16 16-16s16 7.2 16 16V448h128v-26.7c0-8.8 7.2-16 16-16s16 7.2 16 16V448h128v-26.7c0-8.8 7.2-16 16-16s16 7.2 16 16V448h64v-96H0v96z"
//     />
//   </svg>
// );

// Since we can't dynamically create colors for tailwind using
// template liternals, we will create a map with some defined keys.
//
// Ref: https://tailwindcss.com/docs/content-configuration#dynamic-class-names
const summaryProps = {
  // cpu: {
  //   color: 'text-blue-500 border-blue-200',
  //   icon: <CpuIcon fontSize="large" />,
  // },
  // memory: {
  //   color: 'text-green-500 border-green-200',
  //   icon: <MemoryIcon />,
  // },
  // network: {
  //   color: 'text-green-500 border-green-200',
  //   icon: <NetworkIcon fontSize="large" />,
  // },
  train: {
    color: 'text-green-500 border-green-200',
    icon: <TrainIcon fontSize="large" />,
  },
  station: {
    color: 'text-orange-500 border-orange-200',
    icon: <StationIcon fontSize="large" />,
  },
  waitingJob: {
    color: 'text-yellow-500 border-yellow-200',
    icon: <JobsIcon fontSize="large" />,
  },
  runningJob: {
    color: 'text-blue-500 border-blue-200',
    icon: <JobsIcon fontSize="large" />,
  },
  failedJob: {
    color: 'text-red-500 border-red-200',
    icon: <ErrorIcon fontSize="large" />,
  },
  cancelledJob: {
    color: 'text-gray-500 border-gray-200',
    icon: <CloseIcon fontSize="large" />,
  },
};

export default SummaryCard;
