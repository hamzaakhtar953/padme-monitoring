import { useParams } from "react-router-dom";

export default function TrainDetailsPage() {
  const params = useParams();

  return (
    <>
      <h1>Train Details Page</h1>
      <p>Product ID: {params.trainId}</p>
    </>
  );
}
