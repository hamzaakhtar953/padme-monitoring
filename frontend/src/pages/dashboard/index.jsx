import Typography from "@mui/material/Typography";
import Grid from "@mui/material/Grid2";
import TrainIcon from "@mui/icons-material/Train";
import StationIcon from "@mui/icons-material/Warehouse";
import JobsIcon from "@mui/icons-material/WorkHistory";

import StatsCard from "../../components/dashboard/StatsCard";

export default function DashboardPage() {
  return (
    <>
      <Typography variant="h4" fontWeight="bold" mb={5}>
        Dashboard
      </Typography>
      <Grid container spacing={2}>
        {/* Stats Card x6 (in first 2 rows) */}
        <Grid size={{ xl: 2, md: 4, xs: 6 }}>
          <StatsCard
            title="Trains"
            value="25"
            diff={12}
            trend="up"
            icon={<TrainIcon />}
          />
        </Grid>
        <Grid size={{ xl: 2, md: 4, xs: 6 }}>
          <StatsCard
            title="Stations"
            value="10"
            diff={25}
            trend="down"
            icon={<StationIcon />}
          />
        </Grid>
        <Grid size={{ xl: 2, md: 4, xs: 6 }}>
          <StatsCard
            title="Running Jobs"
            value="13"
            diff={26}
            trend="up"
            icon={<JobsIcon />}
          />
        </Grid>
        <Grid size={{ xl: 2, md: 4, xs: 6 }}>
          <StatsCard
            title="Cancelled Jobs"
            value="13"
            diff={26}
            trend="up"
            icon={<JobsIcon />}
          />
        </Grid>
        <Grid size={{ xl: 2, md: 4, xs: 6 }}>
          <StatsCard
            title="Failed Jobs"
            value="13"
            diff={26}
            trend="up"
            icon={<JobsIcon />}
          />
        </Grid>
        <Grid size={{ xl: 2, md: 4, xs: 6 }}>
          <StatsCard
            title="Pending Jobs"
            value="13"
            diff={26}
            trend="up"
            icon={<JobsIcon />}
          />
        </Grid>

        {/* Table */}
        <Grid size={{ md: 8 }}>
          <StatsCard
            title="Recent Jobs"
            value="13"
            diff={26}
            trend="up"
            icon={<JobsIcon />}
          />
        </Grid>
      </Grid>
    </>
  );
}
