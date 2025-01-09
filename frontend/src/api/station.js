import axios from '../service/axios';
import { throwErrorBasedOnResponse } from '../utils/helper';

export async function getStations({ signal }) {
  try {
    const response = await axios.get('/stations', {
      params: {
        response_type: 'default',
        offset: 0,
        limit: 10,
      },
      signal,
    });
    return response.data;
  } catch (error) {
    throwErrorBasedOnResponse(error);
  }
}
