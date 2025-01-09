import { useQuery } from '@tanstack/react-query';

import { getJobCountByState } from '../../../api/dashboard';
import SummaryCard from './SummaryCard';

const jobStateProps = {
  running: { type: 'runningJob', title: 'Running Jobs' },
  waiting: { type: 'waitingJob', title: 'Waiting Jobs' },
  failed: { type: 'failedJob', title: 'Failed Jobs' },
  cancelled: { type: 'cancelledJob', title: 'Cancelled Jobs' },
};

function JobCountCard({ state }) {
  const { data: count } = useQuery({
    queryKey: ['jobs', { count: true, state }],
    queryFn: ({ signal }) => getJobCountByState({ signal, state }),
  });

  return (
    <SummaryCard
      type={jobStateProps[state].type}
      title={jobStateProps[state].title}
      value={count}
    />
  );
}

export default JobCountCard;
