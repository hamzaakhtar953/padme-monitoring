import { useQueryClient } from '@tanstack/react-query';
import { useEffect } from 'react';
import config from '../config';

const API_URL = config.isDevMode ? 'http://localhost:8000' : '/';

export const useJobSSE = () => {
  const queryClient = useQueryClient();

  useEffect(() => {
    const eventSource = new EventSource(`${API_URL}/jobs/sse`);

    eventSource.addEventListener('job_update', (event) => {
      const updatedJob = JSON.parse(event.data);

      // Update jobs list
      queryClient.setQueryData(['jobs'], (prevJobs) => {
        if (!prevJobs) return [updatedJob];

        return prevJobs.map((job) =>
          job.identifier === updatedJob.identifier ? updatedJob : job
        );
      });

      // Update individual job query
      queryClient.setQueryData(
        ['jobs', { id: updatedJob.identifier }],
        updatedJob
      );
    });

    eventSource.onerror = (error) => {
      console.error('SSE error:', error);
    };

    return () => {
      eventSource.close();
    };
  }, [queryClient]);
};
