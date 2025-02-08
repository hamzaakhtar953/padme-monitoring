import { useQueryClient } from '@tanstack/react-query';
import { useEffect } from 'react';
import config from '../config';

export const useJobSSE = () => {
  const queryClient = useQueryClient();

  useEffect(() => {
    const eventSource = new EventSource(`${config.apiUrl}/jobs/sse`);

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
      console.error('Job SSE error:', error);
    };

    return () => {
      eventSource.close();
    };
  }, [queryClient]);
};
