import { useParams } from 'react-router-dom';
import Paper from '@mui/material/Paper';
import Chip from '@mui/material/Chip';
import Grid from '@mui/material/Grid2';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';
import CheckIcon from '@mui/icons-material/Check';
import ClearIcon from '@mui/icons-material/Clear';
import { formatDate } from '../../utils/helper';

const station = {
  id: 'b9e93eae-12d7-4f9a-a180-43b7eca17181',
  name: 'Fraunhofer FIT',
  owner: 'Zeyd Bukhers',
  description: 'PADME-PHT station in the FIT Infrastructure',
  latitude: '50.775345',
  longitude: '6.083887',
  created: '2024-11-25T12:09:07.121622',
  updated: '2024-11-25T12:09:07.121635',
  executionEnvironment: {
    hasGPUSupport: true,
    totalGPUPower: '16 GiB',
    totalCPUCores: '16',
    totalRAM: '64 GiB',
    totalDiskSpace: '1 TB',
    hasInternetConnectivity: true,
    networkBandwidth: '1 Gbps',
  },
};

export default function StationDetailPage() {
  const params = useParams();

  const hasGPUSupport = station.executionEnvironment.hasGPUSupport;

  return (
    <>
      <Stack
        direction={{ sm: 'column', md: 'row' }}
        alignItems={{ md: 'center', sm: '-moz-initial' }}
        justifyContent="space-between"
        spacing={2}
      >
        <Stack spacing={1.5}>
          <Stack direction="row" alignItems="center" gap={3}>
            <Typography variant="h4" fontWeight="bold">
              {station.name}
            </Typography>
            <Chip
              className="text-sm font-bold"
              label={hasGPUSupport ? 'GPU supported' : 'GPU not supported'}
              sx={{ paddingX: 0.5 }}
              icon={hasGPUSupport ? <CheckIcon /> : <ClearIcon />}
              color={hasGPUSupport ? 'success' : 'warning'}
            />
          </Stack>
          <Stack direction="row" alignItems="center" spacing={1}>
            <Typography
              className="rounded-md border-2 border-stone-600 px-1 font-semibold uppercase tracking-wide"
              variant="body2"
            >
              Owner
            </Typography>
            <Typography className="font-semibold">{station.owner}</Typography>
          </Stack>
        </Stack>
        <Stack direction="row" spacing={2}>
          {/* CPU */}
          <Paper className="rounded-xl px-5 py-4" elevation={0}>
            <Stack alignItems="center" spacing={0.5}>
              <Typography className="text-sm font-bold uppercase text-gray-500">
                CPU Cores
              </Typography>
              <Typography variant="h4" className="font-semibold">
                {station.executionEnvironment.totalCPUCores}
              </Typography>
            </Stack>
          </Paper>
          {/* RAM */}
          <Paper className="rounded-xl px-5 py-4" elevation={0}>
            <Stack alignItems="center" spacing={0.5}>
              <Typography className="text-sm font-bold uppercase text-gray-500">
                Memory
              </Typography>
              <Typography variant="h4" className="font-semibold">
                {station.executionEnvironment.totalRAM}
              </Typography>
            </Stack>
          </Paper>
          {/* NETWORK */}
          <Paper className="rounded-xl px-5 py-4" elevation={0}>
            <Stack alignItems="center" spacing={0.5}>
              <Typography className="text-sm font-bold uppercase text-gray-500">
                Network Bandwidth
              </Typography>
              <Typography variant="h4" className="font-semibold">
                {station.executionEnvironment.networkBandwidth}
              </Typography>
            </Stack>
          </Paper>
          {/* DISK */}
          <Paper className="rounded-xl px-5 py-4" elevation={0}>
            <Stack alignItems="center" spacing={0.5}>
              <Typography className="text-sm font-bold uppercase text-gray-500">
                Disk Space
              </Typography>
              <Typography variant="h4" className="font-semibold">
                {station.executionEnvironment.totalDiskSpace}
              </Typography>
            </Stack>
          </Paper>
          {/* GPU Memory */}
          {hasGPUSupport && (
            <Paper className="rounded-xl px-5 py-4" elevation={0}>
              <Stack alignItems="center" spacing={0.5}>
                <Typography className="text-sm font-bold uppercase text-gray-500">
                  GPU Memory
                </Typography>
                <Typography variant="h4" className="font-semibold">
                  {station.executionEnvironment.totalGPUPower}
                </Typography>
              </Stack>
            </Paper>
          )}
        </Stack>
      </Stack>
      {/* INFO */}
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
              <Typography>{station.description}</Typography>
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
              {/* ID */}
              <Stack direction="row" alignItems="center" spacing={2}>
                <Typography className="font-bold text-stone-600">
                  Station ID:
                </Typography>
                <Typography>{station.id}</Typography>
              </Stack>
              {/* TODO: Meta URI */}
              <Stack direction="row" alignItems="center" spacing={2}>
                <Typography className="font-bold text-stone-600">
                  Metadata URI:
                </Typography>
                <Typography>
                  https://monitoring.padme-analytics.de/stations/Klee
                </Typography>
              </Stack>
              {/* Created at */}
              <Stack direction="row" alignItems="center" spacing={2}>
                <Typography className="font-bold text-stone-600">
                  Created at:
                </Typography>
                <Typography>{formatDate(station.created)}</Typography>
              </Stack>
              {/* Updated at */}
              <Stack direction="row" alignItems="center" spacing={2}>
                <Typography className="font-bold text-stone-600">
                  Updated at:
                </Typography>
                <Typography>{formatDate(station.updated)}</Typography>
              </Stack>
              {/* Model */}
              <Stack>
                <Stack direction="row" alignItems="center">
                  <Typography className="w-24 font-bold text-stone-600">
                    Latitude:
                  </Typography>
                  <Typography>{station.latitude}</Typography>
                </Stack>
                <Stack direction="row" alignItems="center">
                  <Typography className="w-24 font-bold text-stone-600">
                    Longitude:
                  </Typography>
                  <Typography>{station.longitude}</Typography>
                </Stack>
              </Stack>
            </Stack>
          </Paper>
        </Grid>
      </Grid>
    </>
  );
}
