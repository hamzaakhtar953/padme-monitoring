import Typography from "@mui/material/Typography";
import Avatar from "@mui/material/Avatar";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Stack from "@mui/material/Stack";
import ArrowUpIcon from "@mui/icons-material/ArrowUpward";
import ArrowDownIcon from "@mui/icons-material/ArrowDownward";

export default function StatsCard({ title, value, diff, trend, icon }) {
  const trendColor = trend === "up" ? "success" : "error";
  const TrendIcon = trend === "up" ? ArrowUpIcon : ArrowDownIcon;

  return (
    <Card>
      <CardContent>
        <Stack spacing={3}>
          <Stack
            direction="row"
            spacing={3}
            sx={{
              alignItems: "flex-start",
              justifyContent: "space-between",
            }}
          >
            <Stack spacing={1}>
              <Typography
                color="text.secondary"
                variant="overline"
                fontWeight={700}
              >
                {title}
              </Typography>
              <Typography variant="h4">{value}</Typography>
            </Stack>
            <Avatar
              sx={{
                color: "primary.main",
                height: "56px",
                width: "56px",
              }}
            >
              {icon}
            </Avatar>
          </Stack>
          {diff ? (
            <Stack sx={{ alignItems: "center" }} direction="row" spacing={2}>
              <Stack
                sx={{ alignItems: "center" }}
                direction="row"
                spacing={0.5}
              >
                <TrendIcon
                  color={trendColor}
                  // fontSize="var(--icon-fontSize-md)"
                />
                <Typography color={trendColor} variant="body2">
                  {diff}%
                </Typography>
              </Stack>
              <Typography color="text.secondary" variant="caption">
                Since last month
              </Typography>
            </Stack>
          ) : null}
        </Stack>
      </CardContent>
    </Card>
  );
}
