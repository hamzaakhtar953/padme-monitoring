import { useQueryClient } from '@tanstack/react-query';
import { useEffect } from 'react';
import config from '../config';

export const useMetricSSE = (jobId) => {
  const queryClient = useQueryClient();

  useEffect(() => {
    const eventSource = new EventSource(
      `${config.apiUrl}/jobs/${jobId}/metrics/sse`
    );

    eventSource.addEventListener('metric_update', (event) => {
      const updatedMetrics = JSON.parse(event.data);
      queryClient.setQueryData(
        ['jobs', { id: jobId, metric: updatedMetrics.source }],
        updatedMetrics
      );
    });

    eventSource.onerror = (error) => {
      console.error('Metric SSE error:', error);
    };

    return () => {
      eventSource.close();
    };
  }, [queryClient, jobId]);
};
