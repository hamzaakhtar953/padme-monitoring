import { useParams } from 'react-router-dom';
import Paper from '@mui/material/Paper';
import Chip from '@mui/material/Chip';
import Grid from '@mui/material/Grid2';
import Stack from '@mui/material/Stack';
import Typography from '@mui/material/Typography';
import Divider from '@mui/material/Divider';

export default function TrainDetailPage() {
  const params = useParams();

  return (
    <>
      <Stack direction="row" alignItems="center" gap={1}>
        <Typography variant="h4" fontWeight="bold">
          Hello World Train
        </Typography>
        <Chip
          className="font-bold"
          size="small"
          label="v1.0.1"
          color="warning"
        />
      </Stack>
      <Stack mt={1.5} direction="row" alignItems="center" spacing={1}>
        <Typography
          className="rounded-md border-2 border-stone-600 px-1 font-semibold uppercase tracking-wide"
          variant="body2"
        >
          Created By
        </Typography>
        <Typography>Alice Johnson</Typography>
      </Stack>
      <Grid container mt={3} spacing={2}>
        {/* Description */}
        <Grid size={{ md: 6, xs: 12 }}>
          <Paper className="h-full rounded-xl" elevation={0} sx={{ padding: 3 }}>
            <Stack spacing={1}>
              <Typography className="font-bold text-stone-600">
                Description
              </Typography>
              <Typography>
                Alice Johnson third additional train, known as Train Three, is a
                meticulously designed and highly efficient model. It features
                state-of-the-art technology and advanced engineering, making it
                a standout in the fleet. This train is known for its
                reliability, speed, and comfort, providing an exceptional travel
                experience for passengers. With its sleek design and
                cutting-edge features, Train Three represents the pinnacle of
                modern train travel.
              </Typography>
            </Stack>
          </Paper>
        </Grid>
        {/* Other Details */}
        <Grid size={{ md: 6, xs: 12 }}>
          <Paper className="h-full rounded-xl" elevation={0} sx={{ padding: 3 }}>
            <Stack rowGap={2} divider={<Divider flexItem />}>
              {/* ID */}
              <Stack direction="row" alignItems="center" spacing={2}>
                <Typography className="font-bold text-stone-600">
                  Train ID:
                </Typography>
                <Typography>hello-world</Typography>
              </Stack>
              {/* ID */}
              <Stack direction="row" alignItems="center" spacing={2}>
                <Typography className="font-bold text-stone-600">
                  Metadata URI:
                </Typography>
                <Typography>
                  https://monitoring.padme-analytics.de/trains/hello-world
                </Typography>
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
              {/* Model */}
              <Stack direction="row" alignItems="center" spacing={2}>
                <Typography className="font-bold text-stone-600">
                  Model:
                </Typography>
                <Typography>LLM32</Typography>
              </Stack>
            </Stack>
          </Paper>
        </Grid>
      </Grid>
    </>
  );
}
