import Typography from '@mui/material/Typography';
import Grid from '@mui/material/Grid2';

import SummaryChart from './chart/SummaryChart';
import SummaryTable from './table/SummaryTable';
import StationCountCard from './card/StationCountCard';
import TrainCountCard from './card/TrainCountCard';
import JobCountCard from './card/JobCountCard';

export default function DashboardPage() {
  return (
    <>
      <Typography variant="h4" fontWeight="bold" mb={5}>
        Dashboard
      </Typography>
      <Grid container spacing={2}>
        {/* Summary Cards */}
        <Grid size={{ xl: 2, md: 4, sm: 6, xs: 12 }}>
          <TrainCountCard />
        </Grid>
        <Grid size={{ xl: 2, md: 4, sm: 6, xs: 12 }}>
          <StationCountCard />
        </Grid>
        <Grid size={{ xl: 2, md: 4, sm: 6, xs: 12 }}>
          <JobCountCard state="running" />
        </Grid>
        <Grid size={{ xl: 2, md: 4, sm: 6, xs: 12 }}>
          <JobCountCard state="waiting" />
        </Grid>
        <Grid size={{ xl: 2, md: 4, sm: 6, xs: 12 }}>
          <JobCountCard state="failed" />
        </Grid>
        <Grid size={{ xl: 2, md: 4, sm: 6, xs: 12 }}>
          <JobCountCard state="cancelled" />
        </Grid>
        {/* Table */}
        <Grid size={{ md: 7, xs: 12 }}>
          <SummaryTable />
        </Grid>
        {/* Chart */}
        <Grid size={{ md: 5, xs: 12 }}>
          <SummaryChart />
        </Grid>
      </Grid>
    </>
  );
}
