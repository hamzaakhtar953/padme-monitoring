import Typography from "@mui/material/Typography";
import { Link } from "react-router-dom";

export default function Trains() {
  const temp = "";

  return (
    <>
      <Typography variant="h4" fontWeight="bold" mb={3}>
        Trains
      </Typography>
      <div>TrainsPage</div>
      <ul>
        <li>
          <Link to="/trains/hello-world">Train: hello-world:latest</Link>
        </li>
        <li>
          <Link to="/trains/metrics-csv">Train: metrics-csv:latest</Link>
        </li>
        <li>
          <Link to="/trains/malaria">Train: malaria:latest</Link>
        </li>
      </ul>
    </>
  );
}
