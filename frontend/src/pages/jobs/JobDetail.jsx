import { useParams } from 'react-router-dom';
import Paper from '@mui/material/Paper';
import Chip from '@mui/material/Chip';
import Grid from '@mui/material/Grid2';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import RefreshIcon from '@mui/icons-material/Cached';
import PendingIcon from '@mui/icons-material/PauseCircleOutline';
import FailedIcon from '@mui/icons-material/ErrorOutline';
import CancelledIcon from '@mui/icons-material/Close';
import { Gauge, gaugeClasses } from '@mui/x-charts/Gauge';

const cpuConsumed = 90;
const ramConsumed = 82;
const netConsumed = 33;

const getGaugeColor = (value) => {
  if (value < 80) return '#52b202'; // Green for normal range
  if (value < 90) return '#FFA500'; // Orange for warning range
  return '#ef4444'; // Red for critical range
};

const chipColor = {
  running: { color: 'info', icon: <RefreshIcon className="text-red" /> },
  pending: { color: 'warning', icon: <PendingIcon /> },
  failed: { color: 'error', icon: <FailedIcon /> },
  cancelled: { color: 'primary', icon: <CancelledIcon /> },
};

export default function JobDetailPage() {
  const params = useParams();
  const label = 'running';

  return (
    <>
      <Stack
        direction={{ sm: 'column', md: 'row' }}
        justifyContent="space-between"
        spacing={2}
      >
        <Stack spacing={1.5}>
          <Typography variant="h4" fontWeight="bold">
            44bc00a0-9208-11ef-a539-579e5c650fb5
          </Typography>
          <Stack direction="row" alignItems="center" spacing={1}>
            <Typography
              className="rounded-md border-2 border-stone-600 px-1 font-semibold uppercase tracking-wide"
              variant="body2"
            >
              Created By
            </Typography>
            <Typography>Hamza Akhtar</Typography>
          </Stack>
        </Stack>
        {/* METRICS */}
        <Stack
          direction="row"
          justifyContent={{ sm: 'space-between' }}
          spacing={2}
        >
          {/* CPU */}
          <Paper className="w-full rounded-xl px-5 py-4" elevation={0}>
            <Stack alignItems="center" spacing={0.5}>
              <Typography className="text-sm font-bold uppercase text-gray-500">
                CPU Usage
              </Typography>
              <Gauge
                value={cpuConsumed}
                width={150}
                height={150}
                startAngle={-110}
                endAngle={110}
                innerRadius="70%"
                text={(prop) => `${prop.value}%`}
                sx={{
                  [`& .${gaugeClasses.valueText}`]: {
                    fontSize: 28,
                    fontWeight: 600,
                    transform: 'translate(0px, 0px)',
                  },
                  [`& .${gaugeClasses.valueArc}`]: {
                    fill: getGaugeColor(cpuConsumed),
                  },
                }}
              />
            </Stack>
          </Paper>
          {/* RAM */}
          <Paper className="w-full rounded-xl px-5 py-4" elevation={0}>
            <Stack alignItems="center" spacing={0.5}>
              <Typography className="text-sm font-bold uppercase text-gray-500">
                RAM Usage
              </Typography>
              <Gauge
                width={150}
                height={150}
                value={ramConsumed}
                startAngle={-110}
                endAngle={110}
                innerRadius="70%"
                text={(prop) => `${prop.value}%`}
                sx={{
                  [`& .${gaugeClasses.valueText}`]: {
                    fontSize: 28,
                    fontWeight: 600,
                    transform: 'translate(0px, 0px)',
                  },
                  [`& .${gaugeClasses.valueArc}`]: {
                    fill: getGaugeColor(ramConsumed),
                  },
                }}
              />
            </Stack>
          </Paper>
          {/* Network */}
          <Paper className="w-full rounded-xl px-5 py-4" elevation={0}>
            <Stack alignItems="center" spacing={0.5}>
              <Typography className="text-sm font-bold uppercase text-gray-500">
                Network Usage
              </Typography>
              <Gauge
                width={150}
                height={150}
                value={netConsumed}
                startAngle={-110}
                endAngle={110}
                innerRadius="70%"
                text={(prop) => `${prop.value}%`}
                sx={{
                  [`& .${gaugeClasses.valueText}`]: {
                    fontSize: 28,
                    fontWeight: 600,
                    transform: 'translate(0px, 0px)',
                  },
                  [`& .${gaugeClasses.valueArc}`]: {
                    fill: getGaugeColor(netConsumed),
                  },
                }}
              />
            </Stack>
          </Paper>
        </Stack>
      </Stack>
      <Grid container mt={3} spacing={2}>
        {/* Description */}
        <Grid size={{ md: 6, xs: 12 }}>
          <Paper
            className="h-full rounded-xl"
            elevation={0}
            sx={{ padding: 3 }}
          >
            <Stack spacing={1}>
              <Typography className="font-bold text-stone-600">
                Description
              </Typography>
              <Typography>
                Executing train on two stations e.g. Klee and Bruegel for
                statistical analysis
              </Typography>
            </Stack>
          </Paper>
        </Grid>
        {/* Other Details */}
        <Grid size={{ md: 6, xs: 12 }}>
          <Paper
            className="h-full rounded-xl"
            elevation={0}
            sx={{ padding: 3 }}
          >
            <Stack rowGap={2} divider={<Divider flexItem />}>
              {/* STATUS */}
              <Stack direction="row" alignItems="center" spacing={2}>
                <Typography className="font-bold text-stone-600">
                  Job Status:
                </Typography>
                <Chip
                  className="w-[8rem] text-sm font-bold"
                  label={label}
                  sx={{ paddingX: 0.5 }}
                  icon={chipColor[label].icon}
                  color={chipColor[label].color}
                />
              </Stack>
              {/* ID */}
              <Stack direction="row" alignItems="center" spacing={2}>
                <Typography className="font-bold text-stone-600">
                  Train Class:
                </Typography>
                <Typography>
                  train_class_repository/hello-world:latest
                </Typography>
              </Stack>
              {/* ID */}
              <Stack direction="row" alignItems="center" spacing={2}>
                <Typography className="font-bold text-stone-600">
                  Metadata URI:
                </Typography>
                <Typography>
                  https://monitoring.padme-analytics.de/jobs/44bc00a0-9208-11ef-a539-579e5c650fb5
                </Typography>
              </Stack>
              {/* Current Station */}
              <Stack direction="row" alignItems="center" spacing={2}>
                <Typography className="font-bold text-stone-600">
                  Current Station:
                </Typography>
                <Typography>Klee</Typography>
              </Stack>
              {/* Created at */}
              <Stack direction="row" alignItems="center" spacing={2}>
                <Typography className="font-bold text-stone-600">
                  Created at:
                </Typography>
                <Typography>May 20, 2024</Typography>
              </Stack>
              {/* Updated at */}
              <Stack direction="row" alignItems="center" spacing={2}>
                <Typography className="font-bold text-stone-600">
                  Updated at:
                </Typography>
                <Typography>Oct 22, 2024</Typography>
              </Stack>
            </Stack>
          </Paper>
        </Grid>
      </Grid>
    </>
  );
}
