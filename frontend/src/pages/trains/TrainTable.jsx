import * as React from 'react';
import { DataGrid, GridActionsCellItem, GridToolbar } from '@mui/x-data-grid';
import { useNavigate } from 'react-router-dom';
import toast from 'react-hot-toast';
import OpenInNewIcon from '@mui/icons-material/OpenInNew';

import EmptyRowsOverlay from '../../layout/table/EmptyRowsOverlay';
import { LightTooltip } from '../../components/tooltip';
import { formatDate, renderRowIds } from '../../utils/helper';
import { useQuery } from '@tanstack/react-query';
import { getTrains } from '../../api/train';

function TrainTable() {
  const navigate = useNavigate();

  const {
    data: trains,
    isLoading,
    isError,
    error,
  } = useQuery({
    queryKey: ['trains'],
    queryFn: getTrains,
  });

  const columns = React.useMemo(
    () => [
      {
        field: 'lineNo',
        headerName: '#',
        width: 60,
        editable: false,
        resizable: false,
        sortable: false,
        disableColumnMenu: true,
        renderCell: renderRowIds,
      },
      {
        field: 'identifier',
        headerName: 'Train ID',
        width: 180,
        editable: true,
      },
      { field: 'title', headerName: 'Title', width: 190, editable: true },
      { field: 'creator', headerName: 'Creator', width: 130 },
      { field: 'description', headerName: 'Description', width: 320 },
      {
        field: 'createdAt',
        headerName: 'Created at',
        width: 150,
        valueGetter: formatDate,
      },
      {
        field: 'updatedAt',
        headerName: 'Updated at',
        width: 150,
        valueGetter: formatDate,
      },
      { field: 'version', headerName: 'Version', width: 80 },
      {
        field: 'actions',
        type: 'actions',
        getActions: (params) => [
          /* eslint-disable react/jsx-key */
          <GridActionsCellItem
            label="View train details"
            icon={
              <LightTooltip
                disableInteractive
                placement="left"
                title="View details"
              >
                <OpenInNewIcon />
              </LightTooltip>
            }
            onClick={() => navigate(params.id)}
          />,
        ],
      },
    ],
    [navigate]
  );

  if (isError) {
    toast.error(error.message);
  }

  return (
    <DataGrid
      rows={trains}
      columns={columns}
      loading={isLoading}
      pageSizeOptions={[20]}
      getRowId={(row) => row.identifier}
      disableRowSelectionOnClick
      initialState={{
        density: 'comfortable',
        pagination: {
          paginationModel: {
            pageSize: 20,
          },
        },
      }}
      slots={{ noRowsOverlay: EmptyRowsOverlay, toolbar: GridToolbar }}
      slotProps={{
        toolbar: {
          showQuickFilter: true,
        },
      }}
    />
  );
}

export default TrainTable;
