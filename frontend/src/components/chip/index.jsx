import CancelledIcon from '@mui/icons-material/Close';
import FailedIcon from '@mui/icons-material/ErrorOutline';
import FinishedIcon from '@mui/icons-material/Check';
import WaitingIcon from '@mui/icons-material/PauseCircleOutline';
import RunningIcon from '@mui/icons-material/Cached';

export const chipColor = {
  waiting: { color: 'warning', icon: <WaitingIcon /> },
  running: { color: 'info', icon: <RunningIcon /> },
  finished: { color: 'success', icon: <FinishedIcon /> },
  failed: { color: 'error', icon: <FailedIcon /> },
  cancelled: { color: 'primary', icon: <CancelledIcon /> },
};
